# Deduplication Scripts
By Kelvin Lin, Summer 2024 Data Systems Engineering Intern

This repository contains a script for data manipulation and web scraping using Python. The script leverages several libraries for handling CSV files, web scraping with Selenium, and string matching with fuzzywuzzy.

## Prerequisites

Before running the script, ensure you have the following installed:

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Required Python Libraries

The script requires several Python libraries. You can install them using `pip` or `pip3`. Below are the libraries needed:

- pandas
- selenium
- pyperclip
- fuzzywuzzy
- python-Levenshtein
- thefuzz

Install in VSCode Terminal Using...

```
pip install pandas selenium pyperclip fuzzywuzzy python-Levenshtein thefuzz
```
or
```
pip3 install pandas selenium pyperclip fuzzywuzzy python-Levenshtein thefuzz
```

## Microsoft Edge WebDriver Setup
1. Check Your Edge Browser Version:
- Open Microsoft Edge.
- Go to the menu (three dots in the upper right corner) -> Settings -> About Microsoft Edge.
- Note the version number of your Edge browser.

2. Download and Extract WebDriver
- Go to the [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads) download page. 
- Download the correct Edge WebDriver
- Then, extract the downloaded zip file, and note the path to the driver executable. You can do this by right-clicking on the file, and copy file path. 

## Hardcoded Path Updates

- The file paths are hardcoded, so the file paths in each need to be changed.
- Go into the Python files, and update the driver path variables or wherever you see a driver file path to your driver path.
- Bring your csv files that you want to process into this directory. Then, update all the input file paths. Note that these can be full paths (if it's in a different directory), or just the file name in this directory
- Also, update the output file names. The file outputs does not need to exist before, as the script will create one. If it already exists, it will overwrite an existing file. 

## Other Notes
- Functionality exists for a the script to continue from a certain line in the input file. Update this variable in the code to determine which line to continue from if the script crashes or for whatever reason. 

## What Does Each File Do? 
- cleanfuncs.py: This file contains functions that are used for cleaning of information. Functions from this file are used in other files, and we don't need to touch this file. 
- doublecsv.py: This file is used for matching institutions from our Salesforce instance and schools in the United States. This takes in two csvs, one csv for all schools in the United States, and one csv with accounts to be matched. This returns two csvs where one is accounts to be upserted with their respective master accounts, and one where no accounts were found in Salesforce. Adjust paths in this file, and run. Note that you will need the file generated from thefuzzscript.py in order to run this effectively. 
- engineering.py: This file takes in two csvs, one with engineering universities and one with all school accounts. Update paths and run for a csv that has a created field Engineering Universities with a corresponding Boolean value.
- ipscripts.py: Takes csv file with an IP Address field, and returns a csv with Institution concatenated to it. The Institution value contains the associated institution of that IP address. 
- location_information_scraper.py: This is the file that scrapes location information from Google Maps. Takes csv with instnm (institution name) and state (the Billing State) and looks them up in Google Maps. Then, it copies address, website, and phone number. Update paths and run. Run in a fullscreen separate monitor (if you have a multi monitor setup) for best results. 
- normalizewebsite.py: Takes in fields Website and Phone Number. This then returns a csv with phone number in format xxx-xxx-xxxx and website xxx.edu
- ownermap.py: Assign owners based on state.
- rankentries.py: This is the logic for finding the master account based on set up criteria. Used in other files.
- removebeauty.py: This is the file that filters out misc schools that we do not need. Update file paths and run.
- thefuzzscript.py: This is the file you want to run before running doublecsv.py. Takes in raw SF report, and creates match groups based on fuzzy matching critera, and assigns a master account for each match group. Then assigns group ids based on the similarity. Does general cleanup of account names and other things. Replace paths and run this for the csvs that doublecsv.py will need. 

## Workflow After Setup
1. Pull csv1 report of EDU accounts from Salesforce that we'd like to match with verified universities
2. Get csv2 with schools that we want verified information for
3. Run csv2 in removebeauty.py to remove non-strategic institutions for csv2.1
4. Run csv2.1 in location_information_scraper.py to start GMaps information gathering process. This will give us csv2.2
5. Run csv1 in thefuzzscript.py to get csv1.1
6. Run csv1.1 and csv2.2 in doublecsv.py to get two csvs. One csv with matches in our SF and one csv with the remaining institutions that were not found
7. The other files are for other data cleaning efforts
