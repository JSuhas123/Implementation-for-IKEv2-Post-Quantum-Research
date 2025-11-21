"""
Visualization module for IKEv2 Post-Quantum

Creates charts and graphs to visualize simulation results and comparisons.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, List, Any
import logging
from pathlib import Path

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class Visualizer:
    """Creates visualizations from simulation and analysis results."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path("results")
        self.output_dir.mkdir(exist_ok=True)
        
        # Color scheme for crypto types
        self.crypto_colors = {
            'classical': '#2E86AB',
            'hybrid': '#A23B72', 
            'post_quantum': '#F18F01'
        }
    
    def create_all_visualizations(self, simulation_results: Dict, analysis: Dict) -> None:
        """Create all visualization charts."""
        
        self.logger.info("Generating visualization charts")
        
        try:
            # Performance comparison charts
            self._create_handshake_time_comparison(simulation_results, analysis)
            self._create_message_size_comparison(simulation_results, analysis)
            self._create_success_rate_comparison(simulation_results, analysis)
            
            # Network impact charts
            self._create_network_impact_chart(simulation_results)
            self._create_latency_sensitivity_chart(simulation_results)
            
            # Algorithm ranking charts
            self._create_algorithm_ranking_chart(analysis)
            self._create_performance_heatmap(simulation_results)
            
            # Overhead analysis
            self._create_overhead_comparison(analysis)
            
            self.logger.info("All visualizations created successfully")
            
        except Exception as e:
            self.logger.error(f"Error creating visualizations: {e}")
    
    def _create_handshake_time_comparison(self, simulation_results: Dict, analysis: Dict) -> None:
        """Create handshake time comparison chart."""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Extract data
        crypto_types = []
        mean_times = []
        std_times = []
        
        if "crypto_type_comparisons" in analysis:
            speed_comp = analysis["crypto_type_comparisons"].get("speed_comparison", {})
            
            for crypto_type, metrics in speed_comp.items():
                crypto_types.append(crypto_type.replace('_', ' ').title())
                mean_times.append(metrics["mean_time_ms"])
                std_times.append(metrics["std_time_ms"])
        
        # Chart 1: Bar chart with error bars
        colors = [self.crypto_colors.get(ct.lower().replace(' ', '_'), '#666666') 
                 for ct in [ct.lower().replace(' ', '_') for ct in crypto_types]]
        
        bars = ax1.bar(crypto_types, mean_times, yerr=std_times, 
                      capsize=5, color=colors, alpha=0.8, edgecolor='black')
        
        ax1.set_title('Average IKE Handshake Time by Crypto Type', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Handshake Time (ms)')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar, mean_time in zip(bars, mean_times):
            height = bar.get_height()
            ax1.annotate(f'{mean_time:.1f}ms',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontweight='bold')
        
        # Chart 2: Detailed scenario breakdown
        scenario_data = []
        for scenario_name, scenario_results in simulation_results.items():
            for crypto_type, crypto_results in scenario_results.items():
                avg_time = np.mean([r["mean_handshake_time_ms"] for r in crypto_results["results"]])
                scenario_data.append({
                    'scenario': scenario_name.replace('_', ' ').title(),
                    'crypto_type': crypto_type.replace('_', ' ').title(),
                    'time_ms': avg_time
                })
        
        if scenario_data:
            df = pd.DataFrame(scenario_data)
            
            # Pivot for grouped bar chart
            pivot_df = df.pivot(index='scenario', columns='crypto_type', values='time_ms')
            pivot_df.plot(kind='bar', ax=ax2, color=[self.crypto_colors.get(ct.lower().replace(' ', '_'), '#666666') 
                                                    for ct in pivot_df.columns])
            
            ax2.set_title('Handshake Time by Scenario', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Handshake Time (ms)')
            ax2.set_xlabel('Network Scenario')
            ax2.legend(title='Crypto Type', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax2.grid(axis='y', alpha=0.3)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "handshake_time_comparison.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_message_size_comparison(self, simulation_results: Dict, analysis: Dict) -> None:
        """Create message size comparison chart."""
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Collect all algorithm data
        algorithm_data = []
        for scenario_name, scenario_results in simulation_results.items():
            for crypto_type, crypto_results in scenario_results.items():
                for result in crypto_results["results"]:
                    algorithm_data.append({
                        'algorithm': result["algorithm"],
                        'crypto_type': crypto_type,
                        'message_size': result["mean_message_size"],
                        'scenario': scenario_name
                    })
        
        if algorithm_data:
            df = pd.DataFrame(algorithm_data)
            
            # Group by algorithm and take mean across scenarios
            grouped = df.groupby(['algorithm', 'crypto_type'])['message_size'].mean().reset_index()
            grouped = grouped.sort_values('message_size')
            
            # Create horizontal bar chart
            colors = [self.crypto_colors.get(ct, '#666666') for ct in grouped['crypto_type']]
            bars = ax.barh(range(len(grouped)), grouped['message_size'], color=colors, alpha=0.8)
            
            # Customize chart
            ax.set_yticks(range(len(grouped)))
            ax.set_yticklabels([f"{row['algorithm']}\n({row['crypto_type']})" 
                               for _, row in grouped.iterrows()], fontsize=9)
            ax.set_xlabel('Average Message Size (bytes)')
            ax.set_title('IKE Message Sizes by Algorithm', fontsize=14, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            # Add value labels
            for i, (bar, size) in enumerate(zip(bars, grouped['message_size'])):
                ax.annotate(f'{size:.0f}B',
                           xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                           xytext=(3, 0),
                           textcoords="offset points",
                           va='center', ha='left', fontsize=8)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "message_size_comparison.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_success_rate_comparison(self, simulation_results: Dict, analysis: Dict) -> None:
        """Create success rate comparison chart."""
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract success rates by scenario and crypto type
        success_data = []
        for scenario_name, scenario_results in simulation_results.items():
            for crypto_type, crypto_results in scenario_results.items():
                avg_success = np.mean([r["success_rate"] for r in crypto_results["results"]])
                success_data.append({
                    'scenario': scenario_name.replace('_', ' ').title(),
                    'crypto_type': crypto_type.replace('_', ' ').title(),
                    'success_rate': avg_success
                })
        
        if success_data:
            df = pd.DataFrame(success_data)
            
            # Create grouped bar chart
            pivot_df = df.pivot(index='scenario', columns='crypto_type', values='success_rate')
            pivot_df.plot(kind='bar', ax=ax, 
                         color=[self.crypto_colors.get(ct.lower().replace(' ', '_'), '#666666') 
                               for ct in pivot_df.columns])
            
            ax.set_title('Success Rate by Scenario and Crypto Type', fontsize=14, fontweight='bold')
            ax.set_ylabel('Success Rate (%)')
            ax.set_xlabel('Network Scenario')
            ax.set_ylim(80, 105)  # Focus on the interesting range
            ax.legend(title='Crypto Type', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(axis='y', alpha=0.3)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "success_rate_comparison.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_network_impact_chart(self, simulation_results: Dict) -> None:
        """Create network impact visualization."""
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Extract network conditions and performance
        network_data = []
        for scenario_name, scenario_results in simulation_results.items():
            # Get network conditions from first crypto type (they should be the same)
            first_crypto = next(iter(scenario_results.values()))
            if "network_conditions" in first_crypto:
                network_cond = first_crypto["network_conditions"]
                
                for crypto_type, crypto_results in scenario_results.items():
                    avg_time = np.mean([r["mean_handshake_time_ms"] 
                                      for r in crypto_results["results"]])
                    avg_size = np.mean([r["mean_message_size"] 
                                      for r in crypto_results["results"]])
                    
                    network_data.append({
                        'scenario': scenario_name,
                        'crypto_type': crypto_type,
                        'latency_ms': network_cond.get('latency_ms', 0),
                        'bandwidth_mbps': network_cond.get('bandwidth_mbps', 100),
                        'packet_loss': network_cond.get('packet_loss_percent', 0),
                        'handshake_time': avg_time,
                        'message_size': avg_size
                    })
        
        if network_data:
            df = pd.DataFrame(network_data)
            
            # Chart 1: Latency vs Handshake Time
            for crypto_type in df['crypto_type'].unique():
                crypto_df = df[df['crypto_type'] == crypto_type]
                color = self.crypto_colors.get(crypto_type, '#666666')
                ax1.scatter(crypto_df['latency_ms'], crypto_df['handshake_time'], 
                           label=crypto_type.replace('_', ' ').title(), 
                           color=color, s=100, alpha=0.7)
            
            ax1.set_xlabel('Network Latency (ms)')
            ax1.set_ylabel('Handshake Time (ms)')
            ax1.set_title('Handshake Performance vs Network Latency', fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Chart 2: Bandwidth vs Performance
            for crypto_type in df['crypto_type'].unique():
                crypto_df = df[df['crypto_type'] == crypto_type]
                color = self.crypto_colors.get(crypto_type, '#666666')
                ax2.scatter(crypto_df['bandwidth_mbps'], crypto_df['handshake_time'],
                           label=crypto_type.replace('_', ' ').title(),
                           color=color, s=100, alpha=0.7)
            
            ax2.set_xlabel('Network Bandwidth (Mbps)')
            ax2.set_ylabel('Handshake Time (ms)')
            ax2.set_title('Handshake Performance vs Network Bandwidth', fontweight='bold')
            ax2.set_xscale('log')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "network_impact_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_algorithm_ranking_chart(self, analysis: Dict) -> None:
        """Create algorithm ranking visualization."""
        
        if "algorithm_rankings" not in analysis:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        rankings = analysis["algorithm_rankings"]
        
        # Speed rankings
        if "by_speed" in rankings:
            speed_data = rankings["by_speed"][:8]  # Top 8
            algorithms = [item["algorithm"] for item in speed_data]
            times = [item["time_ms"] for item in speed_data]
            crypto_types = [item["crypto_type"] for item in speed_data]
            
            colors = [self.crypto_colors.get(ct, '#666666') for ct in crypto_types]
            
            bars1 = ax1.barh(range(len(algorithms)), times, color=colors, alpha=0.8)
            ax1.set_yticks(range(len(algorithms)))
            ax1.set_yticklabels([f"{alg[:30]}{'...' if len(alg) > 30 else ''}" 
                                for alg in algorithms], fontsize=9)
            ax1.set_xlabel('Handshake Time (ms)')
            ax1.set_title('Top Algorithms by Speed', fontweight='bold')
            ax1.grid(axis='x', alpha=0.3)
            
            # Add value labels
            for bar, time in zip(bars1, times):
                ax1.annotate(f'{time:.1f}ms',
                           xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                           xytext=(3, 0),
                           textcoords="offset points",
                           va='center', ha='left', fontsize=8)
        
        # Balanced rankings
        if "balanced_score" in rankings:
            balanced_data = rankings["balanced_score"][:8]
            algorithms = [item["algorithm"] for item in balanced_data]
            scores = [item["balanced_score"] for item in balanced_data]
            crypto_types = [item["crypto_type"] for item in balanced_data]
            
            colors = [self.crypto_colors.get(ct, '#666666') for ct in crypto_types]
            
            bars2 = ax2.barh(range(len(algorithms)), scores, color=colors, alpha=0.8)
            ax2.set_yticks(range(len(algorithms)))
            ax2.set_yticklabels([f"{alg[:30]}{'...' if len(alg) > 30 else ''}" 
                                for alg in algorithms], fontsize=9)
            ax2.set_xlabel('Balanced Score')
            ax2.set_title('Top Algorithms by Balanced Score', fontweight='bold')
            ax2.grid(axis='x', alpha=0.3)
            
            # Add value labels
            for bar, score in zip(bars2, scores):
                ax2.annotate(f'{score:.2f}',
                           xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                           xytext=(3, 0),
                           textcoords="offset points",
                           va='center', ha='left', fontsize=8)
        
        # Add legend
        legend_elements = [mpatches.Patch(color=color, label=crypto_type.replace('_', ' ').title()) 
                          for crypto_type, color in self.crypto_colors.items()]
        fig.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.02), ncol=3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "algorithm_rankings.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_overhead_comparison(self, analysis: Dict) -> None:
        """Create overhead comparison chart."""
        
        if "crypto_type_comparisons" not in analysis:
            return
        
        rel_perf = analysis["crypto_type_comparisons"].get("relative_performance", {})
        if not rel_perf:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        crypto_types = []
        time_overheads = []
        size_overheads = []
        
        for crypto_type, metrics in rel_perf.items():
            if crypto_type != "classical":  # Skip baseline
                crypto_types.append(crypto_type.replace('_', ' ').title())
                time_overheads.append(metrics.get("time_overhead_percent", 0))
                size_overheads.append(metrics.get("size_overhead_percent", 0))
        
        if crypto_types:
            colors = [self.crypto_colors.get(ct.lower().replace(' ', '_'), '#666666') 
                     for ct in [ct.lower().replace(' ', '_') for ct in crypto_types]]
            
            # Time overhead
            bars1 = ax1.bar(crypto_types, time_overheads, color=colors, alpha=0.8)
            ax1.set_title('Time Overhead vs Classical', fontweight='bold')
            ax1.set_ylabel('Overhead (%)')
            ax1.grid(axis='y', alpha=0.3)
            
            for bar, overhead in zip(bars1, time_overheads):
                height = bar.get_height()
                ax1.annotate(f'{overhead:.1f}%',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontweight='bold')
            
            # Size overhead
            bars2 = ax2.bar(crypto_types, size_overheads, color=colors, alpha=0.8)
            ax2.set_title('Message Size Overhead vs Classical', fontweight='bold')
            ax2.set_ylabel('Overhead (%)')
            ax2.grid(axis='y', alpha=0.3)
            
            for bar, overhead in zip(bars2, size_overheads):
                height = bar.get_height()
                ax2.annotate(f'{overhead:.1f}%',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "overhead_comparison.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_performance_heatmap(self, simulation_results: Dict) -> None:
        """Create performance heatmap."""
        
        # Prepare data for heatmap
        heatmap_data = []
        scenarios = []
        algorithms = set()
        
        for scenario_name, scenario_results in simulation_results.items():
            scenarios.append(scenario_name.replace('_', ' ').title())
            
            for crypto_type, crypto_results in scenario_results.items():
                for result in crypto_results["results"]:
                    algorithm_name = f"{result['algorithm']} ({crypto_type})"
                    algorithms.add(algorithm_name)
                    
                    heatmap_data.append({
                        'scenario': scenario_name.replace('_', ' ').title(),
                        'algorithm': algorithm_name,
                        'time_ms': result["mean_handshake_time_ms"]
                    })
        
        if heatmap_data:
            df = pd.DataFrame(heatmap_data)
            pivot_df = df.pivot(index='algorithm', columns='scenario', values='time_ms')
            
            fig, ax = plt.subplots(figsize=(12, max(8, len(algorithms) * 0.4)))
            
            sns.heatmap(pivot_df, annot=True, fmt='.1f', cmap='RdYlGn_r', 
                       ax=ax, cbar_kws={'label': 'Handshake Time (ms)'})
            
            ax.set_title('Performance Heatmap: Handshake Time by Algorithm and Scenario', 
                        fontweight='bold', pad=20)
            ax.set_xlabel('Network Scenario')
            ax.set_ylabel('Algorithm')
            
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.savefig(self.output_dir / "performance_heatmap.png", 
                       dpi=300, bbox_inches='tight')
            plt.close()
    
    def _create_latency_sensitivity_chart(self, simulation_results: Dict) -> None:
        """Create latency sensitivity analysis chart."""
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Collect data for different crypto types across scenarios
        crypto_sensitivity = {}
        
        for scenario_name, scenario_results in simulation_results.items():
            # Get latency for this scenario
            first_crypto = next(iter(scenario_results.values()))
            latency = first_crypto.get("network_conditions", {}).get("latency_ms", 0)
            
            for crypto_type, crypto_results in scenario_results.items():
                if crypto_type not in crypto_sensitivity:
                    crypto_sensitivity[crypto_type] = {'latencies': [], 'times': []}
                
                avg_time = np.mean([r["mean_handshake_time_ms"] 
                                  for r in crypto_results["results"]])
                crypto_sensitivity[crypto_type]['latencies'].append(latency)
                crypto_sensitivity[crypto_type]['times'].append(avg_time)
        
        # Plot sensitivity curves
        for crypto_type, data in crypto_sensitivity.items():
            if len(data['latencies']) > 1:
                # Sort by latency for proper line plotting
                sorted_data = sorted(zip(data['latencies'], data['times']))
                latencies, times = zip(*sorted_data)
                
                color = self.crypto_colors.get(crypto_type, '#666666')
                ax.plot(latencies, times, 
                       marker='o', linewidth=2, markersize=8,
                       label=crypto_type.replace('_', ' ').title(),
                       color=color)
        
        ax.set_xlabel('Network Latency (ms)')
        ax.set_ylabel('Handshake Time (ms)')
        ax.set_title('Latency Sensitivity Analysis', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "latency_sensitivity.png", 
                   dpi=300, bbox_inches='tight')
        plt.close()