from setuptools import setup, Extension
from Cython.Build import cythonize
import sys

# Config of extensions is still handled in setup.py for two reasons:
# 1. As of time of writing (14 May 2025), a full configuration of Cython extensions in pyproject.toml using setuptools is still experimental
# 2. The compiler flags are platform dependent, and the Cython extension module is not yet able to handle this in pyproject.toml
#
# - bjorge

IS_WINDOWS = sys.platform.startswith("win")

extra_compile_args = [] if IS_WINDOWS else ["-Wno-unused-function", "-std=c++11"]

extensions = [
    Extension(
        "isf_pandas_msgpack.msgpack._packer",
        sources=["src/isf_pandas_msgpack/msgpack/_packer.pyx"],
        language="c++",
        include_dirs=["src/isf_pandas_msgpack/includes"],
        extra_compile_args=extra_compile_args,
    ),
    Extension(
        "isf_pandas_msgpack.msgpack._unpacker",
        sources=["src/isf_pandas_msgpack/msgpack/_unpacker.pyx"],
        language="c++",
        include_dirs=["src/isf_pandas_msgpack/includes"],
        extra_compile_args=extra_compile_args,
    ),
    Extension(
        "isf_pandas_msgpack._move",
        sources=["src/isf_pandas_msgpack/move.c"]
    ),
]

setup(
    ext_modules=cythonize(extensions),
)
