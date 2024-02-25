from setuptools import setup, Extension

module = Extension('simpleddc',
                   sources=['simpleddc.c', 'simpleddc-python.c'],
                   libraries=['ddcutil'],
                   library_dirs=['/usr/lib/aarch64-linux-gnu/libddcutil.so.4'],
                   include_dirs=['/usr/include'])

setup(name='example',
      version='1.0',
      ext_modules=[module])
