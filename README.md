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

#### _If an error is thrown, let me know and I will update README to include a fix._
## Managing the Database:
To enter the database manually and make changes to the table, the following instructions must be followed:

   <br/> 1. Switch to postgre user and enter SQL:

```
sudo -u postgres psql
```
<br/> 2. Select photon database:

```
\c photon
```

<br/> 3. Display all records in player table:

```
SELECT * from player;
```

<br/> From here you can delete, add, or rename records in the table.
    
---
