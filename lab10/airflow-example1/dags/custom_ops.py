from airflow.models import BaseOperator
import pandas as pd
import logging


class CustomTransformationOperator(BaseOperator):
    def __init__(self, file_name: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.file_name = file_name

    def execute(self, context):
        df = pd.read_csv(self.file_name)
        logging.info(df)
        df_return = df.groupby(['customer_id'])['unit_sales'].sum().reset_index()
        file_returned = 'unit_sales_sum.csv'
        df_return.to_csv(file_returned, index=False)
        return file_returned
