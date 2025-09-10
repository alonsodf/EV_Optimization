# Tests

This directory contains test files for the EV optimization project.

## Running Tests

Run all tests:
```bash
pytest tests/
```

Run tests with coverage:
```bash
pytest tests/ --cov=src
```

Run specific test file:
```bash
pytest tests/test_basic_functionality.py
```

## Test Organization

- `test_basic_functionality.py` - Basic tests for core classes and functions
- `test_algorithms.py` - Tests for optimization algorithms
- `test_models.py` - Tests for data models
- `test_utils.py` - Tests for utility functions

## Writing Tests

### Test Structure
Follow the AAA pattern:
- **Arrange**: Set up test data and objects
- **Act**: Execute the function being tested
- **Assert**: Verify the results

### Test Naming
- Test files: `test_<module_name>.py`
- Test classes: `TestClassName`
- Test methods: `test_<functionality>`

### Fixtures
Use pytest fixtures for reusable test data:
```python
@pytest.fixture
def sample_vehicle():
    specs = VehicleSpecs(...)
    return ElectricVehicle(specs)
```

### Testing Guidelines
1. Test both normal and edge cases
2. Test error conditions and exceptions
3. Use meaningful assertions with clear error messages
4. Keep tests independent and isolated
5. Mock external dependencies when appropriate

## Continuous Integration

Tests should pass before merging code. The test suite validates:
- Algorithm correctness
- Model behavior
- Data processing functions
- Error handling
- Performance (where applicable)