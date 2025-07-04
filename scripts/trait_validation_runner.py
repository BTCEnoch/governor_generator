#!/usr/bin/env python3
"""
Governor Trait Validation Runner
===============================

This script provides a comprehensive system for checking and adjusting governor traits
using the existing dialog system infrastructure. It validates trait mappings, 
behavioral preferences, and suggests improvements.

Usage:
    python scripts/trait_validation_runner.py --governor OCCODON
    python scripts/trait_validation_runner.py --all
    python scripts/trait_validation_runner.py --batch governors.txt
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json
from dataclasses import asdict

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from game_mechanics.dialog_system import (
    GovernorPreferencesManager,
    GovernorProfile,
    PreferenceEncoder,
    TraitMapper,
    BehavioralFilter,
    GovernorPreferences,
    TonePreference,
    InteractionType
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trait_validation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TraitValidationRunner:
    """
    Main orchestrator for governor trait validation and adjustment processes.
    
    This class provides comprehensive validation of governor traits, behavioral
    preferences, and integration with the dialog system infrastructure.
    """
    
    def __init__(self, output_dir: str = "validation_output"):
        """
        Initialize the trait validation runner.
        
        Args:
            output_dir: Directory to store validation results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize dialog system components
        self.preferences_manager = GovernorPreferencesManager()
        self.trait_mapper = TraitMapper()
        self.preference_encoder = PreferenceEncoder()
        self.behavioral_filter = BehavioralFilter()
        
        # Load governor data
        self.governor_data = self._load_governor_data()
        
        # Initialize validation results
        self.validation_results: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"TraitValidationRunner initialized with {len(self.governor_data)} governors")
    
    def validate_single_governor(self, governor_name: str) -> Dict[str, Any]:
        """
        Validate traits and preferences for a single governor.
        
        Args:
            governor_name: Name of the governor to validate
            
        Returns:
            Validation results dictionary
        """
        logger.info(f"Validating governor: {governor_name}")
        
        if governor_name not in self.governor_data:
            logger.error(f"Governor {governor_name} not found in data")
            return {"error": f"Governor {governor_name} not found"}
        
        governor_info = self.governor_data[governor_name]
        
        try:
            # Step 1: Create GovernorProfile from data
            profile = self._create_governor_profile(governor_name, governor_info)
            
            # Step 2: Validate trait mappings
            trait_validation = self._validate_trait_mappings(profile)
            
            # Step 3: Generate and validate preferences
            preference_validation = self._validate_preferences(profile)
            
            # Step 4: Check behavioral consistency
            behavioral_validation = self._validate_behavioral_consistency(profile)
            
            # Step 5: Performance validation
            performance_validation = self._validate_performance(profile)
            
            # Compile results
            validation_result = {
                "governor_name": governor_name,
                "status": "completed",
                "trait_validation": trait_validation,
                "preference_validation": preference_validation,
                "behavioral_validation": behavioral_validation,
                "performance_validation": performance_validation,
                "timestamp": self._get_timestamp()
            }
            
            self.validation_results[governor_name] = validation_result
            logger.info(f"Validation completed for {governor_name}")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Validation failed for {governor_name}: {e}")
            error_result = {
                "governor_name": governor_name,
                "status": "failed",
                "error": str(e),
                "timestamp": self._get_timestamp()
            }
            self.validation_results[governor_name] = error_result
            return error_result
    
    def validate_all_governors(self) -> Dict[str, Dict[str, Any]]:
        """
        Validate all governors in the dataset.
        
        Returns:
            Dictionary of all validation results
        """
        logger.info(f"Starting validation of all {len(self.governor_data)} governors")
        
        for governor_name in self.governor_data.keys():
            self.validate_single_governor(governor_name)
        
        logger.info("Completed validation of all governors")
        return self.validation_results
    
    def validate_batch_from_file(self, file_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Validate governors listed in a file.
        
        Args:
            file_path: Path to file containing governor names (one per line)
            
        Returns:
            Dictionary of validation results
        """
        logger.info(f"Starting batch validation from file: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                governor_names = [line.strip() for line in f if line.strip()]
            
            logger.info(f"Found {len(governor_names)} governors in batch file")
            
            for governor_name in governor_names:
                self.validate_single_governor(governor_name)
            
            logger.info("Completed batch validation")
            return self.validation_results
            
        except FileNotFoundError:
            logger.error(f"Batch file not found: {file_path}")
            return {"batch_error": {"error": f"Batch file not found: {file_path}"}}
        except Exception as e:
            logger.error(f"Batch validation failed: {e}")
            return {"batch_error": {"error": f"Batch validation failed: {e}"}}
    
    def _load_governor_data(self) -> Dict[str, Any]:
        """
        Load governor data from the canonical sources.
        
        Returns:
            Dictionary of governor data
        """
        try:
            # Load from canon profiles
            canon_file = Path("canon/canon_governor_profiles.json")
            if canon_file.exists():
                with open(canon_file, 'r') as f:
                    canon_list = json.load(f)
                
                # Convert list to dictionary keyed by governor name
                canon_data = {}
                for governor in canon_list:
                    if "governor_info" in governor and "name" in governor["governor_info"]:
                        governor_name = governor["governor_info"]["name"]
                        canon_data[governor_name] = governor
                
                logger.info(f"Loaded {len(canon_data)} governors from canon profiles")
                return canon_data
            
            # Fallback to governor output directory
            output_dir = Path("governor_output")
            if output_dir.exists():
                governor_data = {}
                for json_file in output_dir.glob("*.json"):
                    governor_name = json_file.stem
                    with open(json_file, 'r') as f:
                        governor_data[governor_name] = json.load(f)
                logger.info(f"Loaded {len(governor_data)} governors from output directory")
                return governor_data
            
            logger.warning("No governor data found")
            return {}
            
        except Exception as e:
            logger.error(f"Failed to load governor data: {e}")
            return {}
    
    def _create_governor_profile(self, governor_name: str, governor_info: Dict[str, Any]) -> GovernorProfile:
        """
        Create a GovernorProfile from raw governor data.
        
        Args:
            governor_name: Name of the governor
            governor_info: Raw governor data
            
        Returns:
            GovernorProfile object
        """
        try:
            # Extract traits from different possible locations
            traits = []
            
            # Check trait_choices structure
            if "trait_choices" in governor_info:
                trait_choices = governor_info["trait_choices"]
                if "virtues" in trait_choices:
                    traits.extend(trait_choices["virtues"])
                if "flaws" in trait_choices:
                    traits.extend(trait_choices["flaws"])
            
            # Check canonical_data structure  
            if "canonical_data" in governor_info and "traits" in governor_info["canonical_data"]:
                traits.extend(governor_info["canonical_data"]["traits"])
            
            # Extract preferences
            preferences = {}
            if "trait_choices" in governor_info:
                trait_choices = governor_info["trait_choices"]
                if "baseline_tone" in trait_choices:
                    preferences["tone"] = trait_choices["baseline_tone"]
                if "baseline_approach" in trait_choices:
                    preferences["approach"] = trait_choices["baseline_approach"]
            
            # Create profile
            profile = GovernorProfile(
                governor_id=governor_name,
                name=governor_name,
                traits=traits,
                preferences=preferences,
                interaction_models=[InteractionType.RIDDLE_KEEPER, InteractionType.CEREMONIAL_GOVERNOR],
                reputation_thresholds={
                    0: "basic_interactions",
                    5: "intermediate_content", 
                    10: "advanced_content",
                    15: "secret_knowledge",
                    20: "master_level"
                }
            )
            
            return profile
            
        except Exception as e:
            logger.error(f"Failed to create profile for {governor_name}: {e}")
            # Return minimal profile on error
            return GovernorProfile(
                governor_id=governor_name,
                name=governor_name,
                traits=[],
                preferences={}
            )
    
    def _validate_trait_mappings(self, profile: GovernorProfile) -> Dict[str, Any]:
        """
        Validate trait mappings for a governor profile.
        
        Args:
            profile: Governor profile to validate
            
        Returns:
            Validation results dictionary
        """
        try:
            results = {
                "total_traits": len(profile.traits),
                "mapped_traits": 0,
                "unmapped_traits": [],
                "mapping_conflicts": [],
                "trait_details": {}
            }
            
            # Check each trait for mappings
            for trait in profile.traits:
                trait_mapping = self.trait_mapper.get_trait_mapping(trait)
                if trait_mapping:
                    results["mapped_traits"] += 1
                    results["trait_details"][trait] = {
                        "mapped": True,
                        "behavior_type": trait_mapping.behavior_type.value,
                        "effect_strength": trait_mapping.effect_strength,
                        "parameter_count": len(trait_mapping.parameter_modifications)
                    }
                else:
                    results["unmapped_traits"].append(trait)
                    results["trait_details"][trait] = {
                        "mapped": False,
                        "suggestion": f"Consider adding mapping for '{trait}' trait"
                    }
            
            # Check for conflicts
            trait_mappings = self.trait_mapper.get_all_mappings_for_traits(profile.traits)
            trait_weights = {trait: 1.0 / len(profile.traits) for trait in profile.traits}
            conflicts = self.trait_mapper.resolve_parameter_conflicts(trait_mappings, trait_weights)
            
            results["mapping_conflicts"] = [
                {
                    "parameter": param,
                    "resolved_value": value
                }
                for param, value in conflicts.items()
            ]
            
            results["validation_status"] = "passed" if results["mapped_traits"] > 0 else "warning"
            
            return results
            
        except Exception as e:
            logger.error(f"Trait mapping validation failed for {profile.governor_id}: {e}")
            return {
                "validation_status": "failed",
                "error": str(e),
                "total_traits": len(profile.traits),
                "mapped_traits": 0
            }
    
    def _validate_preferences(self, profile: GovernorProfile) -> Dict[str, Any]:
        """
        Validate behavioral preferences for a governor profile.
        
        Args:
            profile: Governor profile to validate
            
        Returns:
            Validation results dictionary
        """
        try:
            # Generate preferences using the preferences manager
            preferences = self.preferences_manager.get_governor_preferences(profile)
            
            results = {
                "governor_id": preferences.governor_id,
                "tone_preference": preferences.tone_preference.value,
                "interaction_style": preferences.interaction_style,
                "behavioral_parameters": {
                    "greeting_formality": preferences.greeting_formality,
                    "puzzle_difficulty": preferences.puzzle_difficulty.value,
                    "response_patience": preferences.response_patience,
                    "metaphor_tolerance": preferences.metaphor_tolerance,
                    "reputation_sensitivity": preferences.reputation_sensitivity
                },
                "word_analysis": {
                    "trigger_words_count": len(preferences.trigger_words),
                    "forbidden_words_count": len(preferences.forbidden_words),
                    "preferred_topics_count": len(preferences.preferred_topics),
                    "trigger_words": preferences.trigger_words[:5],  # Show first 5
                    "forbidden_words": preferences.forbidden_words[:5]  # Show first 5
                },
                "behavioral_modifiers_count": len(preferences.behavioral_modifiers),
                "validation_status": "passed"
            }
            
            # Validate parameter ranges
            parameter_issues = []
            float_params = {
                "greeting_formality": preferences.greeting_formality,
                "response_patience": preferences.response_patience,
                "metaphor_tolerance": preferences.metaphor_tolerance,
                "reputation_sensitivity": preferences.reputation_sensitivity
            }
            
            for param_name, value in float_params.items():
                if not (0.0 <= value <= 1.0):
                    parameter_issues.append(f"{param_name}: {value} (should be 0.0-1.0)")
            
            if parameter_issues:
                results["validation_status"] = "warning"
                results["parameter_issues"] = parameter_issues
            
            return results
            
        except Exception as e:
            logger.error(f"Preference validation failed for {profile.governor_id}: {e}")
            return {
                "validation_status": "failed",
                "error": str(e),
                "governor_id": profile.governor_id
            }
    
    def _validate_behavioral_consistency(self, profile: GovernorProfile) -> Dict[str, Any]:
        """
        Validate behavioral consistency for a governor profile.
        
        Args:
            profile: Governor profile to validate
            
        Returns:
            Validation results dictionary
        """
        try:
            # Get preferences for consistency checking
            preferences = self.preferences_manager.get_governor_preferences(profile)
            
            results = {
                "consistency_checks": [],
                "inconsistencies": [],
                "recommendations": [],
                "validation_status": "passed"
            }
            
            # Check tone vs traits consistency
            tone_trait_consistency = self._check_tone_trait_consistency(profile.traits, preferences.tone_preference)
            results["consistency_checks"].append({
                "check": "tone_trait_consistency",
                "result": tone_trait_consistency
            })
            
            # Check formality vs traits consistency
            formality_consistency = self._check_formality_consistency(profile.traits, preferences.greeting_formality)
            results["consistency_checks"].append({
                "check": "formality_consistency", 
                "result": formality_consistency
            })
            
            # Check patience vs traits consistency
            patience_consistency = self._check_patience_consistency(profile.traits, preferences.response_patience)
            results["consistency_checks"].append({
                "check": "patience_consistency",
                "result": patience_consistency
            })
            
            # Determine overall status
            failed_checks = [check for check in results["consistency_checks"] if not check["result"]["consistent"]]
            if failed_checks:
                results["validation_status"] = "warning"
                results["inconsistencies"] = [check["result"]["issue"] for check in failed_checks]
                results["recommendations"] = [check["result"]["recommendation"] for check in failed_checks]
            
            return results
            
        except Exception as e:
            logger.error(f"Behavioral consistency validation failed for {profile.governor_id}: {e}")
            return {
                "validation_status": "failed",
                "error": str(e),
                "governor_id": profile.governor_id
            }
    
    def _validate_performance(self, profile: GovernorProfile) -> Dict[str, Any]:
        """
        Validate performance characteristics for a governor profile.
        
        Args:
            profile: Governor profile to validate
            
        Returns:
            Validation results dictionary
        """
        try:
            import time
            
            results = {
                "performance_metrics": {},
                "benchmarks": {},
                "validation_status": "passed"
            }
            
            # Test preference generation performance
            start_time = time.perf_counter()
            preferences = self.preferences_manager.get_governor_preferences(profile)
            preference_time = (time.perf_counter() - start_time) * 1000  # Convert to ms
            
            results["performance_metrics"]["preference_generation_ms"] = preference_time
            results["benchmarks"]["preference_generation"] = {
                "time_ms": preference_time,
                "target_ms": 50.0,
                "passed": preference_time < 50.0
            }
            
            # Test trait mapping performance
            start_time = time.perf_counter()
            trait_mappings = self.trait_mapper.get_all_mappings_for_traits(profile.traits)
            mapping_time = (time.perf_counter() - start_time) * 1000
            
            results["performance_metrics"]["trait_mapping_ms"] = mapping_time
            results["benchmarks"]["trait_mapping"] = {
                "time_ms": mapping_time,
                "target_ms": 10.0,
                "passed": mapping_time < 10.0
            }
            
            # Test response filtering performance
            start_time = time.perf_counter()
            test_content = "This is a test message for performance validation."
            filter_result = self.behavioral_filter.filter_content_by_preferences(test_content, preferences)
            filtering_time = (time.perf_counter() - start_time) * 1000
            
            results["performance_metrics"]["content_filtering_ms"] = filtering_time
            results["benchmarks"]["content_filtering"] = {
                "time_ms": filtering_time,
                "target_ms": 5.0,
                "passed": filtering_time < 5.0
            }
            
            # Overall performance assessment
            failed_benchmarks = [name for name, bench in results["benchmarks"].items() if not bench["passed"]]
            if failed_benchmarks:
                results["validation_status"] = "warning"
                results["failed_benchmarks"] = failed_benchmarks
            
            return results
            
        except Exception as e:
            logger.error(f"Performance validation failed for {profile.governor_id}: {e}")
            return {
                "validation_status": "failed",
                "error": str(e),
                "governor_id": profile.governor_id
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _check_tone_trait_consistency(self, traits: List[str], tone_preference: TonePreference) -> Dict[str, Any]:
        """Check if tone preference is consistent with traits."""
        # Define trait-tone compatibility
        tone_trait_mappings = {
            TonePreference.SOLEMN_CRYPTIC: ['cryptic', 'mysterious', 'stern', 'formal'],
            TonePreference.MYSTICAL_POETIC: ['mystical', 'poetic', 'wise', 'spiritual'],
            TonePreference.SCHOLARLY_PATIENT: ['scholarly', 'patient', 'methodical', 'wise'],
            TonePreference.STERN_FORMAL: ['stern', 'formal', 'disciplined', 'authoritative'],
            TonePreference.PLAYFUL_RIDDLES: ['playful', 'clever', 'humorous', 'creative'],
            TonePreference.WARM_ENCOURAGING: ['compassionate', 'encouraging', 'supportive', 'gentle'],
            TonePreference.ENIGMATIC_BRIEF: ['enigmatic', 'brief', 'mysterious', 'cryptic'],
            TonePreference.COLD_DISTANT: ['cold', 'distant', 'aloof', 'detached']
        }
        
        compatible_traits = tone_trait_mappings.get(tone_preference, [])
        trait_matches = [trait for trait in traits if trait.lower() in compatible_traits]
        
        consistency_score = len(trait_matches) / len(traits) if traits else 0
        
        return {
            "consistent": consistency_score >= 0.3,  # At least 30% of traits should match
            "score": consistency_score,
            "matching_traits": trait_matches,
            "issue": f"Tone {tone_preference.value} doesn't match traits well" if consistency_score < 0.3 else None,
            "recommendation": f"Consider traits like {compatible_traits[:3]} for {tone_preference.value}" if consistency_score < 0.3 else None
        }
    
    def _check_formality_consistency(self, traits: List[str], formality_level: float) -> Dict[str, Any]:
        """Check if formality level is consistent with traits."""
        formal_traits = ['formal', 'stern', 'disciplined', 'methodical', 'scholarly']
        informal_traits = ['playful', 'casual', 'spontaneous', 'irreverent']
        
        formal_count = sum(1 for trait in traits if trait.lower() in formal_traits)
        informal_count = sum(1 for trait in traits if trait.lower() in informal_traits)
        
        expected_formality = 0.5  # Default
        if formal_count > informal_count:
            expected_formality = 0.7 + (formal_count * 0.1)
        elif informal_count > formal_count:
            expected_formality = 0.3 - (informal_count * 0.1)
        
        expected_formality = max(0.0, min(1.0, expected_formality))
        formality_diff = abs(formality_level - expected_formality)
        
        return {
            "consistent": formality_diff <= 0.3,
            "expected_formality": expected_formality,
            "actual_formality": formality_level,
            "difference": formality_diff,
            "issue": f"Formality {formality_level:.2f} doesn't match traits (expected ~{expected_formality:.2f})" if formality_diff > 0.3 else None,
            "recommendation": f"Adjust formality to {expected_formality:.2f} based on traits" if formality_diff > 0.3 else None
        }
    
    def _check_patience_consistency(self, traits: List[str], patience_level: float) -> Dict[str, Any]:
        """Check if patience level is consistent with traits."""
        patient_traits = ['patient', 'methodical', 'wise', 'contemplative', 'scholarly']
        impatient_traits = ['impulsive', 'quick', 'hasty', 'restless', 'energetic']
        
        patient_count = sum(1 for trait in traits if trait.lower() in patient_traits)
        impatient_count = sum(1 for trait in traits if trait.lower() in impatient_traits)
        
        expected_patience = 0.5  # Default
        if patient_count > impatient_count:
            expected_patience = 0.7 + (patient_count * 0.1)
        elif impatient_count > patient_count:
            expected_patience = 0.3 - (impatient_count * 0.1)
        
        expected_patience = max(0.0, min(1.0, expected_patience))
        patience_diff = abs(patience_level - expected_patience)
        
        return {
            "consistent": patience_diff <= 0.3,
            "expected_patience": expected_patience,
            "actual_patience": patience_level,
            "difference": patience_diff,
            "issue": f"Patience {patience_level:.2f} doesn't match traits (expected ~{expected_patience:.2f})" if patience_diff > 0.3 else None,
            "recommendation": f"Adjust patience to {expected_patience:.2f} based on traits" if patience_diff > 0.3 else None
        }
    
    def generate_report(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive validation report.
        
        Args:
            output_file: Optional file path to save the report
            
        Returns:
            Complete validation report
        """
        report = {
            "validation_summary": {
                "total_governors": len(self.validation_results),
                "passed": len([r for r in self.validation_results.values() if r.get("status") == "completed"]),
                "failed": len([r for r in self.validation_results.values() if r.get("status") == "failed"]),
                "timestamp": self._get_timestamp()
            },
            "system_status": self.preferences_manager.get_system_status(),
            "detailed_results": self.validation_results
        }
        
        if output_file:
            output_path = self.output_dir / output_file
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"Report saved to {output_path}")
        
        return report


def main():
    """Main execution function for the trait validation runner."""
    parser = argparse.ArgumentParser(description="Governor Trait Validation Runner")
    parser.add_argument("--governor", type=str, help="Validate specific governor")
    parser.add_argument("--all", action="store_true", help="Validate all governors")
    parser.add_argument("--batch", type=str, help="Validate governors from file")
    parser.add_argument("--output", type=str, default="validation_output", help="Output directory")
    parser.add_argument("--report", type=str, help="Generate report file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create output directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    try:
        # Initialize the validation runner
        runner = TraitValidationRunner(output_dir=args.output)
        
        # Execute validation based on arguments
        if args.governor:
            print(f"🔍 Validating governor: {args.governor}")
            result = runner.validate_single_governor(args.governor)
            print(f"✅ Validation completed for {args.governor}")
            print(f"Status: {result.get('status', 'unknown')}")
            
        elif args.all:
            print("🔍 Validating all governors...")
            results = runner.validate_all_governors()
            print(f"✅ Validation completed for all governors")
            print(f"Total: {len(results)}")
            
        elif args.batch:
            print(f"🔍 Validating governors from batch file: {args.batch}")
            results = runner.validate_batch_from_file(args.batch)
            print(f"✅ Batch validation completed")
            print(f"Total: {len(results)}")
            
        else:
            print("❌ Please specify --governor, --all, or --batch")
            parser.print_help()
            return
        
        # Generate report if requested
        if args.report:
            print(f"📊 Generating report: {args.report}")
            report = runner.generate_report(args.report)
            print(f"✅ Report generated: {args.report}")
            
            # Print summary
            summary = report["validation_summary"]
            print(f"\n📋 Summary:")
            print(f"  Total governors: {summary['total_governors']}")
            print(f"  Passed: {summary['passed']}")
            print(f"  Failed: {summary['failed']}")
    
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        print(f"❌ Execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 