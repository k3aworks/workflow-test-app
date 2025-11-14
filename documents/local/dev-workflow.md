# Sub-issue → Branch → PR Workflow

This document describes how we work on sub-issues in the *workflow-test-app* repo, in a way that matches our GitHub Project automation rules and our desired issue/PR status transitions.

We follow this exact order:

1. Create sub-issue → Issue `Ready`, no PR  
2. Create branch → Issue `Ready`, no PR  
3. Create PR with `Fixes #<issue>` → Issue `In progress`, PR `Ready`  
4. Do the work on the PR branch → Issue `In progress`, PR `Ready`  
5. PR moves to `In review` (auto-approval by CI) → Issue `In progress`, PR `In review`  
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
  - From `main`, create and switch to a branch named from the sub-issue, for example:
    - Issue: `Sub 1.1 - Setup initial project structure`  
    - Branch: `sub-1-1-setup-initial-project-structure`

- **Resulting Status**
  - **Issue:** `Ready`  
  - **PR:** _none yet_

---

## 3. Create a pull request linked to the sub-issue

- **Action**
  - Push the branch to GitHub.  
  - Update `documents/local/current-sub-issue.md` with the current sub-issue information (issue number, title, branch name, and current workflow step). This provides a minimal, non-functional change for the branch and documents what we are working on.
  - Open a PR from this branch into `main`.
  - In the PR description, include a closing keyword linking the sub-issue, for example:

    ```text
    Fixes #<sub-issue-number>
    ```

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

## 5. PR moves to In review (auto-approval by CI)

- **Action**
  - A GitHub Actions workflow (`.github/workflows/pr-auto-review.yml`) automatically approves qualifying PRs (non-draft `sub-*` branches into `main`), which counts as a code review approval.
  - You may still perform a manual review/approval if desired, but it is no longer required for the status transition.

- **Resulting Status** (from automation rules)
  - **Issue:** `In progress`  
    - Approval does **not** change the issue status.  
  - **PR:** `In review`  
    - Rule: "Code review approved" → Status = In review (for the PR).

Now the work is done and the PR has effectively been approved (by CI or manually). Next we validate the result.

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
3. **PR created** with `Fixes #<issue>` → Issue `In progress`, PR `Ready`.  
4. **Work done** on the PR branch → Issue `In progress`, PR `Ready`.  
5. **PR moves to In review (auto-approval by CI)** → Issue `In progress`, PR `In review`.  
6. **Result tested / verified** → Issue `In progress`, PR `In review`.  
7. **PR merged** → Issue `Done`, PR `Done`.
