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

  _source_files= [
    "aioetherscan/client.pyx",
    "aioetherscan/common.pyx",
    "aioetherscan/exceptions.pyx",
    "aioetherscan/network.pyx",
    "aioetherscan/url_builder.pyx",
    "aioetherscan/modules/account.pyx",
    "aioetherscan/modules/base.pyx",
    "aioetherscan/modules/block.pyx",
    "aioetherscan/modules/contract.pyx",
    "aioetherscan/modules/gas_tracker.pyx",
    "aioetherscan/modules/logs.pyx",
    "aioetherscan/modules/proxy.pyx",
    "aioetherscan/modules/stats.pyx",
    "aioetherscan/modules/token.pyx",
    "aioetherscan/modules/transaction.pyx",
    "aioetherscan/modules/extra/contract.pyx",
    "aioetherscan/modules/extra/link.pyx",
    "aioetherscan/modules/extra/generators/blocks_parser.pyx",
    "aioetherscan/modules/extra/generators/blocks_range.pyx",
    "aioetherscan/modules/extra/generators/generator_utils.pyx",
    "aioetherscan/modules/extra/generators/helpers.pyx"
  ]

  def _file_name_get(
    _path):
    return str(
      Path(
        _path).with_suffix(
          ''))

  def _file_extension_replace(
    _path,
    _extension):
    return str(
      Path(
        _file_name_get(
          _path)).with_suffix(
            _extension))

  def _build_extension_name_get(
    _source_file):
    return _file_name_get(
      _source_file.replace(
        "/",
        "."))

  def _build_extension_get(
    _source_file):
    _extension_name = _build_extension_name_get(
      _source_file)
    _extension = Extension(
      name=_extension_name,
      sources=[
        _source_file])
    return _extension

  def _build_extensions_get(
    _source_files):
    return [ _build_extension_get(
      _file) for _file in _source_files]

  def _excluded_package_data_get(
    _source_files):
    _excluded_files = []
    for _file in _source_files:
      _c_file = _file_extension_replace(
        _file,
        ".c")
      _excluded_files.append(
        _c_file)
      _excluded_files.append(
        _file)
    return _excluded_files

  def _included_package_data_get():
    _included_files = [
      "aioetherscan/*.so",
      "aioetherscan/modules/*.so",
      "aioetherscan/modules/extra/*.so"]
    return _included_files 

  def build(
    setup_kwargs):
    _build_extensions = _build_extensions_get(
      _source_files)
    _excluded_package_data = _excluded_package_data_get(
      _source_files)
    _included_package_data = _included_package_data_get()
    _extensions = [
      *_build_extensions
    ]
    _exclude_package_data = {
      '':
        _excluded_package_data,
    }
    _include_package_data = {
      '':
        _included_package_data,
      'aioetherscan':
        ['modules/*.so',
         'modules/*.py'],
      'aioetherscan.modules.extra':
        ['generators/*.so',
         'generaters/*.py']
    }
    _ext_modules = cythonize(
      _extensions,
      language_level = 3,
      compiler_directives = {
        'linetrace':
          True })
    _cmdclass = {
      'build_ext':
        build_ext }
    os.environ['CFLAGS'] = '-O3'
    setup_kwargs.update(
      { 'exclude_package_data':
          _exclude_package_data,
         'package_data':
          _include_package_data,
        'ext_modules':
          _ext_modules,
        'cmdclass':
          _cmdclass
      })
