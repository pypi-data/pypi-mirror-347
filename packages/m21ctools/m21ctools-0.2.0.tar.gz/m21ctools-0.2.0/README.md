# m21ctools

**m21ctools** is a Python library designed to handle cubed-sphere data efficiently. It provides tools for reading, processing, interpolating, and visualizing data from cubed-sphere NetCDF-4 files.

## Key Features

### Data Loading and Cleaning
- **Reading NetCDF Files:**  
  Easily read from NetCDF-4 files using the `xarray` library with the `h5netcdf` engine.
- **Handling Duplicate Dimensions:**  
  Automatically resolves issues with duplicate 'ncontact' dimension names by replacing them with unique names, ensuring the dataset is ready for analysis.

### Longitude Adjustment
- **Standardizing Coordinates:**  
  Automatically adjusts longitudes to fall within the standard range of -180° to 180°.

### Data Aggregation
- **Combining Data Faces:**  
  Aggregates data from the six faces of the cubed-sphere into flat lists, which simplifies further analysis and processing.

### Interpolation to Regular Grid
- **Grid Interpolation:**  
  Interpolates irregular cubed-sphere data onto a regular latitude-longitude grid using interpolation methods from SciPy.

### Visualization
- **Plotting Tools:**  
  Visualizes the interpolated data with contour plots using Matplotlib and Cartopy, complete with coastlines and axis labels.

### Ensemble Spread Analysis
- **Efficient Processing:**  
  Process ensemble spread data from tar archives with parallel processing support. Reads ensemble data directly from `.tar` archives containing `.nc4` files.
- **Parallel Processing:**
  Processes multiple input files efficiently using Python's `multiprocessing`.
- **Data Version Control (`icechunk`):**
  Uses `icechunk` for efficient versioning and storage of the processed (e.g., averaged) time-series data. Supports tracking history via commits.
- **Time Series Analysis:**  
  Track ensemble spread evolution with Hovmöller diagrams for both 2D and 3D variables.
- **Incremental Updates & Overwriting:**
  - Smart processing that skips already processed timestamps for efficient updates.
  - Skips processing for timestamps already present in the `icechunk` repository (based on `get_existing_times`).
  - Includes a `force_rerun` flag in the `parallel_process_files_2d3d` function to allow users to bypass skipping and force reprocessing for a specific date range (e.g., if input data changed).

## Usage Example

### Basic Cubed-Sphere Data Processing

```python
from m21ctools.data_handler import CubedSphereData

# Initialize the CubedSphereData object with your NetCDF file path, time and level (indices), variable name, and grid resolution value.
data_handler = CubedSphereData(
    file_path="path/to/your/datafile.nc4",
    time=0,
    lev=0,
    variable="QV",
    resolution=1.0
)

# Access raw and cleaned data.
raw_data = data_handler.raw_data
clean_data = data_handler.raw_data_cleaned

# Retrieve aggregated latitudes, longitudes, and data as flat 1D arrays.
all_lats, all_lons, all_data = data_handler.all_lats, data_handler.all_lons, data_handler.all_data

# Interpolate data to a uniform latitude-longitude grid.
lat_grid, lon_grid, data_grid = data_handler.interpolate_to_latlon_grid(method='linear')  # Default interpolation method is 'linear'

# Visualize the data.
data_handler.plot_data(lat_grid, lon_grid, data_grid)
```

### Ensemble Spread Analysis

```python
from datetime import datetime
import icechunk
import m21ctools.data_handler as m21c_handler
import m21ctools.config as cfg

# Define time range and variables
start_date = datetime(2010, 1, 4, 0) # Example date range
end_date = datetime(2010, 1, 5, 0)
force_reprocess = False # Set to True to force overwrite for this range


# Use variables from config or define manually
var3d_list = cfg.DEFAULT_VAR3D # Example: ['u']
var2d_list = cfg.DEFAULT_VAR2D # Example: ['ps']

# Initialize icechunk repository
icechunk_repo_path = "ensemble_store"
storage = icechunk.local_filesystem_storage(icechunk_repo_path)
icechunk_repo = icechunk.Repository.open_or_create(storage)

# Get already processed timestamps
times_to_skip = m21c_handler.get_existing_times(icechunk_repo, 'u')

# Process new data with parallel processing
combined_averages = m21c_handler.parallel_process_files_2d3d(
    start_date, end_date,
    var3d_list, var2d_list,
    skip_times=times_to_skip,
    num_workers=4,
    force_rerun=force_reprocess
)

# Save to icechunk repository
m21c_handler.save_to_icechunk(icechunk_repo, combined_averages, "Processed new data")

# Load and visualize
u_data = m21c_handler.load_from_icechunk(icechunk_repo, 'u')
ps_data = m21c_handler.load_from_icechunk(icechunk_repo, 'ps')

# Create Hovmöller diagrams
m21c_handler.plot_hovmoeller_3d(u_data, var='u')  # For 3D variables
m21c_handler.plot_hovmoeller_2d(ps_data, var='ps')  # For 2D variables
```

For more examples, check the `examples/` directory in the repository.
