import pandas as pd
import logging 
import os
from  sqlalchemy import inspect
from src.database.db_connection import engine


#-----------------Logging Setup--------------#

logging.basicConfig(
    filename = "logs/data_ingestion.log",
    level = logging.INFO,
    format = "%(asctime)s  - %(levelname)s - %(message)s"

)


#----------------- Functions ------------ #

def read_data(file_path):
    try:
        logging.info(f"Reading File from path:{file_path}"
                     )
        if not os.path.exists(file_path):
             raise FileNotFoundError(f"File not found: {file_path}")
            
        df = pd.read_csv(file_path)

        logging.info('File read successfully')

        return df

    except Exception as e:
        logging.error(f"Error in reading file:{e}")
        raise e
    
def standardize_columns(df):
    logging.info("Standardizing columns names")
    df.columns = df.columns.str.strip().str.lower()
    return df

def get_table_columns(table_name):
    logging.info("Fetching DB table columns")
    inspector = inspect(engine)
    return[col['name'] for col in inspector.get_columns(table_name)]


def align_columns(df , table_columns):
    logging.info('Aligning columns with DB schema')

    # drop id (auto increment)

    if "id" in df.columns:
        df = df.drop(columns=["id"])

    df = df[[col for col in table_columns if col in df.columns]]
    
    return df

def clean_data(df):
    logging.info("Cleaning Data")

    df.drop_duplicates(inplace=True)

    for col in df.columns:
        if df[col].dtype == 'object':
             df[col].fillna(df[col].mode()[0] , inplace=True)

        else:
            df[col].fillna(df[col].median() , inplace=True)

    return df


def insert_into_db(df,table_name):
    try:
        logging.info('Inserting data into Database')

        df.to_sql(table_name , con=engine , if_exists = "append" , index = False
                  )
        
    except Exception as e:
        logging.error(f"Error in inserting data:{e} ")


#---- PIPELINE------#

def run_pipeline(file_path , table_name):
    try:
        logging.info("======== PIPELINE STARTED=====")

        df = read_data(file_path)

        df = standardize_columns(df)

        table_columns = get_table_columns(table_name)

        df = align_columns(df , table_columns)

        df = clean_data(df)

        insert_into_db(df , table_name)

        logging.info("==== PIPELINE COMPLETED=====")

    except Exception as e:
        logging.error(f"Pipeline failed : {e}")

        print("error , e")

## Run block

if __name__ == "__main__":
    run_pipeline(
        r"C:\Users\shiva\Downloads\archive (6)\train.csv",
        "insurance_data"
    )