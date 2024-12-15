import os

try:
  from Cython.Build import cythonize
except ImportError:
  def build(
    setup_kwargs):
      pass
else:
  from setuptools import Extension
  from setuptools.dist import Distribution
  from distutils.command.build_ext import build_ext

  # This function will be executed in setup.py:
  def build(
    setup_kwargs):
    extensions = [
      "aioetherscan/client.pyx",
      "aioetherscan/common.pyx",
      "aioetherscan/exceptions.pyx",
      "aioetherscan/network.pyx",
      "aioetherscan/url_builder.pyx",
      "aioetherscan/modules/account.pyx"
    ]
    os.environ['CFLAGS'] = '-O3'
    setup_kwargs.update({
      'ext_modules':
        cythonize(
          extensions,
          language_level=3,
          compiler_directives={'linetrace':
                                 True},
      ),
      'cmdclass':
        {'build_ext':
           build_ext}
    })
