
# midihum with simple GUI

forked from:
https://github.com/erwald/midihum

I added a simple GUI and compiled into exe.

![](dialog.png)

# Usage

1. Click "midihum_gui.exe" (takes a while to boot up)
2. Click "Select output folder"
3. Click "Select input midi files"
4. Conversion will start
5. Output folder will automatically open after conversion

If you want to cancel the conversion, just close the window.

# For developers

## Requirements

* Python 3.11
* uv 0.7.12

## Installation
`uv sync`

## Build (Windows only)
`.\build_win.bat`

OR

Run Release workflow of GitHub Actions.
