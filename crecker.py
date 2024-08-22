import hashlib
import os
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Hash function map
hash_map = {
    '1': hashlib.md5,
    '2': hashlib.sha1,
    '3': hashlib.sha224,
    '4': hashlib.sha256,
    '5': hashlib.sha384,
    '6': hashlib.sha512,
    '7': hashlib.sha3_224,
    '8': hashlib.sha3_256,
    '9': hashlib.sha3_384,
    '10': hashlib.sha3_512,
    '11': hashlib.blake2b,
    '12': hashlib.blake2s
}

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome():
    clear_terminal()
    print(f"{Fore.CYAN}Welcome to the Hash Keyword Matcher!{Style.RESET_ALL}")
    print(f"{Fore.RED}\
       /\_/\\\n\
      ( o.o )\n\
       > ^ <{Style.RESET_ALL}")

def hash_keyword(keyword, hash_type):
    hash_function = hash_map.get(hash_type)
    if not hash_function:
        raise ValueError("Invalid hash type selected.")
    hash_object = hash_function()
    hash_object.update(keyword.encode())
    return hash_object.hexdigest()

def match_single_keyword_with_hash(keyword, hash_value, hash_type):
    keyword_hash = hash_keyword(keyword, hash_type)
    if keyword_hash == hash_value:
        return f"{Fore.GREEN}Successful: The keyword and hash match.\n{Style.RESET_ALL}Keyword: {keyword}\nHash: {hash_value}\n"
    return f"{Fore.RED}No match: The keyword does not match the hash.\n{Style.RESET_ALL}"

def match_single_keyword_with_hash_file(keyword, hash_file, hash_type):
    try:
        keyword_hash = hash_keyword(keyword, hash_type)
        results = []
        with open(hash_file, 'r') as hf:
            for line in hf:
                hash_value = line.strip()
                if keyword_hash == hash_value:
                    results.append(f"{Fore.GREEN}Successful: The keyword and hash match.\n{Style.RESET_ALL}Keyword: {keyword}\nHash: {hash_value}\n")
        if not results:
            results.append(f"{Fore.RED}No match: The keyword does not match any hash in the hash file.\n{Style.RESET_ALL}")
        return ''.join(results)
    except FileNotFoundError:
        return f"{Fore.RED}Error: File not found.\n{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}An error occurred: {e}\n{Style.RESET_ALL}"

def match_keywords_with_single_hash(keyword_file, hash_value, hash_type):
    try:
        results = []
        with open(keyword_file, 'r') as kf:
            for line in kf:
                keyword = line.strip()
                keyword_hash = hash_keyword(keyword, hash_type)
                if keyword_hash == hash_value:
                    results.append(f"{Fore.GREEN}Successful: The keyword and hash match.\n{Style.RESET_ALL}Keyword: {keyword}\nHash: {hash_value}\n")
        if not results:
            results.append(f"{Fore.RED}No match: No keywords in the file match the hash.\n{Style.RESET_ALL}")
        return ''.join(results)
    except FileNotFoundError:
        return f"{Fore.RED}Error: File not found.\n{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}An error occurred: {e}\n{Style.RESET_ALL}"

def match_keywords_with_hashes(keyword_file, hash_file, hash_type):
    try:
        with open(hash_file, 'r') as hf:
            hash_values = {line.strip() for line in hf}
        results = []
        with open(keyword_file, 'r') as kf:
            for line in kf:
                keyword = line.strip()
                keyword_hash = hash_keyword(keyword, hash_type)
                if keyword_hash in hash_values:
                    results.append(f"Keyword: {keyword} -> Hash: {keyword_hash}\n")
        if not results:
            results.append(f"{Fore.RED}No match: No keywords in the file match any hash in the hash file.\n{Style.RESET_ALL}")
        return ''.join(results)
    except FileNotFoundError:
        return f"{Fore.RED}Error: File not found.\n{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}An error occurred: {e}\n{Style.RESET_ALL}"

def save_results(results):
    save_option = input(f"{Fore.YELLOW}Do you want to save this data? (Y/n): {Style.RESET_ALL}").strip().lower()
    if save_option == 'y':
        filename = input(f"{Fore.YELLOW}Enter the filename to save the data: {Style.RESET_ALL}").strip()
        try:
            with open(filename, 'w') as file:
                file.write(results)
            print(f"{Fore.GREEN}Data successfully saved to {filename}.")
        except Exception as e:
            print(f"{Fore.RED}An error occurred while saving the file: {e}")

def get_user_input():
    print(f"{Fore.CYAN}Select keyword source:{Style.RESET_ALL}")
    print("1. Single keyword")
    print("2. Keyword file")
    keyword_source = input(f"{Fore.CYAN}Enter the number corresponding to your choice: {Style.RESET_ALL}")

    if keyword_source == '1':
        keyword = input(f"{Fore.CYAN}Enter the keyword: {Style.RESET_ALL}")
        return keyword, None
    elif keyword_source == '2':
        keyword_file = input(f"{Fore.CYAN}Enter the path to the keyword file: {Style.RESET_ALL}")
        return None, keyword_file
    else:
        print(f"{Fore.RED}Invalid option selected for keyword source.{Style.RESET_ALL}")
        return None, None

def get_hash_source():
    print(f"{Fore.CYAN}Select hash source:{Style.RESET_ALL}")
    print("1. Single hash value")
    print("2. Hash file")
    hash_source = input(f"{Fore.CYAN}Enter the number corresponding to your choice: {Style.RESET_ALL}")

    if hash_source == '1':
        hash_value = input(f"{Fore.CYAN}Enter the hash value: {Style.RESET_ALL}")
        return hash_value, None
    elif hash_source == '2':
        hash_file = input(f"{Fore.CYAN}Enter the path to the hash file: {Style.RESET_ALL}")
        return None, hash_file
    else:
        print(f"{Fore.RED}Invalid option selected for hash source.{Style.RESET_ALL}")
        return None, None

def get_hash_type():
    print(f"{Fore.CYAN}Select hash type:{Style.RESET_ALL}")
    print("1. MD5")
    print("2. SHA-1")
    print("3. SHA-224")
    print("4. SHA-256")
    print("5. SHA-384")
    print("6. SHA-512")
    print("7. SHA3-224")
    print("8. SHA3-256")
    print("9. SHA3-384")
    print("10. SHA3-512")
    print("11. BLAKE2b")
    print("12. BLAKE2s")
    hash_type = input(f"{Fore.CYAN}Enter the number corresponding to your choice: {Style.RESET_ALL}")
    return hash_type

def main():
    print_welcome()
    keyword, keyword_file = get_user_input()
    hash_value, hash_file = get_hash_source()
    hash_type = get_hash_type()

    try:
        if keyword and hash_value:
            results = match_single_keyword_with_hash(keyword, hash_value, hash_type)
        elif keyword and hash_file:
            results = match_single_keyword_with_hash_file(keyword, hash_file, hash_type)
        elif keyword_file and hash_value:
            results = match_keywords_with_single_hash(keyword_file, hash_value, hash_type)
        elif keyword_file and hash_file:
            results = match_keywords_with_hashes(keyword_file, hash_file, hash_type)
        else:
            print(f"{Fore.RED}Invalid input. Please make sure all inputs are provided correctly.{Style.RESET_ALL}")
            return

        print(results)  # Print results to the user
        save_results(results)  # Ask to save results
    except ValueError as e:
        print(f"{Fore.RED}{e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

