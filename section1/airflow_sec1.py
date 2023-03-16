import os, time, hashlib
from datetime import datetime, timedelta
import pandas as pd

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'start_date': days_ago(2),
    'retries':0,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='section1',
    description='DETC section 1',
    default_args=default_args,
    schedule_interval='55 * * * *',
    max_active_runs=1,
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
    tags=['section1']
)

# Set up input, successful & unsuccessful directories
input_dir = "Desktop/DETC/section1/datasets/"
success_dir = "Desktop/DETC/section1/successful/"
unsuccessful_dir = "Desktop/DETC/section1/unsuccessful/"

def check_files():
    """This function find files created for the current hour inside input directory and output to a list of filename."""
    latest = 0
    now = time.strftime('%Y-%m-%d %H', time.localtime())
    my_list = []
    # loop the dir and get files that are created during the current hour
    for fname in os.listdir(input_dir):
        if fname.endswith(''):
            createtime = os.stat(os.path.join(input_dir, fname)).st_ctime
            if createtime > latest:
                latest = createtime
                out = time.strftime('%Y-%m-%d %H', time.localtime(latest))
                # if latest out is equal to current hour, append name into my_list
                if out == now:
                    print (fname, "was created during the current hour.")
                    my_list.append(fname)
                else:
                    pass
    return my_list

# Main function to concat raw dataframes, clean and verify the data
def main():
    raw_df = pd.DataFrame()
    my_list = check_files()
    # loop through the list and append all the data into one dataframe, raw_df
    for filenames in my_list:
        new_df = pd.read_csv(input_dir + str(filenames), header=0)
        raw_df = pd.concat([raw_df, new_df], axis=0, ignore_index=True)

main_func = PythonOperator(
    task_id='py_func1',
    python_callable=main,
    dag=dag
)
