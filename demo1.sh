#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 [-c <commit message>] [-b <branch name>] [-p <remote URL>]" 1>&2
    exit 1
}

# Parse command-line arguments
while getopts ":c:b:p:" o; do
    case "${o}" in
        c)
            commit_message=${OPTARG}
            ;;
        b)
            branch_name=${OPTARG}
            ;;
        p)
            remote_url=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

# Check for required arguments
if [ -z "${commit_message}" ] || [ -z "${branch_name}" ] || [ -z "${remote_url}" ]; then
    usage
fi

# Initialize and configure the Git repository
git init
git add --all
git status 
git branch
git log
git config user.name "chsatyasaikumar"
git config user.email "satyasaikumar@gmail.com"
git remote add origin ${remote_url}

# Create a new branch and make changes to the repository
git checkout -b ${branch_name}
# echo "Some file content" > file.txt
# git add file.txt

# Commit and push changes to the remote repository
git commit -m "${commit_message}"
git push -u origin ${branch_name}
