#!/bin/bash
pandoc --pdf-engine=xelatex --highlight-style zenburn \
	-V colorlinks -V urlcolor=NavyBlue \
	-V geometry:"top=2cm, bottom=1.5cm, left=2cm, right=2cm" \
	-o README.pdf README.md