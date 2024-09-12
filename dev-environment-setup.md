# Developer Environment Setup

### Table of Contents
- [Creating a shared folder](https://github.com/andrewamidei/photon-team-io/blob/main/dev-environment-setup.md#creating-a-shared-folder)
- [Installing Dependencies](https://github.com/andrewamidei/photon-team-io/blob/main/dev-environment-setup.md#install-Dependencies)
- [Run your Python Code](https://github.com/andrewamidei/photon-team-io/blob/main/dev-environment-setup.md#run-python-code)

---

### Creating a shared folder
This shared folder can be used to transfer files to and from your VirtualBox system.

- Before opening your VM navigate to the location you want to save the shared folder (I put mine in the location where my VM files are stored) 
- Open VirtualBox and go to the setting of the VM.
- Select shared folders.
- Hit the folder plus icon in the top right corner.
- Enter the path where your folder is stored.
- Enter the folder name (name you will see on Linux)
- Check auto mount and make permanent.
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

### Install Dependencies

install pip
```
sudo apt install -y python3-pip
```

This is a python library witch you can use to display UI elements.
```
pip install customtkinter
```

Customtkinter uses Pillow as a dependancy.
```
pip install pillow
```

Customtkinter also requires tkinter to function. The python built into Debian does not come with it, so use the below command to install it on python3.
```
sudo apt-get install python3-tk
```

### Run Python Code

Navigate to the folder location where you have placed your python code. 

Right click on the folder and select `Open Terminal Here`.

Run your code by starting the main file
```
python3 main.py
```
