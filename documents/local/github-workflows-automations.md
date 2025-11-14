# workflow-test-kanban – Automation Rules

1️⃣ **Auto-add sub-issues to project**

- **Trigger:** When an item in the project has sub-issues  
- **Action:** Add sub-issues to the project

2️⃣ **Auto-add to project**

- **Trigger:** When the filter matches a new or updated item  
- **Filters:** `is:issue,pr is:open`  
- **Action:** Add the item to the project

3️⃣ **Auto-close issue**

- **Trigger:** When the status is updated  
- **Condition:** `Status: Done`  
- **Action:** Close the issue

4️⃣ **Code changes requested**

- **Trigger:** When a pull request has a review requesting changes  
- **Action:** Set `Status = Ready`

5️⃣ **Code review approved**

- **Trigger:** When a pull request is approved  
- **Action:** Set `Status = In review`

6️⃣ **Item added to project**

- **Trigger:** When an item is added to the project (issue or pull request)  
- **Action:** Set `Status = Ready`

7️⃣ **Item closed**

- **Trigger:** When an item is closed (issue or pull request)  
- **Action:** Set `Status = Done`

8️⃣ **Item reopened**

- **Trigger:** When an item is reopened (issue or pull request)  
- **Action:** Set `Status = Ready`

9️⃣ **Pull request linked to issue**

- **Trigger:** When a pull request is linked to an issue  
- **Action:** Set `Status = In progress`

🔟 **Pull request merged**

- **Trigger:** When a pull request is merged  
- **Action:** Set `Status = Done`
