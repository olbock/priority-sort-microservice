"""Test program for the Priority Sort Microservice.

This program does not directly call the microservice. It only writes a request
text file and reads the response text file.
"""

from pathlib import Path
import time

REQUEST_FILE = Path("requests/priority_request.txt")
RESPONSE_FILE = Path("responses/priority_response.txt")


def main() -> None:
    REQUEST_FILE.parent.mkdir(exist_ok=True)
    RESPONSE_FILE.parent.mkdir(exist_ok=True)

    if RESPONSE_FILE.exists():
        RESPONSE_FILE.unlink()

    print("Writing priority sort request...")
    REQUEST_FILE.write_text(
        "sort_order=descending\n"
        "item=Biology Exam, priority=5\n"
        "item=Math Homework, priority=3\n"
        "item=Discussion Post, priority=1\n"
        "item=Extra Credit Worksheet\n",
        encoding="utf-8",
    )

    print("Waiting for response...")
    while not RESPONSE_FILE.exists():
        time.sleep(1)

    response = RESPONSE_FILE.read_text(encoding="utf-8")
    print("Response received:")
    print(response)


if __name__ == "__main__":
    main()
