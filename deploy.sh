#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 <comment>"
	exit 0
fi

rm -rf seleniumprocessor/__pycache__

git add .
git commit -m "$1"
git push -u origin main

python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*

rm -rf build 2> /dev/null
rm -rf dist 2> /dev/null
rm -rf seleniumprocessor.egg-info 2> /dev/null
rm -rf seleniumprocessor.egg-info 2> /dev/null
