from PyInstaller.utils.hooks import get_package_paths
import os.path

(_, root) = get_package_paths('slidize')

datas = [(os.path.join(root, 'assemblies', 'pycore'), os.path.join('slidize', 'assemblies', 'pycore'))]

datas += [(os.path.join(root, 'pycore'), os.path.join('slidize', 'pycore'))]

hiddenimports = [ 'slidize', 'slidize.pygc' ]

