# Hands Landmark Variability Detection

A Python tool for testing the variability of MediaPipe hand landmark detection by running the same video through multiple iterations and analyzing the consistency of detected landmarks.

## Overview

This tool addresses the important question of how consistent MediaPipe's hand landmark detection is across multiple runs of the same video. It processes a video multiple times and calculates statistical measures of variability for each landmark point, helping you understand the reliability and precision of the landmark detection system.

## Features

- **Multi-iteration Analysis**: Runs the same video through MediaPipe hands detection multiple times
- **Statistical Variability Metrics**: Calculates mean, standard deviation, min/max for landmark position consistency
- **Coordinate-wise Analysis**: Separate variability analysis for X, Y, and Z coordinates
- **Detection Rate Analysis**: Tracks how consistently hands are detected across iterations
- **Comprehensive Reporting**: Outputs detailed JSON reports with all raw data and statistical summaries
- **Right-half Video Processing**: Focuses analysis on the right half of the video frame


### Basic Usage

```python
from variability_test import test_landmark_variability_hands

# Run variability test on a video
report = test_landmark_variability_hands(
    video_path="path/to/your/video.mp4",
    num_iterations=5,
    output_report_path="variability_report.json"
)
```

### Parameters

- `video_path` (str): Path to the input video file
- `num_iterations` (int, default=5): Number of times to process the video
- `output_report_path` (str, default="variability_report_hands.json"): Path for the output report



## Key Metrics Explained

### Detection Rate Statistics
- **Mean**: Average percentage of frames where hands were detected across all iterations
- **Std**: Standard deviation of detection rates (lower = more consistent)
- **Min/Max**: Range of detection rates across iterations

### Landmark Position Variability
- **Average Std**: Mean standard deviation of landmark positions across iterations
- **Max Std**: Maximum standard deviation observed for any landmark
- **Coordinate Analysis**: Separate analysis for X, Y, Z coordinates


## Limitations

- Currently processes only the landmarks of the hands


