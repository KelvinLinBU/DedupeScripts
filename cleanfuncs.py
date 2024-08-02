import re
import pandas as pd

def capitalize_account_names(df, column_name):
    df[column_name] = df[column_name].str.title()
    return df

def remove_commas(df, column_name):
    df[column_name] = df[column_name].str.replace(',', '')
    return df

def remove_parentheses_content(df, column_name):
    df[column_name] = df[column_name].str.replace(r'\s*\([^)]*\)', '', regex=True).str.strip()
    return df

# Function to update owner based on billing state/country
def update_owners(df, state_column, country_column, owner_column, other_owner_column, location_dict):
    def get_owner(state, country):
    
        # First, try to match the specific (state, country) pair
        if (state, country) in location_dict:
            return location_dict[(state, country)]
        # If no specific match, try to match the country alone
        elif ('', country) in location_dict:
            return location_dict[('', country)]
        else:
            return None

    # Overwrite the owner columns with the determined owner
    df[owner_column] = df.apply(lambda row: get_owner(row[state_column], row[country_column]), axis=1)
    df[other_owner_column] = df.apply(lambda row: get_owner(row[state_column], row[country_column]), axis=1)
    return df


def normalize_acronyms(df, column_name):
    replacements = {
    r'\bHS\b': 'High School',
    r'\bMS\b': 'Middle School',
    r'\bSD\b': 'School District',
    r'\bElem\b': 'Elementary',
    r'\bSch\b': 'School',
    r'\bUniv\b': 'University',
    r'\bColl\b': 'College',
    r'\bInst\b': 'Institute',
    r'\bAcad\b': 'Academy',
    r'\bJr\b': 'Junior',
    r'\bSr\b': 'Senior',
    r'\bHighschool\b': 'High School',
    r'\bMiddleschool\b': 'Middle School',
    r'\bSci\b': 'Science',
    r'\bTech\b': 'Technology',
    r'\bComm\b': 'Community',
    r'\bVoc\b': 'Vocational',
    r'\bEdu\b': 'Education',
    r'\bIntl\b': 'International',
    r'\bPrep\b': 'Preparatory',
    r'\bPoly\b': 'Polytechnic',
    r'\bSec\b': 'Secondary',
    r'\bPrim\b': 'Primary',
    r'\bNatl\b': 'National',
    r'\bRegl\b': 'Regional',
    r'\bMgmt\b': 'Management',
    r'\bEng\b': 'Engineering',
    r'\bComp\b': 'Computer',
    r'\bMed\b': 'Medical',
    r'\bNurs\b': 'Nursing',
    r'\bPharm\b': 'Pharmacy',
    r'\bDent\b': 'Dental',
    r'\bVet\b': 'Veterinary',
    r'\bArch\b': 'Architecture',
    r'\bCul\b': 'Culinary',
    r'\bHort\b': 'Horticulture',
    r'\bAgri\b': 'Agriculture',
    r'\bBus\b': 'Business',
    r'\bAdmin\b': 'Administration',
    r'\bGovt\b': 'Government',
    r'\bHR\b': 'Human Resources',
    r'\bSoc\b': 'Social',
    r'\bPsych\b': 'Psychology',
    r'\bHist\b': 'History',
    r'\bGeo\b': 'Geography',
    r'\bEcon\b': 'Economics',
    r'\bPhil\b': 'Philosophy',
    r'\bPol\b': 'Political',
    r'\bRel\b': 'Religious',
    r'\bTheo\b': 'Theology',
    r'\bLit\b': 'Literature',
    r'\bLang\b': 'Language',
    r'\bBio\b': 'Biology',
    r'\bChem\b': 'Chemistry',
    r'\bPhys\b': 'Physics',
    r'\bMath\b': 'Mathematics',
    r'\bStat\b': 'Statistics',
    r'\bAcct\b': 'Accounting',
    r'\bFin\b': 'Finance',
    r'\brvths\b': 'Regional Vocational Technical High School'
}
    for abbrev, full_form in replacements.items():
        df[column_name] = df[column_name].str.replace(abbrev, full_form, flags=re.IGNORECASE, regex=True)
    return df

def extract_account_name(domain):
    # Known TLDs and country codes
    known_tlds = {"com", "org", "net", "edu", "gov", "mil", "int"}
    country_codes = {"us", "uk", "ca", "au", "de", "fr", "jp", "cn", "ru", "in"}
    
    # Known subdomains
    subdomains = {"www", "mail", "smtp", "ftp", "student", "admin", "login", "webmail", "secure"}
    
    # Split the domain by dots
    parts = domain.lower().split('.')
    
    # Filter out known TLDs, country codes, and subdomains
    filtered_parts = [part for part in parts if part not in known_tlds and part not in country_codes and part not in subdomains]
    
    # Join the remaining parts
    account_name = ' '.join(filtered_parts)
    
    # Capitalize properly
    account_name = account_name.title()
    
    return account_name

def clean_account_names(df, column_name):
    df[column_name] = df[column_name].apply(extract_account_name)
    return df