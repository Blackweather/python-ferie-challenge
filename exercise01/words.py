import re
import requests

def get_text():
    print("Please provide a word or sentence")
    return input()

def parse_text(text):
    regex = re.compile("[^a-zA-Z]+")
    parsed = regex.sub("", text).lower()
    if not parsed:
        print("Your text is invalid")
        exit(-1)
    return parsed

def is_palindrome(text):
    return text == text[::-1]

def fetch_anagrams(text):
    url = f"http://anagramica.com/all/:{text}"
    try:
        data = requests.get(url).json()
        return data["all"]
    except:
        print(f"Cannot fetch anagrams, request error")
        exit()

def main():
    text = get_text()
    text = parse_text(text)
    print(f"Your text after parsing: {text}")
    print(f"Reversed: {text[::-1]}")
    if is_palindrome(text):
        print("Your text is a palindrome")
    else:
        print("Your text is not a palindrome")
    
    results = fetch_anagrams(text)
    print("\nAnagrams:")
    for result in results:
        print(result)
    

if __name__ == "__main__":
    main()