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

# Fetch all integration packages
packages_url = f"{BASE_URL}/IntegrationPackages?$top=1"

response = requests.get(packages_url, headers=headers)

if response.status_code == 200:
    print("Success!")
else:
    print("StatusVikas",response.status_code)
    print(response.text)
response.raise_for_status()
print("vikas1", response.json());
packages = response.json().get("d", {}).get("results", [])
for package in packages:
    package_id = package["Id"]
    package_dir = os.path.join(OUTPUT_DIR, package_id)
    os.makedirs(package_dir, exist_ok=True)

    # Save package metadata
    with open(os.path.join(package_dir, "metadata.json"), "w") as f:
        json.dump(package, f, indent=2)

    # Fetch iFlows in the package
    iflows_url = f"{BASE_URL}/IntegrationDesigntimeArtifacts?$filter=PackageId eq '{package_id}'"
    iflow_response = requests.get(iflows_url, auth=AUTH)
    iflow_response.raise_for_status()
    iflows = iflow_response.json().get("d", {}).get("results", [])

    for iflow in iflows:
        iflow_id = iflow["Id"]
        iflow_metadata_file = os.path.join(package_dir, f"{iflow_id}_metadata.json")
        with open(iflow_metadata_file, "w") as f:
            json.dump(iflow, f, indent=2)

        # Download iFlow artifact
        artifact_url = f"{BASE_URL}/IntegrationDesigntimeArtifacts('{iflow_id}')/$value"
        artifact_response = requests.get(artifact_url, auth=AUTH)
        artifact_response.raise_for_status()
        artifact_file = os.path.join(package_dir, f"{iflow_id}.zip")
        with open(artifact_file, "wb") as f:
            f.write(artifact_response.content)

print(f"Fetched {len(packages)} packages and their iFlows into '{OUTPUT_DIR}' folder.")
