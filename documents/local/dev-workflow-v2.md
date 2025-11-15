# Sub-issue → Branch → PR Workflow (v2)

This document defines a **tight, predictable workflow** for working on sub-issues in the *workflow-test-app* repo.

It is designed to:

- Keep GitHub Project statuses (`Ready`, `In progress`, `In review`, `Done`) in sync with reality.
- Avoid branching from stale `main`.
- Avoid merging `main` back into feature branches.
- Minimize merge conflicts in `documents/local/current-sub-issue.md`.

Cascade may automate parts of this workflow, but the steps and rules apply regardless of who runs the commands.

---

## Global rules

These apply to **every** sub-issue:

1. **One sub-issue at a time per repo**  
   Do not work on Sub 2.3 and 2.4 in parallel in this repository. Finish and merge one sub-issue before starting the next.

2. **Always branch from up-to-date `main`**  
   Before creating any new sub-issue branch:

   ```bash
   git switch main
   git pull
   ```

3. **Never merge `main` into a sub-issue branch**  
   The lifetime of a sub-issue branch is:

   ```text
   main (up to date) → sub-X-Y-... → PR → merge back into main
   ```

   If `main` moves forward while the branch is open, **do not** merge `main` into the branch. Instead, finish and merge the branch as soon as it is ready.

4. **`documents/local/current-sub-issue.md` is branch-local helper**  
   This file is only a small, non-functional diff and a local reminder of the current sub-issue. Its content is considered "correct" for the **current branch**, not as a global truth. It is expected to change from branch to branch.

---

## Status mapping

We use the following statuses on the project board:

- **Issue statuses**: `Ready`, `In progress`, `In review`, `Done`  
- **PR statuses**: `Ready`, `In review`, `Done`

Automation rules (summarized):

- **PR linked to issue** → Issue `In progress`.
- **Approved review on PR** (by `kareemdrive001-dev`) → Issue `In review`, PR `In review`.
- **Review requesting changes on PR** → PR `Ready`.
- **Issue or PR closed/merged** → Status `Done`.

---

## Step 1 – Pick the next sub-issue

- Choose the next `Sub N.M` under an active main issue where all prior sub-issues for that main are `Done`.

**Resulting status**

- Issue: `Ready`
- PR: *(none yet)*

---

## Step 2 – Create a branch for the sub-issue

1. Ensure `main` is up to date:

   ```bash
   git switch main
   git pull
   ```

2. Create and switch to the sub-issue branch. Example for Sub 2.4:

   ```bash
   git switch -c sub-2-4-update-ui-to-show-selected-person-info
   ```

3. Update `documents/local/current-sub-issue.md`:

   ```markdown
   # Current Sub-issue

   - Issue: #29
   - Title: Sub 2.4 - Update UI to show selected person info
   - Branch: sub-2-4-update-ui-to-show-selected-person-info
   - Workflow step: 2 – Branch created
   ```

4. Commit and push this small, non-functional diff:

   ```bash
   git add documents/local/current-sub-issue.md
   git commit -m "Record current sub-issue 2.4 branch creation"
   git push -u origin sub-2-4-update-ui-to-show-selected-person-info
   ```

**Resulting status**

- Issue: `Ready`
- PR: *(none yet)*

> **Rule reminder:** After this step, do **not** merge `main` into this branch. All work for this sub-issue happens on this branch until it is merged back to `main`.

---

## Step 3 – Create a PR linked to the sub-issue

1. Create a PR from the sub-issue branch into `main` using the GitHub MCP or UI. The PR description **must** include:

   ```text
   Fixes #<sub-issue-number>
   ```

   Example:

   ```text
   Fixes #29
   ```

2. Assign reviewer: `kareemdrive001-dev`.
3. Ensure the PR is on the `workflow-test-kanban` project.

**Resulting status** (via automation)

- Issue: `In progress`  
- PR: `Ready`

Implementation work now happens directly on this branch.

---

## Step 4 – Do the work on the PR branch

- Implement all code changes required to complete the sub-issue (**only on this branch**).
- Make small, focused commits related to this sub-issue.
- Optionally adjust `documents/local/current-sub-issue.md` to reflect progress, for example:

  ```markdown
  - Workflow step: 4 – Implementation done
  ```

  and commit that change as well.

- Push changes to GitHub as you go.

**Resulting status**

- Issue: `In progress`
- PR: `Ready`

---

## Step 5 – Approve the PR (using CLI as `kareemdrive001-dev`)

Once the implementation looks ready for review, approve the PR using the GitHub CLI, authenticated as `kareemdrive001-dev`:

```bash
gh pr review <pr-number> --approve -b "Looks good, moving to In review"
```

**Resulting status** (via automations)

- Issue: `In review`  
- PR: `In review`

At this point, the code is considered ready and we move on to testing.

---

## Step 6 – Test and handle pass/fail

Run automated tests and manual/visual checks appropriate for the sub-issue. For example:

- Backend tests calling `wiki_backend` helpers.
- Running the local GUI: `python src/gui.py`.
- Manual UI interactions (e.g. selecting results in the list and verifying the info panel).

### 6a. If tests **pass**

- Leave the PR and issue in `In review`.
- Proceed to **Step 7 – Merge the PR** when you are happy.

### 6b. If tests **fail after approval**

As soon as you know the PR is broken, its status `In review` is no longer correct.

**Failure path:**

1. **Submit a "Request changes" review (CLI as `kareemdrive001-dev`)**

   From the repo root:

   ```bash
   gh pr review <pr-number> --request-changes -b "Tests failed: <short reason>"
   ```

   This triggers the "Code changes requested" project workflow and sets:

   - **PR status → Ready** (back to "needs work").

2. **Fix the code on the same branch**

   - Make whatever changes are needed.

   ```bash
   # on the same sub-issue branch
   git add <files>
   git commit -m "Fix test failures for Sub X.Y"
   git push
   ```

3. **Re-approve the PR (CLI) once fixed**

   ```bash
   gh pr review <pr-number> --approve -b "All tests passing after fixes"
   ```

   Automation moves:

   - **Issue → In review**
   - **PR → In review**

4. Re-run tests; if they now pass, proceed to Step 7.

This gives a clean loop:

```text
Ready → In review → (fail) Request changes → Ready → … → In review → (pass) Merge
```

---

## Step 7 – Merge the PR

When:

- PR status is `In review`, and
- Tests and manual checks have passed

merge the PR into `main` (via GitHub UI or MCP):

- The `Fixes #<issue>` line closes the sub-issue automatically.
- Automation marks both issue and PR as `Done`.

After merge:

```bash
git switch main
git pull
```

Now the repository is ready for the **next** sub-issue (back to Step 1).

---

## Summary of the tightened workflow

1. **Pick sub-issue** (Issue `Ready`).
2. **Create branch from up-to-date `main`**, record `current-sub-issue` (Issue `Ready`, PR none).
3. **Create PR with `Fixes #…` and assign reviewer** (Issue `In progress`, PR `Ready`).
4. **Do the work only on that branch** (Issue `In progress`, PR `Ready`).
5. **Approve via `gh pr review --approve`** as `kareemdrive001-dev` (Issue `In review`, PR `In review`).
6. **Test**:
   - If pass → keep `In review` and go to merge.
   - If fail → `gh pr review --request-changes`, fix, re-approve, re-test.
7. **Merge PR** → Issue `Done`, PR `Done`; update local `main`.
