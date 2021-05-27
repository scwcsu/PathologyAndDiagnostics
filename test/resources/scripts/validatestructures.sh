#!/bin/bash

#########################################################################################
# Bash script to validate the set of fhir structure definitions required to run validation  #
#########################################################################################
java -jar validator_cli.jar ./../structures/*.xml -version 3.0 -ig https://interopen.github.io/careconnect-base-stu3 -ig ./../structures/ -tx n/a -output structurevalidationresults.xml
