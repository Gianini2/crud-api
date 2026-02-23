#!/usr/bin/env bash
set -e

GITHUB_USER=$1
REPO_NAME=$2
BRANCH=${3:-master}   # default = master

if [ -z "$GITHUB_USER" ] || [ -z "$REPO_NAME" ]; then
  echo "Usage: $0 <github-username> <repo-name> [branch]"
  exit 1
fi

git init
git add .
git commit -m "Initial commit"
echo ">> Repository initialized and first commit made."

git remote add origin "https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
echo ">> Remote repository added."

git branch -M "$BRANCH"
echo ">> Branch renamed to $BRANCH."

git fetch origin
echo ">> Fetched changes from remote repository."

git pull origin "$BRANCH" --allow-unrelated-histories
echo ">> Pulled changes from remote repository."

git branch --set-upstream-to="origin/$BRANCH" "$BRANCH"
git push -u origin "$BRANCH"

echo ">> Changes pushed to remote repository."
