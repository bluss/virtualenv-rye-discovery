Note: This work is contributed to the community by implementing a solution
and sharing it, long term maintainership is uncertain.

# virtualenv-rye-discovery

virtualenv plugin to allow discovery of versions through [Rye][rye] - which can
supply an installed version or fetch if missing.

Currently supports version specs like: py39, cpython39, pypy39.

[rye]: https://rye-up.com

This plugin was built to enable Tox version finding through rye.
Tox 4 instructs that custom python finding happens through virtualenv:
https://tox.wiki/en/latest/plugins.html

## Example

See https://github.com/bluss/tox-rye for the tox configuration "interface"
plugin for this - prefer installing it and use this functionality through it.

How to use this with virtualenv:

1. Install Rye
2. `rye sync`
3. `virtualenv --discovery rye -p 3.9 myenv`

If `--discovery` can't be passed directly, then `VIRTUALENV_DISCOVERY=rye`
cnn be explicitly set in the environment to enable.


## Other

Requires rye >= 0.7
