# 🌍 LandCalc: Analysing Land Cover Statistics 🌍


[![image](https://img.shields.io/pypi/v/landcalc.svg)](https://pypi.python.org/pypi/landcalc)


Welcome to **LandCalc**, a Python package for creating interactive maps and performing land cover analysis with ease. It provides both simple map visualization tools and a powerful user interface (`landcalc.ui`) for analyzing land cover distributions and changes over time.

## Key Features
- 🗺️ Create interactive maps using built-in base layers
- 📐 Select your region of interest (ROI) by:
  - Drawing on the map
  - Uploading a shapefile or custom geometry
- 🌱 Analyze land cover within your selected geometry:
  - Calculate **percent** and **total area (m²)** of each land cover type
  - Generate an **interactive chart** of land cover composition
  - **Export results** as a CSV file
- 📊 Perform **change detection** between two years (if supported by the dataset):
  - Visualize land cover changes over time
  - Quantify increase or decrease in land cover categories

## 🧰 Getting Started 🛠️
```python
import landcalc
from landcalc import Map
from landcalc.ui import build_gui

# Initialize Your Map
m = Map(center=(37.5, -95), zoom=4)

# Launch Land Cover Tool
gui_map = build_gui(m)
gui_map
```

## How to Use
1. Select land cover dataset from the dropdown menu
2. Select available year from dropdown menu
3. Click 'Add Layer to Map' button
4. Upload a shapefile/ geometry or draw your own directly on the map using the draw tool
5. Click the 'Calculate' button to visualize the statistics
6. Click 'Show Chart' to create a chart of the statistics
7. Export the statistics using the 'Export as CSV' button

## Upcoming Tools & Releases
* 🌴 Island Calc Tool 🌊
* 🌳 Tree Calc Tool 🪵

### Additional Information
-   Free software: MIT License
-   Documentation: <https://acpotgieter.github.io/landcalc>
