# Section 1

To implement this pipeline, the following steps outlined below:

1. Create a folder to store the incoming datasets and another folder to store the output data. 
  * initiate input_dir, success_dir & unsuccessful_dir file path.
2. Set up an Apache Airflow DAG to schedule the data processing pipeline on an hourly interval.
  * schedule interval is set every hour at 55 minutes (e.g. 10.55am, 11.55am...)
  ```
  schedule_interval='55 * * * *'
  ```
3. Use the read_csv() to read the incoming CSV files from the folder and load them into a Pandas DataFrame.
  * check_files() function will create a list of filenames by checking the specified directory and check for creation datetime for the current hour.
  * In Main() function, using the filename list with for loop to read incoming CSV files and concat them into a dataframe (raw_df).
4. Clean and process the data according to the requirements. 
  * Split the name column into first_name and last_name columns using the str.split() function with 1 space as seperator.
  * Remove invalid date "1996/02/31" by getting the index of the row label and drop that row.
  * Format the birthday field into YYYYMMDD format using the to_datetime() & strftime() function.
  * Remove any rows which do not have a name field using the dropna() function.
  * Perform the validity checks on the data:
    Check if the mobile number is 8 digits long using the str.len() function, create new column "valid_mobile_no" which output 1 for valid mobile number and 0 for invalid numbers.
    Check if the email is valid by checking if it ends with ".com" or ".net" using the str.endswith() function, create new column "valid_email" which output 1 for valid email and 0 for invalid email.
    Check if the applicant is over 18 years old as of 1 Jan 2022 by comparing the date_of_birth with the date '2022-01-01', extracting the days between the 2 dates, dividing by 365 to get the number of years. Create a new column named "above_18", output 1 if applicant's years is large than 18 and 0 for lesser than 18.
    Get all the index of rows values for the above new 3 columns if any rows value are 0 and drop those rows.
5. Generate "membership_id" column for successful applications using the user's last name and SHA256 hash of the applicant's birthday truncated to the first 5 digits of the hash in hexadecimal. 
6. Drop unwanted columns (new columns created and name column), rearrange columns and output successful applications into a CSV file and into seperate folder. 
7. Compare and seperate unsuccessful appplications by taking the difference between raw and successful dataframe and output into a CSV file and into seperate folder.
