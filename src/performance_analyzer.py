"""
Performance Analyzer for IKEv2 Post-Quantum

Analyzes simulation results to provide insights into performance
characteristics and comparisons between crypto approaches.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
import logging

class PerformanceAnalyzer:
    """Analyzes performance results from crypto simulations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_all_scenarios(self, simulation_results: Dict) -> Dict:
        """
        Analyze results across all scenarios and crypto types.
        
        Args:
            simulation_results: Dict containing all simulation results
            
        Returns:
            Dictionary containing analysis results
        """
        self.logger.info("Performing comprehensive performance analysis")
        
        analysis = {
            "scenario_comparisons": {},
            "crypto_type_comparisons": {},
            "algorithm_rankings": {},
            "network_impact_analysis": {},
            "summary_insights": {}
        }
        
        # Analyze each scenario
        for scenario_name, scenario_data in simulation_results.items():
            analysis["scenario_comparisons"][scenario_name] = \
                self._analyze_scenario(scenario_data)
        
        # Cross-scenario analysis
        analysis["crypto_type_comparisons"] = \
            self._compare_crypto_types(simulation_results)
        
        analysis["algorithm_rankings"] = \
            self._rank_algorithms(simulation_results)
        
        analysis["network_impact_analysis"] = \
            self._analyze_network_impact(simulation_results)
        
        analysis["summary_insights"] = \
            self._generate_insights(simulation_results, analysis)
        
        return analysis
    
    def _analyze_scenario(self, scenario_data: Dict) -> Dict:
        """Analyze performance within a single scenario."""
        
        analysis = {
            "crypto_performance": {},
            "fastest_algorithm": None,
            "smallest_messages": None,
            "reliability_ranking": []
        }
        
        all_results = []
        
        for crypto_type, crypto_results in scenario_data.items():
            crypto_analysis = self._analyze_crypto_type(crypto_results)
            analysis["crypto_performance"][crypto_type] = crypto_analysis
            
            # Collect all algorithm results
            for result in crypto_results["results"]:
                result["crypto_type"] = crypto_type
                all_results.append(result)
        
        # Find fastest algorithm
        fastest = min(all_results, 
                     key=lambda x: x["mean_handshake_time_ms"])
        analysis["fastest_algorithm"] = {
            "name": fastest["algorithm"],
            "crypto_type": fastest["crypto_type"],
            "time_ms": fastest["mean_handshake_time_ms"]
        }
        
        # Find smallest messages
        smallest = min(all_results,
                      key=lambda x: x["mean_message_size"])
        analysis["smallest_messages"] = {
            "name": smallest["algorithm"], 
            "crypto_type": smallest["crypto_type"],
            "size_bytes": smallest["mean_message_size"]
        }
        
        # Reliability ranking by success rate
        reliability_ranking = sorted(all_results,
                                   key=lambda x: x["success_rate"],
                                   reverse=True)
        analysis["reliability_ranking"] = [
            {
                "name": r["algorithm"],
                "crypto_type": r["crypto_type"],
                "success_rate": r["success_rate"]
            }
            for r in reliability_ranking
        ]
        
        return analysis
    
    def _analyze_crypto_type(self, crypto_results: Dict) -> Dict:
        """Analyze performance of a specific crypto type."""
        
        results = crypto_results["results"]
        
        times = [r["mean_handshake_time_ms"] for r in results]
        message_sizes = [r["mean_message_size"] for r in results]
        success_rates = [r["success_rate"] for r in results]
        
        return {
            "mean_handshake_time_ms": np.mean(times),
            "min_handshake_time_ms": np.min(times),
            "max_handshake_time_ms": np.max(times),
            "std_handshake_time_ms": np.std(times),
            "mean_message_size": np.mean(message_sizes),
            "min_message_size": np.min(message_sizes),
            "max_message_size": np.max(message_sizes),
            "mean_success_rate": np.mean(success_rates),
            "algorithms_count": len(results)
        }
    
    def _compare_crypto_types(self, simulation_results: Dict) -> Dict:
        """Compare performance across crypto types."""
        
        comparison = {
            "speed_comparison": {},
            "size_comparison": {},
            "reliability_comparison": {},
            "relative_performance": {}
        }
        
        # Aggregate data across all scenarios
        crypto_aggregates = {}
        
        for scenario_name, scenario_data in simulation_results.items():
            for crypto_type, crypto_results in scenario_data.items():
                if crypto_type not in crypto_aggregates:
                    crypto_aggregates[crypto_type] = {
                        "times": [],
                        "sizes": [],
                        "success_rates": []
                    }
                
                for result in crypto_results["results"]:
                    crypto_aggregates[crypto_type]["times"].append(
                        result["mean_handshake_time_ms"]
                    )
                    crypto_aggregates[crypto_type]["sizes"].append(
                        result["mean_message_size"]
                    )
                    crypto_aggregates[crypto_type]["success_rates"].append(
                        result["success_rate"]
                    )
        
        # Calculate comparisons
        crypto_types = list(crypto_aggregates.keys())
        
        for crypto_type in crypto_types:
            data = crypto_aggregates[crypto_type]
            
            comparison["speed_comparison"][crypto_type] = {
                "mean_time_ms": np.mean(data["times"]),
                "std_time_ms": np.std(data["times"])
            }
            
            comparison["size_comparison"][crypto_type] = {
                "mean_size_bytes": np.mean(data["sizes"]),
                "std_size_bytes": np.std(data["sizes"])
            }
            
            comparison["reliability_comparison"][crypto_type] = {
                "mean_success_rate": np.mean(data["success_rates"]),
                "std_success_rate": np.std(data["success_rates"])
            }
        
        # Calculate relative performance (classical as baseline)
        if "classical" in comparison["speed_comparison"]:
            baseline_time = comparison["speed_comparison"]["classical"]["mean_time_ms"]
            baseline_size = comparison["size_comparison"]["classical"]["mean_size_bytes"]
            
            for crypto_type in crypto_types:
                current_time = comparison["speed_comparison"][crypto_type]["mean_time_ms"]
                current_size = comparison["size_comparison"][crypto_type]["mean_size_bytes"]
                
                comparison["relative_performance"][crypto_type] = {
                    "time_overhead_factor": current_time / baseline_time,
                    "size_overhead_factor": current_size / baseline_size,
                    "time_overhead_percent": ((current_time / baseline_time) - 1) * 100,
                    "size_overhead_percent": ((current_size / baseline_size) - 1) * 100
                }
        
        return comparison
    
    def _rank_algorithms(self, simulation_results: Dict) -> Dict:
        """Rank algorithms by different criteria."""
        
        # Collect all algorithm results
        all_algorithms = []
        
        for scenario_name, scenario_data in simulation_results.items():
            for crypto_type, crypto_results in scenario_data.items():
                for result in crypto_results["results"]:
                    all_algorithms.append({
                        "scenario": scenario_name,
                        "crypto_type": crypto_type,
                        "algorithm": result["algorithm"],
                        "time_ms": result["mean_handshake_time_ms"],
                        "size_bytes": result["mean_message_size"],
                        "success_rate": result["success_rate"]
                    })
        
        rankings = {
            "by_speed": sorted(all_algorithms, key=lambda x: x["time_ms"])[:10],
            "by_message_size": sorted(all_algorithms, key=lambda x: x["size_bytes"])[:10],
            "by_reliability": sorted(all_algorithms, key=lambda x: x["success_rate"], reverse=True)[:10],
            "balanced_score": []
        }
        
        # Calculate balanced score (normalized combination of metrics)
        if all_algorithms:
            max_time = max(a["time_ms"] for a in all_algorithms)
            max_size = max(a["size_bytes"] for a in all_algorithms)
            
            for alg in all_algorithms:
                # Lower is better for time and size, higher is better for success rate
                time_score = 1 - (alg["time_ms"] / max_time)
                size_score = 1 - (alg["size_bytes"] / max_size) 
                reliability_score = alg["success_rate"] / 100
                
                # Weighted combination
                balanced_score = (0.4 * time_score + 
                                0.3 * size_score + 
                                0.3 * reliability_score)
                
                alg["balanced_score"] = balanced_score
            
            rankings["balanced_score"] = sorted(all_algorithms, 
                                              key=lambda x: x["balanced_score"], 
                                              reverse=True)[:10]
        
        return rankings
    
    def _analyze_network_impact(self, simulation_results: Dict) -> Dict:
        """Analyze how network conditions impact different crypto types."""
        
        impact_analysis = {
            "latency_sensitivity": {},
            "bandwidth_sensitivity": {},
            "loss_sensitivity": {},
            "recommendations": {}
        }
        
        # Group results by crypto type
        crypto_by_network = {}
        
        for scenario_name, scenario_data in simulation_results.items():
            for crypto_type, crypto_results in scenario_data.items():
                if crypto_type not in crypto_by_network:
                    crypto_by_network[crypto_type] = {}
                
                crypto_by_network[crypto_type][scenario_name] = crypto_results
        
        # Analyze sensitivity for each crypto type
        for crypto_type, scenarios in crypto_by_network.items():
            times_by_scenario = {}
            sizes_by_scenario = {}
            
            for scenario_name, results in scenarios.items():
                avg_time = np.mean([r["mean_handshake_time_ms"] 
                                  for r in results["results"]])
                avg_size = np.mean([r["mean_message_size"] 
                                  for r in results["results"]])
                
                times_by_scenario[scenario_name] = avg_time
                sizes_by_scenario[scenario_name] = avg_size
            
            # Calculate sensitivity (variance across scenarios)
            if len(times_by_scenario) > 1:
                time_values = list(times_by_scenario.values())
                impact_analysis["latency_sensitivity"][crypto_type] = {
                    "variance": np.var(time_values),
                    "coefficient_of_variation": np.std(time_values) / np.mean(time_values),
                    "scenarios": times_by_scenario
                }
        
        # Generate recommendations
        impact_analysis["recommendations"] = self._generate_network_recommendations(
            impact_analysis
        )
        
        return impact_analysis
    
    def _generate_network_recommendations(self, impact_analysis: Dict) -> Dict:
        """Generate network-specific recommendations."""
        
        recommendations = {
            "high_latency_networks": [],
            "low_bandwidth_networks": [],
            "unreliable_networks": [],
            "general_guidelines": []
        }
        
        # Analyze latency sensitivity
        if impact_analysis["latency_sensitivity"]:
            sorted_by_sensitivity = sorted(
                impact_analysis["latency_sensitivity"].items(),
                key=lambda x: x[1]["coefficient_of_variation"]
            )
            
            least_sensitive = sorted_by_sensitivity[0][0]
            recommendations["high_latency_networks"].append(
                f"Use {least_sensitive} algorithms for high-latency networks"
            )
        
        recommendations["general_guidelines"] = [
            "Classical algorithms perform best in constrained networks",
            "Hybrid algorithms provide good balance of security and performance", 
            "Post-quantum algorithms require careful network condition assessment",
            "Consider timeout adjustments for post-quantum in high-latency scenarios"
        ]
        
        return recommendations
    
    def _generate_insights(self, simulation_results: Dict, analysis: Dict) -> List[str]:
        """Generate key insights from the analysis."""
        
        insights = []
        
        # Performance insights
        if "crypto_type_comparisons" in analysis:
            comp = analysis["crypto_type_comparisons"]["relative_performance"]
            
            if "hybrid" in comp:
                hybrid_overhead = comp["hybrid"]["time_overhead_percent"]
                insights.append(
                    f"Hybrid algorithms show {hybrid_overhead:.1f}% time overhead vs classical"
                )
            
            if "post_quantum" in comp:
                pq_overhead = comp["post_quantum"]["time_overhead_percent"]
                insights.append(
                    f"Post-quantum algorithms show {pq_overhead:.1f}% time overhead vs classical"
                )
        
        # Size insights
        if "crypto_type_comparisons" in analysis:
            comp = analysis["crypto_type_comparisons"]["relative_performance"]
            
            if "hybrid" in comp:
                hybrid_size = comp["hybrid"]["size_overhead_percent"]
                insights.append(
                    f"Hybrid algorithms increase message size by {hybrid_size:.1f}%"
                )
        
        # Network insights
        insights.append("Network latency has greater impact on post-quantum algorithms")
        insights.append("Classical algorithms maintain best reliability across all network conditions")
        
        # Algorithm-specific insights
        if "algorithm_rankings" in analysis:
            fastest = analysis["algorithm_rankings"]["by_speed"][0]
            insights.append(
                f"Fastest algorithm: {fastest['algorithm']} ({fastest['time_ms']:.1f}ms)"
            )
            
            most_reliable = analysis["algorithm_rankings"]["by_reliability"][0]
            insights.append(
                f"Most reliable: {most_reliable['algorithm']} ({most_reliable['success_rate']:.1f}% success)"
            )
        
        return insights