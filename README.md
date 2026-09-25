# ⚽ Football Sports Analytics — YOLO Player & Ball Tracking

An end-to-end computer vision and sports analytics project that detects and tracks football players and the ball from video, performs movement and speed analysis, and presents the results through an interactive Streamlit dashboard.

## 🚀 Live Demo

**Streamlit Dashboard:**
https://football-sports-analytics-7cxykwvuckxrvq2td76bbv.streamlit.app/

## 📌 Project Overview

This project uses **YOLO-based object detection and tracking** to analyze football video data.

The system detects players and the football, assigns object IDs, stores tracking coordinates, and performs different analytics such as:

* Player movement analysis
* Player speed analysis
* Ball movement analysis
* Ball speed analysis
* Ball trajectory
* Player heatmap
* Object distribution
* Interactive dashboard

## 🎯 Objectives

* Detect football players and the ball from video.
* Track detected objects across video frames.
* Store tracking information in CSV format.
* Calculate player movement and speed.
* Analyze football movement and trajectory.
* Visualize player activity using heatmaps and charts.
* Provide an interactive dashboard for sports analysis.

## 🛠️ Technologies Used

* **Python**
* **YOLO / Ultralytics**
* **OpenCV**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **Plotly**
* **Streamlit**

## 🔄 Project Workflow

```text
Football Video
      ↓
YOLO Object Detection
      ↓
Object Tracking
      ↓
Player & Ball IDs
      ↓
Tracking Coordinates
      ↓
tracking_data.csv
      ↓
Movement & Speed Analysis
      ↓
Heatmap / Trajectory / Charts
      ↓
Interactive Streamlit Dashboard
```

## ✨ Key Features

### 1. Object Detection

YOLO is used to detect objects such as:

* Players
* Football
* Other detected objects

### 2. Player Tracking

Each detected player is assigned an **Object ID**.

The tracking data contains:

```text
Frame
Object_ID
Object
X
Y
```

This allows the movement of individual players to be analyzed across frames.

### 3. Player Movement Analysis

The project calculates the distance travelled by tracked players using their movement coordinates.

The analysis can identify players with higher tracked movement during the video.

### 4. Player Speed Analysis

Player movement between frames is used to calculate an estimated speed in **pixels per frame**.

This is a video-coordinate-based measurement and is not directly equivalent to real-world km/h.

### 5. Player Heatmap

A heatmap is generated using player positions to visualize areas of the field/video where players were detected more frequently.

### 6. Ball Movement Analysis

The football's tracked coordinates are analyzed to calculate its movement distance.

### 7. Ball Speed Analysis

The movement of the tracked football across frames is used to estimate its speed in pixel coordinates.

### 8. Ball Trajectory

The project generates a trajectory visualization showing the movement path of the tracked football.

### 9. Interactive Streamlit Dashboard

The dashboard provides an interactive interface for exploring the analytics.

It includes:

* KPI information
* Player selection
* Movement charts
* Speed charts
* Player heatmap
* Ball trajectory
* Ball speed
* Object distribution
* Tracking data table

## 📊 Sample Results

Some results obtained during analysis:

| Analysis                   |              Result |
| -------------------------- | ------------------: |
| Most active tracked player |        Player ID 21 |
| Player 21 tracked movement |      9190.85 pixels |
| Main tracked ball          |         Ball ID 197 |
| Ball movement              |      5764.08 pixels |
| Fastest tracked player     |       Player ID 224 |
| Player 224 average speed   | 208.46 pixels/frame |

> Note: These values are based on image/video pixel coordinates and should not be interpreted as real-world distances or speeds without camera calibration.

## 📂 Project Structure

```text
football-sports-analytics/
│
├── dashboard.py
├── detection.py
├── tracking.py
├── tracking_data.py
├── tracking_data.csv
│
├── player_movement.py
├── player_movement_chart.py
├── player_heatmap.py
├── player_speed.py
│
├── ball_movement.py
├── ball_speed.py
├── ball_trajectory.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/vedikagole/football-sports-analytics.git
```

Go inside the project folder:

```bash
cd football-sports-analytics
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Dashboard

Run:

```bash
streamlit run dashboard.py
```

The dashboard will open in the browser.

## 📁 Input Data

The project uses football video data for object detection and tracking.

Large model/video files such as:

```text
football.mp4
yolov8n.pt
```

are excluded from the GitHub repository using `.gitignore`.

## ⚠️ Limitations

* Speed is calculated using pixel coordinates.
* Real-world distance requires camera calibration.
* YOLO may occasionally produce incorrect detections.
* Ball tracking can be difficult when the ball is occluded or moves quickly.
* Tracking accuracy can be affected by crowded scenes and overlapping players.

## 🔮 Future Scope

Possible future improvements include:

* Real-world speed calculation using camera calibration.
* Player team classification based on jersey color.
* Automatic player performance reports.
* Pass detection.
* Shot detection.
* Goal detection.
* Formation analysis.
* Possession analysis.
* Advanced sports performance metrics.
* Real-time football analytics.

## 👩‍💻 Project Purpose

This project demonstrates how **Computer Vision, Object Detection, Object Tracking, Data Analysis and Web Visualization** can be combined to build a practical sports analytics system.

## 📌 Conclusion

The project converts football video into structured tracking data and uses that data to generate meaningful player and ball analytics.

The final system combines:

**YOLO Detection → Object Tracking → Data Processing → Sports Analytics → Interactive Dashboard**
