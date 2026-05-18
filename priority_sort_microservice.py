"""Priority Sort Microservice for CS361.

Communication pipe: text files.
The microservice reads requests/priority_request.txt and writes responses/priority_response.txt.
Run this file in one terminal, then run test_program.py in another terminal.
"""

from pathlib import Path
import time

REQUEST_FILE = Path("requests/priority_request.txt")
RESPONSE_FILE = Path("responses/priority_response.txt")


def parse_request(text):
    """Parse the sort order and item priority lines from the request file."""
    sort_order = "descending"
    items = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        if line.startswith("sort_order="):
            sort_order = line.split("=", 1)[1].strip().lower()

        elif line.startswith("item="):
            item_text = line.split("=", 1)[1]
            parts = [part.strip() for part in item_text.split(",")]
            name = parts[0]
            priority = None

            for part in parts[1:]:
                if part.startswith("priority="):
                    try:
                        priority = int(part.split("=", 1)[1].strip())
                    except ValueError:
                        priority = None

            items.append((name, priority))

    return sort_order, items


def sort_items(sort_order, items):
    """Sort items by priority. Missing priorities always go at the end."""
    reverse = sort_order != "ascending"

    items_with_priority = [item for item in items if item[1] is not None]
    items_without_priority = [item for item in items if item[1] is None]

    sorted_items = sorted(items_with_priority, key=lambda item: item[1], reverse=reverse)
    return sorted_items + items_without_priority


def write_response(sorted_items):
    """Write the sorted items to the response file."""
    RESPONSE_FILE.parent.mkdir(exist_ok=True)

    lines = ["sorted_items:"]
    for name, priority in sorted_items:
        if priority is None:
            lines.append(f"{name}, priority=missing")
        else:
            lines.append(f"{name}, priority={priority}")

    RESPONSE_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def handle_request():
    """Read the request file, sort the items, and write the response."""
    request_text = REQUEST_FILE.read_text(encoding="utf-8")
    sort_order, items = parse_request(request_text)
    sorted_items = sort_items(sort_order, items)
    write_response(sorted_items)

    REQUEST_FILE.unlink()


def main():
    print("Priority Sort Microservice is running...")
    print("Waiting for requests/priority_request.txt")

    while True:
        if REQUEST_FILE.exists():
            print("Request received. Sorting items...")
            handle_request()
            print("Response written to responses/priority_response.txt")
        time.sleep(1)


if __name__ == "__main__":
    main()
