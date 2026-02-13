#!/usr/bin/env python3
"""
Test script for MIT Lab Samples
Validates structure and basic functionality without requiring ML dependencies
"""

import os
import sys
from pathlib import Path


def test_directory_structure():
    """Test that all expected directories and files exist."""
    print("Testing directory structure...")
    
    base_dir = Path(__file__).parent
    
    expected_structure = {
        'README.md': True,
        'requirements.txt': True,
        'fastrl/README.md': True,
        'fastrl/fastrl_sample.py': True,
        'sdft/README.md': True,
        'sdft/sdft_trainer.py': True,
        'student-note-learning/README.md': True,
        'student-note-learning/student_note_learning.py': True,
        'test-time-training/README.md': True,
        'test-time-training/test_time_training.py': True,
        'models-catalog/README.md': True,
    }
    
    all_exist = True
    for file_path, should_exist in expected_structure.items():
        full_path = base_dir / file_path
        exists = full_path.exists()
        
        status = "✓" if exists == should_exist else "✗"
        print(f"  {status} {file_path}")
        
        if exists != should_exist:
            all_exist = False
    
    return all_exist


def test_readme_content():
    """Test that README files contain expected content."""
    print("\nTesting README content...")
    
    base_dir = Path(__file__).parent
    
    readme_checks = {
        'README.md': ['FastRL', 'SDFT', 'Student-Note', 'Test-Time', 'Models Catalog'],
        'fastrl/README.md': ['FastRL', 'MIT HAN Lab', 'reinforcement learning'],
        'sdft/README.md': ['Self-Distillation', 'catastrophic forgetting'],
        'student-note-learning/README.md': ['Student-Note', 'study notes'],
        'test-time-training/README.md': ['Test-Time Training', 'inference'],
        'models-catalog/README.md': ['GPT', 'Claude', 'models'],
    }
    
    all_pass = True
    for readme_path, keywords in readme_checks.items():
        full_path = base_dir / readme_path
        
        if not full_path.exists():
            print(f"  ✗ {readme_path} not found")
            all_pass = False
            continue
        
        content = full_path.read_text()
        missing_keywords = [kw for kw in keywords if kw.lower() not in content.lower()]
        
        if missing_keywords:
            print(f"  ✗ {readme_path} missing keywords: {missing_keywords}")
            all_pass = False
        else:
            print(f"  ✓ {readme_path}")
    
    return all_pass


def test_python_syntax():
    """Test that Python files have valid syntax."""
    print("\nTesting Python syntax...")
    
    base_dir = Path(__file__).parent
    
    python_files = [
        'fastrl/fastrl_sample.py',
        'sdft/sdft_trainer.py',
        'student-note-learning/student_note_learning.py',
        'test-time-training/test_time_training.py',
    ]
    
    all_valid = True
    for py_file in python_files:
        full_path = base_dir / py_file
        
        if not full_path.exists():
            print(f"  ✗ {py_file} not found")
            all_valid = False
            continue
        
        try:
            with open(full_path, 'r') as f:
                compile(f.read(), py_file, 'exec')
            print(f"  ✓ {py_file}")
        except SyntaxError as e:
            print(f"  ✗ {py_file} - Syntax error: {e}")
            all_valid = False
    
    return all_valid


def test_imports_structure():
    """Test that Python files have proper import structure."""
    print("\nTesting import structure...")
    
    base_dir = Path(__file__).parent
    
    python_files = [
        'fastrl/fastrl_sample.py',
        'sdft/sdft_trainer.py',
        'student-note-learning/student_note_learning.py',
        'test-time-training/test_time_training.py',
    ]
    
    all_valid = True
    for py_file in python_files:
        full_path = base_dir / py_file
        
        if not full_path.exists():
            continue
        
        content = full_path.read_text()
        
        # Check for basic structure
        has_docstring = '"""' in content or "'''" in content
        has_main = 'if __name__ ==' in content
        
        if not has_docstring:
            print(f"  ⚠ {py_file} - Missing module docstring")
        
        if has_main:
            print(f"  ✓ {py_file} - Has main guard")
        else:
            print(f"  ⚠ {py_file} - Missing main guard (optional)")
    
    return all_valid


def run_simple_demo():
    """Run a simple demo that doesn't require ML dependencies."""
    print("\nRunning Test-Time Training demo (no ML dependencies)...")
    
    base_dir = Path(__file__).parent
    ttt_file = base_dir / 'test-time-training' / 'test_time_training.py'
    
    if not ttt_file.exists():
        print("  ✗ Test-Time Training file not found")
        return False
    
    try:
        # Import and run the demo
        import sys
        sys.path.insert(0, str(ttt_file.parent))
        
        from test_time_training import demo_test_time_training
        demo_test_time_training()
        
        print("\n  ✓ Demo completed successfully")
        return True
    except Exception as e:
        print(f"\n  ✗ Demo failed: {e}")
        return False


def main():
    """Run all tests."""
    print("="*80)
    print("MIT Lab Samples - Test Suite")
    print("="*80)
    
    results = {
        'Directory Structure': test_directory_structure(),
        'README Content': test_readme_content(),
        'Python Syntax': test_python_syntax(),
        'Import Structure': test_imports_structure(),
        'Demo Execution': run_simple_demo(),
    }
    
    print("\n" + "="*80)
    print("Test Results Summary")
    print("="*80)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("="*80)
    
    if all_passed:
        print("\n✓ All tests passed! MIT Lab Samples are ready to use.")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
