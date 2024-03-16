import os
import json
import subprocess

# Get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the JSON configuration file
config_file = os.path.join(current_dir, 'setup.json')
with open(config_file) as f:
    config = json.load(f)

# Process the "models" section
models = config.get('models', [])
for each_model_type in models:
    folder = each_model_type.get('folder')
    files = each_model_type.get('files')
    os.chdir(os.path.join(current_dir, folder))
    for each_file in files:
        getter = each_file.get('getter')
        url = each_file.get('url')
        # Get the file name from the URL
        file_name = url.split('/')[-1]
        # If the file does not exists in current directory
        if not os.path.exists(file_name):
            # Get the file
            subprocess.run(f"{getter} {url}", shell=True)
        else:
            print(f"File {file_name} already exists")

# Process the "nodes" section
nodes = config.get('nodes', [])
for each_node_type in nodes:
    folder = each_node_type.get('folder')
    files = each_node_type.get('files')
    os.chdir(os.path.join(current_dir, folder))
    print(f"Current directory: {os.getcwd()}")
    for each_file in files:
        getter = each_file.get('getter')
        url = each_file.get('url')
        # Get the file name from the URL
        repo_folder_name = url.split('/')[-1].split('.')[0]
        # If the file does not exists in current directory
        if not os.path.exists(repo_folder_name):
            # Get the file
            subprocess.run(f"{getter} {url}", shell=True)
        else:
            print(f"File {repo_folder_name} already exists")
