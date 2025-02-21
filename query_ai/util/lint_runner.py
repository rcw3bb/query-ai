"""
This script runs pylint on the target file and checks if there are any errors.

Author: Ron Webb
Since: 1.0.0
"""

import subprocess
import sys

def main():
    """
    This function runs pylint on the target file and checks if there are any errors.
    :return: None
    """

    target = "query_ai"
    try:
        subprocess.run(["pylint", target], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Pylint failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
