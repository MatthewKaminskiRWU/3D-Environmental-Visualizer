
#Quick code to clean the noaa data

import pandas as pd
import os
import pathlib as path
import csv

start = input("Is base path set? (Y/N) ")


#window method
def Windows (t,x,y,z):
    f = t
    base = rf"C:\Users\{x}\{y}\{z}"
    full = path.Path(base) / f
    return full,base

def linux (t,x,y,z):
    f = t
    basef = f"/Users/{x}/{y}/{z}"
    base = f"/Users/{user}/{main}"
    full = path.Path(basef) / file
    return full


if start == "N":
    os = int(input("Opertating system is 1: Windows or 2: Linux "))
    if os == 1:
        file = input("enter file name: ")
        user= input("enter user: ")
        main = input("Main folder: ")
        folder = input("sub folder: ")
        data,grab = Windows(file, user, main,folder)
        with open("base.txt", "w") as file:
            file.write(f"{grab}\n")
    else: 
        file = input("enter file name")
        user= input("enter user")
        main = input("Main folder")
        folder = input("sub folder")
        data = linux(file, user, main,folder)
else:
    file = input("enter file name: ")
    with open ("base.txt", "r")as f:
        grab= f.readline().strip()
    base= path.Path(grab)
    data = path.Path(base) / file


# cleaning 
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

df.to_csv('data.csv', index=False)





