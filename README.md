# photon-team-io
#### _Team 10_
#### _Primary Language:_ **Python**

### Team Members:
- andrewamidei - Andrew Amidei
- tb087 - Tyler Brandon
- DConly - Duncan Conly
- EvanMeyerss - Evan Meyers
- ppolav01 - Pranav Polavarapu

### Table of Contents:
- [Installing Dependencies on vm](#install-dependencies-on-vm)
- [Run your Python Code on vm](#run-python-code-on-vm)
- [Database Instructions](#connect-database-to-python-file)

If you are looking to setup other parts of the VM check out [Developer Environment Setup](https://github.com/andrewamidei/photon-team-io/blob/main/dev-environment-setup.md).

---

## Install Dependencies on vm

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

## Run Python Code on vm

Navigate to the folder location where you have placed your Python code. 



Right click on the folder and select `Open Terminal Here`.

Run your code by starting the main file.
```
python3 main.py
```

---
