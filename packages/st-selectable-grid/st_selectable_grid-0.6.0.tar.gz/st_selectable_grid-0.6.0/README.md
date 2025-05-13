# Streamlit Selectable Grid

A Streamlit component that displays a selectable grid of cells with support for headers, row indices, and custom styling options.

![simple ss](docs/simple_example.png)

## Installation

```bash
pip install st-selectable-grid
```

## Usage

```python
import streamlit as st
from st_selectable_grid import st_selectable_grid

# Create a grid with header and index
cells = [
    [
        {"label": "A1", "cell_color": "#f0f8ff", "tooltip": "Cell A1", "mark": True},
        {"label": "<b>A2</b>", "cell_color": "#e6e6fa", "html": True},
        {"label": "A3", "cell_color": "#f5f5dc"}
    ],
    [
        {"label": "B1", "cell_color": "#f0ffff"},
        {"label": "<span style='color:red'>B2</span>", "cell_color": "#f5f5f5", "html": True},
        {"label": "B3", "cell_color": "#fffaf0"}
    ],
    [
        {"label": "C1", "cell_color": "#fff0f5"},
        {"label": "C2", "cell_color": "#f0f0f0"},
        {"label": "<i>C3</i>", "cell_color": "#fffff0", "html": True}
    ]
]

header = [
    {"label": "Column 1", "cell_color": "#e0e0e0", "mark": True},
    {"label": "Column 2", "cell_color": "#e0e0e0"},
    {"label": "Column 3", "cell_color": "#e0e0e0"}
]

index = ["Row 1", "Row 2", "Row 3"]

selection = st_selectable_grid(
    cells=cells,
    header=header,
    index=index,
    aspect_ratio=1.0,
    allow_secondary_selection=True,
    allow_header_selection=True,
    height=300,
    grid_position="center",
    resize=True,
    mark_color="#2196F3",
    primary_selection_color="#2196F3",
    secondary_selection_color="#FF9800",
    key="grid1"
)

if selection:
    if "primary" in selection:
        st.write("Primary selection (left click):", selection["primary"])
    if "secondary" in selection:
        st.write("Secondary selection (right click):", selection["secondary"])
```

## Features

- Interactive grid with selectable cells
- Support for headers and row indices
- Customizable cell colors and aspect ratio
- Primary (left-click) and secondary (right-click) selections
- Tooltips on hover
- Cell marking with indicator dots
- Responsive design with positioning options
- Fixed or flexible sizing options
- HTML formatting support for cell content

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cells` | List[List[dict or str]] | Required | 2D array of dictionaries or strings to be displayed in the grid. Dictionary keys: `label`, `cell_color`, `tooltip`, `mark`, `html`. |
| `header` | List[dict or str] or None | None | Optional 1D array for column headers. Same format as cells. |
| `index` | List[dict or str] or None | None | Optional 1D array for row indices. Same format as cells. |
| `aspect_ratio` | float | 1.0 | Controls the aspect ratio (height/width) of cells. |
| `allow_secondary_selection` | bool | False | If True, allows right-click to select a secondary cell. |
| `allow_header_selection` | bool | False | If True, allows header cells to be selected. |
| `height` | int or None | None | Optional height constraint in pixels. If None, grid sizes automatically based on width. |
| `resize` | bool | True | If True, grid resizes to fill available space. If False, maintains size based on content. |
| `grid_position` | str | 'center' | Horizontal alignment of the grid. Options: 'left', 'center', 'right'. Not applied if `resize = True`. |
| `mark_color` | str | '#2196F3' | Color for marker dots that appear on cells with mark=True. |
| `primary_selection_color` | str | '#2196F3' | Color for the primary (left-click) selection highlight. |
| `secondary_selection_color` | str | '#FF9800' | Color for the secondary (right-click) selection highlight. |
| `key` | str or None | None | Unique identifier for the component. |

## Cell Dictionary Format

Each cell can be either a string (which becomes the label) or a dictionary with these keys:

- `label` (str): The text to display in the cell
- `cell_color` (str): Background color in CSS format (e.g., "#f0f8ff" or "red")
- `tooltip` (str): Text to display when hovering over the cell
- `mark` (bool): If True, shows a marker dot in the top-right corner of the cell
- `html` (bool): If True, renders the label content as HTML, allowing formatting tags

## HTML Formatting Example

You can use HTML tags in cell labels when the `html` flag is set to `True`:

```python
cells = [
    [
        {"label": "Normal Text"},
        {"label": "<b>Bold Text</b>", "html": True},
        {"label": "<span style='color:red'>Red Text</span>", "html": True}
    ],
    [
        {"label": "<i>Italic</i>", "html": True},
        {"label": "<b>Bold</b> and <i>italic</i>", "html": True},
        {"label": "<u>Underlined</u>", "html": True}
    ]
]
```

## Return Value

```
{
    "primary": {"x": col_index, "y": row_index},  # For left-click selection
    "secondary": {"x": col_index, "y": row_index}  # For right-click selection (if enabled)
}
```

Secondary selection is only available after a primary selection has been made.

## How to run in development mode

1. Clone the repository:

   ```bash
   git clone https://github.com/hoggatt/st-selectable-grid.git
   cd st-selectable-grid
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies for both Python and frontend:

   ```bash
   pip install -e .
   cd st_selectable_grid/frontend
   npm install
   ```

4. Run the frontend in development mode:

   ```bash
   cd st_selectable_grid/frontend
   npm start
   ```

5. In a separate terminal, run the Streamlit app:

   ```bash
   streamlit run st_selectable_grid/example.py
   ```

This will start the React development server for the component and connect it to your Streamlit app, allowing you to see changes in real-time as you modify the component code.
