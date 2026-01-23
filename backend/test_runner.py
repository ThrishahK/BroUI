#!/usr/bin/env python3
"""
runs tests. if it breaks, it's your fault.
"""

import json
import subprocess
import tempfile
import os
import sys
from pathlib import Path

# hardcoded paths cause why not
SCRIPT_DIR = Path(__file__).parent
TEST_CASES_FILE = SCRIPT_DIR / "test_cases.json"


def load_test_cases():
    """read the json. try not to cry."""
    with open(TEST_CASES_FILE, "r") as f:
        return json.load(f)


def run_brocode(code: str, input_data: str, timeout: int = 5) -> tuple[bool, str]:
    """
    runs the code.
    
    5s timeout because i have places to be.
    """
    # dumping your garbage code into a temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.homie', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # executing... brace for impact
        result = subprocess.run(
            ['brocode', temp_file],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # trimming whitespace to save your grade
        output = result.stdout.strip()
        
        if result.returncode != 0:
            # it died. rip.
            error_msg = result.stderr.strip() if result.stderr else "it just died"
            return False, f"Runtime Error: {error_msg}"
        
        return True, output
        
    except subprocess.TimeoutExpired:
        # too slow. killing it.
        return False, "Time Limit Exceeded"
    except FileNotFoundError:
        # brocode isn't even installed. astounding.
        return False, "BroCode interpreter not found. Install with: pipx install brocode-lang"
    except Exception as e:
        # god knows what happened here
        return False, f"Execution Error: {str(e)}"
    finally:
        # cleaning up the crime scene
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_submission(question_id: str, code: str) -> dict:
    """
    judgement day.
    """
    test_cases = load_test_cases()
    
    # basic sanity check
    question_id = question_id.upper()
    if question_id not in test_cases:
        return {
            "status": "FAIL",
            "error": f"Unknown question ID: {question_id}",
            "valid_ids": list(test_cases.keys())
        }
    
    question = test_cases[question_id]
    cases = question["test_cases"]
    
    passed = 0
    failed = 0
    results = []
    
    # testing each case. hope you prayed.
    for i, case in enumerate(cases):
        input_data = case["input"]
        expected = case["expected"].strip()
        
        success, actual = run_brocode(code, input_data)
        
        if success and actual == expected:
            # a miracle happened
            passed += 1
            results.append({"case": i + 1, "status": "PASS"})
        else:
            # as expected. failure.
            failed += 1
            results.append({
                "case": i + 1,
                "status": "FAIL",
                "expected": expected,
                "actual": actual
            })
    
    # did you survive?
    if failed == 0:
        return {
            "status": "PASS",
            "question": question_id,
            "name": question["name"],
            "points": question["points"],
            "tests_passed": passed,
            "tests_total": len(cases)
        }
    else:
        # disappoint your parents properly
        return {
            "status": "FAIL",
            "question": question_id,
            "name": question["name"],
            "points": 0,
            "tests_passed": passed,
            "tests_total": len(cases),
            "details": results
        }


def main():
    """entry point. don't mess this up."""
    if len(sys.argv) < 2:
        print("Usage: python test_runner.py <question_id> [code_file]")
        print("       python test_runner.py <question_id> --stdin")
        print("")
        print("Examples:")
        print("  python test_runner.py E01 solution.homie")
        print("  echo 'code...' | python test_runner.py E01 --stdin")
        print("")
        print("Question IDs: E01-E10, M01-M10, H01-H10")
        sys.exit(1)
    
    question_id = sys.argv[1]
    
    # getting input. logic is hard.
    if len(sys.argv) >= 3:
        if sys.argv[2] == "--stdin":
            code = sys.stdin.read()
        else:
            with open(sys.argv[2], 'r') as f:
                code = f.read()
    else:
        # manual entry. brave.
        print("Enter code (Ctrl+D to finish):")
        code = sys.stdin.read()
    
    # running it
    result = test_submission(question_id, code)
    
    # output. plain and simple.
    print(result["status"])
    
    # 0 for pass, 1 for fail. binary, like your chances.
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
