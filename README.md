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
2. Run the command `python main.py --chatbot_id comeChatbotId --start_date yyyy-mm-dd 00:00:00 --end_date yyyy-mm-dd 23:59:59 --debug false`.
   1. `start_date` and `end_date` values should be in the formats `"YYYY-MM-DD 00:00:00"` and `"YYYY-MM-DD 23:59:59"`, __respectively__.
   2. If these values aren't provided, then the default values defined in `main.py` will be used.
   3. If `debug` is set to True, all lines from the exported conversation will be printed on screen.
3. Repeat for all values for `CHATBOT_ID`.
4. The exported conversations will be in `data/exports` in the format `<chatbot_id>_export.csv`.

## .ENV File Format

```env
DATABASE_URI = "path/to/the/database"
```
