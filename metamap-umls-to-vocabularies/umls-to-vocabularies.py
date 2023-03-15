# 1: INTITATE BASE-SETTINGS
# Import module

import pandas as pd
import requests
import json as js
import csv
from pprint import pprint
import openpyxl

pd.set_option('display.max_columns',
              None)  # expands output view to display more columns

print('\033[1;4m' + 'UMLS TO VOCABULARY\n' + '\033[0m')

# 2: PREPROCESSING: WE PREP OUR FILE FOR OUR API DATA
# Read our Excel input file
xlsx = pd.ExcelFile('Table_1.xlsx')
table_1 = pd.read_excel(xlsx, 'Table_1')

# Send the table to a CSV UTF-8 file
table_1.to_csv('Table_1.csv', encoding='utf-8', index=False)

# Print vocabularies for validation (True/False/(NaN--(if row doesn't exist))
vocabulary = (table_1["Vocabularies"])

# Define function for user selecting UMLS vocabulary of choice 1) LNC, 2)MTH, 3) NCI, 4) SNOMEDCT_US


def user_selects(options):
    print("Choose from the following vocabulary:")
    print("")

    # Display the options as a numbered list
    for index, element in enumerate(options):
        print("{}) {}".format(index + 1, element))

    # If no option is selected from the available list i.e (1, 2, 3, 4), provide
    # user with error dialog
    print("")
    i = input("Please type your response: ")
    if i.lower() not in ('1', '2', '3', '4'):
        print("")
        print("UNABLE TO EXECUTE: RESPONSE MUST BE A NUMBER FROM THE LIST!")
        print("Please restart the program...")
        print(" ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) - 1
    except:
        pass


# Option for vocabulary initiated
options = ['LNC', 'MTH', 'NCI', 'SNOMEDCT_US']

# Store user's choice
user_res = user_selects(options)

while True:
    try:
        print(options[user_res])
        break
    except TypeError:
        pass

# Initiate variable for user choice
user_choice = options[user_res]

# Validation check for vocabulary of choice
validation = (table_1["Vocabularies"].str.contains(user_choice))

# Concert validation to a list, so that we can insert it into a new col for the
# validation file
validation_list = validation.values.tolist()

# Create a new table from Table_1 so as not to overwrite the original data file
table_1v = table_1.copy()

# Add a new col called validation, wherein the True, False, and NaN values are
# added to let us know which rows have vocabulary of choice as a means for
# validation
table_1v.insert(
    4, column="Validation", value=" "
)  # the new column is left empty so we can add our values from the
# validation_list

# Add validation_list to our newly created validation table
table_1v["Validation"] = validation_list

# Clean up leading spaces
table_1v = table_1v.replace(r"^ +| +$", r"", regex=True)

# Before exporting to a new CSV, clean up empty rows in the current CSV file
# --in this case we will drop rows with ALL empty cells (where we saw the NaNs
# earlier); retains rows that do NOT include na (NaN)
table_1v = table_1v[table_1v['Validation'].notna()]

# Export the validation table to a new CSV file
table_1v.to_csv('Table_1v.csv',
                index=False)  # Index=False to export without index

# Create a copy of Table_1v so as not to overwrite the original file
table_2v = table_1v.copy()

# The next step involves only pulling out concepts that are not flagged (False)
# for the choice of vocabulary in the "Validation" col
# --the same code as when we cleaned up nas above can be utilized (Table_2)
table_2v = table_2v[table_2v['Validation'] == True]

# Export the table choice of vocabulary to a new CSV file
table_2v.to_csv(
    'Table_2v.csv', index=False
)  # index = False to export without index--retain this for validation purposes

# Now that we have confirmed our list only includes our choice of vocabulary,
# we can drop the validation column from Table_2v
del table_2v['Validation']

# Create a copy of Table_2v so as not to overwrite the new validation data file
table_2 = table_2v.copy()
table_2.to_csv('Table_2.csv', index=False)
# Insert new headers to a copy of Table 2 --we will use these when we join our
# API data to Table 2 in laters steps
table_3 = table_2.copy()
table_3.insert(4, column=user_choice + " Concept Name",
               value="")
table_3.insert(5, column=user_choice + " Concept Code",
               value="")

table_3.to_csv('Table_3.csv', index=False)

# 3. DATA-PROCESSING: WE INITIALIZE API SETTINGS & QUERY FOR OUR DATA
# Create a list from the CUIs in Table_2 (column 2)
cuis = table_2['UMLS Concept CUI'].tolist()

# Inititate your API --user adds API here
myAPI = 'd0d565b2-a736-4de5-b9df-45d6b06d05c6'

# Initiate rest API url
base_url = 'https://uts-ws.nlm.nih.gov/rest/content/current/CUI/{}/atoms?language=ENG&apiKey=' + myAPI

# Initiate the list variable as mydata
my_data = cuis

# Create lists to store ALL results for atoms
results = dict()

# For loop to call rest API
for i in my_data:  # For every CUI in the list we will get a response request
    r = requests.get(base_url.format(i))  # Initiate variable for our request
    # If statement for api request success/fail
    if r.status_code != 200:  # 200==request succeeded
        print("Request to {} failed".format(i))
    else:
        data = js.loads(r.text)  # Load data as json
        results.update({i: data})  # Update our dict

# Write list to .txt file
with open('data.txt', 'w') as data_file:
    pprint(
        results,
        stream=data_file)  # Pretty print results into the text file we created

# Create a json file
with open("res_data_json.json", "w") as json_file:
    js.dump(results, json_file)

my_list = []  # Store our final file into a list

# For loop to filter through our json data results
for r in results:
    nestedResult = results[r][
        'result']  # We iterate through each item in our results
    for rr in nestedResult:  # We iterate through each item in our nested results
        if rr['rootSource'] == user_choice:  # Filter for choice of vocabulary
            # in 'rootSource'
            # Initiate variables below for our individual data
            concept = rr['concept']
            conceptSplit = concept.rsplit('/', 1)[-1]
            name = rr['name']
            rootSource = rr['rootSource']
            sourceConcept = rr['sourceConcept']
            sourceConceptSplit = sourceConcept.rsplit('/',
                                                      1)[-1]
            arr = [conceptSplit, name, rootSource, sourceConceptSplit
                   ]  # Create a list for our variables initated above
            my_list.append(arr)  # Append to our intiated variable

# 4: POSTPROCESSING:
# We restructure our files here so that we can match them to the data that was
# retrieved from our query based on our vocabulary of choice. We want to end up
# with an output file that is able to map the UMLS Concept CUI to the
# vocabulary of choice by being able to filter for the correctly corresponding
# name and code, this is possible due to the pre-processing steps we took to use
# our vocabulary col as a filter. Therefore, we are able to join the tables
# based on matching CUIs between our original files and the API data file to
# get the desired results

# We create a new file and write our headers to the file
field_names = [
    'UMLS Concept CUI', user_choice + ' Concept Name', 'rootSource',
    user_choice + ' Concept Code'
]  # New header
with open('My_List.csv', 'w') as res_final:  # Create new CSV file for writing
    write = csv.writer(res_final)  # Initiate CSV writer to our new file
    write.writerow(field_names)  # Write our field names above
    write.writerows(my_list)  # Write all rows to the csv file

# Convert our list to a dataframe and left join
temp_table_1 = pd.DataFrame(my_list, columns=[field_names])

# The newly created table will convert to a CSV file
temp_table_1.to_csv('Temp_Table_1.csv',
                    index=False)  # index = False to export without index

temp_table_2 = pd.read_csv(
    'Temp_Table_1.csv'
)  # Clean table without the 'rootSource' --we don't need this anymore
del temp_table_2['rootSource']

temp_table_2.to_csv('Temp_Table_2.csv',
                    index=False)  # Move clean table to a CSV file

# Left join on table 3
temp_table_3 = pd.merge(table_3,
                        temp_table_2,
                        on='UMLS Concept CUI',
                        how='left')

temp_table_3.to_csv(
    'Temp_Table_3.csv',  # Move merged table to a CSV file
    index=False)

temp_table_3.pop(user_choice + ' Concept Name_x')  # Remove col
temp_table_3.pop(user_choice + ' Concept Code_x')  # Remove col
temp_table_4a = temp_table_3.rename(
    {user_choice + ' Concept Name_y': user_choice + ' Concept Name'},
    axis=1)  # Rename newly created columns from left join
temp_table_4b = temp_table_4a.rename(
    {user_choice + ' Concept Code_y': user_choice + ' Concept Code'},
    axis=1)  # Rename newly created columns from left join

temp_table_4b.to_csv('Temp_Table_4.csv', index=False)

temp_table_4b = pd.read_csv('Temp_Table_4.csv').drop_duplicates(
    subset=['CDE Name', 'UMLS Concept Name',
            'UMLS Concept CUI', 'Vocabularies'],
    keep='first').reset_index(
    drop=True)  # Read our final table while dropping our duplicates

# EOF (End of File) marker
temp_table_4b.to_csv('Final_Table.csv',
                     index=False)  # Index = False to export without index
print(" ")
print("Execution Results: Successful")
