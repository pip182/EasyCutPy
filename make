#!/bin/bash


if [[ -z "$1" ]]
  then
    echo "Usage: $0 WHAT"
    echo ""
    echo "What are we making?":
    echo "  ui - Translate all ui file into .py files."
    echo "  rc - Translate .grc file into .poy files."
    echo "  all - Make everything!"
    exit 1
fi

if [ "$1" == "ui" ] || [ "$1" == "all" ];
  then
    pyuic5 main.ui >> main_gui.py
fi

if [ "$1" == "rc" ] | [ "$1" == "all" ];
  then
  pyrcc5 -o resources_rc.py resources.qrc
fi
