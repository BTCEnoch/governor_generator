#!/usr/bin/env python3
"""
Performance Benchmark for Governor Preferences System
====================================================

This script measures the performance of the governor preferences system
and identifies optimization opportunities for production deployment.
"""

import time
import sys
import statistics
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from game_mechanics.dialog_system import (
    GovernorPreferencesManager,
    GovernorProfile,
    PlayerState,
    InteractionType,
    TonePreference,
    PuzzleDifficulty
)

@dataclass
class PerformanceMetrics:
    """Performance measurement results"""
    operation_name: str
    avg_time_ms: float
    min_time_ms: float
    max_time_ms: float
    std_dev_ms: float
    target_time_ms: float
    meets_target: bool
    memory_usage_mb: float = 0.0


class PerformanceBenchmark:
    """Performance benchmark suite for governor preferences system"""
    
    def __init__(self):
        """Initialize benchmark suite"""
        self.manager = GovernorPreferencesManager()
        self.test_profiles = self._create_test_profiles()
        self.results: List[PerformanceMetrics] = []
        print("🚀 Performance Benchmark Suite Initialized")
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run all performance benchmarks"""
        print("\n📊 Running Performance Benchmarks...")
        
        # Core operation benchmarks
        self._benchmark_preference_encoding()
        self._benchmark_response_selection()
        self._benchmark_cache_performance()
        self._benchmark_trait_mapping()
        
        # Integration benchmarks
        self._benchmark_dialog_processing()
        self._benchmark_concurrent_load()
        
        # Memory usage benchmarks
        self._benchmark_memory_usage()
        
        return self._generate_performance_report()
    
    def _benchmark_preference_encoding(self) -> None:
        """Benchmark preference encoding performance"""
        print("\n🔧 Benchmarking Preference Encoding...")
        
        times = []
        for _ in range(100):  # Run 100 iterations
            profile = self.test_profiles[0]  # Use first test profile
            
            start_time = time.perf_counter()
            preferences = self.manager.get_governor_preferences(profile)
            end_time = time.perf_counter()
            
            times.append((end_time - start_time) * 1000)  # Convert to milliseconds
        
        metrics = self._calculate_metrics(
            "preference_encoding", 
            times, 
            target_ms=50.0  # Target: <50ms
        )
        self.results.append(metrics)
        
        print(f"   ✅ Preference Encoding: {metrics.avg_time_ms:.2f}ms avg (target: <50ms)")
    
    def _benchmark_response_selection(self) -> None:
        """Benchmark response selection performance"""
        print("\n🎯 Benchmarking Response Selection...")
        
        times = []
        test_variants = [
            'Indeed, seeker, your wisdom grows through patient study.',
            'Yeah, whatever, here\'s your answer dude.',
            'The ancient knowledge reveals itself to those who seek.',
            'Contemplate the deeper mysteries that await.',
            'Your understanding expands with each question asked.'
        ]
        
        for _ in range(200):  # Run 200 iterations
            profile = self.test_profiles[1]  # Use second test profile
            preferences = self.manager.get_governor_preferences(profile)
            player_state = PlayerState(player_id='test_player')
            context = {'base_reputation': 1}
            
            start_time = time.perf_counter()
            response = self.manager.process_dialog_interaction(
                player_input='I seek wisdom about the sacred mysteries.',
                response_variants=test_variants,
                governor_profile=profile,
                player_state=player_state,
                context=context
            )
            end_time = time.perf_counter()
            
            times.append((end_time - start_time) * 1000)
        
        metrics = self._calculate_metrics(
            "response_selection", 
            times, 
            target_ms=10.0  # Target: <10ms
        )
        self.results.append(metrics)
        
        print(f"   ✅ Response Selection: {metrics.avg_time_ms:.2f}ms avg (target: <10ms)")
    
    def _benchmark_cache_performance(self) -> None:
        """Benchmark cache hit/miss performance"""
        print("\n💾 Benchmarking Cache Performance...")
        
        # Cold cache (first access)
        cold_times = []
        for profile in self.test_profiles[:5]:
            start_time = time.perf_counter()
            preferences = self.manager.get_governor_preferences(profile)
            end_time = time.perf_counter()
            cold_times.append((end_time - start_time) * 1000)
        
        # Warm cache (repeated access)
        warm_times = []
        for _ in range(50):
            profile = self.test_profiles[0]  # Reuse same profile
            start_time = time.perf_counter()
            preferences = self.manager.get_governor_preferences(profile)
            end_time = time.perf_counter()
            warm_times.append((end_time - start_time) * 1000)
        
        cold_metrics = self._calculate_metrics("cache_miss", cold_times, target_ms=50.0)
        warm_metrics = self._calculate_metrics("cache_hit", warm_times, target_ms=1.0)
        
        self.results.extend([cold_metrics, warm_metrics])
        
        print(f"   ✅ Cache Miss: {cold_metrics.avg_time_ms:.2f}ms avg")
        print(f"   ✅ Cache Hit: {warm_metrics.avg_time_ms:.2f}ms avg")
    
    def _create_test_profiles(self) -> List[GovernorProfile]:
        """Create test governor profiles for benchmarking"""
        return [
            GovernorProfile(
                governor_id='benchmark_mystical',
                name='Mystical Benchmark Governor',
                traits=['mystical', 'scholarly', 'patient'],
                preferences={'tone': 'mystical_poetic'}
            ),
            GovernorProfile(
                governor_id='benchmark_cryptic',
                name='Cryptic Benchmark Governor',
                traits=['cryptic', 'stern', 'wise'],
                preferences={'tone': 'solemn_cryptic'}
            ),
            GovernorProfile(
                governor_id='benchmark_formal',
                name='Formal Benchmark Governor',
                traits=['formal', 'methodical', 'scholarly'],
                preferences={'tone': 'stern_formal'}
            ),
            GovernorProfile(
                governor_id='benchmark_playful',
                name='Playful Benchmark Governor',
                traits=['playful', 'patient', 'wise'],
                preferences={'tone': 'warm_encouraging'}
            ),
            GovernorProfile(
                governor_id='benchmark_complex',
                name='Complex Benchmark Governor',
                traits=['mystical', 'cryptic', 'scholarly', 'patient', 'formal', 'wise'],
                preferences={'tone': 'solemn_cryptic'}
            )
        ]
    
    def _calculate_metrics(self, operation_name: str, times: List[float], 
                          target_ms: float) -> PerformanceMetrics:
        """Calculate performance metrics from timing data"""
        if not times:
            return PerformanceMetrics(
                operation_name=operation_name,
                avg_time_ms=0.0,
                min_time_ms=0.0,
                max_time_ms=0.0,
                std_dev_ms=0.0,
                target_time_ms=target_ms,
                meets_target=False
            )
        
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
        
        return PerformanceMetrics(
            operation_name=operation_name,
            avg_time_ms=avg_time,
            min_time_ms=min_time,
            max_time_ms=max_time,
            std_dev_ms=std_dev,
            target_time_ms=target_ms,
            meets_target=avg_time <= target_ms
        )
    
    def _benchmark_trait_mapping(self) -> None:
        """Benchmark trait mapping performance"""
        print("\n🎭 Benchmarking Trait Mapping...")
        
        times = []
        for _ in range(100):
            traits = ['mystical', 'scholarly', 'patient', 'cryptic', 'formal']
            
            start_time = time.perf_counter()
            # Access trait mapper through manager
            trait_mappings = self.manager.trait_mapper.get_all_mappings_for_traits(traits)
            trait_weights = {'mystical': 0.4, 'scholarly': 0.3, 'patient': 0.3}
            resolved_params = self.manager.trait_mapper.resolve_parameter_conflicts(trait_mappings, trait_weights)
            end_time = time.perf_counter()
            
            times.append((end_time - start_time) * 1000)
        
        metrics = self._calculate_metrics("trait_mapping", times, target_ms=5.0)
        self.results.append(metrics)
        
        print(f"   ✅ Trait Mapping: {metrics.avg_time_ms:.2f}ms avg (target: <5ms)")
    
    def _benchmark_dialog_processing(self) -> None:
        """Benchmark complete dialog processing pipeline"""
        print("\n💬 Benchmarking Dialog Processing Pipeline...")
        
        times = []
        test_variants = [
            'Indeed, seeker, your wisdom grows through patient study.',
            'The ancient knowledge reveals itself to those who seek.',
            'Contemplate the deeper mysteries that await your understanding.'
        ]
        
        for _ in range(50):
            profile = self.test_profiles[2]
            player_state = PlayerState(player_id='test_player')
            player_state.add_reputation(profile.governor_id, 10)
            context = {'base_reputation': 2, 'interaction_count': 5}
            
            start_time = time.perf_counter()
            response = self.manager.process_dialog_interaction(
                player_input='I humbly seek your guidance on the sacred mysteries.',
                response_variants=test_variants,
                governor_profile=profile,
                player_state=player_state,
                context=context
            )
            end_time = time.perf_counter()
            
            times.append((end_time - start_time) * 1000)
        
        metrics = self._calculate_metrics("dialog_processing", times, target_ms=25.0)
        self.results.append(metrics)
        
        print(f"   ✅ Dialog Processing: {metrics.avg_time_ms:.2f}ms avg (target: <25ms)")
    
    def _benchmark_concurrent_load(self) -> None:
        """Benchmark performance under concurrent load simulation"""
        print("\n⚡ Benchmarking Concurrent Load...")
        
        times = []
        # Simulate multiple governors being accessed simultaneously
        for _ in range(30):
            start_time = time.perf_counter()
            
            # Process multiple governors in sequence (simulating concurrent requests)
            for profile in self.test_profiles:
                preferences = self.manager.get_governor_preferences(profile)
                summary = self.manager.get_preference_summary(profile.governor_id)
            
            end_time = time.perf_counter()
            times.append((end_time - start_time) * 1000)
        
        metrics = self._calculate_metrics("concurrent_load", times, target_ms=100.0)
        self.results.append(metrics)
        
        print(f"   ✅ Concurrent Load: {metrics.avg_time_ms:.2f}ms avg (target: <100ms)")
    
    def _benchmark_memory_usage(self) -> None:
        """Benchmark memory usage characteristics"""
        print("\n💾 Benchmarking Memory Usage...")
        
        try:
            import psutil
            import os
            
            # Get memory before creating many governors
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Create preferences for many governors
            test_profiles = []
            for i in range(100):
                profile = GovernorProfile(
                    governor_id=f'memory_test_{i}',
                    name=f'Memory Test Governor {i}',
                    traits=['mystical', 'scholarly', 'patient'],
                    preferences={'tone': 'mystical_poetic'}
                )
                test_profiles.append(profile)
                preferences = self.manager.get_governor_preferences(profile)
            
            # Get memory after
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_used = memory_after - memory_before
            
            # Create dummy metrics for memory usage
            metrics = PerformanceMetrics(
                operation_name="memory_usage",
                avg_time_ms=0.0,
                min_time_ms=0.0,
                max_time_ms=0.0,
                std_dev_ms=0.0,
                target_time_ms=0.0,
                meets_target=memory_used <= 100.0,  # Target: <100MB for 100 governors
                memory_usage_mb=memory_used
            )
            self.results.append(metrics)
            
            print(f"   ✅ Memory Usage: {memory_used:.2f}MB for 100 governors (target: <100MB)")
            
        except ImportError:
            print("   ⚠️  psutil not available, skipping memory benchmark")
    
    def _generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        report = {
            'timestamp': time.time(),
            'total_benchmarks': len(self.results),
            'passed_benchmarks': sum(1 for r in self.results if r.meets_target),
            'failed_benchmarks': sum(1 for r in self.results if not r.meets_target),
            'detailed_results': [
                {
                    'operation': r.operation_name,
                    'avg_time_ms': r.avg_time_ms,
                    'target_ms': r.target_time_ms,
                    'meets_target': r.meets_target,
                    'memory_mb': r.memory_usage_mb
                }
                for r in self.results
            ]
        }
        
        return report


def main():
    """Run performance benchmarks"""
    benchmark = PerformanceBenchmark()
    results = benchmark.run_all_benchmarks()
    
    # Print final results
    print("\n" + "="*60)
    print("📊 PERFORMANCE BENCHMARK RESULTS")
    print("="*60)
    
    for metric in benchmark.results:
        status = "✅ PASS" if metric.meets_target else "❌ FAIL"
        if metric.memory_usage_mb > 0:
            print(f"{status} {metric.operation_name}: {metric.memory_usage_mb:.2f}MB")
        else:
            print(f"{status} {metric.operation_name}: {metric.avg_time_ms:.2f}ms (target: <{metric.target_time_ms}ms)")
    
    # Overall assessment
    passed = sum(1 for m in benchmark.results if m.meets_target)
    total = len(benchmark.results)
    print(f"\n📈 Overall: {passed}/{total} benchmarks passed")
    
    if passed == total:
        print("🎉 All performance targets met!")
    else:
        print("⚠️  Performance optimization needed")


if __name__ == "__main__":
    main() 