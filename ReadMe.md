#Codenames

## Overview

This script generates unique code names by combining an adjective and a noun. By default, it fetches word lists from the MIT word database online. You can also specify your own local files for adjectives, nouns, and used code names. The output code name is in uppercase.

## Prerequisites

- Python 3.x

## Options

```bash
-a, --adjectives: Path to a local file containing adjectives (one per line).
-n, --nouns: Path to a local file containing nouns (one per line).
-u, --used: Path to a file with used code names (each code name on a new line in the format "ADJECTIVE NOUN").
```

## Usage Examples

1. Using Default MIT Word Lists <br />
Generate a code name using the default online word lists and without any prior used code names: <br />

```bash
python codenames.py
```

2. Specifying a Used Code Names File <br />
Generate a code name using the default online word lists but exclude previously used code names from used_code_names.txt: <br />

```bash
python codenames.py -u used_code_names.txt
```

3. Using Local Adjectives and Nouns Files <br />
Generate a code name using custom adjective and noun files, excluding used code names from used_code_names.txt: <br />

```bash
python codenames.py -a adjectives.txt -n nouns.txt -u used_code_names.txt
```

4. To generate a code name and append it to the list of used code names:

```bash
python codenames.py -a adjectives.txt -n nouns.txt -u used_codenames.txt -ap
```

## Used Code Names File Format
The used code names file should list each code name on a new line in the following format: <br />

```bash
ADJECTIVE NOUN
ADJECTIVE NOUN
ADJECTIVE NOUN
...
```

Example: <br />

```bash
BRAVE TIGER
SILENT COMET
ICY TABLE
```