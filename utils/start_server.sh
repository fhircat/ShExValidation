#!/bin/bash
process="ShEx.shex"
while :
do
	if ! pgrep -qf "$process";
	then
	    date
      echo "###### Validation Server is not running, Starting... Please wait for 30-35 seconds before you can use it! ####### "
      validate -x ./fhir_rdf_validation/ShExSchemas/R5One/ShEx.shex --diagnose --human  --serve http://localhost/validate &
      sleep 45
  else
      #echo "****** Validation Server is running.. checking again in 10 seconds *******"
      sleep 10
  fi
done