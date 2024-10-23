#!/bin/bash
diff_output=$(git diff HEAD)
#new_files=$(git status | awk '/new file:/ {print $NF}')
#renamed_files=$(git status | awk '/renamed:/ {print $2, $3, $4}')
#git restore --staged .

echo "$diff_output"
#echo ""
#echo "$new_files"
#echo ""
#echo "$renamed_files"
