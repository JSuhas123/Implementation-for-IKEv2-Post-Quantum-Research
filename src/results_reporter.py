"""
Results Reporter for IKEv2 Post-Quantum

Generates comprehensive reports and summaries of simulation results.
"""

import json
from datetime import datetime
from typing import Dict, List, Any
from tabulate import tabulate
from colorama import Fore, Style
import logging

class ResultsReporter:
    """Generates reports and summaries from analysis results."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_summary_report(self, simulation_results: Dict, analysis: Dict) -> Dict:
        """
        Generate a comprehensive summary report.
        
        Args:
            simulation_results: Raw simulation results
            analysis: Analyzed results from PerformanceAnalyzer
            
        Returns:
            Dictionary containing complete summary report
        """
        self.logger.info("Generating summary report")
        
        report = {
            "metadata": {
                "generation_time": datetime.now().isoformat(),
                "version": "1.0.0",
                "scenarios_tested": list(simulation_results.keys()),
                "crypto_types": self._extract_crypto_types(simulation_results)
            },
            "executive_summary": self._generate_executive_summary(analysis),
            "performance_overview": self._generate_performance_overview(analysis),
            "algorithm_comparison": self._generate_algorithm_comparison(analysis),
            "network_impact": self._generate_network_impact_summary(analysis),
            "recommendations": self._generate_recommendations(analysis),
            "detailed_results": simulation_results,
            "detailed_analysis": analysis
        }
        
        return report
    
    def print_console_summary(self, analysis: Dict) -> None:
        """Print a formatted summary to console."""
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print("📊 IKEv2 POST-QUANTUM RESULTS SUMMARY")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        # Performance Overview
        self._print_performance_overview(analysis)
        
        # Algorithm Rankings
        self._print_algorithm_rankings(analysis)
        
        # Key Insights
        self._print_key_insights(analysis)
        
        # Recommendations
        self._print_recommendations(analysis)
    
    def _extract_crypto_types(self, simulation_results: Dict) -> List[str]:
        """Extract unique crypto types from results."""
        crypto_types = set()
        for scenario_data in simulation_results.values():
            crypto_types.update(scenario_data.keys())
        return sorted(list(crypto_types))
    
    def _generate_executive_summary(self, analysis: Dict) -> Dict:
        """Generate executive summary section."""
        
        summary = {
            "key_findings": [],
            "performance_impact": {},
            "security_trade_offs": {},
            "deployment_readiness": {}
        }
        
        # Extract key findings from insights
        if "summary_insights" in analysis:
            summary["key_findings"] = analysis["summary_insights"]
        
        # Performance impact summary
        if "crypto_type_comparisons" in analysis:
            rel_perf = analysis["crypto_type_comparisons"].get("relative_performance", {})
            
            for crypto_type, metrics in rel_perf.items():
                summary["performance_impact"][crypto_type] = {
                    "time_overhead": f"{metrics.get('time_overhead_percent', 0):.1f}%",
                    "size_overhead": f"{metrics.get('size_overhead_percent', 0):.1f}%"
                }
        
        return summary
    
    def _generate_performance_overview(self, analysis: Dict) -> Dict:
        """Generate performance overview section."""
        
        overview = {
            "crypto_type_performance": {},
            "speed_rankings": [],
            "size_rankings": [],
            "reliability_rankings": []
        }
        
        # Extract crypto type performance
        if "crypto_type_comparisons" in analysis:
            speed_comp = analysis["crypto_type_comparisons"].get("speed_comparison", {})
            size_comp = analysis["crypto_type_comparisons"].get("size_comparison", {})
            
            for crypto_type in speed_comp.keys():
                overview["crypto_type_performance"][crypto_type] = {
                    "avg_handshake_time_ms": speed_comp[crypto_type]["mean_time_ms"],
                    "avg_message_size_bytes": size_comp[crypto_type]["mean_size_bytes"]
                }
        
        # Extract rankings
        if "algorithm_rankings" in analysis:
            rankings = analysis["algorithm_rankings"]
            
            overview["speed_rankings"] = [
                {
                    "algorithm": r["algorithm"],
                    "crypto_type": r["crypto_type"], 
                    "time_ms": r["time_ms"]
                }
                for r in rankings.get("by_speed", [])[:5]
            ]
            
            overview["size_rankings"] = [
                {
                    "algorithm": r["algorithm"],
                    "crypto_type": r["crypto_type"],
                    "size_bytes": r["size_bytes"]
                }
                for r in rankings.get("by_message_size", [])[:5]
            ]
        
        return overview
    
    def _generate_algorithm_comparison(self, analysis: Dict) -> Dict:
        """Generate detailed algorithm comparison."""
        
        comparison = {
            "top_performers": {},
            "balanced_rankings": [],
            "trade_off_analysis": {}
        }
        
        if "algorithm_rankings" in analysis:
            rankings = analysis["algorithm_rankings"]
            
            # Top performers by category
            if "by_speed" in rankings and rankings["by_speed"]:
                comparison["top_performers"]["fastest"] = rankings["by_speed"][0]
            
            if "by_message_size" in rankings and rankings["by_message_size"]:
                comparison["top_performers"]["smallest"] = rankings["by_message_size"][0]
            
            if "by_reliability" in rankings and rankings["by_reliability"]:
                comparison["top_performers"]["most_reliable"] = rankings["by_reliability"][0]
            
            # Balanced rankings
            comparison["balanced_rankings"] = rankings.get("balanced_score", [])[:5]
        
        return comparison
    
    def _generate_network_impact_summary(self, analysis: Dict) -> Dict:
        """Generate network impact analysis summary."""
        
        network_summary = {
            "latency_sensitivity": {},
            "recommendations_by_network": {}
        }
        
        if "network_impact_analysis" in analysis:
            impact = analysis["network_impact_analysis"]
            
            # Extract latency sensitivity
            if "latency_sensitivity" in impact:
                for crypto_type, sensitivity in impact["latency_sensitivity"].items():
                    network_summary["latency_sensitivity"][crypto_type] = {
                        "variance": sensitivity["variance"],
                        "stability_score": 1 / (1 + sensitivity["coefficient_of_variation"])
                    }
            
            # Extract recommendations
            if "recommendations" in impact:
                network_summary["recommendations_by_network"] = impact["recommendations"]
        
        return network_summary
    
    def _generate_recommendations(self, analysis: Dict) -> Dict:
        """Generate deployment recommendations."""
        
        recommendations = {
            "by_use_case": {},
            "migration_strategy": [],
            "implementation_priorities": []
        }
        
        # Use case recommendations
        recommendations["by_use_case"] = {
            "high_security_requirements": "Consider hybrid or post-quantum algorithms",
            "performance_critical": "Use classical algorithms for now, monitor PQ development",
            "balanced_approach": "Deploy hybrid algorithms for future-proofing",
            "constrained_networks": "Stick with classical, evaluate hybrid carefully"
        }
        
        # Migration strategy
        recommendations["migration_strategy"] = [
            "Phase 1: Deploy hybrid algorithms in controlled environments",
            "Phase 2: Gradually expand to production systems",
            "Phase 3: Monitor performance and adjust configurations",
            "Phase 4: Evaluate pure post-quantum for high-security applications"
        ]
        
        # Implementation priorities
        recommendations["implementation_priorities"] = [
            "Implement timeout adjustments for post-quantum algorithms",
            "Deploy network monitoring for message size tracking",
            "Establish fallback mechanisms to classical algorithms",
            "Create performance baseline measurements"
        ]
        
        return recommendations
    
    def _print_performance_overview(self, analysis: Dict) -> None:
        """Print performance overview to console."""
        
        print(f"{Fore.YELLOW}🚀 PERFORMANCE OVERVIEW{Style.RESET_ALL}")
        
        if "crypto_type_comparisons" in analysis:
            speed_comp = analysis["crypto_type_comparisons"].get("speed_comparison", {})
            
            table_data = []
            for crypto_type, metrics in speed_comp.items():
                table_data.append([
                    crypto_type.title(),
                    f"{metrics['mean_time_ms']:.1f} ms",
                    f"±{metrics['std_time_ms']:.1f} ms"
                ])
            
            if table_data:
                print(tabulate(
                    table_data,
                    headers=["Crypto Type", "Avg Handshake Time", "Std Dev"],
                    tablefmt="rounded_grid"
                ))
        
        print()
    
    def _print_algorithm_rankings(self, analysis: Dict) -> None:
        """Print algorithm rankings to console."""
        
        print(f"{Fore.YELLOW}🏆 TOP PERFORMING ALGORITHMS{Style.RESET_ALL}")
        
        if "algorithm_rankings" in analysis:
            rankings = analysis["algorithm_rankings"]
            
            # Speed rankings
            print(f"\n{Fore.GREEN}⚡ Fastest Algorithms:{Style.RESET_ALL}")
            speed_data = []
            for i, alg in enumerate(rankings.get("by_speed", [])[:3], 1):
                speed_data.append([
                    f"#{i}",
                    alg["algorithm"],
                    alg["crypto_type"],
                    f"{alg['time_ms']:.1f} ms"
                ])
            
            if speed_data:
                print(tabulate(
                    speed_data,
                    headers=["Rank", "Algorithm", "Type", "Time"],
                    tablefmt="simple"
                ))
            
            # Size rankings
            print(f"\n{Fore.GREEN}📦 Smallest Message Sizes:{Style.RESET_ALL}")
            size_data = []
            for i, alg in enumerate(rankings.get("by_message_size", [])[:3], 1):
                size_data.append([
                    f"#{i}",
                    alg["algorithm"],
                    alg["crypto_type"],
                    f"{alg['size_bytes']} bytes"
                ])
            
            if size_data:
                print(tabulate(
                    size_data,
                    headers=["Rank", "Algorithm", "Type", "Message Size"],
                    tablefmt="simple"
                ))
        
        print()
    
    def _print_key_insights(self, analysis: Dict) -> None:
        """Print key insights to console."""
        
        print(f"{Fore.YELLOW}💡 KEY INSIGHTS{Style.RESET_ALL}")
        
        if "summary_insights" in analysis:
            for i, insight in enumerate(analysis["summary_insights"], 1):
                print(f"  {i}. {insight}")
        else:
            print("  No insights available")
        
        print()
    
    def _print_recommendations(self, analysis: Dict) -> None:
        """Print recommendations to console."""
        
        print(f"{Fore.YELLOW}📋 RECOMMENDATIONS{Style.RESET_ALL}")
        
        if "network_impact_analysis" in analysis:
            recs = analysis["network_impact_analysis"].get("recommendations", {})
            
            if "general_guidelines" in recs:
                print(f"\n{Fore.GREEN}General Guidelines:{Style.RESET_ALL}")
                for i, rec in enumerate(recs["general_guidelines"], 1):
                    print(f"  {i}. {rec}")
        
        print(f"\n{Fore.GREEN}Migration Strategy:{Style.RESET_ALL}")
        migration_steps = [
            "Start with hybrid algorithms in test environments",
            "Monitor performance impact carefully", 
            "Implement gradual rollout strategy",
            "Maintain classical fallback options"
        ]
        
        for i, step in enumerate(migration_steps, 1):
            print(f"  {i}. {step}")
        
        print()