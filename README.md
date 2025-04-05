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

## Usage

1. Contact an administrator to query the database via SQL directly and present the conversations for the given date-time range.
   1. You need to provide them with the following.
      1. The `ID` of the chatbot.
      2. The Datetime range for the conversations.
   2. The raw SQL query is

        ```sql
        select 
            ac.id,
            ac.raw_data,
            ac.data,
            ac.extra_data
        from 
            public.assistants_conversation ac 
        where 
            ac.assistant_id = <chatbotId> 
        and 
            ac.is_completed = true
        and 
            ac.created_at >= <startingDatetimeStr> and ac.created_at <= <endingDatetimeStr>;
        ```

   3. The `data` and `raw_data` columns are __MANDATORY__.
2. The administrator then needs to export the conversation query result as a __CSV__ only with the naming scheme of "\<chatbotId\>-convo.csv".
3. Copy the CSV file to the root of the `data` directory in the repository.
   1. You can have multiple export CSVs saved to the `data` directory.
4. Edit the `CHATBOT_ID` declared at the top of the `main.py` file to be the chatbot ID for the use-case.
5. Run `python main.py`
6. The exported conversation CSV should be in `data/cleaned` with the naming scheme "\<chatbotId\>_cleaned_convo.csv".
