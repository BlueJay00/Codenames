import random
import requests
import json
import argparse

def load_words_from_file(file_path, encoding="utf-8"):
    """
    Load use code names from a given file in plain text but with UTF-8 encoding.
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []
    except UnicodeDecodeError as e:
        print(f"Error reading file {file_path} with encoding {encoding}: {e}")
        return []


def fetch_words_from_url(url, key):
    """
    Fetch words from a JSON URL for MIT word lists where words are stored under a specific key.
    
    Args:
        url (str): The URL to fetch the JSON data from.
        key (str): The key in the JSON file where the list of words is stored.
        
    Returns:
        list: A list of words fetched from the JSON data.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        
        # Parse JSON and extract words under the given key
        data = response.json()
        words = data.get(key, [])
        
        if not words:
            print(f"No words found under key '{key}' in the JSON file.")
        
        return words
    except requests.RequestException as e:
        print(f"Error fetching words from {url}: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {url}: {e}")
        return []

# URLs for MIT word lists
adjectives_url = "https://raw.githubusercontent.com/dariusk/corpora/master/data/words/adjs.json"
nouns_url = "https://raw.githubusercontent.com/dariusk/corpora/master/data/words/nouns.json"

def get_words(adjective_file=None, noun_file=None):
    """
    Get lists of adjectives and nouns. Defaults to fetching from URLs unless local files are provided.
    
    Args:
        adjective_file (str): Path to local adjectives file (optional).
        noun_file (str): Path to local nouns file (optional).
        
    Returns:
        tuple: A tuple containing two lists: adjectives and nouns.
    """
    if adjective_file:
        adjectives = load_words_from_file(adjective_file)
    else:
        adjectives = fetch_words_from_url(adjectives_url, "adjs")  # Fetch from URL

    if noun_file:
        nouns = load_words_from_file(noun_file)
    else:
        nouns = fetch_words_from_url(nouns_url, "nouns")  # Fetch from URL

    return adjectives, nouns

def load_used_code_names(file_path):
    """
    Load and parse used code names from a TXT file, splitting them into adjectives and nouns.
    
    Args:
        file_path (str): Path to the TXT file containing used code names.
        
    Returns:
        tuple: Two sets containing used adjectives and used nouns.
    """
    used_adjectives = set()
    used_nouns = set()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                if len(words) == 2:
                    adj, noun = words
                    used_adjectives.add(adj.lower())
                    used_nouns.add(noun.lower())
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    
    return used_adjectives, used_nouns

def generate_unique_code_name(adjectives, nouns, used_adjectives, used_nouns):
    available_adjectives = [adj for adj in adjectives if adj.lower() not in used_adjectives]
    available_nouns = [noun for noun in nouns if noun.lower() not in used_nouns]

    if not available_adjectives or not available_nouns:
        print("No more unique code names available.")
        return None

    while available_adjectives and available_nouns:
        adj = random.choice(available_adjectives)
        noun = random.choice(available_nouns)
        code_name = f"{adj} {noun}".upper()  # Convert to uppercase

        if adj.lower() not in used_adjectives and noun.lower() not in used_nouns:
            used_adjectives.add(adj.lower())
            used_nouns.add(noun.lower())
            return code_name

    return None

# Main function to run the code name generator
def main(adjective_file=None, noun_file=None, used_code_names_file=None):
    adjectives, nouns = get_words(adjective_file, noun_file)
    if not adjectives or not nouns:
        print("Error: Adjective or noun list is empty.")
        return

    used_adjectives, used_nouns = set(), set()
    if used_code_names_file:
        used_adjectives, used_nouns = load_used_code_names(used_code_names_file)

    code_name = generate_unique_code_name(adjectives, nouns, used_adjectives, used_nouns)
    if code_name:
        print(f"Generated code name: {code_name}")
    else:
        print("No unique code names could be generated.")

# Argument parser to handle command-line options
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a unique code name.")
    parser.add_argument("-a", "--adjectives", help="Path to the local adjectives file", default=None)
    parser.add_argument("-n", "--nouns", help="Path to the local nouns file", default=None)
    parser.add_argument("-u", "--used", help="Path to the file containing used code names", default=None)

    args = parser.parse_args()

    main(adjective_file=args.adjectives, noun_file=args.nouns, used_code_names_file=args.used)