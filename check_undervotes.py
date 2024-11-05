from typing import Set

def get_accesses(input_file: str) -> Set[str]:
    """Retrieve unique valid voter accesses from the input log file."""
    return _get_entries(input_file, 'Valid Voter Access')

def get_votes(input_file: str) -> Set[str]:
    """Retrieve unique votes cast from the input log file."""
    return _get_entries(input_file, 'Valid Cast Vote')

def _get_entries(input_file: str, keyword: str) -> Set[str]:
    """Generic function to retrieve unique user entries based on a keyword."""
    entries = set()
    try:
        with open(input_file, 'r') as infile:
            for line in infile:
                if keyword in line:
                    user = get_user(line)
                    entries.add(user)
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except IOError as e:
        print(f"Error while reading the file: {e}")
    return entries

def get_user(line: str) -> str:
    """Extract the user from the log line."""
    limit_1 = line.rfind(":") + 1  # Find the last occurrence of ':' and move one character ahead
    return line[limit_1:].strip()

if __name__ == "__main__":
    input_file = 'access.log'

    accesses = get_accesses(input_file)
    votes = get_votes(input_file)
    undervotes = accesses.difference(votes)
    
    print("Number of undervotes: " + str(len(undervotes)))
    if len(undervotes) > 0:
        for user in sorted(undervotes):
            print(user)
    