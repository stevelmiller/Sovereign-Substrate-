"""
Test suite for Sovereign Substrate (Build 10)
Verifies the LAGRANGIAN_AUDIT logging is present and functional.
"""

import subprocess
import sys
import os


def test_lagrangian_audit_line_exists():
    """
    Test that the LAGRANGIAN_AUDIT line is present in main.py.
    This is critical for verification and provenance tracking.
    """
    main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    with open(main_py_path, 'r') as f:
        content = f.read()
    
    assert 'LAGRANGIAN_AUDIT' in content, \
        "LAGRANGIAN_AUDIT line must be present in main.py for physics verification logging"
    
    print("✓ LAGRANGIAN_AUDIT line found in main.py")


def test_lagrangian_audit_output():
    """
    Test that running main.py produces LAGRANGIAN_AUDIT output.
    If the physics aren't logged, the verification is invisible.
    """
    main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
    
    try:
        result = subprocess.run(
            [sys.executable, main_py_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        output = result.stdout + result.stderr
        
        assert 'LAGRANGIAN_AUDIT' in output, \
            "LAGRANGIAN_AUDIT must appear in program output"
        
        print("✓ LAGRANGIAN_AUDIT logging verified in runtime output")
        print(f"  Output excerpt: {[line for line in output.split('\\n') if 'LAGRANGIAN_AUDIT' in line][0]}")
        
    except subprocess.TimeoutExpired:
        raise AssertionError("main.py execution timed out")
    except Exception as e:
        raise AssertionError(f"Failed to run main.py: {e}")


def test_contract_md_exists():
    """Test that CONTRACT.md exists with required content."""
    contract_path = os.path.join(os.path.dirname(__file__), 'CONTRACT.md')
    
    assert os.path.exists(contract_path), "CONTRACT.md must exist"
    
    with open(contract_path, 'r') as f:
        content = f.read()
    
    assert '400 days' in content.lower() or '400-day' in content.lower(), \
        "CONTRACT.md must include 400-day provenance statement"
    
    assert 'MANIFESTO' in content.upper(), \
        "CONTRACT.md must include the Sovereign Manifesto"
    
    print("✓ CONTRACT.md exists with required provenance and manifesto")


def test_dockerfile_exists():
    """Test that Dockerfile exists with python:3.10-slim base."""
    dockerfile_path = os.path.join(os.path.dirname(__file__), 'Dockerfile')
    
    assert os.path.exists(dockerfile_path), "Dockerfile must exist"
    
    with open(dockerfile_path, 'r') as f:
        content = f.read()
    
    assert 'python:3.10-slim' in content, \
        "Dockerfile must use python:3.10-slim as base image"
    
    print("✓ Dockerfile exists with correct base image")


def test_env_example_exists():
    """Test that .env.example exists with proper instructions."""
    env_example_path = os.path.join(os.path.dirname(__file__), '.env.example')
    
    assert os.path.exists(env_example_path), ".env.example must exist"
    
    with open(env_example_path, 'r') as f:
        content = f.read()
    
    assert 'GEMINI_API_KEY' in content, \
        ".env.example must include GEMINI_API_KEY placeholder"
    
    assert 'your_gemini_api_key_here' in content or 'your_' in content.lower(), \
        ".env.example must use placeholder, not actual key"
    
    print("✓ .env.example exists with secrets-only configuration")


def test_codeowners_exists():
    """Test that CODEOWNERS file exists and points to @stevelmiller."""
    codeowners_path = os.path.join(os.path.dirname(__file__), 'CODEOWNERS')
    
    assert os.path.exists(codeowners_path), "CODEOWNERS must exist"
    
    with open(codeowners_path, 'r') as f:
        content = f.read()
    
    assert '@stevelmiller' in content, \
        "CODEOWNERS must reference @stevelmiller"
    
    print("✓ CODEOWNERS exists with correct ownership")


if __name__ == "__main__":
    print("=" * 60)
    print("SOVEREIGN SUBSTRATE (BUILD 10) - TEST SUITE")
    print("=" * 60)
    print()
    
    tests = [
        test_lagrangian_audit_line_exists,
        test_lagrangian_audit_output,
        test_contract_md_exists,
        test_dockerfile_exists,
        test_env_example_exists,
        test_codeowners_exists,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            print(f"Running: {test.__name__}")
            test()
            passed += 1
            print()
        except AssertionError as e:
            print(f"✗ FAILED: {e}")
            print()
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            print()
            failed += 1
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        sys.exit(1)
    else:
        print("\n✓ ALL TESTS PASSED - THE SUBSTRATE IS SOUND")
        sys.exit(0)
