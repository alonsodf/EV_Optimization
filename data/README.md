# Data Directory

This directory contains data files for the EV optimization project.

## Directory Structure

- `raw/` - Raw, unprocessed data files
- `processed/` - Cleaned and processed data ready for analysis
- `external/` - References to external datasets (not stored in repository)

## Data Guidelines

### File Size Limits
- **Small files** (< 10 MB): Can be stored directly in this repository
- **Medium files** (10-100 MB): Use Git LFS (Large File Storage)
- **Large files** (> 100 MB): Store externally and provide download scripts

### Data Documentation
For each dataset, provide:
1. **Data source** and collection methodology
2. **Data format** and schema description
3. **Preprocessing steps** applied (if any)
4. **License** and usage restrictions
5. **Sample data** for testing and development

## Example Data Types

Common data types for EV optimization include:
- Vehicle specifications and performance data
- Battery test data and degradation models
- Traffic and route data
- Weather and environmental data
- Electricity pricing data
- Charging station locations and utilization
- Energy demand patterns

## Adding New Data

1. Place small datasets in the appropriate subdirectory
2. Create a README or metadata file describing the dataset
3. For large datasets, create a download script and place it in `external/`
4. Update this README with information about the new dataset

## Sample Data

Sample datasets for testing and development should be included even when full datasets are stored externally. This ensures:
- Tests can run without downloading large files
- New contributors can quickly get started
- Continuous integration works smoothly