import pandas as pd
def write_to_excel(input,m):

    # Your data: list of rows
    data = input

    # Create DataFrame with column names
    df = pd.DataFrame(data, columns=['m', 'length', 'acr', 'balance', 'Unique Count', 'D_U_C'])

    # Write DataFrame to Excel file
    df.to_excel(f'output_m{m}.xlsx', index=False)
