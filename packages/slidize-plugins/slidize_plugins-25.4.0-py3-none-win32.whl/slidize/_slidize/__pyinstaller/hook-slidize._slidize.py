from PyInstaller.utils.hooks import get_package_paths
import os.path

(_, root) = get_package_paths('slidize')

datas = [(os.path.join(root, 'assemblies', '_slidize'), os.path.join('slidize', 'assemblies', '_slidize'))]

hiddenimports = [ 'slidize', 'slidize.pydrawing', 'slidize.pyreflection', 'slidize.pygc', 'slidize.pycore' ]

