#!/bin/bash

# create/change/commit/push a named branch - assumes on master branch

git branch $1
git checkout $1
git commit --allow-empty -m "Started work on $1."
git push origin $1