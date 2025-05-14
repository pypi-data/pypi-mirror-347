from setuptools import setup
from setuptools_rust import Binding, RustExtension

setup(name='cpp-demangle2',
      author="Untether AI",
      author_email="software@untether.ai",
      url='http://github.com/untetherai/py-cpp-demangle/',
      description="A package for demangling C++ linker symbols",
      long_description=open("README.rst").read(),
      version="0.1.3",
      rust_extensions=[RustExtension('cpp_demangle', 'Cargo.toml',  binding=Binding.PyO3)],
      test_suite="tests",
      license="MIT",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities"],
      zip_safe=False)
