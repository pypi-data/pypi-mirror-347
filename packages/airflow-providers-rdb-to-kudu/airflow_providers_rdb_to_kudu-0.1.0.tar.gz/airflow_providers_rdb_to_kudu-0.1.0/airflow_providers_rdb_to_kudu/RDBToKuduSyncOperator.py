import logging
from typing import List, Optional

import psycopg2
import pymysql
from airflow.hooks.base import BaseHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from kudu.client import KuduClient
from kudu.errors import KuduError


class RDBToKuduSyncOperator(BaseOperator):
    template_fields = ("rdb_query",)
    @apply_defaults
    def __init__(
        self,
        rdb_type: str,
        rdb_conn_id: str,
        kudu_master: str,
        rdb_query: str,
        kudu_table: str,
        mode: str = "upsert",  # insert, upsert, insert_overwrite
        batch_size: int = 1000,
        primary_keys: Optional[List[str]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.rdb_type = rdb_type
        self.rdb_conn_id = rdb_conn_id
        self.kudu_master = kudu_master
        self.rdb_query = rdb_query
        self.kudu_table = kudu_table
        self.mode = mode
        self.batch_size = batch_size
        self.primary_keys = primary_keys if primary_keys else []

    def get_postgres_connection(self):
        logging.info(f"Connecting to PostgreSQL using connection id: {self.rdb_conn_id}")
        conn = BaseHook.get_connection(self.rdb_conn_id)
        pg_conn = psycopg2.connect(
            host=conn.host,
            port=conn.port,
            user=conn.login,
            password=conn.password,
            dbname=conn.schema
        )
        logging.info("Successfully connected to PostgreSQL")
        return pg_conn

    def get_mysql_connection(self):
        logging.info(f"Connecting to MySQL using connection id: {self.rdb_conn_id}")
        conn = BaseHook.get_connection(self.rdb_conn_id)
        mysql_conn = pymysql.connect(
            host=conn.host,
            port=conn.port,
            user=conn.login,
            password=conn.password,
            database=conn.schema,
            charset="utf8mb4"
        )
        logging.info("Successfully connected to MySQL")
        return mysql_conn

    def get_kudu_client(self):
        logging.info(f"Connecting to Kudu master: {self.kudu_master}")
        client = KuduClient(self.kudu_master)
        logging.info("Successfully connected to Kudu")
        return client

    def get_columns(self, cursor):
        return [desc[0] for desc in cursor.description]

    def convert_value_to_kudu_type(self, value, kudu_type):
        if value is None:
            return None
        if kudu_type == 'int8':
            return int(value)
        elif kudu_type == 'int16':
            return int(value)
        elif kudu_type == 'int32':
            return int(value)
        elif kudu_type == 'int64':
            return int(value)
        elif kudu_type == 'float':
            return float(value)
        elif kudu_type == 'double':
            return float(value)
        elif kudu_type == 'string':
            return str(value)
        elif kudu_type == 'bool':
            return bool(value)
        elif kudu_type == 'timestamp':
            return value
        else:
            return str(value)

    def execute(self, context):
        # Connect to RDB
        if self.rdb_type == "postgresql":
            rdb_conn = self.get_postgres_connection()
        elif self.rdb_type == "mysql":
            rdb_conn = self.get_mysql_connection()
        else:
            raise ValueError(f"Unsupported RDB type: {self.rdb_type}")
        
        rdb_cursor = rdb_conn.cursor()

        # Connect to Kudu
        kudu_client = self.get_kudu_client()
        table = kudu_client.table(self.kudu_table)
        session = kudu_client.new_session()

        logging.info(f"Executing RDB query: {self.rdb_query}")
        rdb_cursor.execute(self.rdb_query)

        # Extract columns
        columns = self.get_columns(rdb_cursor)
        
        # Get Kudu table schema
        kudu_schema = table.schema
        column_types = {col.name: col.type.name for col in kudu_schema.columns}

        if self.mode == "insert_overwrite":
            logging.info(f"Mode is 'insert_overwrite', will truncate table: {self.kudu_table}")
            # Note: Kudu doesn't support TRUNCATE directly, you might need to implement a different strategy
            # such as dropping and recreating the table, or deleting all rows

        logging.info(f"Starting batch synchronization with batch size: {self.batch_size}")
        # Batch synchronization
        total_rows = 0
        while True:
            rows = rdb_cursor.fetchmany(self.batch_size)
            if not rows:
                break

            for row in rows:
                try:
                    if self.mode in ["insert", "insert_overwrite"]:
                        op = table.new_insert()
                    else:  # upsert
                        op = table.new_upsert()

                    # Set values for each column
                    for i, col_name in enumerate(columns):
                        value = self.convert_value_to_kudu_type(row[i], column_types[col_name])
                        op[col_name] = value

                    session.apply(op)
                    total_rows += 1

                    # Flush every batch_size operations
                    if total_rows % self.batch_size == 0:
                        session.flush()
                        logging.info(f"Processed {total_rows} rows")

                except KuduError as e:
                    logging.error(f"Error processing row: {e}")
                    raise

            # Flush remaining operations
            session.flush()

        logging.info(f"Completed synchronization, total rows processed: {total_rows}")

        # Close connections
        rdb_cursor.close()
        rdb_conn.close()
        session.close()
        logging.info("All connections closed successfully") 