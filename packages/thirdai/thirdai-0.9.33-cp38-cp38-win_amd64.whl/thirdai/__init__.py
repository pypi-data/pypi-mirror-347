"""The ThirdAI Python package"""


# start delvewheel patch
def _delvewheel_patch_1_10_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'thirdai.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-thirdai-0.9.33')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-thirdai-0.9.33')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

__all__ = [
    "bolt",
    "search",
    "dataset",
    "data",
    "hashing",
    "distributed_bolt",
    "licensing",
    "demos",
    "gen",
    "telemetry",
    "set_global_num_threads",
    "logging",
]

# Include these so we can use them just by import the top level.
import thirdai.bolt as bolt
import thirdai.data as data
import thirdai.dataset as dataset
import thirdai.demos as demos
import thirdai.gen as gen
import thirdai.hashing as hashing
import thirdai.licensing as licensing
import thirdai.search as search
import thirdai.telemetry as telemetry

# Relay __version__ from C++
from thirdai._thirdai import __version__, logging, set_seed

try:
    from thirdai._thirdai import set_global_num_threads

    __all__.extend(["set_global_num_threads"])
except ImportError:
    pass

# ray's grcpio dependency installation is not trivial on
# Apple Mac M1 Silicon and requires conda.
#
# See:
# [1] https://github.com/grpc/grpc/issues/25082,
# [2] https://docs.ray.io/en/latest/ray-overview/installation.html#m1-mac-apple-silicon-support
# For the time being users are expected to explictly import the package.
#
# TODO(pratkpranav): Uncomment the following when this issue is solved upstream.
# import thirdai.distributed_bolt


# Don't import this or include it in __all__ for now because it requires
# pytorch + transformers.
# import thirdai.embeddings