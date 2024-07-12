from rarfile import RarFile, NoRarEntry, BadRarFile
import os
from itertools import product
from pathlib import Path
from rarfile import RarFile, BadRarFile, NoRarEntry
from tqdm import tqdm
def brute_force(start_length, length, letters=True, numbers=True, symbols=True, spaces=False):
    """
    Generator pasword
    """
    characters = ''
    if letters:
        characters += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if numbers:
        characters += '0123456789'
    if symbols:
        characters += '!@#$%^&*()-_=+[]{}|;:",.<>?'
    if spaces:
        characters += ' '
    
    if not any([letters, numbers, symbols, spaces]):
        print("no character set . choose at least one character set.")
        return

    with open("dictionary.txt", "w") as file:
        brute=1
        for password_length in range(start_length, length + 1):
            for value in range(len(characters) ** password_length):
                password = ''
                remainder = value
                for _ in range(password_length):
                    remainder, char_index = divmod(remainder, len(characters))
                    password = characters[char_index] + password
                file.write(password + "\n")
        print("pass gen is done, starting brute")

def crack_password():

    n_words = sum(1 for _ in open(word_list_path, 'rb'))

 
    print('Total passwords to test:', f'{n_words:,}')

    with open(word_list_path, 'rb') as wordlist:
        for word in tqdm(wordlist, total=n_words, unit='word'):
            password = word.strip().decode('utf-8')
            try:
                with RarFile(rar_file_path) as rar_file:
                    rar_file.setpassword(password)

                    rar_file.extract(rar_file.namelist()[0], path='temp')
                    extracted_file = Path('temp', rar_file.namelist()[0])
                    if extracted_file.is_file() and extracted_file.stat().st_size > 0:
                        print('\n\n ***password is-->',str(password),"***")
                        print('\n total passwords tested:')
                        return True
                    else:
                        continue
            except (BadRarFile, NoRarEntry):
                continue
            except Exception as e:
                print(f"Error occurred: {e}")
                continue



    print("\n[!] Password not found, try other wordlist.")
    return False


if __name__ == '__main__':
    print("----------------------------------------------------")
    print('    WinRAR Cracker')
    print('    by Seville')
    print('')
    print('preqs (make sure you have these working): rarfile, Path, tqdm, pathlib, itertools3 (if you need it for product module)')
    print("----------------------------------------------------")
    
    filename = input("enter filename/ path: ")
    while not os.path.isfile(filename):
        filename = input("file not found. Enter filename again: ")

    mode = ''
    while mode != "dictionary" and mode != "brute":
        mode = input("choose mode [dictionary/brute(passgen)]: ")

    pwdGen = None
    if mode == "dictionary":
        word_list_path = Path(input('word list path: '))
        rar_file_path = Path(input('RAR file path: '))
        if word_list_path.exists() and rar_file_path.exists():
            crack_password()
        else:
            print("path incorrect")


    if mode == "brute":
        letters = input("Include letters? [yes/no] (default yes) ") != 'no'
        symbols = input("Include symbols? [yes/no] (default yes) ") != 'no'
        numbers = input("Include numbers? [yes/no] (default yes) ") != 'no'
        spaces = input("Include spaces? [yes/no] (default no) ") == 'yes'
        start_length = int(input("enter minimum length: "))
        length = int(input("enter maximum length: "))
        pwdGen = brute_force(start_length=start_length, length=length, letters=letters, numbers=numbers, symbols=symbols, spaces=spaces)
        rar_file_path = Path(filename)
        word_list_path = Path("dictionary.txt")
        print("starting brute-->",str(rar_file_path))
        if word_list_path.exists() and rar_file_path.exists():
            crack_password()
            print()
            print("operation finished, a dictionary.txt file is created in directory.")
            print()
            input("press enter to exit...")
        else:
            print("path incorrect")

