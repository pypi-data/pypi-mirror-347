#!/bin/bash
rm -rf build/ dist/ *.egg-info*/
uv build
#python setup.py bdist_wheel --universal
#mv dist/strym-1.0.1-cp39-abi3-linux_x86_64.whl dist/strym-1.0.1-cp39-abi3-manylinux_2_28_x86_64.whl
for f in dist/strym-*-cp39-abi3-linux_x86_64.whl; do
  mv -- "$f" "${f/linux_x86_64/manylinux_2_28_x86_64}"
done
twine upload dist/*
