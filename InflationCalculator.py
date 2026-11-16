import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===================================================================================
# Part 1: Reading the CSV file and preparing the data frame for Matplotlib plotting
# ===================================================================================

# Read the CSV file and transposing it into a Pandas data frame. As the first 8 rows of the csv are unnecessary, they have been skipped.
data_frame = pd.read_csv('STATIC_INFLATIONCALC.csv', skiprows=8)

# Default column names are renamed to "Date" and "CPI" respectively for clarity and ease of use in the code.
data_frame.columns = ['Date', 'CPI']

# To effectively filter for the correct dates later on when the user is prompted.
# Create two empty lists to hold the year and month values to be added to the data frame as new columns.
years = []
months = []

# The default YYYY-MM-DD format string is split into two separate columns (Year and Month) using a for loop to go through the "Date" column and extract the year and month values.
for d in data_frame['Date']:
    parts = d.split('-')
    years.append(int(parts[0]))
    months.append(int(parts[1]))

# Assigning the lists of years and months to the data frame as new columns, "Year" and "Month", respectively.
data_frame['Year'] = years
data_frame['Month'] = months

# Adding a new column that holds the annual percentage change in CPI.
data_frame['Annual_Pct_Change'] = data_frame['CPI'].pct_change(periods=12) * 100

# ===================================================================================
# Part 2: Plotting the CPI and annual percentage change on a dual-axis graph
# ===================================================================================

# Create a figure and axis object using Matplotlib's subplots() function, and specifying the figure size and layout.
fig, ax1 = plt.subplots(figsize=(10, 5), layout='constrained')

# Plot Date on x-axis and CPI on the y-axis.
ax1.plot(data_frame['Year'], data_frame['CPI'], color='tab:blue', label='Monthly CPI')

# Add a horizontal line at y=100 to indicate the base level where 2002 = 100.
ax1.axhline(y=100.0, color='black', linestyle=':', label='Base Level (2002 = 100)')

# Set the title and labels for the axes.
ax1.set_title('Canadian Consumer Price Index (CPI) and Annual Percentage Change')
ax1.set_xlabel('Year')
ax1.set_ylabel('CPI Level (2002 = 100)')

# Create another y-axis for the Annual Percentage Change.
ax2 = ax1.twinx()
ax2.plot(data_frame['Year'], data_frame['Annual_Pct_Change'], color='tab:orange', linewidth=0.8, label='Annual % Change')
ax2.set_ylabel('Annual Percentage Change (%)')

# Add legends.
ax1.legend(loc='upper left')
ax2.legend(loc='lower right')

# Save the plot as a PNG image.
plt.savefig('cpi_graph.png')

# ==============================================================================
# PART 3: Setting up functions to be called upon later in the program when the user is prompted for input
# ==============================================================================

# Function to get a valid price input from the user.
def get_price():
    # Loop until the user provides a valid price input (greater than zero and a valid number).
    while True:
        # Prompt the user for a price input, removing any dollar signs or commas, and stripping whitespace.
        user_price = input("Enter the price of goods/services ($): ").replace('$', '').replace(',', '').strip()

        # isdigit cannot read decimal points so the decimal point is removed for the check. If there is more than one decimal point, the input is invalid.
        # The digits are then converted to a float and checked to ensure they are greater than zero. If valid, the float value is returned, otherwise, an error message is displayed and the loop continues.
        if user_price.replace('.', '', 1).isdigit() and float(user_price) > 0:
            return float(user_price)
        else:
            print("Invalid input. Please enter a positive dollar amount (e.g., 100 or 100.00).")

# Function to get a valid date input from the user in the format YYYY-MM.
def get_date(prompt):
    # Loop until the user provides a valid date input in the format YYYY-MM.
    while True:
        user_date = input(prompt).strip()
        date_parts = user_date.split('-')

        # If the number of date_parts is equal to 2 and both parts are digits, the year and month are extracted as integers.
        if len(date_parts) == 2 and date_parts[0].isdigit() and date_parts[1].isdigit():
            year = int(date_parts[0])
            month = int(date_parts[1])

            # If the user input is valid but doesn't exist in the dataset, an error message is displayed indicating the range of available dates in the dataset.
            if get_cpi(year, month) is not None:
                return user_date
            # Shows the user the first and last available dates in the dataset if the input date is out of range.
            else:
                first_available = data_frame['Date'].iloc[0]
                last_available = data_frame['Date'].iloc[-1]
                print("Date out of range. Dataset covers {} to {}.".format(first_available, last_available))
        else:
            print("Invalid format. Please enter the date as YYYY-MM (e.g., 2002-05).")

# Function to get the CPI using the year and month extracted from the get_date function. If the year and month do not exist in our dataset, None is returned.
def get_cpi(year, month):
    # Filter the data frame to find the row that matches the provided year and month. This is done by first filtering for the year, and then filtering that result for the month.
    matching_year = data_frame[data_frame['Year'] == year]
    matching_row = matching_year[matching_year['Month'] == month]

    # If the length of the matching row is greater than zero, it means we found a match.
    if len(matching_row) > 0:
        # After finding and confirming the match, we return the CPI value from that row using iloc[0] to get the first row of the filtered data frame.
        return matching_row['CPI'].iloc[0]
    else:
        return None

# ==================================================================================
# PART 4: User interface and running the inflation calculator using the functions defined above
# ==================================================================================

# Print a header for the inflation calculator.
print(60 * '-')
print("BANK OF CANADA MONTHLY INFLATION CALCULATOR")
print(60 * '-')

# Only once the user has provided valid inputs for the price and dates, we can proceed with the calculations.
cost_1 = get_price()
date_1 = get_date("Enter the first period (YYYY-MM): ")
date_2 = get_date("Enter the second period (YYYY-MM): ")

# Extract year and month as integers from each validated date string.
year_1 = int(date_1.split('-')[0])
month_1 = int(date_1.split('-')[1])
year_2 = int(date_2.split('-')[0])
month_2 = int(date_2.split('-')[1])

# Look up the CPI for each period.
cpi_1 = get_cpi(year_1, month_1)
cpi_2 = get_cpi(year_2, month_2)

# Inflation calculations.
cost_2 = cost_1 * (cpi_2 / cpi_1)
pct_change = ((cost_2 - cost_1) / cost_1) * 100

# Difference in years and months between the two periods, calculated using the year and month values extracted from the date strings.
total_months = (year_2 - year_1) * 12 + (month_2 - month_1)
difference_in_years = total_months / 12.0

# If the differnece in years is zero like the user inputting the same date for both periods, the annual rate of inflation is set to zero to avoid division by zero errors.
if difference_in_years == 0:
    annual_rate = 0.0
else:
    # Use np.power() from NumPy to calculate the compound annual rate of change.
    annual_rate = (np.power(cpi_2 / cpi_1, 1.0 / difference_in_years) - 1.0) * 100

# Print formatted results (rounded to nearest penny, with $ and CAD currency symbol, and commas for thousands).
print(60 * '-')
print("A basket of goods and services that cost ${:,.2f} CAD in {}".format(cost_1, date_1))
print("would cost ${:,.2f} CAD in {}.".format(cost_2, date_2))
print(60 * '-')
print("Percent change:                    {:.2f}%".format(pct_change))
print("Difference in number of years:     {:.2f} years ({} months)".format(difference_in_years, total_months))
print("Average annual rate of inflation:  {:.2f}%".format(annual_rate))
print("CPI for first period ({}):    {:.1f}".format(date_1, cpi_1))
print("CPI for second period ({}):   {:.1f}".format(date_2, cpi_2))
print("Base Level:                        2002 CPI = 100.0")
print(60 * '-')
plt.show()