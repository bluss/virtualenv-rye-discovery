# virtualenv-rye-discovery

virtualenv plugin to allow discovery of versions through [Rye][rye] - which can
supply an installed version or fetch if missing.

Currently supports version specs like: py39, cpython39, pypy39.

[rye]: https://rye-up.com

This plugin was built to enable Tox version finding through rye.
Tox 4 instructs that custom python finding happens through virtualenv:
https://tox.wiki/en/latest/plugins.html

## Example

Test the example in this repository. The rye project here has tox as a
dev-dependency for this demo. It will pull down the required versions
from Rye (see `tox.ini`).

1. Install Rye
2. `rye sync`
3. `VIRTUALENV_DISCOVERY=rye rye run tox`

`VIRTUALENV_DISCOVERY` needs to be explicitly set, or set in `toxfile.py`
(as shown in the repo).
