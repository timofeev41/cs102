#!/usr/bin/env bash

# Simple script to create new venv and install all deps

# Main config
ver=0.0.2
ENVPATH=$HOME/.envs
ENVNAME=$(basename $PWD)
FINAL=$ENVPATH/$ENVNAME
REQSPATH=$PWD/requirements.txt

# Pretty colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NOCOLOR='\033[0m'

echo "Simple Python Env setup v$ver"

main() {
  if [ -d $HOME/.envs ]; then
    echo -e "Found ${RED}$ENVPATH${NOCOLOR} dir, will create ${RED}$ENVNAME${NOCOLOR} env here"
    if [ -d $FINAL ]; then
      echo -e "Env for ${RED}$ENVNAME${NOCOLOR} already exists"
    else
      tput civis
      echo -ne "Env for ${RED}$ENVNAME${NOCOLOR} [ ]\r"
      python -m venv $FINAL
      echo -ne "Env for ${RED}$ENVNAME${NOCOLOR} [${GREEN}✓${NOCOLOR}]\r"
      echo
      tput cnorm
    fi
  else
    echo -e "Dir ${RED}$ENVPATH${NOCOLOR} not found, exiting..."
  fi
}

dbg() {
  rm -rf $FINAL
  echo "Deleted $FINAL env"
}

help() {
  echo
  echo "Syntax ./setup.sh [-h|d|i]"
  echo "Options:"
  echo "h    Help facility"
  echo "d    Debug mode"
  echo "i    Install deps"
  echo
}

deps() {
  tput civis
  while read line; do
    echo -ne "Installing $line [ ]\r"
    $FINAL/bin/pip install $line &>/dev/null
    echo -ne "Installing $line [${GREEN}✓${NOCOLOR}]\r"
    echo
  done <$REQSPATH
  tput cnorm
  echo -en "Source your repo using ${GREEN}source $FINAL/bin/activate\n"
}

checkreqs() {
  if [ -f $REQSPATH ]; then
    deps
  else
    echo -e "Not found ${RED}requirements.txt${NOCOLOR} file"
  fi
}

while getopts ":hdi" option; do
  case $option in
  h)
    help
    exit
    ;;
  d)
    dbg
    exit
    ;;
  i)
    checkreqs
    exit
    ;;
  *)
    echo "Unknown argument"
    exit
    ;;
  esac
done

main
