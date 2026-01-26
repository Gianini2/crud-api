#!/bin/bash

## If not configured:
# git config --global user.name "Seu Nome"
# git config --global user.email "seu-email@example.com"

git init
git add .
git commit -m "Initial commit"
echo "Repository initialized and first commit made."

git remote add origin https://github.com/Gianini2/crud-api
echo "Remote repository added."

git branch -M master
echo "Branch renamed to master."

git fetch origin
echo "Fetched changes from remote repository."

git pull origin master --allow-unrelated-histories
echo "Pulled changes from remote repository (for guarantee)."

git branch --set-upstream-to=origin/master master
echo "Remote repository set and pushed to master branch."

git push -u origin master
echo "Changes pushed to remote repository."

