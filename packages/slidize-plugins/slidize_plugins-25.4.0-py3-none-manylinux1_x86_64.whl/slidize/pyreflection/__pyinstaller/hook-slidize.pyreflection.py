from PyInstaller.utils.hooks import get_package_paths
import os.path

(_, root) = get_package_paths('slidize')

datas = [(os.path.join(root, 'assemblies', 'pyreflection'), os.path.join('slidize', 'assemblies', 'pyreflection'))]

hiddenimports = [ 'slidize', 'slidize.pygc' ]

