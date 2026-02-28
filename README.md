# R6S Settings Tool

A small Windows GUI tool (Tkinter) for editing two values in **Rainbow Six Siege**’s `GameSettings.ini`:

- `MouseSensitivityMultiplierUnit` (sensitivity multiplier)
- `DataCenterHint` (server / data center region)

The tool helps you quickly change these settings without manually opening the `.ini` file.

## Screenshot

Main window and dialogs:

- Main window (Image 1)
- Sensitivity dialog (Image 2)
- Region selection dialog (Image 3)

## Features

- Clean dark-themed UI
- Two one-click actions:
  - **Change Sensitivity Multiplier**
  - **Change Server Region**
- Remembers your selected settings folder in a config file:
  - `~/.r6s_settings_tool.cfg`
- Displays current multiplier and current region in the main window
- Safety check: refuses to run if **RainbowSix.exe** is running (to avoid editing while the game is open)

## Requirements

- Windows (uses `tasklist` to detect `RainbowSix.exe`)
- Python 3.10+ recommended
- Tkinter (usually included with standard Python on Windows)

No third‑party Python packages required.

## How it works

This program edits the following lines in `GameSettings.ini`:

- `MouseSensitivityMultiplierUnit=...`
- `DataCenterHint=...`

It reads the current values, shows them in the UI, and rewrites only the matching line(s) when you apply a change.

## Usage

1. Close **Rainbow Six Siege** if it is running.
2. Run the script:

   ```bash
   python main.py
   ```

3. On first run, you’ll be prompted to select your R6S settings folder (it must contain `GameSettings.ini`).
4. Use the buttons to change:
   - sensitivity multiplier, or
   - server region
5. Press **Escape** to close the app.

### Finding `GameSettings.ini`

The location depends on your Ubisoft/Steam setup and account ID. The tool will ask you to select the correct folder; just choose the folder that **contains** `GameSettings.ini`.

## Notes / Behavior

- The window is borderless and stays on top.
- You can drag the window by clicking and dragging anywhere.
- The selected folder is stored in `~/.r6s_settings_tool.cfg`.
- The UI displays a privacy-friendly shortened path (e.g. `...\Parent\Folder\GameSettings.ini`).

## Supported regions

The region picker includes:

- Default
- West US, Central US, South Central US, East US
- West Europe, North Europe
- East Asia, Southeast Asia, Japan East
- South Africa North
- Australia East
- Brazil South
- UAE North

(These map to `DataCenterHint` values like `playfab/westus`, etc.)

## Disclaimer

This tool edits a game configuration file. Use at your own risk. Always keep backups if you’re unsure, and make sure the game is closed before applying changes.
