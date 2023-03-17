# Section 1

To implement this pipeline, the following steps outlined below:

1. Create a folder to store the incoming datasets and another folder to store the output data. 
  * initiate input_dir, success_dir & unsuccessful_dir file path.
2. Set up an Apache Airflow DAG (Directed Acyclic Graph) to schedule the data processing pipeline on an hourly interval.
  * schedule interval is set every hour at 55 minutes (e.g. 10.55am, 11.55am...)
  ```linux
  schedule_interval='55 * * * *'
  ```
3. Use the Pandas library to read the incoming CSV files from the folder and load them into a Pandas DataFrame.
  * check_files function will create a list of filenames
  * In Main function, using the filename list with for loop to read incoming CSV files into dataframes and concat the dataframes.
4. Clean and process the data according to the requirements. 
  * Split the name column into first_name and last_name columns using the str.split() function.
  * Format the birthday field into YYYYMMDD format using the to_datetime() function.
  * Remove any rows which do not have a name field using the dropna() function.
  * Perform the validity checks on the data:
    Check if the mobile number is 8 digits long using the str.len() function.
    Check if the email is valid by checking if it ends with ".com" or ".net" using the str.endswith() function.
    Check if the applicant is over 18 years old as of 1 Jan 2022 by comparing the birthday with the date '2022-01-01' using the datetime module.
    Create a new field named above_18 based on the applicant's date of birth
5. Generate Membership IDs for successful applications using the user's last name and SHA256 hash of the applicant's birthday truncated to the first 5 digits of the hash using the hashlib module. 
6. Drop unwanted columns, rearrange columns and output successful applications into a CSV file. 
7. Compare and seperate unsuccessful appplications by taking the difference between raw and successful dataframe and output into a CSV file.
