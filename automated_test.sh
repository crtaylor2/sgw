#!/bin/env bash

# Test Command Line
python SpreadGodsWord.py --print-supported-languages
python SpreadGodsWord.py --print-supported-translations english
python SpreadGodsWord.py --reference gen1:1
python SpreadGodsWord.py --reference Acts15:1-5,10,15 --version aov

# TODO: Validate results of each command line command

# Test REST Service
python SpreadGodsWord.py --server &
curl http://localhost:5000/languages
curl http://localhost:5000/translations/english
curl http://localhost:5000/references/gen1:1
curl http://localhost:5000/references/Acts15:1-5,10,15/aov

# TODO: Validate results of each REST command
