#!/bin/bash
diff_output=$(git diff --staged)
echo "$diff_output"