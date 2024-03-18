import os
import json
import subprocess
import pprint
# Get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the JSON configuration file
config_file = os.path.join(current_dir, 'setup.json')
with open(config_file) as f:
    config = json.load(f)

update_config = []
# Process the "models" section
for each_folder in config.get('wget', []):
    folder = each_folder.get('folder')
    urls = each_folder.get('urls')
    os.chdir(os.path.join(current_dir, folder))
    for url in urls:
        if isinstance(url, str):
            # Check for and handle civitai links that dont have filenames
            if 'civitai' in url:
                files_before = os.listdir(os.getcwd())
                subprocess.run(f"wget {url} --content-disposition", shell=True)
                files_after = os.listdir(os.getcwd())
                new_files = list(set(files_after) - set(files_before))
                print(new_files)
                if len(new_files) == 1:
                    file_name = new_files[0]
                    update_config.append({'org': url, 'new':{'file_name': file_name, 'link': url}})
                else:
                    print(f"Error: Multiple files downloaded for {url}")
            else:
                file_name = url.split('/')[-1]
                if not os.path.exists(file_name):
                    subprocess.run(f"wget {url}", shell=True)
                else:
                    print(f"{folder} {file_name} already exists")

        elif isinstance(url, dict):
            file_name = url.get('file_name')
            url = url.get('link')
            if not os.path.exists(file_name):
               subprocess.run(f"wget {url} --content-disposition", shell=True)
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

if update_config:
    update = config.copy()
    for each_folder in update.get('wget', []):
        folder = each_folder.get('folder')
        urls = each_folder.get('urls')
        for i, each_urls in enumerate(urls):
            for update_item in update_config:
                if each_urls == update_item['org']:
                    urls[i] = update_item['new']

    with open(config_file, 'w') as f:
        json.dump(update, f, indent=4)
