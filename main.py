import pandas as pd
from os import sep, getenv
from json import loads, dumps
from sqlalchemy import create_engine
from dotenv import load_dotenv
import argparse

CHATBOT_ID = 2848
FILE_PATH = f"data{sep}{CHATBOT_ID}-convo.csv"
load_dotenv()

def get_raw_export():
    engine = create_engine(getenv("DATABASE_URI"))

    prepared_statement = """
    SELECT 
        ac.id, 
        ac.assistant_id, 
        ac.data, 
        ac.extra_data, 
        ac.created_at 
    FROM 
        public.assistants_conversation ac
    WHERE 
        assistant_id = :CHATBOT_ID
    ORDER BY
        created_at DESC;
    """

    with engine.connect() as conn:
        result = conn.execute(prepared_statement, {"CHATBOT_ID": CHATBOT_ID})
        rows = result.fetchall()
        data = []

        for row in rows:
            data.append(
                {
                    "id": row.id,
                    "chatbot_id": row.chatbot_id,
                    "data": dumps(row.data),
                    "extra_data": dumps(row.extra_data),
                    "created_at": row.created_at,
                    "updated_at": row.updated_at
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
    dataframe = pd.read_csv(f"data{sep}cleaned{sep}{CHATBOT_ID}_cleaned_convo.csv")

    convo_json = []

    for row in dataframe.itertuples():
        data_001 = loads(row.data)
        data_002 = loads(row.extra_data)
        full_data = {
            "id": row.id
        }
        for key in data_001:
            full_data[key] = data_001.get(key, "")
        for key in data_002:
            full_data[key] = data_001.get(key, "")
        convo_json.append(full_data)
    df = pd.DataFrame(convo_json)
    df.to_csv(f"data{sep}export{sep}{CHATBOT_ID}_export.csv")

def run():
    get_raw_export()
    export_cleaned_conversation()
    export_conversation()

if __name__=="__main__":
    run()
