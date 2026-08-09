import os
import re
import sys
import tempfile
import subprocess

# Default workspace directory for temporary execution
WORKSPACE_DIR = os.path.join(os.getcwd(), "sandbox_workspace")
DEFAULT_TIMEOUT = 10  # Fallback timeout if not specified by Mistral


def extract_timeout(raw_llm_text: str) -> int:
    """
    Parses the first line of the text for 'TIMEOUT: <seconds>'.
    Returns the extracted integer or DEFAULT_TIMEOUT if not found.
    """
    first_line = raw_llm_text.strip().split("\n")[0]
    match = re.search(r"TIMEOUT:\s*(\d+)", first_line, re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            pass
    return DEFAULT_TIMEOUT


def clean_code_block(raw_llm_text: str) -> str:
    """
    Strips away commentary/explanations and extracts pure Python code
    enclosed within ```python ... ``` fences.
    """
    pattern = r"```python\s*(.*?)\s*```"
    match = re.search(pattern, raw_llm_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Fallback: If model forgot backticks, return text stripped of TIMEOUT tag
    lines = raw_llm_text.strip().split("\n")
    if lines and lines[0].startswith("TIMEOUT:"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def run_in_sandbox(raw_llm_text: str) -> tuple[bool, str]:
    """
    Main sandbox entry point.
    Returns:
        (success: bool, output_logs: str)
    """
    # 1. Parse dynamic timeout and clean code
    timeout = extract_timeout(raw_llm_text)
    clean_code = clean_code_block(raw_llm_text)

    if not clean_code:
        return False, "Execution Error: No valid Python code block found in response."

    # 2. Ensure sandbox workspace directory exists
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    temp_file_path = os.path.join(WORKSPACE_DIR, "temp_runner.py")

    # 3. Write code to disk
    try:
        with open(temp_file_path, "w", encoding="utf-8") as f:
            f.write(clean_code)
    except Exception as e:
        return False, f"FileSystem Error: Could not create runner file ({str(e)})"

    # 4. Run subprocess execution
    try:
        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        # 5. Check exit status
        if result.returncode == 0:
            output = result.stdout if result.stdout else "[Code executed successfully with no stdout output]"
            return True, output
        else:
            return False, result.stderr

    except subprocess.TimeoutExpired:
        return False, f"Timeout Error: Execution exceeded the dynamic timeout limit of {timeout} seconds."
    except Exception as e:
        return False, f"Subprocess Execution Exception: {str(e)}"
    finally:
        # Cleanup temporary runner file
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError:
                pass


# --- Standalone Testing Suite ---
if __name__ == "__main__":
    print("--- Running Sandbox Standalone Tests ---\n")

    # Test 1: Successful execution
    test_pass = """TIMEOUT: 5
```python
def add(a, b):
    return a + b

print(f"Result: {add(10, 20)}")
```"""
    success, logs = run_in_sandbox(test_pass)
    print(f"Test 1 (Pass Case) -> Success: {success}\nOutput:\n{logs}\n")

    # Test 2: Runtime Exception
    test_fail = """TIMEOUT: 5
```python
x = 10 / 0
```"""
    success, logs = run_in_sandbox(test_fail)
    print(f"Test 2 (Crash Case) -> Success: {success}\nOutput:\n{logs.strip()}\n")

    # Test 3: Infinite loop timeout
    test_timeout = """TIMEOUT: 2
```python
import time
print("Starting loop...")
while True:
    time.sleep(0.5)
```"""
    success, logs = run_in_sandbox(test_timeout)
    print(f"Test 3 (Timeout Case) -> Success: {success}\nOutput:\n{logs}")
