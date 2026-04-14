from setuptools import setup, Extension
import pybind11

ext = Extension(
    "sat_backend",
    sources=["sat_backend.cpp"],
    include_dirs=[pybind11.get_include()],
    extra_compile_args=["/O2", "/openmp"]
)

setup(
    name="sat_backend",
    version="1.0",
    ext_modules=[ext]
)

