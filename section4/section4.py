import requests
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Fetch the data using the COVID19 API, change country to singapore 
url = "https://api.covid19api.com/country/singapore/status/confirmed"
response = requests.get(url)
data = response.json()
# print(json.dumps(data, indent=4, sort_keys=True)) # print to check data

# Extract the relevant data from the response, which are dates and cases. 
dates = []
cases = []
for record in data:
    dates.append(record["Date"])
    cases.append(record["Cases"])

# Convert the dates to a datenum format that can be used by matplotlib
dates = [mdates.datestr2num(date) for date in dates]

# Create a line chart using figure & axes
fig, ax = plt.subplots()
ax.plot_date(dates, cases)

# Label the chart
plt.title("COVID-19 Cases in Singapore")
plt.xlabel("Date")
plt.ylabel("Number of Confirmed Cases")

# Retrieve the y-axis tick values and then converts them to strings with full integer values using a list
y_ticks = ax.get_yticks()
y_tick_labels = [str(int(y_tick)) for y_tick in y_ticks]
plt.yticks(y_ticks, y_tick_labels)

# Set the x-axis tick format to show month abbreviated name intervals and year 
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# Rotate the x-axis tick labels to vertical, plot grid and set y axis minimum value of 0
plt.xticks(rotation=90)
plt.ylim(0)
plt.grid(True)

# Display the chart | save to png
plt.show()
#plt.savefig('Desktop/SG_covid19_cases.png')
