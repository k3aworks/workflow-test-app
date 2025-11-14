# Sub-issue → Branch → PR Workflow

This document describes how we work on sub-issues in the *workflow-test-app* repo, in a way that matches our GitHub Project automation rules and our desired issue/PR status transitions.

ALWAYS DO THE STEPS IN ORDER AND CREATE A TASK FOR EACH STEP

**Approval rule**
- After each numbered step (1-7), wait for the maintainer to explicitly approve that step before starting the next one.
- When using the Cascade assistant, it must ask for approval before executing each step and must not move to the next step without clear confirmation.

We follow this exact order:

1. Create sub-issue → Issue `Ready`, no PR  
2. Create branch → Issue `Ready`, no PR  
3. Create PR with `Fixes #<issue>` and assign `kareemdrive001-dev` as reviewer → Issue `In progress`, PR `Ready`  
4. Do the work on the PR branch → Issue `In progress`, PR `Ready`  
5. Approve PR (review by `kareemdrive001-dev`) → Issue `In progress`, PR `In review`  
6. Test / verify result → Issue `In progress`, PR `In review`  
7. Merge PR → Issue `Done`, PR `Done`

---

## 1. Create the sub-issue

- **Action**
  - Create a sub-issue under the correct main issue using the `Main / Sub` naming convention.
  - Ensure the sub-issue is added to the `workflow-test-kanban` project.

- **Resulting Status**
  - **Issue:** `Ready`  
  - **PR:** _none yet_

---

## 2. Create a branch for the sub-issue

- **Action**
  - From `main`, create and switch to a branch named from the sub-issue. **Always use a command that both creates and switches the branch.**

  - Typical local flow (new branch not yet on GitHub):

    ```bash
    git checkout main
    git checkout -b sub-1-2-add-gui-layout
    ```

  - If the branch was already created on GitHub (e.g. via an API or MCP tool), first fetch and then create the local tracking branch:

    ```bash
    git fetch origin
    git checkout -b sub-1-2-add-gui-layout origin/sub-1-2-add-gui-layout
    ```

  - Example naming pattern:
    - Issue: `Sub 1.1 - Setup initial project structure`  
    - Branch: `sub-1-1-setup-initial-project-structure`

- **Resulting Status**
  - **Issue:** `Ready`  
  - **PR:** _none yet_

---

## 3. Create a pull request linked to the sub-issue

- **Action**
  - Push the branch to GitHub.  
  - Open a PR from this branch into `main`.
  - In the PR description, include a closing keyword linking the sub-issue, for example:
  - Assign `kareemdrive001-dev` as the reviewer on the PR. This is because `kareemdrive001-dev` is the designated reviewer for this project, and their approval is required before proceeding.

    ```text
    Fixes #<sub-issue-number>
    ```

Using `kareemdrive001-dev` as the standard reviewer makes it easy to complete Step 5 with `gh pr review` and ensures the "Code review approved" project rule fires consistently.

- **Resulting Status** (from automation rules)
  - **Issue:** `In progress`  
    - Rule: "Pull request linked to issue" → Status = In progress (for the issue).  
  - **PR:** `Ready`  
    - Rule: "Item added to project" → Status = Ready (for the PR).

At this point the issue is officially **In progress** and we do the bulk of the implementation work on the PR branch.

---

## 4. Do the work on the PR branch

- **Action**
  - Implement all code changes needed to complete the sub-issue on this branch.  
  - Make focused commits related only to this sub-issue.

- **Resulting Status**
  - **Issue:** `In progress` (unchanged)  
  - **PR:** `Ready` (still awaiting review)

---

## 5. Approve the pull request

- **Action**
  - As `kareemdrive001-dev`, approve the PR using GitHub CLI, for example:

    ```bash
    gh pr review <pr-number> --approve
    ```

  - Alternatively, approve the PR from the GitHub web UI as `kareemdrive001-dev`.
  - **Only `kareemdrive001-dev` (or another explicitly designated reviewer) should perform this approval step.**
  - If Cascade is assisting, it must ask the maintainer for approval before Step 5. After the maintainer confirms, Cascade runs the `gh pr review` command on their behalf as `kareemdrive001-dev`.

- **Resulting Status** (from automation rules)
  - **Issue:** `In progress`  
    - Approval does **not** change the issue status.  
  - **PR:** `In review`  
    - Rule: "Code review approved" → Status = In review (for the PR).

Now the work is done and the PR has been approved. Next we validate the result.

---

## 6. Test and verify the result

- **Action**
  - Run automated tests and/or manual checks to confirm behavior.  
  - Double-check the diff and ensure the PR is ready to integrate.

- **Resulting Status**
  - **Issue:** `In progress`  
  - **PR:** `In review`  

Testing and verification do not change status by themselves; they are part of our manual process before merge.

---

## 7. Merge the pull request

- **Action**
  - Merge the PR into `main` (with `Fixes #<sub-issue-number>` still present in the description).

- **Resulting Status** (from GitHub + automation rules)
  - **Issue:** `Done`  
    - GitHub automatically closes the issue because of `Fixes #<issue>`.  
    - Rule: "Item closed" → Status = Done (for the issue).  
  - **PR:** `Done`  
    - Rule: "Pull request merged" → Status = Done (for the PR).

No extra manual "close issue" step is required as long as the PR description includes `Fixes #<sub-issue-number>`.

---

## Summary of key checkpoints

1. **Sub-issue created** and added to project → Issue `Ready`, no PR.  
2. **Branch created** for that sub-issue → Issue `Ready`, no PR.  
3. **PR created** with `Fixes #<issue>` and `kareemdrive001-dev` assigned as reviewer → Issue `In progress`, PR `Ready`.  
4. **Work done** on the PR branch → Issue `In progress`, PR `Ready`.  
5. **PR approved by `kareemdrive001-dev`** → Issue `In progress`, PR `In review`.  
6. **Result tested / verified** → Issue `In progress`, PR `In review`.  
7. **PR merged** → Issue `Done`, PR `Done`.

**Note:** Each step requires explicit approval from the maintainer before proceeding.
