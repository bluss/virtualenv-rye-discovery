#!/bin/bash

set -ex
: ${RYE_HOME:=$HOME/.rye}
. "$RYE_HOME"/env

# check that we can use rye discovery with virtualenv

export VIRTUALENV_DISCOVERY=rye

for version in py39 3.9 cpython3.10 py310 3.10 pypy39; do
    rye run virtualenv -p "$version" testenv/"$version"
done

rm -fr ./testenv
