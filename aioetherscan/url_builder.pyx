from typing import Optional
from shutil import which
from subprocess import check_output as sh
from sys import stdout
from urllib.parse import urlunsplit, urljoin


class UrlBuilder:

  BASE_URL: str = None
  API_URL: str = None

  def __init__(
    self,
    api_key: str,
    api_kind: str,
    network: str) -> None:
    self._API_KEY = api_key
    self._init_api_kinds()
    self._set_api_kind(
      api_kind)
    self._network = network.lower(
      ).strip()

    self.API_URL = self._get_api_url()
    self.BASE_URL = self._get_base_url()

  def _init_api_kinds(
    self):
    _api_kinds = {
      'eth': ('etherscan.io', 'ETH'),
      'etc': ('etc.blockscout.com', 'ETC'),
      'ethw': ('oklink.com/api/v5/explorer/ethw', 'ETH'),
      'bsc': ('bscscan.com', 'BNB'),
      'avax': ('snowtrace.io', 'AVAX'),
      'polygon': ('polygonscan.com', 'MATIC'),
      'polygonzk': ('zkevm.polygonscan.com', 'ETH'),
      'optimism': ('etherscan.io', 'ETH'),
      'base': ('basescan.org', 'ETH'),
      'arbitrum': ('arbiscan.io', 'ETH'),
      'fantom': ('ftmscan.com', 'FTM'),
      'taiko': ('taikoscan.io', 'ETH'),
      'snowscan': ('snowscan.xyz', 'AVAX'),
      'gnosis': ('gnosisscan.io', 'DAI'),
      'kcc': ('scan.kcc.io', 'KCS'),
      'one': ('explorer.harmony.one', 'ONE'),
      'doge': ('explorer.dogechain.dog', 'DOGE'),
    }
    self._API_KINDS = _api_kinds

  def _generate_api_kind(
    self,
    _api_kind: str) -> None:
      _cmd = [
        "evm-chains-explorers",
          "-s",
            "kirsh",
          "-c",
            _api_kind,
          "get",
          "keys_explorers"
      ]
      _out= sh(
        _cmd).decode(
          stdout.encoding)
      _keys_explorers = [
        _key_explorer for _key_explorer in _out.split(
          "\n") if _key_explorer != ""]
      if ( _keys_explorers != [] ):
        for _key_explorer in _keys_explorers:
          self._API_KINDS[_api_kind] = (
            _key_explorer,
            'KIRSH')

  def _set_api_kind(
    self,
    _api_kind: str) -> None:
    _api_kind = _api_kind.lower(
      ).strip()
    if _api_kind not in self._API_KINDS:
      if ( which(
             "evm-chains-explorers")):
        self._generate_api_kind(
          _api_kind)
      else:
        _msg=(
          f'evm-chains-explorers not installed, '
          f'impossible to generate support for '
          f'api_kind {_api_kind} at run-time. '
          f'Only hard-coded api_kind keys are: '
          f'{", ".join(self._API_KINDS)}'
        )
        raise ValueError(
          _msg)
    self.api_kind = _api_kind

  @property
  def _is_main(
    self) -> bool:
    return self._network == 'main'

  @property
  def _base_netloc(
    self) -> str:
    netloc, _ = self._API_KINDS[self.api_kind]
    return netloc

  @property
  def currency(
    self) -> str:
    _, currency = self._API_KINDS[self.api_kind]
    return currency

  def get_link(
    self,
    path: str) -> str:
    return urljoin(
      self.BASE_URL,
      path)

  def _build_url(
    self,
    prefix: Optional[str],
    path: str = '') -> str:
    netloc = self._base_netloc if prefix is None else f'{prefix}.{self._base_netloc}'
    return urlunsplit(
      ('https',
       netloc,
       path,
       '',
       ''))

  def _get_api_url(
    self) -> str:
    prefix_exceptions = {
      ('doge',
       True): None,
      ('ethw',
       True): None,
      ('optimism',
       True): 'api-optimistic',
      ('optimism',
       False): f'api-{self._network}-optimistic',
    }
    default_prefix = 'api' if self._is_main else f'api-{self._network}'
    prefix = prefix_exceptions.get(
      (self.api_kind,
       self._is_main),
      default_prefix)
    return self._build_url(
      prefix,
      'api')

  def _get_base_url(
    self) -> str:
    network_exceptions = {
      ('polygon',
       'testnet'): 'mumbai'}
    network = network_exceptions.get(
      (self.api_kind,
       self._network),
      self._network)
    prefix_exceptions = {
        ('optimism',
         True): 'optimistic',
        ('optimism',
         False): f'{network}-optimism',
    }
    default_prefix = None if self._is_main else network
    prefix = prefix_exceptions.get(
      (self.api_kind,
       self._is_main),
      default_prefix)
    return self._build_url(
      prefix)

  def filter_and_sign(
    self,
    params: dict):
    return self._sign(
      self._filter_params(
        params or {}))

  def _sign(
    self,
    params: dict) -> dict:
    if not params:
      params = {}
    params['apikey'] = self._API_KEY
    return params

  @staticmethod
  def _filter_params(
    params: dict) -> dict:
    return {k: v for k, v in params.items() if v is not None}
