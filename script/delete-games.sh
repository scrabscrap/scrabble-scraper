#!/bin/bash

# working directory is $PROJECT/work
SCRIPTPATH=$(dirname "$0")
PROJECT="$(cd "$SCRIPTPATH/.." && pwd)"
WORKDIR=$PROJECT/work

rm -rf $WORKDIR/web/*
