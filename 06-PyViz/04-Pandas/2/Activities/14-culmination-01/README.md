# Bank of America Stock Data

In this exercise you'll be learning to use the pandas module.

## Instructions

1. Import the `pandas` library

2. Create a variable `bac_path` that represents the path to the [BAC.csv](Resources/BAC.csv) using the Pathlib library.

3. Read the CSV into a Pandas DataFrame.

4. Count the number of rows in the DataFrame.

5. Calculate the minimum and maximum dates.

6. Set the `Date` column as the index.

7. Filter the DataFrame to a six month date range selection between `2017-01-03` to `2017-06-03`.

8. Drop the extra columns: 'Open', 'High', 'Low', 'Close', 'Volume'.

9. Use the `pct_change` function to calculate the daily returns over the six month date range of closing BAC prices.

10. Plot the Daily Returns for 6 Months of BAC Stock.

---

© 2019 Trilogy Education Services, a 2U, Inc. brand. All Rights Reserved.
