# UX Datasource
from typing import List
import os
import json
from datetime import datetime, date, timedelta, timezone
from warnings import warn
from requests.auth import HTTPBasicAuth
from pmc_automation_tools.api.common import (
    DataSourceInput,
    DataSourceResponse,
    DataSource,
    CustomSslContextHTTPAdapter,
    RETRY_COUNT,
    BACKOFF,
    RETRY_STATUSES
    )
from pmc_automation_tools.common.exceptions import(
    UXResponseErrorLog
)
from pmc_automation_tools.common.utils import plex_date_formatter
import requests
from urllib3.util.retry import Retry
from itertools import chain
from concurrent.futures import ThreadPoolExecutor

class UXDatetime():
    def __init__(self, datestring):
        self.datestring = datestring
        self.datasource_date = None if self.datestring == '' else self._dateparse()
    def __repr__(self):
        return f"UXDatetime(datestring='{self.datestring}', datasource_date='{self.datasource_date}')"
    def __str__(self):
        return f"{self.datasource_date}"


    def _dateparse(self):
        formats = ["%m/%d/%Y %I:%M:%S %p", "%b %d %Y %I:%M%p"]
        # When converting datetime objects to varchars, the format is using spaces for padding rather than zeroes.
        standardized_datestring = ' '.join(self.datestring.split())
        for f in formats:
            try:
                self.plex_date = datetime.strptime(standardized_datestring, f)
                return plex_date_formatter(self.plex_date)
            except:
                continue
        self.plex_date = None
        return "Invalid Datetime Format"


    def to_json(self):
        return self.datasource_date


class UXDatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UXDatetime):
            return obj.to_json()
        return super().default(obj)


class UXDataSourceInput(DataSourceInput):
    def __init__(self, data_source_key: str, *args, template_folder: str=None, **kwargs):
        super().__init__(data_source_key, type='ux', *args, **kwargs)
        self.__input_types__ = {}
        self.__template_folder__ = template_folder
        if self.__template_folder__:
            template_query = self._query_template_import()
            if template_query:
                for key, value in template_query.items():
                    setattr(self, key, value)
        self._type_create()


    def __repr__(self):
        _attrs = [f"{k}='{v}'" for k, v in vars(self).items() if not k.startswith('_')]
        return f"UXDataSourceInput(data_source_key={self.__api_id__}, {', '.join(_attrs)})"


    def __str__(self):
        return '\n'.join([f"{k} : {v}" for k,v in self._query_string.items()])


    def _query_template_import(self):
        for file in os.listdir(self.__template_folder__):
            if f'{self.__api_id__}.json' == file:
                with open(os.path.join(self.__template_folder__, file), 'r', encoding='utf-8') as j:
                    template = json.loads(j.read())
                if 'inputs' in template.keys():
                    return template['inputs']
                return template


    def _update_input_parameters(self):
        self._query_string = {k:v for k, v in vars(self).items() if not k.startswith('_')}


    def _type_create(self):
        for k, v in vars(self).items():
            if not v or k.startswith('_'):
                continue
            value_type = type(v)
            if value_type is int and len(str(v)) == 1:
                self.__input_types__[k] = bool
            elif value_type is str and self._xdate(v):
                self.__input_types__[k] = UXDatetime
            else:
                self.__input_types__[k] = value_type


    def get_type(self, attribute):
        """
        Return the expected input type for the provided attribute.
        
        Expects a data source template file to be used during object creation.

        Parameters:
        
        - attribute: Data source input name

        Returns:
        
        - type of the attribute derived from the data source template file.
        """
        return getattr(self, '__input_types__').get(attribute, None)

    def _xstr(self, s):
        return str(s or '')


    def _xbool(self, b):
        if isinstance(b, int):
            return bool(b)
        if isinstance(b, str):
            try:
                return bool(int(b)) if len(b) == 1 else b.strip().upper() == 'TRUE'
            except ValueError:
                pass
        return bool(b)


    def _xdate(self, d):
        try:
            datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%fZ')
            return True
        except ValueError:
            return False


    def type_reconcile(self):
        """
        Adjusts the object attribute types to match the expected types of the data source.
        """
        for k, v in vars(self).items():
            if k.startswith('_') or k not in self.__input_types__.keys() or v is None:
                continue
            target_type = getattr(self, '__input_types__')[k]
            if target_type is int:
                new_val = None if isinstance(v, str) and not v.strip() else target_type(v)
            elif target_type is str:
                new_val = self._xstr(v)
            elif target_type is bool:
                new_val = self._xbool(v)
            else:
                new_val = target_type(v)
            setattr(self, k, new_val)


    def get_to_update(self, get_instance:'UXDataSourceResponse', response_index:int=0, **kwargs):
        """
        Adjusts the attribute types to match the expected types of the data source.

        Parameters:
        - get_instance: a UXDataSourceResponse object returned from a call to a 'get' type datasource.
        - response_index: formated response index for retrieving the data.
        - kwargs: Intended for use with key:replacement pairs of data. Often time the datasource_get response keys will not match the datasource_update input names.
                EX:
                    ui.get_to_update(response, Champion_PUN='Champion')
                    This will apply the value in the "Champion_PUN" output key to the "Champion" input key.
        """
        if not getattr(get_instance,'_transformed_data',None):
            raise AttributeError('Provided UXDataSourceResponse object has no _transformed_data attribute.')
        for k, v in get_instance._transformed_data[response_index].items():
            if k in kwargs.keys():
                k = kwargs.get(k)
            setattr(self, k, v)
        self.type_reconcile()
        self.purge_empty()

    def purge_empty(self):
        """
        Removes empty/Nonetype attributes from the input.

        Additionally removes any attributes not existing in the input_types dictionary.
        """
        super().purge_empty()
        purge_attrs = []
        for y in vars(self).keys():
            if y not in self.__input_types__.keys() and not y.startswith('_'):
                purge_attrs.append(y)
        for y in purge_attrs:
            self.pop_inputs(y)

class UXDataSource(DataSource):
    def __init__(self, auth: HTTPBasicAuth | str,
                 *args,
                 test_db: bool = True,
                 pcn_config_file: str = 'resources/pcn_config.json',
                 **kwargs):
        """
        Parameters:

        - auth: HTTPBasicAuth | str
            - HTTPBasicAuth object
            - PCN Reference key for getting the username/password in a json config file.
            
        - test_db: bool, optional
            - Use test or production database
        
        - pcn_config_file: str, optional
            - Path to JSON file containing username/password credentials for HTTPBasicAuth connections.
        """
        super().__init__(*args, auth=auth, test_db=test_db, pcn_config_file=pcn_config_file, type='ux', **kwargs)
        self.url_db = 'test.' if self._test_db else ''


    def __repr__(self):
        return f"UXDataSource(auth={self.__auth_key__}, test_db={self._test_db}, pcn_config_file={self._pcn_config_file})"


    def _create_session(self):
        session = requests.Session()
        retry = Retry(total=RETRY_COUNT, connect=RETRY_COUNT, backoff_factor=BACKOFF, status_forcelist=RETRY_STATUSES, raise_on_status=True)
        adapter = CustomSslContextHTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        return session
    
    def call_data_source(self, query:UXDataSourceInput) -> 'UXDataSourceResponse':
        """
        Call the UX data source.

        Parameters:

        - query: UXDataSourceInput object

        Returns:

        - UXDataSourceResponse object
        """
        json_query = json.loads(json.dumps(query._query_string, cls=UXDatetimeEncoder))
        url = f'https://{self.url_db}cloud.plex.com/api/datasources/{query.__api_id__}/execute?format=2'
        session = self._create_session()
        response = session.post(url, json=json_query, auth=self._auth)
        json_data = response.json()
        return UXDataSourceResponse(query.__api_id__, **json_data)
    

    def call_data_source_threaded(self, query_list:List['UXDataSourceInput']) -> List['UXDataSourceResponse']:
        def error_safe_call(query):
            try:
                return self.call_data_source(query)
            except UXResponseErrorLog as e:
                return e
        with ThreadPoolExecutor(max_workers=8) as pool:
            response_list = list(pool.map(error_safe_call, query_list))
        return response_list
    

    def list_data_source_access(self, pcn:HTTPBasicAuth|str|list):
        """
        Get a list of data sources that are enabled for a specific account or any number of accounts.

        Parameters:

        - pcn: Authentication for the account(s)

        Returns:

        - UXDataSourceResponse object
        """
        url = f'https://{self.url_db}cloud.plex.com/api/datasources/search?name='
        session = self._create_session()
        access_list = []
        if isinstance(pcn, list):
            pcn_list = pcn
        else:
            pcn_list = [pcn]
        for pcn in pcn_list:
            self._auth = self.set_auth(pcn)
            response = session.get(url, auth=self._auth)
            j = json.loads(response.text)
            for ds in j:
                ds['pcn'] = pcn
            access_list.append(j)
        all_datasources = list(chain.from_iterable(access_list))
        return UXDataSourceResponse('access_list', rows=all_datasources)

class UXDataSourceResponse(DataSourceResponse):
    def __init__(self, data_source_key, **kwargs):
        super().__init__(data_source_key, **kwargs)
        if isinstance(getattr(self, 'outputs', None), dict):
            for k, v in self.outputs.items():
                setattr(self, k, v)
        if getattr(self, 'rowLimitExceeded', False):
            warn('Row limit was exceeded in response. Review input filters and adjust to limit returned data.', category=UserWarning, stacklevel=3)
        if getattr(self, 'errors', []):
            raise UXResponseErrorLog(self.errors, transaction_no = self.transactionNo)
        self._format_response()
    
    
    def __repr__(self):
        _attrs = [f"{k}='{v}'" for k, v in vars(self).items() if not k.startswith('_')]
        return f"UXDataSourceResponse(data_source_key={self.__api_id__}, {', '.join(_attrs)})"
    
    
    def _format_response(self):
        self._transformed_data = getattr(self, 'rows', [])
        return self._transformed_data