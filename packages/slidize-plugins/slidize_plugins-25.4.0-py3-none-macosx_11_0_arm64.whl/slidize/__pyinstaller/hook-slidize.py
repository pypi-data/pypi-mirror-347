from PyInstaller.utils.hooks import get_package_paths
import os
import sys
import importlib.machinery as impmach

(_, root) = get_package_paths('slidize')

datas = [(os.path.join(root, 'netcore'), os.path.join('slidize', 'netcore'))]

datas += [(os.path.join(root, '__init__.py'), 'slidize')]

hiddenimports = []

def get_vspec_ext_suffixes():
    ver_maj_min = ''.join(str(x) for x in sys.version_info[:2])
    return tuple([sfx for sfx in impmach.EXTENSION_SUFFIXES if ver_maj_min in sfx])

_vspec_ext_suffixes = get_vspec_ext_suffixes()

for filename in os.listdir(root):
    fullname = os.path.join(root, filename)
    mod_name = next((filename[:-len(sfx)] for sfx in _vspec_ext_suffixes if filename.endswith(sfx)), None)
    if os.path.isfile(fullname) and filename.endswith(_vspec_ext_suffixes):
        datas += [(fullname, 'slidize')]
        hiddenimports += ['slidize.' + mod_name]
