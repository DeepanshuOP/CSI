import argparse
import os
import re
from termcolor import colored

def grep(pattern, filenames, options):
    total_matches = 0

    for filename in filenames:
        try:
            if os.path.isdir(filename) and options['recursive']:
                for root, dirs, files in os.walk(filename):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if match_file(file_path, pattern, options):
                            total_matches += 1
            else:
                if match_file(filename, pattern, options):
                    total_matches += 1
        except FileNotFoundError:
            print(f"grep: {filename}: No such file or directory")

    if options['count_only']:
        print(f"Total matches: {total_matches}")

def match_file(filename, pattern, options):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if match_line(line, pattern, options):
                    print_output(filename, line_number, line, options)
                    return True
    except IOError:
        print(f"Error: Unable to read file {filename}")
    return False

def match_line(line, pattern, options):
    flags = re.IGNORECASE if options['ignore_case'] else 0
    if options['word_match']:
        pattern = r"\b" + pattern + r"\b"
    if options['invert_match']:
        return not re.search(pattern, line, flags=flags)
    else:
        return re.search(pattern, line, flags=flags)

def print_output(filename, line_number, line, options):
    if options['line_numbers']:
        print(f"{filename}:{line_number}: {line.strip()}")
    else:
        print(line.strip())

def main():
    pattern = input("Enter the pattern to search for: ")
    filenames = input("Enter the files to search (separated by space): ").split()

    parser = argparse.ArgumentParser(description="Grep-like text search")
    parser.add_argument("-i", "--ignore-case", action="store_true", help="Perform case-insensitive search")
    parser.add_argument("-n", "--line-numbers", action="store_true", help="Display line numbers")
    parser.add_argument("-c", "--count-only", action="store_true", help="Count only the number of matches")
    parser.add_argument("-r", "--recursive", action="store_true", help="Search files in directories recursively")
    parser.add_argument("-v", "--invert-match", action="store_true", help="Invert the match")
    parser.add_argument("-w", "--word-match", action="store_true", help="Search for whole words only")
    args = parser.parse_args()

    options = {
        'ignore_case': args.ignore_case,
        'line_numbers': args.line_numbers,
        'count_only': args.count_only,
        'recursive': args.recursive,
        'invert_match': args.invert_match,
        'word_match': args.word_match,
    }

    grep(pattern, filenames, options)

if __name__ == "__main__":
    main()
