# Section 1

To implement this pipeline, the following steps outlined below:

1. Create a folder to store the incoming datasets and another folder to store the output data. 
  * initiate input_dir, success_dir & unsuccessful_dir file path.
2. Set up an Apache Airflow DAG (Directed Acyclic Graph) to schedule the data processing pipeline on an hourly interval.
  * schedule interval is set every hour at 55 minutes (e.g. 10.55am, 11.55am...)
3. Use the Pandas library to read the incoming CSV files from the folder and load them into a Pandas DataFrame.
  * check_files function will create a list of filenames
  * In Main function, using the filename list with for loop to read incoming CSV files into dataframes and concat the dataframes.
