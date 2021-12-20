#!/bin/bash

# working directory is $PROJECT/work
SCRIPTPATH=$(dirname "$0")
PROJECT="$(cd "$SCRIPTPATH/.." && pwd)"
WORKDIR=$PROJECT/work

cp -f $PROJECT/python/default/* $WORKDIR/
