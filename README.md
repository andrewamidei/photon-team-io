# photon-team-io
#### _Team 10_
#### _Primary Language:_ **Python**
---

## Connect Database to Python file:
Use the following line to give the postgre user (used to manipulate database) access to the shared folder:

    "sudo usermod -aG vboxsf postgres"

Install the following dependincies in the **_project folder_**:

```
pip install psycopg2-binary
```

#### Currently, the main.py file contains the following SQL-related functions:
  1. Database setup
  2. Addition of a test user _**(COMMENTED OUT)**_
  3. Selection of all entries in the player table _**(COMMENTED OUT)**_
  4. Printing of all players _**(COMMENTED OUT)-(To function, list item 3 must be added back to code)**_
     
#### _If an error is thrown, let me know and I will update README to include a fix._
---