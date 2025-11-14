# Sub-issue → Branch → PR Workflow

This document describes how we work on sub-issues in the *workflow-test-app* repo, in a way that matches our GitHub Project automation rules and our desired issue/PR status transitions.

Before starting, Cascade proposes **which sub-issue should be worked on next** (based on open issues and the project board). You then confirm or override that choice.

We follow this exact order:

1. Create sub-issue → Issue `Ready`, no PR  
2. Create branch and record `documents/local/current-sub-issue.md`, then push branch → Issue `Ready`, no PR  
3. Create PR with `Fixes #<issue>` and assign reviewer `kareemdrive001-dev` → Issue `In progress`, PR `Ready`  
4. Do the work on the PR branch → Issue `In progress`, PR `Ready`  
5. Approve the PR via `gh pr review --approve` → Issue `In review`, PR `In review`  
6. Test / verify result → Issue `In review`, PR `In review`  
7. Merge PR → Issue `Done`, PR `Done`

Once you explicitly allow it for a given sub-issue (for example: *"Start Sub X.Y, run steps 1–5 automatically"*), Cascade may execute **Steps 1–5 in a single sequence** using your local Git and GitHub CLI and the GitHub MCP GitHub API, while you retain approval gates at testing (Step 6) and merge (Step 7).

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
  - Create or update `documents/local/current-sub-issue.md` with:
    - the sub-issue number and title
    - the branch name
    - the current workflow step (for example: `2 – Branch created`)
  - Commit this change as a small, non-functional diff.
  - Push the new branch to GitHub (so it exists remotely before creating the PR).

- **Resulting Status**
  - **Issue:** `Ready`  
  - **PR:** _none yet_

---

## 3. Create a pull request linked to the sub-issue

- **Action**
  - Open a PR from this branch into `main` **using the GitHub MCP GitHub API as the `k3aworks` account** (not via the local `gh` CLI).
  - In the PR description, include a closing keyword linking the sub-issue, for example:

    ```text
    Fixes #<sub-issue-number>
    ```
  - Assign reviewer `kareemdrive001-dev`.
  - Ensure the PR is on the `workflow-test-kanban` project (either via automation or by adding it manually).

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

## 5. Approve the PR (moves issue and PR to In review)

- **Action**
  - After Step 4 is complete and you are ready to move the PR into review, Cascade approves the PR using the GitHub CLI, which is authenticated as `kareemdrive001-dev`:

    ```bash
    gh pr review --approve <pr-number>
    ```

  - This may happen as part of the **automatic Steps 1–5 sequence** (after you give a single approval for that sub-issue, such as *"run steps 1–5 automatically"*), or as a dedicated step when you say something like *"do step 5"*.

- **Resulting Status** (from automation rules and custom workflow)
  - **Issue:** `In review`  
    - New workflow `issue-to-in-review-on-pr-approval.yml` sets the linked issue's `Status = In review` on the `workflow-test-kanban` project whenever a PR review is approved.  
  - **PR:** `In review`  
    - Rule: "Code review approved" → Status = In review (for the PR).

Now the work is done and the PR has been explicitly approved. Next we validate the result.

---

## 6. Test and verify the result

- **Action**
  - Run automated tests and/or manual checks to confirm behavior.  
  - Double-check the diff and ensure the PR is ready to integrate.

- **Resulting Status**
  - **Issue:** `In review`  
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
5. **PR moves to In review (approval)** → Issue `In review`, PR `In review`.  
6. **Result tested / verified** → Issue `In review`, PR `In review`.  
7. **PR merged** → Issue `Done`, PR `Done`.
