import pandas as pd
import matplotlib.pyplot as plt

# Load tracking data
df = pd.read_csv("tracking_data.csv")

# Select only players
players = df[df["Object"] == "person"]

# Create heatmap
plt.figure(figsize=(10, 6))

plt.hist2d(
    players["X"],
    players["Y"],
    bins=30
)

plt.colorbar(label="Player Activity")

plt.title("Player Movement Heatmap")
plt.xlabel("X Position")
plt.ylabel("Y Position")

# Match video coordinate system
plt.gca().invert_yaxis()

plt.show()