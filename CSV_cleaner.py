
#Quick code to clean the noaa data

import pandas as pd
import os
import pathlib as path
import csv

start = input("Is base path set? (Y/N) ")


"""
file = "gins_decav_t16mn01.csv"
user= "lauri"
main = "Final"
folder = "NOAA_data"
"""

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
df = pd.read_csv(data, skiprows=1)
df = df.rename(columns={'#COMMA SEPARATED LATITUDE': 'Latitude', ' LONGITUDE': 'Longitude', ' AND VALUES AT DEPTHS (M):0' : 'Depth 0(M)'})
df = df.fillna(0.000)


df.to_csv('data.csv', index=False)





