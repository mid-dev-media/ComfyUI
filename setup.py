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
for each_folder in config.get('wget', []):
    folder = each_folder.get('folder')
    urls = each_folder.get('urls')
    os.chdir(os.path.join(current_dir, folder))
    for url in urls:
        file_name = url.split('/')[-1]
        # If the file does not exists in current directory
        if not os.path.exists(file_name):
            # Get the file
            subprocess.run(f"wget {url}", shell=True)
        else:
            print(f"{folder} {file_name} already exists")

# Process the "nodes" section
for each_repo in config.get('git', []):
    folder = each_repo.get('folder')
    urls = each_repo.get('urls')
    os.chdir(current_dir)
    for url in urls:
        # Get the file name from the URL
        repo_name = url.split('/')[-1].split('.')[0]
        # If the file does not exists in current directory
        if not os.path.exists(os.path.join(current_dir, folder, repo_name)):
            # Add the remote repository
            subprocess.run(f"git remote add -f {repo_name} {url}", shell=True)
            # Get the file
            subprocess.run(f"git subtree add --prefix {folder}/{repo_name} {url} main", shell=True)
        else:
            print(f"{folder} {repo_name} already exists")
