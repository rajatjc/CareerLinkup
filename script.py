import os
import sys
from github import Github

# Check if the input file exists
if os.path.isfile("script.txt"):
    # Read the stored inputs from the file
    with open("script.txt", "r") as file:
        inputs = file.readlines()

    # Assign the stored inputs to variables
    REPO_NAME = inputs[0].strip()
    LOCAL_REPO_PATH = os.getcwd()  # Set the current directory as the LOCAL_REPO_PATH
    BRANCH_NAME = inputs[1].strip()
else:
    # Prompt the user for inputs and store them in the file
    REPO_NAME = input("Enter the repository name: ")
    LOCAL_REPO_PATH = os.getcwd()  # Set the current directory as the LOCAL_REPO_PATH
    BRANCH_NAME = input("Enter the branch name: ")

    with open("script.txt", "w") as file:
        file.write(f"{REPO_NAME}\n{BRANCH_NAME}")

# Create or append to the .gitignore file only if it doesn't contain the entries
ignore_entries = ["script.py", "script.txt"]

with open(".gitignore", "r") as file:
    existing_entries = file.read().splitlines()

with open(".gitignore", "a") as file:
    for entry in ignore_entries:
        if entry not in existing_entries:
            file.write(f"\n{entry}")
            
# Rest of the script
# Replace with your GitHub username and personal access token
USERNAME = "rajatjc"
TOKEN = "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"

# Check if the commit message is provided as a command-line argument
if len(sys.argv) > 1:
    commit_message = sys.argv[1]
else:
    print("Please provide a commit message as a command-line argument.")
    sys.exit(1)

# Change the current working directory to the local repository path
os.chdir(LOCAL_REPO_PATH)

# Add all files to the staging area
os.system("git add -A")

# Commit the changes with the provided commit message
os.system(f"git commit -m '{commit_message}'")

# Create a GitHub instance using your credentials
g = Github(USERNAME, TOKEN)

# Get the repository
repo = g.get_user().get_repo(REPO_NAME)

# Push the changes to the remote repository on the specified branch
os.system(f"git push origin {BRANCH_NAME}")

