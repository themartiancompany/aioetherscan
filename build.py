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
  from pathlib import Path

  def _extension_get(
    _extension_path):
    _extension_name = str(
      Path(
        _extension_path).with_suffix(
          '')).replace(
            "/",
            ".")
    _extension = Extension(
      name=_extension_name,
      sources=[
        _extension_path])
    return _extension

  # This function will be executed in setup.py:
  def build(
    setup_kwargs):
    extensions = [
      "aioetherscan/client.pyx",
      "aioetherscan/common.pyx",
      "aioetherscan/exceptions.pyx",
      "aioetherscan/network.pyx",
      "aioetherscan/url_builder.pyx",
      _extension_get(
        "aioetherscan/modules/account.pyx"),
      _extension_get(
        "aioetherscan/modules/base.pyx"),
      _extension_get(
        "aioetherscan/modules/block.pyx"),
      _extension_get(
        "aioetherscan/modules/contract.pyx"),
      _extension_get(
        "aioetherscan/modules/gas_tracker.pyx"),
      _extension_get(
        "aioetherscan/modules/logs.pyx"),
      _extension_get(
        "aioetherscan/modules/proxy.pyx"),
      _extension_get(
        "aioetherscan/modules/stats.pyx"),
      _extension_get(
        "aioetherscan/modules/token.pyx"),
      _extension_get(
        "aioetherscan/modules/transaction.pyx"),
      _extension_get(
        "aioetherscan/modules/extra/contract.pyx"),
      _extension_get(
        "aioetherscan/modules/extra/link.pyx"),
      _extension_get(
        "aioetherscan/modules/extra/generators/blocks_parser.pyx"),
      _extension_get(
        "aioetherscan/modules/extra/generators/blocks_range.pyx"),
      _extension_get(
        "aioetherscan/modules/extra/generators/generator_utils.pyx"),
      _extension_get(
        "aioetherscan/modules/extra/generators/helpers.pyx")
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
