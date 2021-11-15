#!/bin/bash

mkdir -p pdf

for f in *.md; do 
	out="$(basename $f .md)"
	pandoc -f markdown config-yaml $f -o pdf/$out.pdf --highlight-style tango
done
