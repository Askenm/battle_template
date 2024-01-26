"""
The purpose of this is to write all the functionality required to edit the main database
"""
from sqlalchemy import create_engine, text
import pandas as pd
from .query_catalog import query_catalog


class DBMS:
    def __init__(self):
        user = "ckbAdmin"
        password = "CodeKataBattles$"
        host = "ckb.postgres.database.azure.com"
        port = 5432
        database = "postgres"
        DBMS_connection_string = "postgresql://{}:{}@{}:{}/{}".format(
            user, password, host, port, database
        )

        self.engine = create_engine(DBMS_connection_string)

    def DDL(self):
        for query_name, query in query_catalog["init"].items():
            print(f"EXECUTING {query_name}")
            with self.engine.connect() as connection:
                query = text(query)
                connection.execute(query)

    def write(self, query_name, query_processing_info):
        query = query_catalog["write"][query_name]
        for placeholder, value in query_processing_info.items():
            query = query.replace(placeholder, str(value))

        with self.engine.begin() as connection:
            query = text(query)
            return connection.execute(query)

    def read(self, query_name, query_processing_info):
        query = query_catalog["read"][query_name]
        for placeholder, value in query_processing_info.items():
            query = query.replace(placeholder, str(value))

        dataDF = pd.read_sql(query, self.engine)

        return dataDF
