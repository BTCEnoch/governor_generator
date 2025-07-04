#!/usr/bin/env python3
"""
Production Readiness Assessment
==============================

This script evaluates the current state of the Enochian Governor system
and identifies what needs to be completed before production deployment.

Based on the comprehensive review feedback, this will assess:
1. System Integration Completeness
2. Performance and Scalability 
3. Data Consistency and Consolidation
4. Storyline Generation Status
5. UI/UX Implementation Status
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

@dataclass
class AssessmentResult:
    """Result of a specific assessment check."""
    component: str
    status: str  # 'complete', 'partial', 'missing', 'needs_work'
    score: float  # 0.0 to 1.0
    details: str
    priority: str  # 'critical', 'high', 'medium', 'low'
    estimated_work: str  # time estimate
    dependencies: List[str]

class ProductionReadinessAssessment:
    """
    Comprehensive assessment of production readiness.
    """
    
    def __init__(self):
        """Initialize the assessment system."""
        self.project_root = Path(__file__).parent.parent
        self.results: List[AssessmentResult] = []
        self.overall_score = 0.0
        self.critical_blockers: List[str] = []
        
        print("🔍 Production Readiness Assessment")
        print("=" * 50)
    
    def assess_content_generation(self) -> AssessmentResult:
        """Assess the completeness of content generation."""
        print("\n📊 Assessing Content Generation...")
        
        try:
            # Check governor profiles
            canon_file = self.project_root / "canon" / "canon_governor_profiles.json"
            if canon_file.exists():
                with open(canon_file, 'r') as f:
                    governors = json.load(f)
                governor_count = len(governors)
                print(f"✅ Found {governor_count} governor profiles")
            else:
                return AssessmentResult(
                    component="Content Generation",
                    status="missing",
                    score=0.0,
                    details="Canon governor profiles file not found",
                    priority="critical",
                    estimated_work="1-2 weeks",
                    dependencies=[]
                )
            
            # Check governor output files
            output_dir = self.project_root / "governor_output"
            output_files = list(output_dir.glob("*.json")) if output_dir.exists() else []
            print(f"✅ Found {len(output_files)} governor output files")
            
            # Check storyline files (these are likely missing based on review)
            storyline_dir = self.project_root / "storyline_output_v3_batch"
            storyline_files = list(storyline_dir.glob("*.json")) if storyline_dir.exists() else []
            print(f"⚠️  Found {len(storyline_files)} storyline files")
            
            # Calculate score
            content_score = 0.0
            if governor_count >= 91:
                content_score += 0.4  # Governor profiles complete
            if len(output_files) >= 91:
                content_score += 0.3  # Governor interviews complete  
            if len(storyline_files) >= 91:
                content_score += 0.3  # Storyline generation complete
            else:
                self.critical_blockers.append("Storyline generation incomplete")
            
            status = "complete" if content_score >= 0.9 else "partial" if content_score >= 0.5 else "needs_work"
            
            return AssessmentResult(
                component="Content Generation", 
                status=status,
                score=content_score,
                details=f"Governors: {governor_count}/91, Interviews: {len(output_files)}/91, Storylines: {len(storyline_files)}/91",
                priority="critical" if len(storyline_files) < 91 else "medium",
                estimated_work="1-2 weeks" if len(storyline_files) < 91 else "Complete",
                dependencies=["Governor profiles", "Storyline template"]
            )
            
        except Exception as e:
            return AssessmentResult(
                component="Content Generation",
                status="missing", 
                score=0.0,
                details=f"Assessment failed: {e}",
                priority="critical",
                estimated_work="Unknown",
                dependencies=[]
            )
    
    def assess_system_integration(self) -> AssessmentResult:
        """Assess how well different systems are integrated."""
        print("\n🔗 Assessing System Integration...")
        
        integration_score = 0.0
        details = []
        
        try:
            # Check dialog system integration
            dialog_files = [
                "game_mechanics/dialog_system/__init__.py",
                "game_mechanics/dialog_system/governor_preferences.py", 
                "game_mechanics/dialog_system/trait_mapper.py"
            ]
            
            dialog_complete = all((self.project_root / f).exists() for f in dialog_files)
            if dialog_complete:
                integration_score += 0.3
                details.append("✅ Dialog system implemented")
            else:
                details.append("❌ Dialog system incomplete")
            
            # Check storyline engine integration
            storyline_files = [
                "storyline_engine/batch_storyline_generator.py",
                "storyline_engine/semantic_knowledge_integrator.py"
            ]
            
            storyline_complete = all((self.project_root / f).exists() for f in storyline_files)
            if storyline_complete:
                integration_score += 0.3
                details.append("✅ Storyline engine implemented")
            else:
                details.append("❌ Storyline engine incomplete")
            
            # Check knowledge base integration
            kb_files = [
                "knowledge_base/traditions/unified_knowledge_retriever.py",
                "knowledge_base/retrievers/focused_mystical_retriever.py"
            ]
            
            kb_complete = all((self.project_root / f).exists() for f in kb_files)
            if kb_complete:
                integration_score += 0.2
                details.append("✅ Knowledge base implemented")
            else:
                details.append("❌ Knowledge base incomplete")
            
            # Check expansion system UI
            expansion_files = [
                "game_mechanics/expansion_system/ui/dynamic_menu.py",
                "game_mechanics/expansion_system/ui/progressive_loading.py"
            ]
            
            expansion_complete = all((self.project_root / f).exists() for f in expansion_files)
            if expansion_complete:
                integration_score += 0.2
                details.append("✅ Expansion UI implemented")
            else:
                details.append("❌ Expansion UI incomplete")
                self.critical_blockers.append("Progressive loading UI missing")
            
            status = "complete" if integration_score >= 0.9 else "partial" if integration_score >= 0.6 else "needs_work"
            
            return AssessmentResult(
                component="System Integration",
                status=status,
                score=integration_score,
                details=" | ".join(details),
                priority="high",
                estimated_work="2-3 weeks" if integration_score < 0.6 else "1 week",
                dependencies=["Dialog system", "Storyline engine", "Knowledge base"]
            )
            
        except Exception as e:
            return AssessmentResult(
                component="System Integration",
                status="missing",
                score=0.0,
                details=f"Assessment failed: {e}",
                priority="critical",
                estimated_work="Unknown",
                dependencies=[]
            )
    
    def assess_performance_readiness(self) -> AssessmentResult:
        """Assess performance optimization and benchmarking."""
        print("\n⚡ Assessing Performance Readiness...")
        
        performance_score = 0.0
        details = []
        
        try:
            # Check if performance benchmarks exist
            benchmark_file = self.project_root / "tests" / "performance_benchmark.py"
            if benchmark_file.exists():
                performance_score += 0.4
                details.append("✅ Performance benchmarks implemented")
            else:
                details.append("❌ Performance benchmarks missing")
            
            # Check cache optimization
            cache_file = self.project_root / "game_mechanics" / "dialog_system" / "cache_optimizer.py"
            if cache_file.exists():
                performance_score += 0.3
                details.append("✅ Cache optimization implemented") 
            else:
                details.append("❌ Cache optimization missing")
            
            # Check progressive loading implementation
            progressive_file = self.project_root / "game_mechanics" / "expansion_system" / "ui" / "progressive_loading.py"
            if progressive_file.exists():
                performance_score += 0.3
                details.append("✅ Progressive loading implemented")
            else:
                details.append("❌ Progressive loading missing")
                self.critical_blockers.append("Progressive loading not implemented")
            
            status = "complete" if performance_score >= 0.9 else "partial" if performance_score >= 0.5 else "needs_work"
            
            return AssessmentResult(
                component="Performance Readiness",
                status=status,
                score=performance_score,
                details=" | ".join(details),
                priority="high",
                estimated_work="1-2 weeks" if performance_score < 0.5 else "Fine-tuning",
                dependencies=["Cache system", "Progressive loading", "Benchmarks"]
            )
            
        except Exception as e:
            return AssessmentResult(
                component="Performance Readiness",
                status="missing",
                score=0.0,
                details=f"Assessment failed: {e}",
                priority="high", 
                estimated_work="Unknown",
                dependencies=[]
            )
    
    def assess_data_consistency(self) -> AssessmentResult:
        """Assess data consistency and single source of truth."""
        print("\n📋 Assessing Data Consistency...")
        
        consistency_score = 0.0
        details = []
        issues = []
        
        try:
            # Check for redundant or conflicting data sources
            canon_sources = [
                "canon/canon_governor_profiles.json",
                "canon/91_governors_canon.json", 
                "governor_indexes/canonical_traits.json"
            ]
            
            existing_sources = [s for s in canon_sources if (self.project_root / s).exists()]
            if len(existing_sources) >= 2:
                consistency_score += 0.3
                details.append(f"✅ Found {len(existing_sources)} data sources")
            else:
                details.append("❌ Insufficient canonical data sources")
                issues.append("Missing canonical data sources")
            
            # Check trait consistency between sources  
            trait_files = [
                "governor_indexes/virtues_pool.json",
                "governor_indexes/flaws_pool.json",
                "governor_indexes/canonical_traits.json"
            ]
            
            trait_consistency = all((self.project_root / f).exists() for f in trait_files)
            if trait_consistency:
                consistency_score += 0.3
                details.append("✅ Trait indexes consistent")
            else:
                details.append("❌ Trait indexes incomplete")
                issues.append("Trait data sources incomplete")
            
            # Check for deprecated/legacy files
            legacy_patterns = ["*_old", "*_backup", "*_deprecated", "debug_*", "test_*"]
            legacy_files = []
            for pattern in legacy_patterns:
                legacy_files.extend(self.project_root.glob(f"**/{pattern}"))
            
            if len(legacy_files) < 10:  # Some test files are okay
                consistency_score += 0.2
                details.append("✅ Minimal legacy files")
            else:
                details.append(f"⚠️  Found {len(legacy_files)} potential legacy files")
                issues.append("Many legacy files may cause confusion")
            
            # Check knowledge base consistency
            kb_indexes = [
                "knowledge_base/organized_tradition_mapping.json",
                "knowledge_base/unified_knowledge_index.json"
            ]
            
            kb_consistency = all((self.project_root / f).exists() for f in kb_indexes)
            if kb_consistency:
                consistency_score += 0.2
                details.append("✅ Knowledge base indexes present")
            else:
                details.append("❌ Knowledge base indexes missing")
                issues.append("Knowledge base organization incomplete")
            
            if issues:
                self.critical_blockers.extend(issues)
            
            status = "complete" if consistency_score >= 0.8 else "partial" if consistency_score >= 0.5 else "needs_work"
            
            return AssessmentResult(
                component="Data Consistency",
                status=status,
                score=consistency_score,
                details=" | ".join(details),
                priority="medium" if len(issues) == 0 else "high",
                estimated_work="1 week" if len(issues) > 0 else "Maintenance",
                dependencies=["Canonical data", "Trait indexes", "Knowledge base"]
            )
            
        except Exception as e:
            return AssessmentResult(
                component="Data Consistency",
                status="missing",
                score=0.0,
                details=f"Assessment failed: {e}",
                priority="high",
                estimated_work="Unknown",
                dependencies=[]
            )
    
    def assess_ui_ux_readiness(self) -> AssessmentResult:
        """Assess UI/UX implementation status."""
        print("\n🎨 Assessing UI/UX Readiness...")
        
        ui_score = 0.0
        details = []
        
        try:
            # Check expansion system UI components
            ui_components = [
                "game_mechanics/expansion_system/ui/dynamic_menu.py",
                "game_mechanics/expansion_system/ui/progressive_loading.py",
                "game_mechanics/expansion_system/ui/error_recovery.py"
            ]
            
            ui_complete = sum(1 for f in ui_components if (self.project_root / f).exists())
            ui_score += (ui_complete / len(ui_components)) * 0.4
            details.append(f"UI Components: {ui_complete}/{len(ui_components)}")
            
            # Check tarot system UI
            tarot_ui = [
                "mystical_systems/tarot_system/ui/card_render.py"
            ]
            
            tarot_complete = all((self.project_root / f).exists() for f in tarot_ui)
            if tarot_complete:
                ui_score += 0.2
                details.append("✅ Tarot UI implemented")
            else:
                details.append("❌ Tarot UI missing")
            
            # Check for PWA/web components (likely missing)
            web_files = list(self.project_root.glob("**/*.html")) + list(self.project_root.glob("**/*.css"))
            if len(web_files) > 0:
                ui_score += 0.2
                details.append(f"✅ Found {len(web_files)} web files")
            else:
                details.append("❌ No web UI files found")
                self.critical_blockers.append("Web UI not implemented")
            
            # Check CLI interfaces
            cli_files = [
                "cli/mystical_cli.py"
            ]
            
            cli_complete = all((self.project_root / f).exists() for f in cli_files)
            if cli_complete:
                ui_score += 0.2
                details.append("✅ CLI interface available")
            else:
                details.append("❌ CLI interface missing")
            
            status = "complete" if ui_score >= 0.8 else "partial" if ui_score >= 0.4 else "needs_work"
            
            return AssessmentResult(
                component="UI/UX Readiness",
                status=status,
                score=ui_score,
                details=" | ".join(details),
                priority="high" if ui_score < 0.4 else "medium",
                estimated_work="3-4 weeks" if ui_score < 0.4 else "2 weeks",
                dependencies=["Progressive loading", "Web framework", "UI components"]
            )
            
        except Exception as e:
            return AssessmentResult(
                component="UI/UX Readiness",
                status="missing",
                score=0.0,
                details=f"Assessment failed: {e}",
                priority="high",
                estimated_work="Unknown",
                dependencies=[]
            )
    
    def run_full_assessment(self) -> Dict[str, Any]:
        """Run the complete production readiness assessment."""
        
        assessments = [
            self.assess_content_generation,
            self.assess_system_integration,
            self.assess_performance_readiness,
            self.assess_data_consistency,
            self.assess_ui_ux_readiness
        ]
        
        for assessment_func in assessments:
            result = assessment_func()
            self.results.append(result)
        
        # Calculate overall score
        self.overall_score = sum(r.score for r in self.results) / len(self.results)
        
        # Generate summary
        return self.generate_summary()
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive summary of the assessment."""
        
        print("\n" + "=" * 50)
        print("📊 PRODUCTION READINESS SUMMARY")
        print("=" * 50)
        
        # Overall score
        overall_status = "READY" if self.overall_score >= 0.8 else "PARTIAL" if self.overall_score >= 0.6 else "NOT READY"
        print(f"\n🎯 Overall Status: {overall_status}")
        print(f"📈 Overall Score: {self.overall_score:.2f}/1.00")
        
        # Component breakdown
        print(f"\n📋 Component Breakdown:")
        for result in self.results:
            status_emoji = "✅" if result.status == "complete" else "⚠️" if result.status == "partial" else "❌"
            print(f"  {status_emoji} {result.component}: {result.score:.2f} ({result.status})")
        
        # Critical blockers
        if self.critical_blockers:
            print(f"\n🚨 Critical Blockers ({len(self.critical_blockers)}):")
            for blocker in self.critical_blockers:
                print(f"  ❌ {blocker}")
        
        # Priority recommendations
        critical_items = [r for r in self.results if r.priority == "critical"]
        high_items = [r for r in self.results if r.priority == "high"]
        
        print(f"\n🎯 Priority Recommendations:")
        if critical_items:
            print(f"  🔴 Critical ({len(critical_items)} items):")
            for item in critical_items:
                print(f"    • {item.component}: {item.estimated_work}")
        
        if high_items:
            print(f"  🟡 High Priority ({len(high_items)} items):")
            for item in high_items:
                print(f"    • {item.component}: {item.estimated_work}")
        
        # Estimated timeline
        total_critical_weeks = len([r for r in self.results if r.priority == "critical" and "week" in r.estimated_work])
        total_high_weeks = len([r for r in self.results if r.priority == "high" and "week" in r.estimated_work])
        
        print(f"\n⏱️  Estimated Timeline to Production:")
        print(f"  Critical work: ~{total_critical_weeks * 2} weeks")
        print(f"  High priority work: ~{total_high_weeks * 1.5} weeks")
        print(f"  Total estimated: ~{total_critical_weeks * 2 + total_high_weeks * 1.5} weeks")
        
        return {
            "overall_score": self.overall_score,
            "overall_status": overall_status,
            "critical_blockers": self.critical_blockers,
            "component_results": [
                {
                    "component": r.component,
                    "status": r.status,
                    "score": r.score,
                    "priority": r.priority,
                    "estimated_work": r.estimated_work
                } for r in self.results
            ],
            "estimated_weeks": total_critical_weeks * 2 + total_high_weeks * 1.5,
            "timestamp": datetime.now().isoformat()
        }

def main():
    """Run the production readiness assessment."""
    assessment = ProductionReadinessAssessment()
    summary = assessment.run_full_assessment()
    
    # Save results
    output_file = Path("production_readiness_report.json")
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Detailed report saved to: {output_file}")
    print("\n🚀 Next: Review critical blockers and prioritize development work!")

if __name__ == "__main__":
    main() 