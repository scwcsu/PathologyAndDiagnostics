#!/bin/bash

#########################################################################################
# Bash script to validate the set of fhir structure definitions required to run validation  #
#########################################################################################
java -jar validator_cli.jar ./../../../suppliersubmissions/lims1/*.xml -version 3.0 -ig https://interopen.github.io/careconnect-base-stu3 -ig ./../structures/ -tx n/a -output ./../../../suppliersubmissions/lims1validationresults.xml
