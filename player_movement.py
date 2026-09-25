import pandas as pd
import math

# Load tracking data
df = pd.read_csv("tracking_data.csv")

# Sirf players/persons ka data
players = df[df["Object"] == "person"]

# Store total distance of each player
player_distance = {}

# Process each player ID separately
for player_id, data in players.groupby("Object_ID"):

    # Sort by frame number
    data = data.sort_values("Frame")

    total_distance = 0

    # Previous position
    previous_x = None
    previous_y = None

    # Check every position
    for _, row in data.iterrows():

        current_x = row["X"]
        current_y = row["Y"]

        # Calculate movement from previous position
        if previous_x is not None:

            dx = current_x - previous_x
            dy = current_y - previous_y

            distance = math.sqrt(dx**2 + dy**2)

            total_distance += distance

        previous_x = current_x
        previous_y = current_y

    player_distance[player_id] = total_distance


# Display results
print("\nPLAYER MOVEMENT ANALYSIS")
print("-------------------------")

for player_id, distance in player_distance.items():

    print(
        "Player ID:",
        player_id,
        "| Distance:",
        round(distance, 2),
        "pixels"
    )


# Find player with highest movement
if player_distance:

    most_active_player = max(
        player_distance,
        key=player_distance.get
    )

    print("\nMost Active Player:")
    print("Player ID:", most_active_player)
    print(
        "Distance:",
        round(player_distance[most_active_player], 2),
        "pixels"
    )