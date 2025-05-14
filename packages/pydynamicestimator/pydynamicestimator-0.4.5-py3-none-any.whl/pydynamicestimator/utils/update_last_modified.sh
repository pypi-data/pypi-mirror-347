#!/bin/bash

staged_files=$(git diff --cached --name-only --diff-filter=M)
for file in $staged_files; do
    if [[ "$file" =~ \.py$|\.txt$ ]]; then
        DATE=$(date '+%Y-%m-%d')  # Only date, without time
        # Update the second line to reflect the new Last Modified date
        sed -i "2s|# Last Modified:.*|# Last Modified: $DATE|" "$file"
        echo "Updated: $file"
        # Stage the file again after modifying it to ensure it's included in the commit
        #git add "$file"
    fi
done
