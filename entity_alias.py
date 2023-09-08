#!/usr/bin/python3

import requests
import json

"""
    VARIABLES
"""
debug       = False
token       = ""
url         = "http://127.0.0.1/v1/"
mount_path  = "auth/ldap3/"

# Retreive entities list from Vault
try:
    headers     = {"X-Vault-Token": token, "X-Vault-Namespace": "admin", "Content-Type": "application/json"}
    response    = requests.get(url + "identity/entity/id?-format=json&list=true", headers = headers)
    entities    = response.json()
    print(f'Entities are {entities}') if debug else False

except Exception as e:
    print(f'Exception retrieving data: {e}')
    exit

"""
    Loop through Vault entities for auth via LDAP 
    Populate metadata to pass to CaC application
"""
for i in entities['data']['key_info']:
    print(f'Entity: {i} has data {entities["data"]["key_info"][i]}') if debug else False
    
    # Not every entity has an alias, so check first
    if 'aliases' in entities['data']['key_info'][i].keys():
        print(f'Has an alias!') if debug else False

        # mount_path is the auth method
        if entities['data']['key_info'][i]['aliases'][0]['mount_path'] == mount_path:
            print(f"\nAlias Name {entities['data']['key_info'][i]['aliases'][0]['name']} has auth method {mount_path}")

            # Create custom metadata entries for Vault entity aliases
            payload = {
                "custom_metadata": { 
                    "email": entities['data']['key_info'][i]['aliases'][0]['name'] + "@test.lab" ,
                    "first_name": entities['data']['key_info'][i]['aliases'][0]['name'] ,
                    "last_name": entities['data']['key_info'][i]['aliases'][0]['name'] ,
                    }
            }
            # Post the update to Vault
            response = requests.post(url + "identity/entity-alias/id/" + entities['data']['key_info'][i]['aliases'][0]['id'], headers = headers, json=payload)
            print(f'Update response: {response}')
    else:
        print(f'No alias for {i}') if debug else False
                                     
