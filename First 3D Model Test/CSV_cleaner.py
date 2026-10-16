# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 21:39:35 2026

@author: Matthew
"""

import pandas as pd

# 1. Read NOAA file (skip the first comment line)
raw_file = "t13mn01.csv"
df = pd.read_csv(raw_file, skiprows=1)

# 2. Fix the messy NOAA column names
# Strip whitespace and rename the first 3 columns properly
df.columns = [c.strip() for c in df.columns]

# Renamed the first three columns to clean names
cols = list(df.columns)
cols[0] = 'Latitude'
cols[1] = 'Longitude'
cols[2] = '0'   # Replaces "AND VALUES AT DEPTHS (M):0" with just "0"
df.columns = cols

# 3. Reshape from Wide -> Tall
df_clean = pd.melt(
    df, 
    id_vars=['Latitude', 'Longitude'], 
    var_name='Depth', 
    value_name='Temperature'
)

# 4. Clean up missing values and convert to numbers
df_clean = df_clean.dropna(subset=['Temperature'])

# Now "0" will convert properly without crashing!
df_clean['Depth'] = -pd.to_numeric(df_clean['Depth'])
df_clean['Temperature'] = pd.to_numeric(df_clean['Temperature'])

# 5. Save the ready-to-plot file!
df_clean.to_csv("clean_noaa_data.csv", index=False)
print("Done! Cleaned file saved as clean_noaa_data.csv")