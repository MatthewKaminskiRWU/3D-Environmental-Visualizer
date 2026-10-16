# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 18:10:09 2026

@author: Matthew
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D





# Load the CSV file
# "df" means DataFrame. So it is making a table stored in the variable.
# "pd" is short for panda.read. So ti is just using Panda to read the CSV.
df = pd.read_csv("clean_noaa_data.csv")



# Finds the smallest and largest longitude in the data
lon_min = df['Longitude'].min()
lon_max = df['Longitude'].max()

# Finds the smallest and largest latitude in the data
lat_min = df['Latitude'].min()
lat_max = df['Latitude'].max()

# Finds the smallest and largest depth in the data
depth_min = df['Depth'].min()
depth_max = df['Depth'].max()



# ==========================================
# 1. TEMPERATURE FIGURE
# ==========================================

# Creates the 3D figure for Temperature
# Create figure with constrained layout (automatically handles margins)
fig1 = plt.figure(figsize=(10, 7), layout='constrained')
# Ax means Axes. 
ax = fig1.add_subplot(111, projection='3d')

# Save the scatter plot into a variable named 'scatter1' so the key can read it
# "Scatter" just means to put a point at those coordinates
# X goes left to right, Y goes backwards and forwards, Z goes up and down
# In 3D Matplotlib, dots have an artificial depth shadow by default that makes them look faded/translucent. depthshade=False removes this.
# s=8 determines the size of the dots
# alpha makes it semi-transparent
scatter1 = ax.scatter(df['Longitude'], df['Latitude'], df['Depth'], c=df['Temperature'], cmap='coolwarm', depthshade=False, s=8, alpha=0.4)

# Title and Axis Labels
# Labels with extra padding so text never touches the numbers
ax.set_title("Ocean Temperature Profile", pad=20, fontsize=14, fontweight='bold')
ax.set_xlabel("Longitude", labelpad=14)
ax.set_ylabel("Latitude", labelpad=14)
ax.set_zlabel("Depth (m)", labelpad=14)

# Set the 3D box limits automatically based on the CSV values
# Dynamic boundaries with 5% breathing room
lon_buffer = (df['Longitude'].max() - df['Longitude'].min()) * 0.05
lat_buffer = (df['Latitude'].max() - df['Latitude'].min()) * 0.05
depth_buffer = abs(df['Depth'].min()) * 0.05

# Sets the boundaries of the 3D box using an equation. Empty space will always be 5% extra.
ax.set_xlim(df['Longitude'].min() - lon_buffer, df['Longitude'].max() + lon_buffer)
ax.set_ylim(df['Latitude'].min() - lat_buffer,   df['Latitude'].max() + lat_buffer)
# For depth: deepest value (most negative) is bottom, surface (0) is top
ax.set_zlim(df['Depth'].min() - depth_buffer,    0)

# The Key (Colorbar)
# pad=0.12 pushes it far enough away from the Depth axis
cbar = fig1.colorbar(scatter1, ax=ax, shrink=0.6, pad=0.12)
cbar.set_label("Temperature (°C)", labelpad=10)





# ==========================================
# 1. 3D TEMPERATURE FIGURE
# ==========================================

import trimesh

# 1. Load the cleaned data
df = pd.read_csv("clean_noaa_data.csv")

# 2. Handle Vertical Exaggeration
# Convert depth to a visible scale relative to Lat/Lon degrees
depth_scale = 0.03  # Adjust this so depth doesn't look too flat or too deep
scaled_depth = df['Depth'] * depth_scale

# 3. Map Temperatures to Colors (RGB)
# Uses the exact same 'coolwarm' colormap from Matplotlib
cmap = plt.get_cmap('coolwarm')
temp_norm = (df['Temperature'] - df['Temperature'].min()) / (df['Temperature'].max() - df['Temperature'].min())
colors = cmap(temp_norm)[:, :3]  # Extract Red, Green, Blue (0.0 to 1.0)
colors_uint8 = (colors * 255).astype(np.uint8)  # Convert to standard 0-255 colors

# 4. Build the 3D Scene
scene = trimesh.Scene()

# Create a base low-poly sphere template
template_sphere = trimesh.creation.icosphere(subdivisions=1, radius=0.4)

print("Generating 3D meshes...")

# Loop through points and add them to the 3D scene
# (We combine them for high performance)
meshes = []
for (lon, lat, d), color in zip(zip(df['Longitude'], df['Latitude'], scaled_depth), colors_uint8):
    # Clone template sphere
    sphere = template_sphere.copy()
    
    # Move it to the (X=Lon, Y=Lat, Z=Depth) coordinate
    sphere.apply_translation([lon, lat, d])
    
    # Apply the temperature color
    sphere.visual.vertex_colors = color
    meshes.append(sphere)

# Combine all spheres into one single optimized 3D object
combined_mesh = trimesh.util.concatenate(meshes)
scene.add_geometry(combined_mesh)

# 5. Export to .GLB
output_filename = "ocean_temperature.glb"
scene.export(output_filename)

print(f"Success! Exported 3D model to {output_filename}")