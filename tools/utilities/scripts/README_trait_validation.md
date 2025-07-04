# Governor Trait Validation System

## 🎯 **Overview**
This system validates and analyzes governor traits using your existing dialog system infrastructure. It checks trait mappings, behavioral preferences, consistency, and performance.

## 🚀 **Quick Start**

### **1. Test the System First**
```bash
python scripts/test_trait_validation.py
```
This runs comprehensive tests to ensure everything works before validating governors.

### **2. Validate a Single Governor**
```bash
python scripts/trait_validation_runner.py --governor OCCODON
```

### **3. Validate All Governors**
```bash
python scripts/trait_validation_runner.py --all --report full_validation_report.json
```

### **4. Validate a Batch from File**
```bash
# Create a file with governor names (one per line)
echo -e "OCCODON\nPASCOMB\nVIROOLI" > test_governors.txt
python scripts/trait_validation_runner.py --batch test_governors.txt --report batch_report.json
```

## 📊 **What Gets Validated**

### **1. Trait Mappings**
- ✅ Checks which traits have behavioral mappings
- ⚠️ Identifies unmapped traits needing attention
- 🔍 Analyzes parameter conflicts between traits

### **2. Behavioral Preferences**
- ✅ Validates preference generation from traits
- 📊 Checks parameter ranges (0.0-1.0)
- 🎯 Analyzes tone preferences and interaction styles
- 📝 Counts trigger words, forbidden words, and topics

### **3. Behavioral Consistency**
- 🎭 **Tone vs Traits**: Does tone match personality traits?
- 📏 **Formality Consistency**: Do formal traits match formality levels?
- ⏱️ **Patience Consistency**: Do patient traits match patience levels?

### **4. Performance Validation**
- ⚡ **Preference Generation**: <50ms target
- 🗺️ **Trait Mapping**: <10ms target  
- 🔍 **Content Filtering**: <5ms target

## 📁 **Output Structure**

### **Validation Report Format**
```json
{
  "validation_summary": {
    "total_governors": 91,
    "passed": 89,
    "failed": 2,
    "timestamp": "2025-01-02T15:30:00"
  },
  "system_status": {
    "cache_enabled": true,
    "cached_governors": 5,
    "trait_mappings_count": 9
  },
  "detailed_results": {
    "OCCODON": {
      "status": "completed",
      "trait_validation": {
        "total_traits": 6,
        "mapped_traits": 4,
        "unmapped_traits": ["transformative", "adaptive"],
        "validation_status": "passed"
      },
      "preference_validation": {
        "tone_preference": "mystical_poetic",
        "behavioral_parameters": {
          "greeting_formality": 0.65,
          "response_patience": 0.78
        },
        "validation_status": "passed"
      },
      "behavioral_validation": {
        "consistency_checks": [
          {
            "check": "tone_trait_consistency",
            "result": {"consistent": true, "score": 0.67}
          }
        ],
        "validation_status": "passed"
      },
      "performance_validation": {
        "benchmarks": {
          "preference_generation": {"time_ms": 2.3, "passed": true},
          "trait_mapping": {"time_ms": 0.8, "passed": true}
        },
        "validation_status": "passed"
      }
    }
  }
}
```

## 🔧 **Command Line Options**

| Option | Description | Example |
|--------|-------------|---------|
| `--governor NAME` | Validate specific governor | `--governor OCCODON` |
| `--all` | Validate all governors | `--all` |
| `--batch FILE` | Validate from file list | `--batch governors.txt` |
| `--output DIR` | Output directory | `--output validation_results` |
| `--report FILE` | Generate JSON report | `--report report.json` |
| `--verbose` | Enable debug logging | `--verbose` |

## 🎯 **Interpretation Guide**

### **✅ Passed Status**
- All trait mappings found
- Preferences generated successfully
- Behavioral consistency checks passed
- Performance targets met

### **⚠️ Warning Status**
- Some traits unmapped (suggestions provided)
- Minor behavioral inconsistencies detected
- Performance slightly below targets
- Parameter range issues

### **❌ Failed Status**
- Critical system errors
- Unable to generate preferences
- Major behavioral inconsistencies
- Severe performance issues

## 🔍 **Troubleshooting**

### **Import Errors**
```bash
# Make sure you're in the project root
cd /path/to/governor_generator
python scripts/test_trait_validation.py
```

### **No Governor Data**
- Check that `canon/canon_governor_profiles.json` exists
- Or ensure `governor_output/` directory has .json files

### **Performance Issues**
- Run with `--verbose` to see detailed timing
- Check system resources if very slow

### **Missing Trait Mappings**
- Review `game_mechanics/dialog_system/trait_mapper.py`
- Add new trait mappings as needed

## 🎮 **Integration with Your Workflow**

### **Daily Validation**
```bash
# Quick check on modified governors
python scripts/trait_validation_runner.py --batch modified_governors.txt
```

### **Full System Validation**
```bash
# Complete validation with comprehensive report
python scripts/trait_validation_runner.py --all --report daily_validation.json --verbose
```

### **Performance Monitoring**
```bash
# Focus on performance metrics
python scripts/trait_validation_runner.py --governor OCCODON --verbose | grep "ms"
```

## 📊 **Expected Results**

With your existing infrastructure:
- **91 governors total** from canon profiles
- **~6-8 traits per governor** (virtues + flaws)
- **Sub-millisecond performance** on most operations
- **High consistency scores** due to systematic trait assignment

## 🚀 **Next Steps After Validation**

1. **Review unmapped traits** - Add mappings for missing traits
2. **Address consistency issues** - Adjust traits or preference logic
3. **Performance optimization** - If any governors are slow
4. **Regular monitoring** - Set up automated daily validation

This system leverages all your existing dialog system infrastructure while providing comprehensive validation and adjustment capabilities! 🎯✨ 