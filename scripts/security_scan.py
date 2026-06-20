import json
import subprocess
import sys
import os

def run_scan(target_dir, output_file, no_llm=True):
    """Runs the skillspector scan command."""
    cmd = ["skillspector", "scan", target_dir, "--format", "json", "--output", output_file]
    if no_llm:
        cmd.append("--no-llm")
    
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode not in [0, 1]:
            print(f"Error running skillspector (exit code {result.returncode}):")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            sys.exit(1)
        print("Scan completed.")
    except FileNotFoundError:
        print("Error: 'skillspector' command not found. Make sure it is installed.")
        sys.exit(1)

def check_risk(report_file, threshold=50):
    """Parses the report and checks if the risk score is above the threshold."""
    if not os.path.exists(report_file):
        print(f"Error: Report file {report_file} not found.")
        sys.exit(1)

    with open(report_file, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON report: {e}")
            sys.exit(1)
    
    score = report.get("risk_assessment", {}).get("score", 0)
    print(f"Risk Score found: {score}")
    
    if score > threshold:
        print(f"FAILURE: Risk score {score} exceeds the allowed threshold of {threshold}!")
        return False
    
    print(f"SUCCESS: Risk score {score} is within the safe limit.")
    return True

if __name__ == "__main__":
    # Usage: python scripts/security_scan.py <target_dir> <threshold>
    target = sys.argv[1] if len(sys.argv) > 1 else "ai/"
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    out = "security_report.json"
    
    run_scan(target, out)
    if not check_risk(out, threshold):
        sys.exit(1)
