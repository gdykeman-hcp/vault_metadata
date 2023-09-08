import requests
import json


token = "<token>"
#examples; url = "https://127.0.0.1:8200/v1/"
url = "<url>"
headers = {"X-Vault-Token": token, "X-Vault-Namespace": "admin", "Content-Type": "application/json"}
mount_path = "auth/userpass-test/"

response = requests.get(url + "identity/entity/id?-format=json&list=true", headers = headers)
entities = response.json()

for i in entities['data']['key_info']:
    if entities['data']['key_info'][i]['aliases'][0]['mount_path'] == mount_path:
        payload = {
            "custom_metadata": {
                "email": entities['data']['key_info'][i]['aliases'][0]['name'] + "@test.lab"
            }
        }
    response = requests.post(url + "identity/entity-alias/id/" + entities['data']['key_info'][i]['aliases'][0]['id'], headers = headers, json=payload)