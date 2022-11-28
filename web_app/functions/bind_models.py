import inspect
import pkgutil
import sys
from pathlib import Path
from web_app.globals import models


class ModelsPackage:
    name = ""
    path = ""
    list = []
    find = False

    def __repr__(self):
        returned = f"name = {self.name}\npath = {self.path}"
        for ls in self.list:
            returned += f"\n\t{ls}"
        return returned


def find_models(app_name):
    models_pkg = ModelsPackage()
    find_models_pkg(app_name, models_pkg)
    return models_pkg


def find_models_pkg(module_name, models_pkg):
    filename = sys.modules[module_name].__file__
    package_path = Path(filename).resolve().parent
    for sub_module in pkgutil.walk_packages([str(package_path)]):
        _, sub_module_name, pkg = sub_module
        qname = f"{module_name}.{sub_module_name}"
        if pkg and qname in sys.modules.keys():
            find_models_pkg(qname, models_pkg)
        if sub_module_name == 'models':
            filename = sys.modules[qname].__file__
            package_path = Path(filename).resolve().parent
            models_pkg.name = qname
            models_pkg.path = package_path
            models_pkg.find = True
            for module in pkgutil.walk_packages([str(package_path)]):
                info, sub_module_name, pkg = module
                if not pkg:
                    models_pkg.list.append(sub_module_name)
            return True
    return False


def bind(app_name):
    package = find_models(app_name)
    for module_name in package.list:
        module = __import__(f'{package.name}.{module_name}', fromlist=[module_name])
        for element_name in dir(module):
            element = getattr(module, element_name)
            if inspect.isclass(element):
                if hasattr(element, '__tablename__'):
                    models[getattr(element, '__tablename__')] = element
