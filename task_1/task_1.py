import os


def isPalindrome(s: str) -> bool:
    s = s.lower()
    n = len(s)
    i = 0
    while i < n//2:
        if s[i] != s[n-i-1]:
            return False
        i+=1
    return True


file_name = "sentence_analysis.txt"
if os.path.exists(file_name):
    os.remove(file_name)

with open("sentences.txt", "r") as fp, open("sentence_analysis.txt", "w") as output_file:
    for line in fp:
        palindrome = None
        words = line.split()
        word_count = len(words)

        longest_string = ""
        for word in words:
            if palindrome is None and isPalindrome(word):
                palindrome = word
            
            if len(word) > len(longest_string):
                longest_string = word

        print(f'Sentence: {line.strip()}', file=output_file)
        print(f'Word Count: {word_count}', file=output_file)
        print(f'Longest Word: {longest_string}', file=output_file)
        print(f'Palindromes: {palindrome}', file=output_file)
        print(file=output_file)
