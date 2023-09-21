import pandas as pd

# Read the input file
input_data = pd.read_excel("./88_Excel/input.xlsx", usecols="A:D", nrows=189)


# Define the columns based on the user's request
columns = [
    "Cash", "Credit Card", "Debit Card", "EBT SNAP", "Tenders In Drawer Totals", 
    "All Voids", "Item Corrects", "No Sales", "Negative Totals", 
    "125 - CHUPA SODA_6PK", "Discount Totals", "LOTTERY WINNER", "LOYALTY", 
    "Paid Out Totals", "Returns", "SCRATCHER WINNER"
]

# Initialize the output DataFrame
output_data = pd.DataFrame()

# For each unique name in the input data
for name in input_data['NAME'].unique():
    # Filter rows for the current name
    name_data = input_data[input_data['NAME'] == name]
    
    # Dictionary to hold the data for the current name
    data_dict = {"Name": name}
    
    # For each column, get the corresponding value from the input data
    for col in columns:
        data_dict[col] = name_data[name_data['DATA'] == col]['AMOUNT'].values[0] if col in name_data['DATA'].values else None
    
    # Append the data to the output DataFrame
    output_data = output_data.append(data_dict, ignore_index=True)



output_data.fillna(0, inplace=True)  # fill NaN values with 0


# Save the refactored output data to an Excel file
output_filepath = "output.xlsx"
output_data.to_excel(output_filepath, index=False)