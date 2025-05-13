# chaya/hookspecs.py
from pluggy import HookspecMarker

hookspec = HookspecMarker("chaya")

@hookspec
def register_record_types() -> dict[str, type]: ...

