# Contributing to EV Optimization

Thank you for your interest in contributing to this project! This guide will help ensure smooth collaboration.

## Getting Started

1. **Fork and Clone**: Fork the repository and clone your fork locally
2. **Create a Branch**: Create a feature branch for your work
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Set up Environment**: Follow the installation instructions in README.md

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Use type hints where appropriate

### Commit Messages
Use clear, descriptive commit messages:
- Start with a short summary (50 chars or less)
- Use present tense ("Add feature" not "Added feature")
- Reference issues when applicable

### Code Organization
- Place algorithms in `src/algorithms/`
- Place data models in `src/models/`
- Place analysis scripts in `src/analysis/`
- Place utility functions in `src/utils/`
- Use Jupyter notebooks in `notebooks/` for exploration and demonstration

### Testing
- Write tests for new functionality in the `tests/` directory
- Run tests before submitting: `pytest tests/`
- Ensure code coverage for critical functions

### Documentation
- Update README.md if adding new features or changing usage
- Document algorithms with mathematical formulations when applicable
- Include examples in docstrings

## Data Contributions

### Small Datasets (< 10 MB)
- Can be added to the `data/` directory
- Include metadata and documentation

### Large Datasets (> 10 MB)
- Do NOT commit large files directly
- Use Git LFS for files up to 100 MB
- For larger datasets, provide download scripts or external links
- Always include sample/subset data for testing

### Data Documentation
For any dataset contribution, provide:
- Source and collection methodology
- Data schema/format description
- Any preprocessing applied
- License and usage restrictions

## Research and Academic Guidelines

### Citation and Attribution
- Cite relevant papers and sources in code comments
- Maintain a bibliography for the project
- Give credit to algorithm sources and inspirations

### Reproducibility
- Make experiments reproducible with clear instructions
- Include random seeds for stochastic algorithms
- Document computational requirements and runtime

### Collaboration Etiquette
- Communicate clearly about ongoing work to avoid conflicts
- Share results and findings openly within the team
- Ask questions when unsure about implementation details

## Pull Request Process

1. **Update Documentation**: Ensure README and relevant docs are updated
2. **Test Your Changes**: Run tests and verify functionality
3. **Clean Commit History**: Squash commits if necessary
4. **Descriptive PR**: Write a clear description of changes and rationale
5. **Code Review**: Be responsive to feedback and suggestions

## Questions and Communication

- Create GitHub issues for bugs or feature requests
- Use clear, descriptive titles for issues
- Provide context and steps to reproduce for bugs
- Tag collaborators when input is needed

## Academic Integrity

- This is an academic research project
- Always attribute sources and prior work
- Ensure any third-party code is properly licensed and attributed
- Follow your institution's guidelines for collaborative research

Thank you for contributing to advancing EV optimization research!