import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Football AI Sports Analytics",
    page_icon="⚽",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
}

.subtitle {
    font-size: 18px;
    color: #666;
}

.metric-card {
    padding: 15px;
    border-radius: 12px;
    background-color: #f5f7fa;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

CSV_FILE = "tracking_data.csv"
VIDEO_FILE = "football.mp4"

if not os.path.exists(CSV_FILE):

    st.error("tracking_data.csv not found!")

    st.stop()

df = pd.read_csv(CSV_FILE)

# Remove empty rows
df = df.dropna(subset=["Frame", "Object_ID", "Object", "X", "Y"])

# Convert columns
df["Frame"] = pd.to_numeric(df["Frame"], errors="coerce")
df["Object_ID"] = pd.to_numeric(df["Object_ID"], errors="coerce")
df["X"] = pd.to_numeric(df["X"], errors="coerce")
df["Y"] = pd.to_numeric(df["Y"], errors="coerce")

df = df.dropna()

# =========================================================
# OBJECT TYPES
# =========================================================

players = df[
    df["Object"].str.lower().isin(
        ["person", "player"]
    )
].copy()

balls = df[
    df["Object"].str.lower().isin(
        ["sports ball", "ball"]
    )
].copy()

# =========================================================
# PLAYER MOVEMENT CALCULATION
# =========================================================

player_results = []

for player_id, data in players.groupby("Object_ID"):

    data = data.sort_values("Frame").copy()

    dx = data["X"].diff()
    dy = data["Y"].diff()

    distance = np.sqrt(dx**2 + dy**2)

    total_distance = distance.sum()

    avg_speed = distance.mean()

    max_speed = distance.max()

    player_results.append({
        "Player ID": int(player_id),
        "Total Distance": total_distance,
        "Average Speed": avg_speed,
        "Maximum Speed": max_speed,
        "Tracking Points": len(data)
    })

player_stats = pd.DataFrame(player_results)

# =========================================================
# BALL MOVEMENT
# =========================================================

ball_results = []

for ball_id, data in balls.groupby("Object_ID"):

    data = data.sort_values("Frame").copy()

    dx = data["X"].diff()
    dy = data["Y"].diff()

    distance = np.sqrt(dx**2 + dy**2)

    ball_results.append({
        "Ball ID": int(ball_id),
        "Total Distance": distance.sum(),
        "Average Speed": distance.mean(),
        "Maximum Speed": distance.max(),
        "Tracking Points": len(data)
    })

ball_stats = pd.DataFrame(ball_results)

# =========================================================
# MAIN BALL
# =========================================================

if len(ball_stats) > 0:

    main_ball_id = int(
        ball_stats.loc[
            ball_stats["Total Distance"].idxmax(),
            "Ball ID"
        ]
    )

    main_ball_distance = ball_stats[
        ball_stats["Ball ID"] == main_ball_id
    ]["Total Distance"].iloc[0]

else:

    main_ball_id = None
    main_ball_distance = 0

# =========================================================
# MOST ACTIVE PLAYER
# =========================================================

if len(player_stats) > 0:

    most_active_player = int(
        player_stats.loc[
            player_stats["Total Distance"].idxmax(),
            "Player ID"
        ]
    )

    max_player_distance = player_stats[
        player_stats["Player ID"] == most_active_player
    ]["Total Distance"].iloc[0]

else:

    most_active_player = "N/A"
    max_player_distance = 0

# =========================================================
# FASTEST PLAYER
# =========================================================

if len(player_stats) > 0:

    fastest_player = int(
        player_stats.loc[
            player_stats["Average Speed"].idxmax(),
            "Player ID"
        ]
    )

    fastest_speed = player_stats[
        player_stats["Player ID"] == fastest_player
    ]["Average Speed"].iloc[0]

else:

    fastest_player = "N/A"
    fastest_speed = 0

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">⚽ Football AI Sports Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'YOLO-based player & ball detection, tracking and performance analysis'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚙️ Dashboard Controls")

st.sidebar.info(
    "Select a player to view individual performance."
)

if len(player_stats) > 0:

    player_ids = sorted(
        player_stats["Player ID"].tolist()
    )

    selected_player = st.sidebar.selectbox(
        "👤 Select Player",
        player_ids
    )

else:

    selected_player = None

# =========================================================
# MATCH OVERVIEW
# =========================================================

st.header("📊 Match Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "👤 Players Tracked",
        len(player_stats)
    )

with col2:
    st.metric(
        "⚽ Ball Tracks",
        len(ball_stats)
    )

with col3:
    st.metric(
        "🏃 Most Active",
        f"Player {most_active_player}"
    )

with col4:
    st.metric(
        "⚡ Fastest Player",
        f"Player {fastest_player}"
    )

with col5:
    st.metric(
        "⚽ Main Ball Distance",
        f"{main_ball_distance:.0f} px"
    )

st.divider()

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🎥 Match",
        "👤 Player Analytics",
        "⚽ Ball Analytics",
        "🔥 Heatmap",
        "📊 Rankings"
    ]
)

# =========================================================
# TAB 1 - VIDEO
# =========================================================

with tab1:

    st.header("🎥 Match Video")

    if os.path.exists(VIDEO_FILE):

        st.video(VIDEO_FILE)

    else:

        st.warning(
            "football.mp4 not found in project folder."
        )

    st.subheader("📋 Tracking Information")

    st.dataframe(
        df.head(100),
        use_container_width=True
    )

# =========================================================
# TAB 2 - PLAYER ANALYTICS
# =========================================================

with tab2:

    st.header(
        f"👤 Player {selected_player} Performance"
    )

    selected_data = players[
        players["Object_ID"] == selected_player
    ].copy()

    selected_data = selected_data.sort_values(
        "Frame"
    )

    # ---------------------------------------------
    # Calculate movement
    # ---------------------------------------------

    selected_data["dx"] = selected_data["X"].diff()
    selected_data["dy"] = selected_data["Y"].diff()

    selected_data["Speed"] = np.sqrt(
        selected_data["dx"]**2 +
        selected_data["dy"]**2
    )

    total_distance = selected_data[
        "Speed"
    ].sum()

    average_speed = selected_data[
        "Speed"
    ].mean()

    maximum_speed = selected_data[
        "Speed"
    ].max()

    tracking_points = len(selected_data)

    # ---------------------------------------------
    # Performance Level
    # ---------------------------------------------

    if average_speed >= 100:
        performance = "🔥 Very High"

    elif average_speed >= 60:
        performance = "🟢 High"

    elif average_speed >= 30:
        performance = "🟡 Medium"

    else:
        performance = "🔵 Low"

    # ---------------------------------------------
    # Metrics
    # ---------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🏃 Total Distance",
        f"{total_distance:.2f} px"
    )

    c2.metric(
        "⚡ Average Speed",
        f"{average_speed:.2f} px/frame"
    )

    c3.metric(
        "🚀 Maximum Speed",
        f"{maximum_speed:.2f} px/frame"
    )

    c4.metric(
        "📊 Performance",
        performance
    )

    st.divider()

    # ---------------------------------------------
    # Movement Path
    # ---------------------------------------------

    st.subheader("🗺️ Player Movement Path")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=selected_data["X"],
            y=selected_data["Y"],
            mode="lines+markers",
            name=f"Player {selected_player}",
            text=[
                f"Frame: {f}"
                for f in selected_data["Frame"]
            ],
            hovertemplate=
            "%{text}<br>" +
            "X: %{x}<br>" +
            "Y: %{y}<extra></extra>"
        )
    )

    fig.update_layout(
        title=f"Movement Path - Player {selected_player}",
        xaxis_title="X Position",
        yaxis_title="Y Position",
        height=500
    )

    fig.update_yaxes(
        autorange="reversed"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------------------------
    # Speed Trend
    # ---------------------------------------------

    st.subheader("⚡ Speed Over Time")

    speed_fig = px.line(
        selected_data,
        x="Frame",
        y="Speed",
        title=f"Speed Trend - Player {selected_player}",
        markers=True
    )

    speed_fig.update_layout(
        xaxis_title="Frame",
        yaxis_title="Speed (pixels/frame)"
    )

    st.plotly_chart(
        speed_fig,
        use_container_width=True
    )

    # ---------------------------------------------
    # Tracking Data
    # ---------------------------------------------

    st.subheader("📋 Player Tracking Data")

    st.dataframe(
        selected_data[
            [
                "Frame",
                "Object_ID",
                "Object",
                "X",
                "Y",
                "Speed"
            ]
        ],
        use_container_width=True
    )

# =========================================================
# TAB 3 - BALL ANALYTICS
# =========================================================

with tab3:

    st.header("⚽ Ball Analytics")

    if len(ball_stats) == 0:

        st.warning(
            "No ball tracking data available."
        )

    else:

        b1, b2, b3 = st.columns(3)

        b1.metric(
            "⚽ Main Ball ID",
            main_ball_id
        )

        b2.metric(
            "📏 Ball Distance",
            f"{main_ball_distance:.2f} px"
        )

        main_ball = balls[
            balls["Object_ID"] == main_ball_id
        ].copy()

        main_ball = main_ball.sort_values(
            "Frame"
        )

        main_ball["dx"] = main_ball["X"].diff()
        main_ball["dy"] = main_ball["Y"].diff()

        main_ball["Speed"] = np.sqrt(
            main_ball["dx"]**2 +
            main_ball["dy"]**2
        )

        ball_avg_speed = main_ball[
            "Speed"
        ].mean()

        b3.metric(
            "⚡ Average Ball Speed",
            f"{ball_avg_speed:.2f} px/frame"
        )

        st.divider()

        # -----------------------------------------
        # Ball Trajectory
        # -----------------------------------------

        st.subheader("🗺️ Ball Trajectory")

        trajectory_fig = go.Figure()

        trajectory_fig.add_trace(
            go.Scatter(
                x=main_ball["X"],
                y=main_ball["Y"],
                mode="lines+markers",
                name="Ball",
                hovertemplate=
                "Frame: %{text}<br>" +
                "X: %{x}<br>" +
                "Y: %{y}<extra></extra>",
                text=main_ball["Frame"]
            )
        )

        trajectory_fig.update_layout(
            title=f"Main Ball Trajectory - ID {main_ball_id}",
            xaxis_title="X Position",
            yaxis_title="Y Position",
            height=550
        )

        trajectory_fig.update_yaxes(
            autorange="reversed"
        )

        st.plotly_chart(
            trajectory_fig,
            use_container_width=True
        )

        # -----------------------------------------
        # Ball Speed
        # -----------------------------------------

        st.subheader("⚡ Ball Speed Analysis")

        ball_speed_fig = px.line(
            main_ball,
            x="Frame",
            y="Speed",
            title="Ball Speed Over Time",
            markers=True
        )

        ball_speed_fig.update_layout(
            xaxis_title="Frame",
            yaxis_title="Speed (pixels/frame)"
        )

        st.plotly_chart(
            ball_speed_fig,
            use_container_width=True
        )

        # -----------------------------------------
        # Ball Table
        # -----------------------------------------

        st.subheader("📋 Ball Tracking Data")

        st.dataframe(
            main_ball[
                [
                    "Frame",
                    "Object_ID",
                    "Object",
                    "X",
                    "Y",
                    "Speed"
                ]
            ],
            use_container_width=True
        )

# =========================================================
# TAB 4 - HEATMAP
# =========================================================

with tab4:

    st.header("🔥 Player Movement Heatmap")

    if len(players) == 0:

        st.warning("No player data available.")

    else:

        heatmap = px.density_heatmap(
            players,
            x="X",
            y="Y",
            nbinsx=40,
            nbinsy=30,
            title="Player Activity Heatmap"
        )

        heatmap.update_yaxes(
            autorange="reversed"
        )

        heatmap.update_layout(
            height=600,
            xaxis_title="X Position",
            yaxis_title="Y Position"
        )

        st.plotly_chart(
            heatmap,
            use_container_width=True
        )

        st.info(
            "Brighter areas represent locations where "
            "players were detected more frequently."
        )

# =========================================================
# TAB 5 - RANKINGS
# =========================================================

with tab5:

    st.header("🏆 Player Rankings")

    # ---------------------------------------------
    # Movement Ranking
    # ---------------------------------------------

    st.subheader("🏃 Top 10 Players by Movement")

    top_movement = player_stats.sort_values(
        "Total Distance",
        ascending=False
    ).head(10)

    movement_fig = px.bar(
        top_movement,
        x="Player ID",
        y="Total Distance",
        title="Top 10 Players by Total Movement",
        text_auto=".0f"
    )

    movement_fig.update_layout(
        xaxis_title="Player ID",
        yaxis_title="Distance (pixels)"
    )

    st.plotly_chart(
        movement_fig,
        use_container_width=True
    )

    # ---------------------------------------------
    # Speed Ranking
    # ---------------------------------------------

    st.subheader("⚡ Top 10 Players by Speed")

    top_speed = player_stats.sort_values(
        "Average Speed",
        ascending=False
    ).head(10)

    speed_rank_fig = px.bar(
        top_speed,
        x="Player ID",
        y="Average Speed",
        title="Top 10 Players by Average Speed",
        text_auto=".2f"
    )

    speed_rank_fig.update_layout(
        xaxis_title="Player ID",
        yaxis_title="Average Speed (pixels/frame)"
    )

    st.plotly_chart(
        speed_rank_fig,
        use_container_width=True
    )

    # ---------------------------------------------
    # Ranking Table
    # ---------------------------------------------

    st.subheader("📊 Complete Player Ranking")

    ranking_table = player_stats.sort_values(
        "Total Distance",
        ascending=False
    ).reset_index(drop=True)

    ranking_table.index = ranking_table.index + 1

    st.dataframe(
        ranking_table,
        use_container_width=True
    )

# =========================================================
# DOWNLOAD DATA
# =========================================================

st.divider()

st.header("📥 Export Analytics")

csv_data = player_stats.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Player Analytics CSV",
    data=csv_data,
    file_name="player_analytics.csv",
    mime="text/csv"
)

st.success(
    "Football AI Analytics Dashboard loaded successfully! ⚽🤖"
)