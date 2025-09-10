#!/usr/bin/env python3
"""
Setup script for EV Optimization project.

This script helps set up the development environment and validates the installation.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_python_version():
    """Check if Python version is adequate."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version} found")


def install_requirements(dev=False):
    """Install project requirements."""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        
        if dev:
            # Install additional development dependencies
            dev_packages = ["pytest-cov", "black", "flake8", "jupyter"]
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + dev_packages)
            print("✅ Development dependencies installed")
            
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)


def run_tests():
    """Run basic tests to validate installation."""
    print("🧪 Running tests...")
    try:
        # Check if pytest is available
        subprocess.check_call([sys.executable, "-m", "pytest", "--version"], 
                            stdout=subprocess.DEVNULL)
        
        # Run tests
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            
    except subprocess.CalledProcessError:
        print("⚠️  pytest not available, skipping tests")
    except FileNotFoundError:
        print("⚠️  No tests found, skipping test run")


def create_config_template():
    """Create configuration template files."""
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    config_template = """# EV Optimization Configuration Template
# Copy this file to local_config.yaml and customize as needed

# Data settings
data:
  raw_data_path: "data/raw"
  processed_data_path: "data/processed" 
  external_data_path: "data/external"

# Algorithm settings
algorithms:
  battery_optimization:
    max_iterations: 1000
    tolerance: 1e-6
  
  route_optimization:
    max_distance: 500  # km
    charging_time_limit: 60  # minutes

# Visualization settings
visualization:
  figure_size: [10, 6]
  dpi: 300
  style: "seaborn"

# Computational settings
computation:
  n_cores: -1  # Use all available cores
  memory_limit: "8GB"
  
# External API settings (add your keys to local_config.yaml)
# apis:
#   weather_api_key: "your_key_here"
#   maps_api_key: "your_key_here"
"""
    
    config_file = config_dir / "config_template.yaml"
    with open(config_file, 'w') as f:
        f.write(config_template)
    
    print("✅ Configuration template created at config/config_template.yaml")


def validate_structure():
    """Validate project directory structure."""
    required_dirs = [
        "src", "src/algorithms", "src/models", "src/analysis", "src/utils",
        "data", "data/raw", "data/processed", "data/external",
        "notebooks", "tests", "docs", "results"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    else:
        print("✅ Project directory structure is valid")
        return True


def show_next_steps():
    """Show next steps after setup."""
    print("\n🎉 Setup complete! Next steps:")
    print("1. Copy config/config_template.yaml to config/local_config.yaml and customize")
    print("2. Add your code to the appropriate src/ subdirectories")
    print("3. Add sample data to data/raw/ (keep files < 10MB)")
    print("4. Create Jupyter notebooks in notebooks/ for analysis")
    print("5. Write tests in tests/ for your algorithms")
    print("6. Update README.md with project-specific information")
    print("\n📚 See CONTRIBUTING.md for development guidelines")
    print("🔗 Repository: https://github.com/alonsodf/EV_Optimization")


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description="Set up EV Optimization project")
    parser.add_argument("--dev", action="store_true", 
                       help="Install development dependencies")
    parser.add_argument("--skip-tests", action="store_true",
                       help="Skip running tests")
    parser.add_argument("--skip-install", action="store_true",
                       help="Skip installing requirements")
    
    args = parser.parse_args()
    
    print("🚗 Setting up EV Optimization project...")
    
    # Check Python version
    check_python_version()
    
    # Validate directory structure
    if not validate_structure():
        print("❌ Project structure validation failed")
        sys.exit(1)
    
    # Install requirements
    if not args.skip_install:
        install_requirements(dev=args.dev)
    
    # Create configuration template
    create_config_template()
    
    # Run tests
    if not args.skip_tests:
        run_tests()
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    main()