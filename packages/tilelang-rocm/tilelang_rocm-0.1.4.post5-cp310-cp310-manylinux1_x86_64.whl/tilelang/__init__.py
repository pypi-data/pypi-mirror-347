# Copyright (c) Tile-AI Corporation.
# Licensed under the MIT License.

import sys
import os
import ctypes
import subprocess

import logging
from tqdm import tqdm


class TqdmLoggingHandler(logging.Handler):
    """Custom logging handler that directs log output to tqdm progress bar to avoid interference."""

    def __init__(self, level=logging.NOTSET):
        """Initialize the handler with an optional log level."""
        super().__init__(level)

    def emit(self, record):
        """Emit a log record. Messages are written to tqdm to ensure output in progress bars isn't corrupted."""
        try:
            msg = self.format(record)
            tqdm.write(msg)
        except Exception:
            self.handleError(record)


def set_log_level(level):
    """Set the logging level for the module's logger.

    Args:
        level (str or int): Can be the string name of the level (e.g., 'INFO') or the actual level (e.g., logging.INFO).
        OPTIONS: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(level)


def _init_logger():
    """Initialize the logger specific for this module with custom settings and a Tqdm-based handler."""
    logger = logging.getLogger(__name__)
    handler = TqdmLoggingHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s  [TileLang:%(name)s:%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    set_log_level("INFO")


_init_logger()

logger = logging.getLogger(__name__)

from .env import SKIP_LOADING_TILELANG_SO
from .env import enable_cache, disable_cache, is_cache_enabled  # noqa: F401

import tvm
import tvm._ffi.base

from . import libinfo


def _load_tile_lang_lib():
    """Load Tile Lang lib"""
    if sys.platform.startswith("win32") and sys.version_info >= (3, 8):
        for path in libinfo.get_dll_directories():
            os.add_dll_directory(path)
    # pylint: disable=protected-access
    lib_name = "tilelang" if tvm._ffi.base._RUNTIME_ONLY else "tilelang_module"
    # pylint: enable=protected-access
    lib_path = libinfo.find_lib_path(lib_name, optional=False)
    return ctypes.CDLL(lib_path[0]), lib_path[0]

def check_and_install_rocm_torch():
    """检查并自动安装ROCm PyTorch"""
    try:
        # 检查torch是否已安装且为ROCm版本
        import torch
        if hasattr(torch.version, 'hip') and torch.version.hip:
            print(f"ROCm PyTorch {torch.version.__version__} is already installed")
            return True
    except ImportError:
        pass
    
    print("ROCm PyTorch not found. Installing...")
    install_rocm_torch()
    
    # 强制重新加载torch模块
    if 'torch' in sys.modules:
        del sys.modules['torch']
    
    try:
        import torch
        print(f"Successfully installed ROCm PyTorch {torch.version.__version__}")
        return True
    except ImportError:
        print("Failed to import torch after installation")
        return False

def install_rocm_torch():
    """安装ROCm PyTorch"""
    print("Installing ROCm PyTorch components...")
    
    wheels = [
        "https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torch-2.4.0%2Brocm6.3.4.git7cecbf6d-cp310-cp310-linux_x86_64.whl",
        "https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torchvision-0.19.0%2Brocm6.3.4.gitfab84886-cp310-cp310-linux_x86_64.whl",
        "https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/pytorch_triton_rocm-3.0.0%2Brocm6.3.4.git75cc27c2-cp310-cp310-linux_x86_64.whl",
        "https://repo.radeon.com/rocm/manylinux/rocm-rel-6.3.4/torchaudio-2.4.0%2Brocm6.3.4.git69d40773-cp310-cp310-linux_x86_64.whl"
    ]
    
    # 卸载现有的torch相关包
    print("Uninstalling existing PyTorch...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "uninstall", 
                       "torch", "torchvision", "pytorch-triton-rocm", "torchaudio", "-y"],
                      capture_output=True)
    except subprocess.CalledProcessError:
        print("No existing PyTorch installation found")
    
    # 安装ROCm版本
    print("Downloading and installing ROCm PyTorch...")
    subprocess.run([sys.executable, "-m", "pip", "install"] + wheels, check=True)

# 在模块导入时自动检查并安装
_rocm_torch_checked = False

def ensure_rocm_torch():
    global _rocm_torch_checked
    if not _rocm_torch_checked:
        check_and_install_rocm_torch()
        _rocm_torch_checked = True

# 在模块导入时立即检查
ensure_rocm_torch()

# only load once here
if SKIP_LOADING_TILELANG_SO == "0":
    _LIB, _LIB_PATH = _load_tile_lang_lib()

from .jit import jit, JITKernel, compile  # noqa: F401
from .profiler import Profiler  # noqa: F401
from .cache import cached, set_cache_dir, get_cache_dir  # noqa: F401

from .utils import (
    TensorSupplyType,  # noqa: F401
    deprecated,  # noqa: F401
)
from .layout import (
    Layout,  # noqa: F401
    Fragment,  # noqa: F401
)
from . import (
    transform,  # noqa: F401
    autotuner,  # noqa: F401
    language,  # noqa: F401
    engine,  # noqa: F401
)
from .transform import PassConfigKey  # noqa: F401

from .engine import lower, register_cuda_postproc, register_hip_postproc  # noqa: F401

from .version import __version__  # noqa: F401

from .math import *  # noqa: F403
