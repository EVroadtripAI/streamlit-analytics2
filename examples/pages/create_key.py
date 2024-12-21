import os

import toml

# Create streamlit secrets directory and secrets.toml if it doesn't exist
secrets_dir = "./.streamlit"
secrets_file = f"{secrets_dir}/secrets.toml"

if not os.path.exists(secrets_dir):
    os.mkdir(secrets_dir)
    open(secrets_file, "a").close()  # 'a' mode to create the file if it doesn't exist

# Correctly specify the path to the JSON file
json_file_path = "firebase-key.json"  # Correctly specify the JSON filename as a string

# Read the JSON file content
with open(json_file_path) as json_file:
    json_text = json_file.read()

# Prepare the TOML configuration
config = {"firebase_key": json_text}
toml_config = toml.dumps(config)

# Write the TOML configuration to the secrets file
with open(secrets_file, "w") as target:
    target.write(toml_config)
