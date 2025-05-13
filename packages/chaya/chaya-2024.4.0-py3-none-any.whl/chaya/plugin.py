# chaya/plugin.py
from pluggy import PluginManager
from chaya import hookspecs

plugin_manager = PluginManager("chaya")
plugin_manager.add_hookspecs(hookspecs)
plugin_manager.load_setuptools_entrypoints("chaya.plugins")

