#!/bin/bash
# Set the commit message to the provided argument
commit_message="$1"

# Run the git commit command with the provided message
git commit -m "$commit_message"
