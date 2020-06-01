#!/bin/bash
zipfile=UCLACaseLawCite_Tristian_Azuara.zip
rm -f $zipfile
zip -r $zipfile . \
	-x "Data/*" -x ".git/*" \
	-x "*/__pycache__" -x "*/__pycache__/*" \
	-x "*.zip" -x .DS_Store

unzip -l $zipfile