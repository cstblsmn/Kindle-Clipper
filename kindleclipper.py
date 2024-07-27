import re
import sys
import os
from datetime import datetime
from collections import defaultdict

def parse_date(date_str):
    # Your date format may not be in here, make sure to add it
    date_formats = [
        "%A, %d %B %Y %H:%M:%S",
        "%A, %d %B %y %H:%M:%S %Z%z",
        "%A, %B %d, %Y %I:%M:%S %p"
    ]
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue
    raise ValueError(f"Date format for '{date_str}' not recognized")

def create_output(template, title, author, first_clipping_date, last_clipping_date, clippings):
    return template.format(
        title=title,
        author=author,
        first_clipping_date=first_clipping_date.strftime("%d %B %Y"),
        last_clipping_date=last_clipping_date.strftime("%d %B %Y"),
        clippings="\n".join(clippings)
    )

def process_clippings(clippings_file, template_file):
    # Ensure the "books" folder exists
    books_folder = "books"
    if not os.path.exists(books_folder):
        try:
            os.makedirs(books_folder)
        except Exception as e:
            print(f"Error creating directory '{books_folder}': {e}")
            sys.exit(1)

    try:
        with open(clippings_file, "r", encoding="utf-8") as f:
            contents = f.read().split("==========")
    except FileNotFoundError:
        print(f"Error: The file '{clippings_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{clippings_file}': {e}")
        sys.exit(1)

    try:
        with open(template_file, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{template_file}' was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{template_file}': {e}")
        sys.exit(1)

    books = defaultdict(lambda: {
        "author": "",
        "first_clipping_date": None,
        "last_clipping_date": None,
        "clippings": []
    })

    for note in contents:
        try:
            title = re.findall(r"(.+?)\s*\(", note)[0].strip()
            author = re.findall(r"\((.+?)\)", note)[0].strip()
            date_str = re.findall(r"Added on (.+)", note)[0].strip()
            clipping_date = parse_date(date_str)

            if books[title]["first_clipping_date"] is None or clipping_date < books[title]["first_clipping_date"]:
                books[title]["first_clipping_date"] = clipping_date
            if books[title]["last_clipping_date"] is None or clipping_date > books[title]["last_clipping_date"]:
                books[title]["last_clipping_date"] = clipping_date

            page_match = re.findall(r"page (\d+)", note)
            page_number = page_match[0] if page_match else None

            text = re.findall(r"\n\n(.*)", note)[0].strip()
            if page_number:
                books[title]["clippings"].append(f"- [p{page_number}] {text}")
            else:
                books[title]["clippings"].append(f"- {text}")
            books[title]["author"] = author

        except IndexError:
            continue

    for title, info in books.items():
        if not info["clippings"]:
            print(f"No clippings found for the book: {title}")
            continue

        # This allows the user to decide the clippings files' extensions (markdown is default)
        sanitized_title = re.sub(r'[^\w\s]', '', title)
        preferred_extension = template_file.rfind('.')
        if preferred_extension != -1:
            output_extension = template_file[preferred_extension:]
        else:
            output_extension = ".md"
        
        output_file = f"{books_folder}/{sanitized_title}{output_extension}"
        try:
            with open(output_file, "a", encoding="utf-8") as f:
                output = create_output(
                    template,
                    title,
                    info['author'],
                    info['first_clipping_date'],
                    info['last_clipping_date'],
                    info['clippings']
                )
                f.write(output)
            print(f"Clippings for '{title}' have been written to {output_file}")
        except Exception as e:
            print(f"Error writing to file '{output_file}': {e}")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <clippings_file> <template_file>")
        sys.exit(1)

    clippings_file = sys.argv[1]
    template_file = sys.argv[2]

    process_clippings(clippings_file, template_file)
