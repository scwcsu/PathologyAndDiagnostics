This folder holds messages submitted by suppliers taking part in testing.

Submission Process
==================
The process for submitting a new set of messages for validation and for testing 
with other suppliers is to create a folder containing the messages for 
testing/validation and submit a pull request to the repository.

Upon succesful validation the Pull Request will be merged to the develop branch.

Note: This process assumes that you make a public fork of the official repository.
If this is not possible, files can be submited directly to the team who will 
validate and merge the files on your nehalf.

Steps
=====
If this is your first submission:
    1 - Fork the repository using the Git web interface

    2 - Clone a local copy of your fork

    3 - Checkout the develop branch of the repository

    4 - Make a branch from the develop branch called submission/[supplier name]

    5 - Create a folder under the suppliersubmissions folder called [supplier name]

One you have create a branch and a folder:

    1 - Place the messages to be tested into the suppliersubmissions/[supplier name]
        Files should be named to indicate which test they are intended to be used for.

    2 - Check the messages using the validation jar included in the repostory

        2a - change the the scripts \test\resources\scripts folder. 

        2b - If there is a script called validate[supplier name].sh you cna run that script.

        2c - If there isn't yet a script created you can run the validator using the following command:

java -jar validator_cli.jar ./../../../suppliersubmissions/[supplier name]/*.xml -version 3.0 -ig https://interopen.github.io/careconnect-base-stu3 -ig ./../structures/ -tx n/a -output ./../../../suppliersubmissions/[suppliername]validationresults.xml

    You may need to adjust the file pattern: ./../../../suppliersubmissions/[supplier name]/*.xml to match the files you have included (e.g. if they are json files you might use ./../../../suppliersubmissions/[supplier name]/*.json) 

When you are ready to submit the files for formal validation:

    1 - Merge the develop branch back to your submission branch

    2 - Add and commit your files your branch

    3 - Push your changes to your repository

    4 - Generate a pull request to the develop branch of the main repository using the git webn interface.