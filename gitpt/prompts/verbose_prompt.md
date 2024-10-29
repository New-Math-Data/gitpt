Write verbose commit message based on the git diff:
- Read the input and figure out what the major changes and upgrades were that happened.
- The first line should be a short summary of the changes.
- Use bullet points for multiple changes.
- If there are no changes, or the input is blank - then return a blank string.
- Use conventional commits - i.e. prefix the commit title with "chore:" (if it's a minor change like refactoring or linting), "feat:" (if it's a new feature), "fix:" if it's a bug fix.
- Write the output message in a {style} manner.

Think carefully before you write your commit message.

The output format should be:

Summary of changes
- changes
- changes

Input: {git_diff}