# TrackAlpaca: A Metric Tracking and Visualization Tool

## Overview

`TrackAlpaca` is a simple and efficient class for logging, saving, loading, and visualizing metrics over multiple epochs. It is perfect for tracking machine learning metrics such as loss and accuracy during training. The class supports saving metrics to a JSON file, loading them for analysis, and graphing them as images for visualization.

## Features

- **Log Metrics**: Log multiple metrics (e.g., loss, accuracy) for each training epoch.
- **Save Metrics**: Persist logged metrics to a JSON file for future analysis.
- **Load Metrics**: Load previously saved metrics from a JSON file.
- **Graph Metrics**: Generate graphs visualizing the metrics over epochs and save them as image files.

## Requirements

- Python 3.9 (tested with 3.12.7)
- `matplotlib` for graphing.
- `PIL` (Pillow) for handling image data.

## Installation

You can install `TrackAlpaca` directly from PyPI by running:

```bash
pip install TrackAlpaca
