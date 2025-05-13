# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semverize']

package_data = \
{'': ['*']}

install_requires = \
['packaging>=23.0', 'semver>=3,<4']

extras_require = \
{'cli': ['click>=8,<9']}

entry_points = \
{'console_scripts': ['semverize = semverize.cli:semverize']}

setup_kwargs = {
    'name': 'semverize',
    'version': '0.1.0',
    'description': 'Coerce PEP 440 to SemVer, when possible',
    'long_description': 'None',
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/metabolize/semverize',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
