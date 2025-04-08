import pandas as pd
from os import sep, getenv
from json import loads, dumps
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import argparse
import re

CHATBOT_ID = 2848
DATE_RANGE_START = "2025-03-06 00:00:00"
DATE_RANGE_END = "2025-04-07 23:59:59"
FILE_PATH = f"data{sep}{CHATBOT_ID}-convo.csv"
URL_REGEX = re.compile(
    r'^(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,}){1,2}\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,}){1,2})|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?')
load_dotenv()


def get_raw_export():
    engine = create_engine(getenv("DATABASE_URI"))

    prepared_statement = """
    SELECT 
        ac.id, 
        ac.assistant_id, 
        ac.raw_data,
        ac.data, 
        ac.extra_data, 
        ac.created_at 
    FROM 
        public.assistants_conversation ac
    WHERE 
        ac.assistant_id = :CHATBOT_ID
    AND
        ac.is_completed = TRUE
    AND
        ac.created_at >= :DATE_RANGE_START
    AND
        ac.created_at <= :DATE_RANGE_END
    ORDER BY
        created_at DESC;
    """

    with engine.connect() as conn:
        result = conn.execute(
            text(prepared_statement),
            {
                "CHATBOT_ID": CHATBOT_ID,
                "DATE_RANGE_START": DATE_RANGE_START,
                "DATE_RANGE_END": DATE_RANGE_END
            }
        )

        rows = result.fetchall()
        data = []

        for row in rows:
            # print(row)
            data.append(
                {
                    "id": row.id,
                    "assistant_id": row.assistant_id,
                    "raw_data": dumps(row.raw_data),
                    "data": dumps(row.data),
                    "extra_data": dumps(row.extra_data),
                    "created_at": row.created_at
                }
            )
        df = pd.DataFrame(data)
        df.to_csv(FILE_PATH, index=False)
        print(f"Exported {len(data)} records to {FILE_PATH}")


def export_cleaned_conversation():
    data_frame = pd.read_csv(FILE_PATH)
    data_frame["chatbot_id"] = CHATBOT_ID
    data_frame = data_frame.drop('raw_data', axis=1)
    data_frame.to_csv(f"data{sep}cleaned{sep}{CHATBOT_ID}_cleaned_convo.csv")


def export_conversation():
    dataframe = pd.read_csv(
        f"data{sep}cleaned{sep}{CHATBOT_ID}_cleaned_convo.csv")

    convo_json = []

    for row in dataframe.itertuples():
        data_001 = loads(row.data)
        data_002 = loads(row.extra_data)
        full_data = {
            "id": row.id
        }

        for key in data_001:
            answer = data_001.get(key)
            if answer and isinstance(answer, str) and re.match(URL_REGEX, answer):
                continue
            full_data[key] = answer

        for key in data_002:
            answer = data_002.get(key)
            if answer and isinstance(answer, str) and re.match(URL_REGEX, answer):
                continue
            full_data[key] = answer

        convo_json.append(full_data)

    df = pd.DataFrame(convo_json)
    df.to_csv(f"data{sep}export{sep}{CHATBOT_ID}_export.csv")


def run():
    get_raw_export()
    export_cleaned_conversation()
    export_conversation()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export chatbot conversation data.")
    # parser.add_argument(
    #     "--get_raw_export",
    #     action="store_true",
    #     help="Export raw conversation data from the database."
    # )
    # parser.add_argument(
    #     "--export_cleaned_conversation",
    #     action="store_true",
    #     help="Export cleaned conversation data."
    # )
    # parser.add_argument(
    #     "--export_conversation",
    #     action="store_true",
    #     help="Export conversation data to CSV."
    # )
    # args = parser.parse_args()
    # if args.get_raw_export:
    #     get_raw_export()
    # if args.export_cleaned_conversation:
    #     export_cleaned_conversation()
    # if args.export_conversation:
    #     export_conversation()
    # if not (args.get_raw_export or args.export_cleaned_conversation or args.export_conversation):
    #     print("No arguments provided. Running all tasks.")
    #     # Run all tasks if no specific argument is provided
    run()
