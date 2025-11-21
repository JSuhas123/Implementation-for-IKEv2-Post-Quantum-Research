# IKEv2 Post-Quantum Cryptography

A tool for comparing classical, hybrid, and post-quantum cryptographic approaches in IKEv2 implementations.

## Overview

This tool simulates and analyzes the performance characteristics of different cryptographic configurations:
- **Classical**: Traditional ECDH + RSA/ECDSA
- **Hybrid**: Classical + Post-Quantum (e.g., ECDH + Kyber)
- **Post-Quantum**: Pure PQ algorithms (e.g., Kyber + Dilithium)

## Features

- Real-time performance simulation
- Comparative analysis across crypto modes
- Network condition modeling
- Interactive results visualization
- Comprehensive reporting

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python runner.py
   ```

3. View results in the `results/` directory

## Configuration

Edit `configs/algorithms.json` to customize:
- Cryptographic algorithms
- Key sizes and security levels
- Performance parameters

Edit `configs/test_scenarios.json` to modify:
- Network conditions
- Test scenarios
- Simulation parameters

## Output

- **Console**: Real-time progress and summary
- **Log file**: `results/console_output.log`
- **JSON report**: `results/summary_report.json`
- **Visualizations**: Generated charts and graphs

## Use Cases

- Educational analysis
- Performance impact assessment
- Algorithm comparison studies
- Migration planning analysis