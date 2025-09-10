# Results

This directory contains output results from optimization algorithms and analysis.

## Directory Structure

```
results/
├── optimization/          # Optimization algorithm results
├── analysis/             # Data analysis results
├── figures/              # Generated plots and visualizations
├── reports/              # Generated reports and summaries
└── experiments/          # Experimental study results
```

## File Organization

### Naming Convention
Use descriptive names with timestamps:
- `battery_optimization_2023-12-01_v1.json`
- `route_analysis_city_data_2023-12-01.csv`
- `comparison_study_algorithms_2023-12-01.pdf`

### Result Types

#### Optimization Results
- Algorithm performance metrics
- Optimal solutions and parameters
- Convergence data and statistics
- Comparison between different approaches

#### Analysis Results
- Statistical analysis outputs
- Data summaries and insights
- Performance benchmarks
- Sensitivity analysis results

#### Visualizations
- Algorithm convergence plots
- Performance comparison charts
- Data distribution plots
- Geographic visualizations (for routing)

## Best Practices

### Data Storage
- Save results in standard formats (JSON, CSV, HDF5)
- Include metadata about the experiment
- Store both raw results and processed summaries
- Use version control for important results

### Documentation
- Include README files for complex result sets
- Document experimental conditions and parameters
- Note any data preprocessing steps
- Record computational requirements and runtime

### Reproducibility
- Save input parameters and configuration
- Include random seeds used
- Document software versions
- Provide scripts to regenerate results

## Large Results

For large result files (> 100 MB):
- Use Git LFS or external storage
- Provide download scripts if needed
- Include sample/summary results in repository
- Compress files when appropriate

## Cleaning Up

Regularly review and clean up old results:
- Archive completed studies
- Remove duplicate or obsolete results
- Maintain only current and reference results
- Document any archived or deleted results