from datetime import datetime


class DatetimeFormatter:

    def __init__(self, fmt: str = "%Y-%m-%d %H:%M:%S"):
        self.fmt = fmt

    def dt_2_str(self, dt: datetime) -> str:
        return dt.strftime(self.fmt)

    def str_2_dt(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, self.fmt)
