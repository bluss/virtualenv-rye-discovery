#!/bin/bash

set -ex
: ${RYE_HOME:=$HOME/.rye}
. "$RYE_HOME"/env

export VIRTUALENV_DISCOVERY=rye

for version in cpython3.10 py39 3.9 py310 3.10 pypy39; do
    rye run virtualenv -p "$version" testenv/"$version"
done

rm -fr ./testenv
