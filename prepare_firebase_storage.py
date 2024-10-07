import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read the private_key from the environment variable
private_key_part_1 = os.getenv("FIREBASE_PRIVATE_KEY_1")
private_key_part_2 = os.getenv("FIREBASE_PRIVATE_KEY_2")
private_key_part_3 = os.getenv("FIREBASE_PRIVATE_KEY_3")
private_key_part_4 = os.getenv("FIREBASE_PRIVATE_KEY_4")
private_key_part_5 = os.getenv("FIREBASE_PRIVATE_KEY_5")

private_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

private_key = f"-----BEGIN PRIVATE KEY-----\n{private_key_part_1}\n{private_key_part_2}\npH0OxJzsZ9Ic6wZy8lbzdEE+8H0H+69MWeC3UczINB2PLjsFVeyObQqqxPoBRw4c\n1JXTqBNfUsG7KJv8ojdP35ZD2gcBPF5M7B3e1ktR3si5ciUXt0JmvQHh7/9+God2\n{private_key_part_3}\nv5WTeqgV1rQLlKbtiq5FgrVfvaFg/HxtrUNPUzUME+G4Am/76rM1L0pPBLbIEmCk\nsVSileRpAgMBAAECggEABwQq1SLLOEUo+WusrNkZenluefyyRCo9YAmfQFrl5tQX\n7Bjin+2SPZXtND2lu0tsdo/8psOe/Po+/Widreh/ff57uslLH82XcA30MVjjQgu6\nvEgwxdKYqJiX7FICPolg+Y93LD1hW0Ngl3A/VAdB4Mcy/Y/PG5eM8FQtDtqJPHSH\n{private_key_part_5}\n33bnlm7oxlL8HGIeU6Rc/xYYjxRauXtd2BTNESdzfdlgKhVotK/08kFcn/1PF793\nD1LOMD0EkxO9Jk9eUxX3qiOAYTA3JzG84+MduN8duQKBgQDeL3PsK9MjZM7xzn3Z\n{private_key_part_4}\nZ/MkVfwCVMCyWhkPrIashws0kxjeQy3/Xw4ZGkR/b0sssp8vGIgWIAi6PxxFQPi1\n70zlp98h4g9DtfVDiEsDh8Aj/QKBgQDVN2b/ZHi3MWghIfpIK8GmDXd3+94iKLKC\n6ydaccJbLS8WehDRB1iYi4TPzuSO8QcOK64oOkkwYL01RME6qGfOuLImSF4zTZJc\nfZ9sERHSIBvYEhua9d9nfWQRS3n8PS9+MDC2zfIEhKVOIGjFSKH75v8XroHaxlU4\nJGIq2XcP3QKBgE0y6bFOjN8IYMsttxZ6SDg3vfjFGinOD1XJ1yXut1xi6FHPagq1\nTAZ2zIw4ArUHDP0tt5nWLVb2q+xfue7rI1UltxlMP2P44CpNBMIfbepHjeV0LCBF\n880PDmvEzLbsHVksyeP+H2ovEXCSoZf9XJeTG3lXZXxeVaiwS3gfi8g1AoGBALjT\n1PIxOz+6kYSfOqHTZIO4isa0zEOaOdypUiziDlQRYA9A81Dv6EocL54gwBp1L+OF\n0+vFUuqgAYSqvEJH9+zISI5ND3Ozm9uXfloklekrsldkow96chX5KYSgg/c3ZvMh\nfSkKb/Cgt9d42rmiE+EUxi7WNHTclsUbLQnuB3r1AoGActa4rtxbbUXJC6+4GGUS\nW+BJzd0K07XUJjTqsID0YiMwBEkkGhXsByTbFISlj05zeU5+3eJa+nPTa/tV0HPu\nPb7Afevx19aWBMr0xMkuXUnoHTL5pFJNlvkNL7FCb6S/vJ2nU17MGov2UAffpSF7\nazOewbw6Y1vDV0IDRUcHPtA=\n-----END PRIVATE KEY-----\n"


def prepare_firebase_storage():
    if private_key is None:
        raise ValueError("PRIVATE_KEY not set in .env file")

    # Create the JSON data
    json_data = {
        "type": "service_account",
        "project_id": "estate-390b4",
        "private_key_id": "391ec9b01d7edf2228274a1dbb5c9126c1c503e7",
        "private_key": private_key,
        "client_email": "firebase-adminsdk-vdn1h@estate-390b4.iam.gserviceaccount.com",
        "client_id": "108941979756550798633",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-vdn1h%40estate-390b4.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    # Write JSON data to a file
    with open(private_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

    print("JSON file created successfully.")
    
    # Load the JSON data from the file
    with open(private_path, "r") as json_file:
        data = json.load(json_file)

    # Print the loaded JSON data
    print("Loaded JSON data:")
    print(json.dumps(data, indent=4))