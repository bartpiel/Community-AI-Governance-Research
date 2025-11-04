#!/usr/bin/env python3
"""
Setup and Run All Foundation Collectors

This script sets up the environment and runs all foundation collectors,
then generates the comprehensive comparison.

Usage:
    python3 run_full_analysis.py
"""

import subprocess
import sys
import os
from datetime import datetime

def log(message):
    """Log with timestamp"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

def check_dependencies():
    """Check if required packages are installed"""
    log("Checking dependencies...")

    required_packages = ['requests', 'beautifulsoup4', 'pandas']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        log(f"Missing packages: {', '.join(missing_packages)}")
        log("Installing missing packages...")

        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            log("Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            log(f"Failed to install dependencies: {e}")
            return False
    else:
        log("All dependencies satisfied")

    return True

def run_collector(collector_name):
    """Run individual foundation collector"""
    log(f"Running {collector_name}...")

    script_path = os.path.join('collectors', f'{collector_name}.py')

    if not os.path.exists(script_path):
        log(f"Collector not found: {script_path}")
        return False

    try:
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            log(f"✅ {collector_name} completed successfully")
            return True
        else:
            log(f"❌ {collector_name} failed:")
            log(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        log(f"⏰ {collector_name} timed out")
        return False
    except Exception as e:
        log(f"❌ Error running {collector_name}: {e}")
        return False

def run_all_collectors():
    """Run all foundation collectors"""
    log("Starting foundation data collection...")

    collectors = [
        'apache_foundation_collector',
        'eclipse_foundation_collector',
        'linux_foundation_collector',
        'mozilla_foundation_collector',
        'osi_ecosystem_collector',
        'fsf_ecosystem_collector'
    ]

    results = {}

    for collector in collectors:
        results[collector] = run_collector(collector)

    successful = sum(1 for success in results.values() if success)
    total = len(collectors)

    log(f"Collection complete: {successful}/{total} collectors successful")

    return results

def generate_comparison():
    """Generate comprehensive comparison"""
    log("Generating comprehensive comparison...")

    try:
        result = subprocess.run([
            sys.executable, 'generate_foundation_comparison.py'
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            log("✅ Comprehensive comparison generated successfully")
            return True
        else:
            log("❌ Comparison generation failed:")
            log(result.stderr)
            return False

    except Exception as e:
        log(f"❌ Error generating comparison: {e}")
        return False

def create_results_directory():
    """Create results directory if it doesn't exist"""
    if not os.path.exists('results'):
        os.makedirs('results')
        log("Created results directory")

def print_summary():
    """Print analysis summary"""
    print("\n" + "="*60)
    print("NONPROFIT FOUNDATION ANALYSIS COMPLETE")
    print("="*60)

    print("\n📁 Generated Files:")

    results_dir = 'results'
    if os.path.exists(results_dir):
        files = os.listdir(results_dir)
        json_files = [f for f in files if f.endswith('.json')]
        csv_files = [f for f in files if f.endswith('.csv')]

        print("\n📄 Detailed Data (JSON):")
        for file in sorted(json_files):
            print(f"• {file}")

        print("\n📊 Summary Data (CSV):")
        for file in sorted(csv_files):
            print(f"• {file}")

    print("\n📚 Documentation:")
    docs_dir = 'docs'
    if os.path.exists(docs_dir):
        docs = os.listdir(docs_dir)
        for doc in sorted(docs):
            print(f"• docs/{doc}")

    print("\n🎯 Analysis Focus:")
    print("• Repository platforms (where code is stored)")
    print("• Communication channels (how communities interact)")
    print("• Infrastructure strategies (self-hosted vs external)")
    print("• Organizational models (governance and structure)")

    print("\n📊 Foundations Analyzed:")
    print("• Apache Software Foundation (~400 projects)")
    print("• Eclipse Foundation (~415 projects)")
    print("• Linux Foundation (~220 major projects)")
    print("• Mozilla Foundation (1,048 projects)")
    print("• Open Source Initiative (70+ affiliates)")
    print("• Free Software Foundation (405+ GNU projects)")

    print("\n" + "="*60)

def main():
    """Main execution function"""
    print("🔍 Starting comprehensive nonprofit foundation analysis...")

    # Check dependencies
    if not check_dependencies():
        log("❌ Dependency check failed")
        return 1

    # Create results directory
    create_results_directory()

    # Run all collectors
    collector_results = run_all_collectors()

    # Generate comparison if at least some collectors succeeded
    successful_collectors = sum(1 for success in collector_results.values() if success)
    if successful_collectors > 0:
        comparison_success = generate_comparison()

        if comparison_success:
            print_summary()
            log("🎉 Full analysis completed successfully!")
            return 0
        else:
            log("⚠️ Data collection completed but comparison generation failed")
            return 1
    else:
        log("❌ All collectors failed - cannot generate comparison")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)