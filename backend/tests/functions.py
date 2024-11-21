from datetime import datetime, timezone


def date_format(date_time: datetime) -> datetime | None:
    """Приводит дату и время к единому формату."""
    if date_time is None:
        return None

    if date_time.tzinfo is None:
        return date_time.replace(tzinfo=timezone.utc)

    return date_time


def date_from_iso_str(date_str: str) -> datetime | None:
    """Преобразует строку с датой в iso формате в datetime."""
    if date_str is None:
        return None
    return datetime.fromisoformat(date_str)
