'''
chaya.core.storage
------------------

define storage interface
'''

from typing import Iterable, Optional, Protocol

from chaya.core.model import BaseRecord


class StorageBackend(Protocol):
    def load_all(self) -> Iterable[BaseRecord]: ...
    def save(self, record: BaseRecord) -> None: ...
    def delete(self, record_id: str) -> None: ...
    def get(self, record_id: str) -> Optional[BaseRecord]: ...
