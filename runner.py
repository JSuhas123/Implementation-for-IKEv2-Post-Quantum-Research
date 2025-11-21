#!/usr/bin/env python3
"""
IKEv2 Post-Quantum Cryptography Runner

Main script that orchestrates the simulation,
analysis, and reporting of IKEv2 post-quantum crypto performance.
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style
from tqdm import tqdm

# Initialize colorama for cross-platform colored output
init()

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from crypto_simulator import CryptoSimulator
from performance_analyzer import PerformanceAnalyzer
from results_reporter import ResultsReporter
from visualization import Visualizer

class Runner:
    """Main runner class that orchestrates the simulation."""
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.setup_logging()
        self.load_configurations()
        
    def setup_logging(self):
        """Configure logging for the application."""
        log_level = logging.DEBUG if self.verbose else logging.INFO
        
        # Create results directory if it doesn't exist
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(results_dir / "console_output.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        
    def load_configurations(self):
        """Load configuration files."""
        try:
            with open("configs/algorithms.json", "r") as f:
                self.algorithms_config = json.load(f)
                
            with open("configs/test_scenarios.json", "r") as f:
                self.scenarios_config = json.load(f)
                
            self.logger.info("Configurations loaded successfully")
            
        except FileNotFoundError as e:
            self.logger.error(f"Configuration file not found: {e}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration: {e}")
            sys.exit(1)
    
    def print_banner(self):
        """Print welcome banner."""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                IKEv2 Post-Quantum Crypto                    ║
║                                                              ║
║  Comparing Classical vs Hybrid vs Post-Quantum Algorithms   ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}🔐 Algorithms to test:{Style.RESET_ALL}
"""
        print(banner)
        
        for crypto_type, algs in self.algorithms_config.items():
            print(f"  {Fore.GREEN}{crypto_type.upper()}:{Style.RESET_ALL}")
            for alg in algs:
                print(f"    • {alg['name']} ({alg['key_size']} bits)")
        print()
    
    def run_crypto_simulation(self):
        """Run the crypto simulation for all scenarios."""
        self.logger.info("Starting IKEv2 Post-Quantum simulation")
        
        simulator = CryptoSimulator(self.algorithms_config)
        all_results = {}
        
        scenarios = self.scenarios_config["scenarios"]
        total_tests = len(scenarios) * len(self.algorithms_config)
        
        with tqdm(total=total_tests, desc="Running simulations") as pbar:
            for scenario in scenarios:
                scenario_name = scenario["name"]
                self.logger.info(f"Testing scenario: {scenario_name}")
                
                scenario_results = {}
                
                for crypto_type in self.algorithms_config:
                    self.logger.info(f"  Testing {crypto_type} algorithms")
                    
                    results = simulator.simulate_ikev2_handshake(
                        crypto_type, scenario
                    )
                    
                    scenario_results[crypto_type] = results
                    pbar.update(1)
                
                all_results[scenario_name] = scenario_results
        
        self.logger.info("Simulation completed")
        return all_results
    
    def analyze_results(self, simulation_results):
        """Analyze simulation results."""
        self.logger.info("Analyzing performance results")
        
        analyzer = PerformanceAnalyzer()
        analysis = analyzer.analyze_all_scenarios(simulation_results)
        
        return analysis
    
    def generate_reports(self, simulation_results, analysis):
        """Generate reports and visualizations."""
        self.logger.info("Generating reports and visualizations")
        
        # Generate summary report
        reporter = ResultsReporter()
        summary = reporter.generate_summary_report(simulation_results, analysis)
        
        # Save JSON report
        with open("results/summary_report.json", "w") as f:
            json.dump(summary, f, indent=2, default=str)
        
        # Generate visualizations
        visualizer = Visualizer()
        visualizer.create_all_visualizations(simulation_results, analysis)
        
        # Print console summary
        reporter.print_console_summary(analysis)
        
        return summary
    
    def run_simulation(self):
        """Run the complete simulation."""
        try:
            self.print_banner()
            
            # Run simulation
            simulation_results = self.run_crypto_simulation()
            
            # Analyze results
            analysis = self.analyze_results(simulation_results)
            
            # Generate reports
            summary = self.generate_reports(simulation_results, analysis)
            
            print(f"\n{Fore.GREEN}✅ Simulation completed successfully!{Style.RESET_ALL}")
            print(f"\n📊 Results available in:")
            print(f"  • Console log: results/console_output.log")
            print(f"  • Summary report: results/summary_report.json")
            print(f"  • Visualizations: results/*.png")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Simulation failed: {e}")
            if self.verbose:
                self.logger.exception("Full traceback:")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="IKEv2 Post-Quantum Cryptography"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    runner = Runner(verbose=args.verbose)
    success = runner.run_simulation()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()