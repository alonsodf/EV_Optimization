# External Data Sources

This directory contains scripts and documentation for accessing external datasets.

## Available External Datasets

### Large Traffic Datasets
- **Source**: [Describe source]
- **Size**: [File size]
- **Download Script**: `download_traffic_data.py`
- **Description**: Detailed traffic patterns for route optimization

### Weather Data
- **Source**: [Describe source]  
- **Size**: [File size]
- **Download Script**: `download_weather_data.py`
- **Description**: Historical weather data affecting EV efficiency

### Charging Station Database
- **Source**: [Describe source]
- **Size**: [File size]
- **Download Script**: `download_charging_stations.py`
- **Description**: Global charging station locations and specifications

## Using External Data

1. Run the appropriate download script
2. Data will be downloaded to the `processed/` directory
3. Check the script documentation for any required API keys or credentials

## Adding New External Sources

1. Create a download script following the naming convention
2. Include error handling and progress reporting
3. Document the data source and any requirements
4. Update this README with the new dataset information

## Data Privacy and Compliance

- Ensure compliance with data source terms of use
- Do not commit API keys or credentials to the repository
- Use environment variables for sensitive configuration
- Respect rate limits and usage restrictions