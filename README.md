# Oculus Dash Customizer

A small utility written in python for customizing the Oculus Dash menu on PC!

## Currently supported features

- Changing the floor texture
- Importing PNG textures
- Converting PNG files to DDS and vice versa

## How to run
Download the latest release from the releases tab, unzip and run ovrdashcus.exe! The program will ask you for elevated permissions due to the fact that the Oculus software is protected and cannot be modified without permission.

## How to build

Requirements:

- Python 3.11 (untested on older versions)
- Pillow
- pydds
- Pyinstaller (for building the project)

Clone the repository and `cd` into it:

```batch
git clone https://github.com/CodyMarkix/OculusDashCustomizer && cd OculusDashCustomize
```

(Optional) activate the venv/create a new one if it doesn't work

```batch
venv\Scripts\activate
```

If you didn't create a virtual environment, install the requirements

```batch
pip install -r requirements.txt
```

Build the project

```batch
pyinstaller ovrdashcus.spec
```

Enjoy!