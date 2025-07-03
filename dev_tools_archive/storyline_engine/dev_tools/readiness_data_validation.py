#!/usr/bin/env python3
"""
Data Validation & Quality Assurance Assessment
Evaluates data handling and validation readiness
"""

from pathlib import Path
import json

def assess_data_validation():
    """Assess data validation and quality assurance readiness"""
    
    print("🔍 DATA VALIDATION ASSESSMENT")
    print("=" * 40)
    
    # Check current capabilities
    data_capabilities = {
        "governor_data_loading": {
            "status": "✅ READY",
            "details": "Safe JSON loading with error handling",
            "confidence": 85
        },
        "input_validation": {
            "status": "❌ MISSING",
            "details": "No schema validation for governor data",
            "confidence": 30
        },
        "output_validation": {
            "status": "❌ MISSING", 
            "details": "No storyline schema validation",
            "confidence": 25
        },
        "canonical_accuracy": {
            "status": "⚠️ PARTIAL",
            "details": "Basic canonical loading but no validation",
            "confidence": 50
        },
        "completeness_checks": {
            "status": "⚠️ PARTIAL",
            "details": "Basic Q&A counting but no semantic validation",
            "confidence": 45
        }
    }
    
    print("\n📋 DATA VALIDATION COMPONENTS:")
    total_confidence = 0
    critical_issues = []
    
    for component, assessment in data_capabilities.items():
        print(f"   {component:20} {assessment['status']}")
        print(f"   {'':20} {assessment['details']}")
        print(f"   {'':20} Confidence: {assessment['confidence']}%\n")
        total_confidence += assessment['confidence']
        
        if assessment['confidence'] < 50:
            critical_issues.append(component)
    
    avg_confidence = total_confidence / len(data_capabilities)
    
    print(f"🎯 DATA VALIDATION: {avg_confidence:.0f}% Ready")
    
    if critical_issues:
        print(f"\n❌ CRITICAL ISSUES ({len(critical_issues)}):")
        for issue in critical_issues:
            print(f"   - {issue}")
    
    if avg_confidence >= 70:
        print("✅ Data validation is production ready")
        return True
    else:
        print("⚠️ Data validation needs significant work")
        return False

def recommend_data_validation_fixes():
    """Recommend specific fixes for data validation"""
    
    print("\n💡 RECOMMENDED FIXES:")
    print("1. Add JSON schema validation for governor input")
    print("2. Add storyline output schema validation")
    print("3. Implement canonical accuracy checks")
    print("4. Add semantic completeness validation")
    print("5. Create data quality metrics and reporting")

if __name__ == "__main__":
    ready = assess_data_validation()
    if not ready:
        recommend_data_validation_fixes() 