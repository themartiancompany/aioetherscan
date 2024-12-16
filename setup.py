# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioetherscan', 'aioetherscan.modules.extra']

package_data = \
{'': ['*'],
 'aioetherscan': ['modules/*'],
 'aioetherscan.modules.extra': ['generators/*']}

install_requires = \
['aiohttp-retry>=2.8.3,<3.0.0',
 'aiohttp>=3.4,<4.0',
 'asyncio_throttle>=1.0.1,<2.0.0',
 'cython>=3.0.11,<4.0.0']

setup_kwargs = {
    'name': 'aioetherscan',
    'version': '0.9.6.1',
    'description': 'Etherscan API async Python wrapper',
    'long_description': 'None',
    'author': 'Pellegrino Prevete',
    'author_email': 'pellegrinoprevete@gmail.com',
    'maintainer': 'Pellegrino Prevete',
    'maintainer_email': 'pellegrinoprevete@gmail.com',
    'url': 'https://github.com/themartiancompany/aioetherscan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
