import pandas as pd
import json, requests
import base64

FILE_LOCATION = "/path/to/folder/" # Location of the file on the shared file store
FILE_NAME = "CRM_Team_-_Technical_Assessment_-_Advanced.docx-EmbeddedFile.xlsx"
SHEET_NAME = "Localisation"
OUTPUT_FILE_NAME = "localisation_exported.csv"

# get the localisation file and transform it into csv
data_xls = pd.read_excel(FILE_LOCATION+FILE_NAME, SHEET_NAME, index_col=None)
data_xls.to_csv(OUTPUT_FILE_NAME, encoding='utf-8', index=False)

# upload to marketing cloud
BEARER_TOKEN = "SAMPLE_TOKEN"
ASSET_ID = "1" # Assuming that there is already a file there and we need to update that asset
URL = f"https://YOUR_SUBDOMAIN.rest.marketingcloudapis.com/asset/v1/content/assets/{ASSET_ID}"

headers = {
    "Authorization":f"Bearer {BEARER_TOKEN}"
}
MC_FILE_NAME = "localisation"
# we must encode the csv file as base64 as per
# https://developer.salesforce.com/docs/atlas.en-us.noversion.mc-apis.meta/mc-apis/file_upload.htm
file_open = open(OUTPUT_FILE_NAME, 'rb').read()
base64_encoded = base64.b64encode(file_open).decode('UTF-8')

data = f"""
{{
    "name":{MC_FILE_NAME},
    "assetType":{{"id":118,"name":"csv"}},
    "file":{base64_encoded}
}}
"""
# a json object must be passed instead of a dictionary
res = requests.put(URL, headers=headers, data = json.dumps(data))
print(res.text)