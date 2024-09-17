# Developer Environment Setup

### Table of Contents
- [Creating a shared folder for vm](#creating-a-shared-folder-for-vm)
- [Install VS Code on vm](#install-vs-code-on-vm)
- [Database Instructions](#connect-database-to-python-file)

---

## Creating a shared folder for vm
This shared folder can be used to transfer files to and from your VirtualBox system.

- Before opening your VM navigate to the location you want to save the shared folder (I put mine in the location where my VM files are stored) 
- Open VirtualBox and go to the settings of the VM.
- Select shared folders.
- Hit the folder plus icon in the top right corner.
- Enter the path where your folder is stored.
- Enter the folder name (name you will see on Linux)
- Check auto mount.
- Hit ok to get out of all dialogs until you are back to the VirtualBox homepage.
- Start the machine.

In the VM open the terminal (hint: hit `View > Zoom In` to make the text larger)

Give yourself permission to view the shared folder.
```
sudo usermod -a -G vboxsf $(whoami)
```

At this point, you either need to restart the VM or log out and log back in to apply the changes.

After you are back you can hit the home folder icon on the desktop and navigate to the new mount point with the name you gave it over to the left of the file explorer under devices.

That should be it!

---

## Install VS Code on vm

Copy and paste the commands below.

Add the repository 
```
sudo apt-get install wget gpg
```

```
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
```

```
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
```

```
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
```

```
rm -f packages.microsoft.gpg
```

Run system update.
```
sudo apt update
```

Install VS Code.
```
sudo apt install code
```
---

After that it will show up under Development in applications.

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

### 1. Switch to postgre user and enter SQL:

```
sudo -u postgres psql
```
### 2. Select photon database:

```
\c photon
```

### 3. Display all records in player table:

```
SELECT * from player;
```

<br/> From here you can delete, add, or rename records in the table.

### To delete (based on codename):
**_(NOTE: All records sharing same selected codename will be deleted)_**

```
DELETE FROM player where(codename='<codename>');
```

---