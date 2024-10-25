#!/bin/bash
echo "committing with message: $1"

# Run the git commit command with the provided message
git commit -m "$1"
echo "commit complete"