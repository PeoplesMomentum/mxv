#!/bin/bash

# switch to updated master branch and delete named branch - assumes on named branch

git checkout master
git pull origin master
git branch -d $1