import importlib, pkgutil, pathlib

PLUGIN_DIR = pathlib.Path(__file__).parent.parent / "plugins"

def load_plugins():
    plugins = {}
    for _, name, _ in pkgutil.iter_modules([str(PLUGIN_DIR)]):
        mod = importlib.import_module(f"plugins.{name}")
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if hasattr(obj, "name") and callable(getattr(obj, "on_node", None)):
                plugins[obj.name] = obj()
    return plugins
