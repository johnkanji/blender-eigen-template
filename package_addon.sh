#!/bin/sh

cd build && make -j8 && cd ..
cp -f build/*.so cppTemplate
