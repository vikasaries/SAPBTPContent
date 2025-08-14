import os
import requests
import json
import logging


# Load CPI credentials from environment variables
CPI_HOST = os.getenv("CPI_HOST")
CPI_USER = os.getenv("CPI_USER")
CPI_PASSWORD = os.getenv("CPI_PASSWORD")

# Validate environment variables
if not all([CPI_HOST, CPI_USER, CPI_PASSWORD]):
    raise EnvironmentError("Missing CPI credentials. Please set CPI_HOST, CPI_USER, and CPI_PASSWORD.")
    
# Authentication tuple
AUTH = (CPI_USER, CPI_PASSWORD)

# OAuth token endpoint (SAP BTP example)
token_url = "https://haleon-cpi-dev-7ua1w2tv.authentication.eu20.hana.ondemand.com/oauth/token"

# Request payload
payload = {
    "grant_type": "client_credentials"
}

# Basic Auth header
response = requests.post(token_url, data=payload, auth=AUTH)

if response.status_code == 200:
    access_token = response.json().get("access_token")
    print("Access Token:", access_token)
else:
    print(f"Failed to fetch token: {response.status_code}")
    print(response.text)


# Base URL for CPI API
BASE_URL = f"https://{CPI_HOST}/api/v1"
print(f"Base Url" )
# Authentication tuple
AUTH = (CPI_USER, CPI_PASSWORD)

# Custom headers
headers = {
    "Accept": "application/json",
    "User-Agent": "MyCPIClient/1.0",
    "Authorization": f"Bearer {access_token}"
}


# Output folder
OUTPUT_DIR = "cpi_packages"
os.makedirs(OUTPUT_DIR, exist_ok=True)

       # Download iFlow artifact
        artifact_url = f"{BASE_URL}/IntegrationDesigntimeArtifacts('B060D_C68_SAP_ECC_To_BNP_Bank_-_Replicate_BNP_Bank_Payment_Files_copy')/$value"
        artifact_response = requests.get(artifact_url, headers=headers)
        artifact_response.raise_for_status()
        artifact_file = os.path.join("Bank", f"{iflow_id}.zip")
        with open(artifact_file, "wb") as f:
            f.write(artifact_response.content)

print(f"Fetched and their iFlows into '{OUTPUT_DIR}' folder.")
