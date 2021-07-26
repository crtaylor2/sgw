#!/bin/env bash

######################################################################
#
# Cariessa Taylor
# July 26, 2021
# CSIS 483 Phase 2
#
# This bash script is an automated test for the Spread God's Word
# program. It tests both the command line interface and REST
# interface.
#
# For more details, see the README.md file.
#
######################################################################

# Test Command Line - Languages
langs_cli=$(python SpreadGodsWord.py --print-supported-languages)
langs_cli_pass=0
langs_cli_fail=0
for lang in `cat languages.txt`
do
    lang=$(echo $lang | tr -d '\r')
    if [[ "$langs_cli" =~ .*"$lang".* ]]
    then
        echo "PASS (command line): found language $lang"
        langs_cli_pass=$((langs_cli_pass + 1))
    else
        echo "FAIL (command line): didn't find language $lang"
        langs_cli_fail=$((langs_cli_fail + 1))
    fi
done
if [ $langs_cli_fail -eq 0 ]
then
    echo "Found all $langs_cli_pass languages for command line"
else
    echo "Did not find $langs_cli_fail languages for command line"
    exit $langs_cli_fail
fi
echo ""

# Test Command Line - Translations
trans_cli=$(python SpreadGodsWord.py --print-supported-translations)
trans_cli_pass=0
trans_cli_fail=0
for lang in `cat languages.txt`
do
    lang=$(echo $lang | tr -d '\r')
    if [[ "$trans_cli" =~ .*"$lang".* ]]
    then
        echo "PASS (command line): found translation for language $lang"
        trans_cli_pass=$((trans_cli_pass + 1))
    else
        echo "FAIL (command line): didn't find translation for language $lang"
        trans_cli_fail=$((trans_cli_fail + 1))
    fi
done
if [ $trans_cli_fail -eq 0 ]
then
    echo "Found translations for all $trans_cli_pass languages for command line"
else
    echo "Did not find translations for $trans_cli_fail languages for command line"
    exit $trans_cli_fail
fi
echo ""

#python SpreadGodsWord.py --reference gen1:1
#python SpreadGodsWord.py --reference Acts15:1-5,10,15 --version aov

# Start REST Service
echo "Starting REST server..."
python SpreadGodsWord.py --server &> /dev/null &
sleep 10
echo ""

# Test REST interface - Languages
langs_cli=$(curl -s http://localhost:5000/languages)
langs_cli_pass=0
langs_cli_fail=0
for lang in `cat languages.txt`
do
    lang=$(echo $lang | tr -d '\r')
    if [[ "$langs_cli" =~ .*"$lang".* ]]
    then
        echo "PASS (rest): found language $lang"
        langs_cli_pass=$((langs_cli_pass + 1))
    else
        echo "FAIL (rest): didn't find language $lang"
        langs_cli_fail=$((langs_cli_fail + 1))
    fi
done
if [ $langs_cli_fail -eq 0 ]
then
    echo "Found all $langs_cli_pass languages for rest"
else
    echo "Did not find $langs_cli_fail languages for rest"
    exit $langs_cli_fail
fi
echo ""

# Test REST interface - Translations
trans_cli=$(curl -s http://localhost:5000/translations)
trans_cli_pass=0
trans_cli_fail=0
for lang in `cat languages.txt`
do
    lang=$(echo $lang | tr -d '\r')
    if [[ "$trans_cli" =~ .*"$lang".* ]]
    then
        echo "PASS (rest): found translation for language $lang"
        trans_cli_pass=$((trans_cli_pass + 1))
    else
        echo "FAIL (rest): didn't find translation for language $lang"
        trans_cli_fail=$((trans_cli_fail + 1))
    fi
done
if [ $trans_cli_fail -eq 0 ]
then
    echo "Found translations for all $trans_cli_pass languages for rest"
else
    echo "Did not find translations for $trans_cli_fail languages for rest"
    exit $trans_cli_fail
fi
echo ""

#curl http://localhost:5000/references/gen1:1
#curl http://localhost:5000/references/Acts15:1-5,10,15/aov
