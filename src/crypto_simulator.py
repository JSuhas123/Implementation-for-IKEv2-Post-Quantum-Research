"""
Crypto Simulator for IKEv2 Post-Quantum Analysis

Simulates cryptographic operations and their performance characteristics
for different algorithm combinations in various network conditions.
"""

import random
import time
import numpy as np
from typing import Dict, List, Any
import logging

class CryptoSimulator:
    """Simulates cryptographic operations for IKEv2 handshakes."""
    
    def __init__(self, algorithms_config: Dict):
        self.algorithms_config = algorithms_config
        self.logger = logging.getLogger(__name__)
        
        # Set random seed for reproducible results
        random.seed(42)
        np.random.seed(42)
    
    def simulate_ikev2_handshake(self, crypto_type: str, scenario: Dict) -> Dict:
        """
        Simulate a complete IKEv2 handshake for given crypto type and scenario.
        
        Args:
            crypto_type: Type of cryptography (classical, hybrid, post_quantum)
            scenario: Network scenario configuration
            
        Returns:
            Dictionary containing simulation results
        """
        self.logger.debug(f"Simulating {crypto_type} handshake in {scenario['name']}")
        
        algorithms = self.algorithms_config[crypto_type]
        network = scenario["network_conditions"]
        test_params = scenario["test_parameters"]
        
        results = []
        
        for algorithm in algorithms:
            self.logger.debug(f"Testing algorithm: {algorithm['name']}")
            
            # Run multiple iterations
            iteration_results = []
            for i in range(test_params["handshake_iterations"]):
                result = self._simulate_single_handshake(algorithm, network)
                iteration_results.append(result)
            
            # Calculate statistics
            stats = self._calculate_statistics(iteration_results)
            stats["algorithm"] = algorithm["name"]
            stats["algorithm_details"] = algorithm
            
            results.append(stats)
        
        return {
            "crypto_type": crypto_type,
            "scenario": scenario["name"],
            "results": results,
            "network_conditions": network
        }
    
    def _simulate_single_handshake(self, algorithm: Dict, network: Dict) -> Dict:
        """Simulate a single IKE handshake."""
        
        # Phase 1: IKE_SA_INIT
        phase1_time = self._simulate_key_exchange(algorithm, network)
        
        # Phase 2: IKE_AUTH
        phase2_time = self._simulate_authentication(algorithm, network)
        
        # Calculate message sizes
        message_sizes = self._calculate_message_sizes(algorithm)
        
        # Network transmission simulation
        transmission_time = self._simulate_network_transmission(
            message_sizes["total"], network
        )
        
        total_handshake_time = phase1_time + phase2_time + transmission_time
        
        return {
            "phase1_time_ms": phase1_time,
            "phase2_time_ms": phase2_time,
            "transmission_time_ms": transmission_time,
            "total_time_ms": total_handshake_time,
            "message_sizes": message_sizes,
            "success": total_handshake_time < 30000  # 30 second timeout
        }
    
    def _simulate_key_exchange(self, algorithm: Dict, network: Dict) -> float:
        """Simulate key exchange phase timing."""
        base_time = algorithm.get("key_gen_time_ms", 1.0)
        
        # Add some realistic variance
        variance = np.random.normal(1.0, 0.1)
        variance = max(0.5, min(1.5, variance))  # Clamp variance
        
        # Network latency impact
        latency_factor = 1.0 + (network["latency_ms"] / 1000.0)
        
        return base_time * variance * latency_factor
    
    def _simulate_authentication(self, algorithm: Dict, network: Dict) -> float:
        """Simulate authentication phase timing."""
        base_time = algorithm.get("verify_time_ms", 1.0)
        
        # Add variance
        variance = np.random.normal(1.0, 0.15)
        variance = max(0.3, min(2.0, variance))
        
        # Packet loss can cause retries
        retry_factor = 1.0
        if random.random() < network["packet_loss_percent"] / 100.0:
            retry_factor = 1.5  # Simulate retry delay
        
        return base_time * variance * retry_factor
    
    def _calculate_message_sizes(self, algorithm: Dict) -> Dict:
        """Calculate IKE message sizes based on algorithm."""
        
        # Base IKE message overhead
        base_overhead = 200  # bytes
        
        # Key exchange payload sizes
        ke_size = algorithm.get("public_key_size", 64)
        
        # Authentication payload sizes  
        auth_size = algorithm.get("signature_size", 256)
        
        # For hybrid algorithms, sum both classical and PQ sizes
        if "pq_ke" in algorithm:
            # Hybrid key exchange includes both classical and PQ
            classical_ke_size = 64  # Typical ECDH size
            pq_ke_size = algorithm.get("public_key_size", 1000)
            ke_size = classical_ke_size + pq_ke_size
        
        if "pq_auth" in algorithm:
            # Hybrid auth includes both signatures
            classical_auth_size = 96  # Typical ECDSA size
            pq_auth_size = algorithm.get("signature_size", 2000)
            auth_size = classical_auth_size + pq_auth_size
        
        # Message breakdown
        ike_sa_init = base_overhead + ke_size + 32  # + nonce
        ike_auth = base_overhead + auth_size + 100  # + certificates
        
        return {
            "ike_sa_init": ike_sa_init,
            "ike_auth": ike_auth,
            "total": ike_sa_init + ike_auth,
            "key_exchange_payload": ke_size,
            "authentication_payload": auth_size
        }
    
    def _simulate_network_transmission(self, total_bytes: int, network: Dict) -> float:
        """Simulate network transmission time."""
        
        # Convert bandwidth to bytes per ms
        bandwidth_bps = network["bandwidth_mbps"] * 1_000_000
        bandwidth_Bpms = bandwidth_bps / 8 / 1000
        
        # Base transmission time
        transmission_time = total_bytes / bandwidth_Bpms
        
        # Add network latency (round trip for handshake)
        latency_overhead = network["latency_ms"] * 2
        
        # Add jitter
        jitter = np.random.normal(0, network["jitter_ms"])
        
        total_time = transmission_time + latency_overhead + abs(jitter)
        
        return total_time
    
    def _calculate_statistics(self, results: List[Dict]) -> Dict:
        """Calculate statistical summary of iteration results."""
        
        # Filter successful handshakes
        successful = [r for r in results if r["success"]]
        success_rate = len(successful) / len(results) * 100
        
        if not successful:
            return {
                "success_rate": 0.0,
                "mean_handshake_time_ms": 0.0,
                "median_handshake_time_ms": 0.0,
                "std_handshake_time_ms": 0.0,
                "min_handshake_time_ms": 0.0,
                "max_handshake_time_ms": 0.0,
                "mean_message_size": 0,
                "iterations": len(results)
            }
        
        times = [r["total_time_ms"] for r in successful]
        message_sizes = [r["message_sizes"]["total"] for r in successful]
        
        return {
            "success_rate": success_rate,
            "mean_handshake_time_ms": np.mean(times),
            "median_handshake_time_ms": np.median(times),
            "std_handshake_time_ms": np.std(times),
            "min_handshake_time_ms": np.min(times),
            "max_handshake_time_ms": np.max(times),
            "p95_handshake_time_ms": np.percentile(times, 95),
            "p99_handshake_time_ms": np.percentile(times, 99),
            "mean_message_size": np.mean(message_sizes),
            "median_message_size": np.median(message_sizes),
            "iterations": len(results),
            "successful_iterations": len(successful)
        }