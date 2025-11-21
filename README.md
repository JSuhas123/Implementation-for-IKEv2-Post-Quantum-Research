# IKEv2 Post-Quantum Cryptography Implementation

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Research](https://img.shields.io/badge/Research-Post--Quantum%20Cryptography-orange.svg)](https://github.com/JSuhas123/Implementation-for-IKEv2-Post-Quantum-Research)

A comprehensive research and simulation tool for analyzing the performance impact of post-quantum cryptographic algorithms in IKEv2 (Internet Key Exchange version 2) implementations. This project provides detailed comparative analysis between classical, hybrid, and post-quantum cryptographic approaches.

## 🔬 Research Overview

This implementation addresses the critical need for evaluating post-quantum readiness in VPN and secure communication protocols. As quantum computing advances threaten current cryptographic standards, this tool helps researchers and security professionals understand the performance implications of quantum-resistant algorithms.

### Cryptographic Configurations Analyzed

- **🔐 Classical**: Traditional ECDH + RSA/ECDSA algorithms
- **🔄 Hybrid**: Classical + Post-Quantum combinations (e.g., ECDH + Kyber)
- **🛡️ Post-Quantum**: Pure quantum-resistant algorithms (e.g., Kyber + Dilithium)

## 🚀 Features

### 📊 Comprehensive Analysis
- **Real-time Performance Simulation**: Accurate timing analysis of cryptographic operations
- **Network Condition Modeling**: Simulates various environments (LAN, WAN, Satellite, Mobile, Constrained)
- **Comparative Performance Metrics**: Side-by-side analysis of different cryptographic approaches
- **Statistical Analysis**: Detailed performance statistics with confidence intervals

### 📈 Advanced Visualization
- **Performance Heatmaps**: Visual representation of algorithm performance across network conditions
- **Comparative Charts**: Handshake time, message size, and success rate comparisons
- **Network Impact Analysis**: Detailed assessment of latency sensitivity
- **Algorithm Rankings**: Performance-based ranking with multiple criteria

### 📋 Detailed Reporting
- **Executive Summaries**: High-level insights for decision makers
- **Technical Reports**: Detailed performance metrics and analysis
- **JSON Export**: Machine-readable results for further analysis
- **Console Output**: Real-time progress and results display

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start
```bash
# Clone the repository
git clone https://github.com/JSuhas123/Implementation-for-IKEv2-Post-Quantum-Research.git
cd Implementation-for-IKEv2-Post-Quantum-Research

# Install dependencies
pip install -r requirements.txt

# Run the simulation
python runner.py
```

### Advanced Usage
```bash
# Run with verbose logging
python runner.py --verbose

# View help information
python runner.py --help
```

## 📊 Sample Results

The tool generates comprehensive analysis including:

- **Performance Overhead**: Quantifies the performance impact of post-quantum algorithms
- **Network Sensitivity**: Analyzes how different network conditions affect each cryptographic approach
- **Migration Recommendations**: Provides actionable insights for transitioning to post-quantum cryptography
- **Security vs Performance Trade-offs**: Detailed analysis of the balance between security and performance

## 📁 Project Structure

```
ikev2-pq/
├── 📄 runner.py                    # Main application entry point
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # Project documentation
├── 📄 .gitignore                   # Git ignore rules
├── 📁 configs/                     # Configuration files
│   ├── algorithms.json             # Cryptographic algorithm definitions
│   └── test_scenarios.json         # Network scenario configurations
├── 📁 src/                         # Source code modules
│   ├── crypto_simulator.py         # Core simulation engine
│   ├── performance_analyzer.py     # Performance analysis logic
│   ├── results_reporter.py         # Report generation
│   └── visualization.py            # Chart and graph generation
└── 📁 results/                     # Generated output files
    ├── console_output.log           # Execution logs
    ├── summary_report.json          # Detailed results in JSON
    └── *.png                        # Generated visualizations
```

## ⚙️ Configuration

Edit `configs/algorithms.json` to customize:
- Cryptographic algorithms
- Key sizes and security levels
- Performance parameters

Edit `configs/test_scenarios.json` to modify:
- Network conditions
- Test scenarios
- Simulation parameters

## 📊 Output & Results

- **Console**: Real-time progress and summary
- **Log file**: `results/console_output.log`
- **JSON report**: `results/summary_report.json`
- **Visualizations**: Generated charts and graphs

## 🎯 Use Cases

- **Research**: Post-quantum cryptography performance analysis
- **Education**: Practical cryptography and network security learning
- **Industry**: VPN and secure communication planning
- **Assessment**: Algorithm comparison and migration studies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Research

This implementation supports research in:
- Post-quantum cryptography adoption
- Network protocol security analysis  
- VPN performance optimization
- Cryptographic algorithm benchmarking

## ✨ Acknowledgments

This project contributes to the ongoing research in post-quantum cryptography and its practical implementation in network security protocols.