import datetime as dt
from ..auxiliar import Logger

class GoogleInterface(Logger):
    name: str
    _token: any
    _service: any
    SCOPES: list
    enable_logs: bool
    
    # CALENDAR
    def calendar_list_events(self, event_count: int = 10, start_date_time: dt.datetime = None, end_date_time: dt.datetime = None) -> list[any]: ...
    
    def calendar_create_event(self, summary: str, start_date_time: dt.datetime, end_date_time: dt.datetime, **keyargs) -> None: ...
    
    # GOOGLE ACCOUNT
    def get_token(self) -> any: ...