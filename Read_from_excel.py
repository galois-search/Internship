import pandas as pd

df = pd.read_excel(r'10_op/m10_sorted_unique_results.xlsx', usecols=['period', 'acr_max','balance'])
print(df.head(15))