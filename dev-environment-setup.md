# Developer Environment Setup

### Table of Contents
- [Creating a shared folder for vm](https://github.com/andrewamidei/photon-team-io/blob/main/dev-environment-setup.md#creating-a-shared-folder-for-vm)
- [Installing Dependencies on vm](https://github.com/andrewamidei/photon-team-io/blob/main/dev-environment-setup.md#install-Dependencies-on-vm)
- [Run your Python Code on vm](https://github.com/andrewamidei/photon-team-io/blob/main/dev-environment-setup.md#run-python-code-on-vm)
- [Install VS Code on vm](https://github.com/andrewamidei/photon-team-io/blob/main/dev-environment-setup.md#install-vs-code-on-vm)

---

### Creating a shared folder for vm
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

### Install Dependencies on vm

Install pip.
```
sudo apt install -y python3-pip
```

Install Tkinter.
```
sudo apt-get install python3-tk
```

Install CustomTkinter, Pillow and psycopg2.
- CustomTkinter is for the UI.
- Pillow is used for images.
- Psycopg2 is used or database access.
```
pip install customtkinter pillow psycopg2-binary
```

---

### Run Python Code on vm

Navigate to the folder location where you have placed your Python code. 

Right click on the folder and select `Open Terminal Here`.

Run your code by starting the main file.
```
python3 main.py
```

---

### Install VS Code on vm

Copy and paste the commands below.

#### Add the repository 

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

After that it will show up under Development in applications.

