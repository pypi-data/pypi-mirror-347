### __init__.py
### MIT LICENSE 2018 Shaun Harker
### MIT LICENSE 2024 Marcio Gameiro


# start delvewheel patch
def _delvewheel_patch_1_10_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'dsgrn.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-dsgrn-1.8.0')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-dsgrn-1.8.0')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_1()
del _delvewheel_patch_1_10_1
# end delvewheel patch

from dsgrn._dsgrn import *
from dsgrn.SubdomainGraph import *
from dsgrn.BlowupGraph import *
from dsgrn.Graphics import *
from dsgrn.Query.Graph import *
from dsgrn.Query.Database import *
from dsgrn.Query.Hexcodes import *
from dsgrn.Query.MonostableQuery import *
from .Query.BistableQuery import *
from .Query.MultistableQuery import *
from .Query.NstableQuery import *
from .Query.SingleFixedPointQuery import *
from .Query.DoubleFixedPointQuery import *
from .Query.MonostableFixedPointQuery import *
from .Query.SingleGeneQuery import *
from .Query.InducibilityQuery import *
from .Query.HysteresisQuery import *
from .Query.PhenotypeQuery import *
from .Query.PosetOfExtrema import *
from .Query.Logging import *
from .Query.StableFCQuery import *
from .Query.ComputeSingleGeneQuery import *
from dsgrn.EssentialParameterNeighbors import *
from dsgrn.BooleanParameterNeighbors import *
from dsgrn.ParameterPartialOrders import *
from dsgrn.ParameterFromSample import *
from dsgrn.SaveDatabaseJSON import *
from dsgrn.EquilibriumCells import *
from dsgrn.MorseGraphIsomorphism import *
from dsgrn.DrawParameterGraph import *

import sys
import os
import pickle

configuration().set_path(os.path.dirname(__file__) + '/Resources')
