from typing import Optional

from pluggy import HookimplMarker

from chaya.core.model import BaseRecord

hookimpl = HookimplMarker("chaya")


class BookRecord(BaseRecord):
    type: str = "book"
    publisher: Optional[str] = None
    isbn: Optional[str] = None


@hookimpl
def register_record_types():
    return {"book": BookRecord}

