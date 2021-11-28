# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    true_letters = []
    set_secret = set(secret_word)
    
    for i in letters_guessed:
      if i in secret_word:
        true_letters.append(i)
    set_letters = set(true_letters)    
    if set_secret == set_letters:
      return True  
    else:
      return False




def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    future_string = []
    for i in secret_word:
      if i in letters_guessed:
        future_string.append(i)
      else:
        future_string.append('_ ')
    
    return ''.join(i for i in future_string)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all = []
    res = []
    for i in string.ascii_lowercase:
      all.append(i)
    for i in all:
      if i not in letters_guessed:
        res.append(i)
    return ''.join(i for i in res)

    



def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3
    
    holos = ['a', 'e', 'i', 'o', 'u']
    print('Welcome to the game Hangman!')
    
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print(get_guessed_word(secret_word, letters_guessed))
    while is_word_guessed(secret_word, letters_guessed) == False and guesses_remaining != 0:
      print('You have', warnings_remaining, 'warnings left.')
      print('You have', guesses_remaining, 'guesses left.')
      print('Available letters: ', get_available_letters(letters_guessed))
      available_let = []
      for i in get_available_letters(letters_guessed):
        available_let.append(i)
      letter = input('Please guess a letter: ').lower()
      if letter.isalpha() == False:
        if warnings_remaining == 0:
          guesses_remaining -= 1
          print('Oops! That is not a valid letter. You have', warnings_remaining, 'warnings and', guesses_remaining, 'guesses left:', get_guessed_word(secret_word, letters_guessed))
        else:
          warnings_remaining -= 1
          print('Oops! That is not a valid letter. You have', warnings_remaining, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
      elif letter not in available_let:
        warnings_remaining -= 1
        print('Oops! You\'ve already guessed that letter. You now have', warnings_remaining, 'warnings:', get_guessed_word(secret_word, letters_guessed))
      else:
        letters_guessed.append(letter)
        if letter in secret_word:
          print('Good guess: ', get_guessed_word(secret_word, letters_guessed))
        else:
          print('Oops! That letter is not in my word: ', get_guessed_word(secret_word, letters_guessed))
          if letter in holos:
            guesses_remaining -= 2
          else:
            guesses_remaining -= 1
      print('--------------')
    else:
      score = guesses_remaining * len(set(secret_word))
      if guesses_remaining <= 0 and is_word_guessed(secret_word, letters_guessed) == False:
        print('You lost :( The secret word was:', secret_word)
      elif is_word_guessed(secret_word, letters_guessed) == True:
        print('Congratulations, you won!\nYour total score for this game is:', score)



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    from collections import Counter
    my_list = [i for i in my_word]
    while ' ' in my_list:
      my_list.remove(' ')
    
    other_list = [i for i in other_word]
    count = Counter(other_list)
    i = 0
    if len(my_list)==len(other_list):
      while i < len(my_list):
        if my_list[i].isalpha() == False and count[other_list[i]] == 1:
          i += 1
          continue
        else:
          if my_list[i] == other_list[i]:
            i += 1
            continue
          else:
            return False
            break
      return True
    else:
      return False



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    count = 0
    for i in wordlist:
      if match_with_gaps(my_word, i) == True:
        print(i, end=' ')
        count += 1
    else:
      if count == 0:
        return print('No matches found')



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = []
    guesses_remaining = 6
    warnings_remaining = 3
    
    holos = ['a', 'e', 'i', 'o', 'u']
    print('Welcome to the game Hangman!')
    
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print(get_guessed_word(secret_word, letters_guessed))
    while is_word_guessed(secret_word, letters_guessed) == False and guesses_remaining != 0:
      print('You have', warnings_remaining, 'warnings left.')
      print('You have', guesses_remaining, 'guesses left.')
      print('Available letters: ', get_available_letters(letters_guessed))
      available_let = []
      for i in get_available_letters(letters_guessed):
        available_let.append(i)
      letter = input('Please guess a letter: ').lower()
      if letter.isalpha() == False:
        if letter == '*':
          print('Possible word matches are: ')
          show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        elif warnings_remaining == 0:
          guesses_remaining -= 1
          print('Oops! That is not a valid letter. You have', warnings_remaining, 'warnings and', guesses_remaining, 'guesses left:', get_guessed_word(secret_word, letters_guessed))
        else:
          warnings_remaining -= 1
          print('Oops! That is not a valid letter. You have', warnings_remaining, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
      elif letter not in available_let:
        warnings_remaining -= 1
        print('Oops! You\'ve already guessed that letter. You now have', warnings_remaining, 'warnings:', get_guessed_word(secret_word, letters_guessed))
      else:
        letters_guessed.append(letter)
        if letter in secret_word:
          print('Good guess: ', get_guessed_word(secret_word, letters_guessed))
        else:
          print('Oops! That letter is not in my word: ', get_guessed_word(secret_word, letters_guessed))
          if letter in holos:
            guesses_remaining -= 2
          else:
            guesses_remaining -= 1
      print('\n--------------')
    else:
      score = guesses_remaining * len(set(secret_word))
      if guesses_remaining <= 0 and is_word_guessed(secret_word, letters_guessed) == False:
        print('You lost :( The secret word was:', secret_word)
      elif is_word_guessed(secret_word, letters_guessed) == True:
        print('Congratulations, you won!\nYour total score for this game is:', score)    



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)

    #FOR TWO PLAYERS:
    #secret_word = input('Choose word: ')
    #print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

    #hangman(secret_word)
    

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
