#!/usr/bin/env python3
"""
Production Readiness Assessment Runner
Quick way to run the complete production assessment
"""

def main():
    """Run complete production readiness assessment"""
    
    print("🚀 STORYLINE ENGINE PRODUCTION READINESS")
    print("=" * 50)
    print("Running chunked assessment...\n")
    
    try:
        from production_readiness_summary import overall_production_assessment, production_deployment_roadmap, quick_wins
        
        # Run complete assessment
        score, component_scores = overall_production_assessment()
        production_deployment_roadmap(score, component_scores)
        quick_wins()
        
        print(f"\n🎯 SUMMARY: {score:.0f}% Production Ready")
        
        if score >= 70:
            print("✅ Engine ready for deployment!")
        elif score >= 50:
            print("⚠️ Engine needs improvements before production")
        else:
            print("❌ Engine requires significant development")
            
    except ImportError as e:
        print(f"❌ Assessment modules not found: {e}")
        print("Make sure all readiness assessment files are present.")
    except Exception as e:
        print(f"❌ Assessment failed: {e}")

if __name__ == "__main__":
    main() 