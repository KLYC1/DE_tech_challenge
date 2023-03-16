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

# Define function to hash a pandas Series of strings representing birthdays in 'YYYYMMDD' format using SHA-256 and return only the first 5 characters
def sha256_hash(values):
    full_hashes = values.apply(lambda dob: hashlib.sha256(dob.encode('utf-8')).hexdigest())
    return full_hashes.str.slice(stop=5)

# Main function to concat raw dataframes, clean and verify the data
def main():
    raw_df = pd.DataFrame()
    my_list = check_files()
    # loop through the list and append all the data into one dataframe, raw_df
    for filenames in my_list:
        new_df = pd.read_csv(input_dir + str(filenames), header=0)
        raw_df = pd.concat([raw_df, new_df], axis=0, ignore_index=True)
        
    # drop row if name is NaN and split 'name' column into 2 columns and add into existing dataframe
    valid_df = raw_df.dropna(axis=0, how='any', subset=['name'], inplace=False)
    valid_df[['first_name','last_name']] = valid_df.name.str.split(" ", 1, expand=True)

    # remove row contains invalid date "31 feb 1996" & format date_of_birth column into YYYYMMDD format
    i = valid_df[(valid_df.date_of_birth == '1996/02/31')].index
    print(i)
    valid_df = valid_df.drop(i)
    valid_df['date_of_birth'] = pd.to_datetime(valid_df.date_of_birth).dt.strftime('%Y%m%d')
    
    # Check validity of mobile_no, age above 18 and email, remove rows which are not valid (value 0)
    valid_df['valid_mobile_no'] = valid_df['mobile_no'].apply(lambda x: 1 if len(str(x)) == 8 else 0)
    valid_df['above_18'] = valid_df['date_of_birth'].apply(lambda x: (datetime(2022,1,1) - pd.to_datetime(x, format='%Y%m%d')).days / 365 > 18)
    valid_df['valid_email'] = valid_df['email'].apply(lambda x: 1 if x.endswith('.com') or x.endswith('.net') else 0)
    index_names = valid_df[(valid_df['valid_mobile_no'] == 0) | (valid_df['above_18'] == 0) | (valid_df['valid_email'] == 0 )].index
    valid_df = valid_df.drop(index_names)
    
    # Apply truncated SHA-256 hash 'date_of_birth' to the 'last_name'
    valid_df['membership_id'] = valid_df['last_name'] + "_" + sha256_hash(valid_df['date_of_birth'])
    
    # drop unwanted columns, rearrange columns and output valid applications to successful directory
    success_df = valid_df.drop(columns=['name', 'valid_mobile_no', 'above_18', 'valid_email'], axis=1)
    success_df = success_df.loc[:,['membership_id','first_name','last_name','email', 'date_of_birth', 'mobile_no']]
    success_df.to_csv(success_dir+"successful.csv", index=False, encoding='utf-8')
    print("csv output for successful.csv completed")
    
    # compare raw and success df on email column values, take the difference and output invalid applications to unsuccessful directory
    invalid_df = raw_df[~raw_df.email.isin(success_df.email)]
    invalid_df.to_csv(unsuccessful_dir+"invalid.csv", index=False, encoding='utf-8')
    print("csv output for invalid.csv completed")

main_func = PythonOperator(
    task_id='py_func1',
    python_callable=main,
    dag=dag
)
