---
layout: single
sidebar: true
author_profile: true
title: "Most common Github scenarios and Commands"
excerpt: "Github commands at our disposable."
description: "Github commands at our disposable."
comments: true
tags: ["Superintelligence", "LLM", "Machine Learning", "ML System Design"]
published: true
comments: true
header:
  teaserlogo:
  teaser: /images_1/big-feature-branch.jpg
  image: /images_1/big-feature-branch.jpg
  caption: "courtesy: Google"
gallery:

  - image_path: ''
    url: ''
    title: ''
---

Hi All,

Let's have a list of common scenarios we come across and a way we can resolve them. All these resolutions are already available on Stackoverflow or you can prompt your favorite LLM to get the answer. The goal is to have it handy and refer to any such scenario whenever required.

## 1. Committed to the Wrong Branch:
* Scenario: You've made changes and committed them to the wrong branch.
* Resolution:

```bash
git reset HEAD~1 # Undo the commit but keep the changes staged.
OR
git reset --hard HEAD~1  # Undo last commit, discard changes
git switch <correct-branch> # Switch to the correct branch.
git commit -m "Moved to correct branch" # Commit the changes to the correct branch
```

## 2. Accidentally Deleted a Branch:
* Scenario: You've deleted a branch locally that you didn't mean to.
* Resolution:

```bash
git reflog # Look for the commit hash of the deleted branch.
git checkout -b <branch-name> <commit-hash> # Create a new branch at the commit where the deleted branch was.
```

## 3. Lost Uncommitted Changes:
* Scenario: You've lost changes that were not committed due to an accidental reset or checkout.
* Resolution:

```bash
git reflog # Find the commit hash before the loss.
git checkout <commit-hash> -- <file-name> # Recover specific files from that commit.
```

## 4. Find Sensitive Information Mistakenly Committed:
* Scenario: You've committed sensitive information and need to remove it from Git history.
* Resolution:

```bash
git log -S <search-term> -- <file-name> # Search for the commit containing the sensitive information.
git filter-branch --tree-filter "rm -f <file-name>" HEAD # Remove the file from all commits. Note: This is a powerful and potentially destructive command, use with caution.
```

## 5. Merged the Wrong Branch:
* Scenario: You've merged a branch that you didn't intend to.
* Resolution:

```bash
git reset --hard HEAD~1 # Undo the merge commit, losing all changes from the merge.
git reset --merge ORIG_HEAD # Undo the merge but keep changes staged.
```

## 6. Need to Undo a Commit:
* Scenario: You want to undo a commit that has been pushed to the repository.
* Resolution:

```bash
git revert <commit-hash> # Create a new commit that reverts the changes of the specified commit. Safe for public repositories.
```

## 7. Find the Difference Between Two Branches
* Scenario: You want to see what changes are in one branch but not in another.
* Resolution:

```bash
git diff <branch-1>..<branch-2>
```

## 8. Check for Unpushed Commits
* Scenario: You want to see if you have any commits that haven’t been pushed yet.
* Resolution:

```bash
git log --branches --not --remotes
```

## 9. Revert a Merge Commit
* Scenario: You merged a branch but want to undo the merge.
* Resolution:

```bash
# Find the merge commit hash
git log --oneline

# Revert the merge commit
git revert -m 1 <merge-commit-hash>
```

## 10. Check Out a Pull Request Locally
* Scenario: You want to test or review a pull request locally.
* Resolution:

```bash
# Fetch the pull request
git fetch origin pull/<PR-number>/head:<local-branch-name>

# Switch to the new branch
git switch <local-branch-name>
```

## 11. Rename a Branch
* Scenario: You want to rename a branch locally and on the remote.
* Resolution:

```bash
# Rename the branch locally
git branch -m <old-branch-name> <new-branch-name>

# Delete the old branch on the remote
git push origin --delete <old-branch-name>

# Push the new branch to the remote
git push origin <new-branch-name>
```

## 12. Amend the Last Commit
* Scenario: You want to add changes to the last commit or update its message.
* Resolution:

```bash
# Add changes to the last commit
git add <file-name>
git commit --amend

# Update the commit message only
git commit --amend -m "New commit message"
```


Thanks,
Ashish
