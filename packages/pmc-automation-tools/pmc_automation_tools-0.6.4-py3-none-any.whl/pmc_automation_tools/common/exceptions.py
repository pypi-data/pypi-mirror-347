class Error(Exception):
    pass
class PmcAutomationToolsError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        for key, value in kwargs.items():
            setattr(self, key, value)
class PlexAutomateError(PmcAutomationToolsError):
    """A base class for handling exceptions in this project"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        for key, value in kwargs.items():
            setattr(self, key, value)
class NoRecordError(PlexAutomateError):
    """Thrown when no records exist in a picker selection."""
class GridError(PlexAutomateError):
    """General Plex UX grid related error."""
class GridColumnError(GridError):
    """Thrown when a matching column name is not found."""
class GridRowError(GridError):
    """Thrown when a matching row value is not found."""
class ActionError(PlexAutomateError):
    """Thrown if there is an error on clicking an action bar item."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.expression = kwargs.get('expression')
        self.message = kwargs.get('message')
class LoginError(PlexAutomateError):
    """Thrown if the expected login screens are not found."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.environtment = kwargs.get('environment')
        self.db = kwargs.get('db')
        self.pcn = kwargs.get('pcn')
        self.message = kwargs.get('message')
class UpdateError(PlexAutomateError):
    """Thrown when a banner prevents an update from occurring."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.clean_message = args[0].replace('×', '').replace('\n', '').strip()
        self.detailed_message = str({k:v for k,v in kwargs.items()})

class PlexApiError(PmcAutomationToolsError):
    """A base class for handling exceptions for API calls"""
class PlexResponseError(PlexApiError):...
class DataSourceError(PlexApiError):...
class ApiError(DataSourceError):...
class ClassicConnectionError(DataSourceError):...

class UXResponseError(PlexResponseError):
    def __init__(self, error_dict, **kwargs):
        self.code = error_dict.get('code')
        self.message = error_dict.get('message')
        self.transaction_no = kwargs.get('transaction_no', '')

    def __str__(self):
        return f"transaction_no: {self.transaction_no} - {self.code}: {self.message}"
    def __repr__(self):
        return f"<ErrorDetail(code={self.code}, message={self.message})>"
class UXResponseErrorLog(PlexResponseError):
    def __init__(self, error_dicts, **kwargs):
        self.transaction_no = kwargs.get('transaction_no', '')
        self.errors = [UXResponseError(err, transaction_no = self.transaction_no) for err in error_dicts]
        
    def __getitem__(self, index):
        return self.errors[index]

    def __len__(self):
        return len(self.errors)

    def __str__(self):
        return self.transaction_no + "\n".join(str(error) for error in self.errors)

    def __repr__(self):
        return f"<UXResponseErrorLog with {len(self)} errors>"

    def print_all_errors(self):
        for error in self.errors:
            print(error)

    def filter_by_code(self, code):
        return [error for error in self.errors if error.code == code]
        