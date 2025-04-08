# Custom Chat Assistant Conversation Exporter

This internal tool can be used by developers and customer success representatives to manually export conversations for a given chatbot assistant for Elay's CRM Automation product.

## Requirements

1. Python
2. BASH
   1. GitBASH for Windows

## Setup

1. Create a new virtual environment using the `python3 -m venv env` command.
   1. On windows, just use the `python -m venv env` command.
2. Give all acripts in the `scripts/` directory execution priviledges via the `chmod +x scripts/*.sh` command.
3. Activate the virtual environment using the `source env/bin/activate` command.
   1. On windows, the command is `source env/Scripts/activate`.
   2. __DO NOT PROCEED FURTHER WITHOUT ACTIVATING THE VIRTUAL ENVIRONMENT!!!__
4. Run the install script via the `sh scripts/install.sh` command.
5. Add a `.env` file with the required values to the root of the directory.

## Usage

1. Activate the python virtual environment created during setup via the command `source env/bin/activate`.
   1. On windows, the command is `source env/Scripts/activate`.
2. Edit the `CHATBOT_ID` in `main.py` to the `ID` of the Assistant (not the `UUID` or the `short_code`).
3. Edit the `DATE_RANGE_START` and `DATE_RANGE_END` values in `main.py` in the formats `"YYYY-MM-DD 00:00:00"` and `"YYYY-MM-DD 23:59:59"`, __respectively__.
4. Run the command `python main.py`.
5. Repeat for all values for `CHATBOT_ID`.
6. The exported conversations will be in `data/exports` in the format `<chatbot_id>_export.csv`.

## .ENV File Format

```env
DATABASE_URI = "path/to/the/database"
```
