import subprocess
import time

def run_script(script_name):
    print(f"\nRunning {script_name}...")
    start = time.time()
    subprocess.run(["python", script_name], check=True)
    end = time.time()
    print(f"Finished {script_name} in {end - start:.2f} seconds\n")

if __name__ == "__main__":
    run_script("iABC.py")
    run_script("IWO.py")
