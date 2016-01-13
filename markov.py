from random import choice
import sys


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    string_file = open(file_path).read()

    return string_file


def make_chains(text_string):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

# search string for first space, call it pos_1
# set everything before first space to word_1
# search from pos_1+1 until first space, call it pos_2
# set everything between pos_1 and pos_2 to word_2
#  search from pos_2+1 until first space, call it pos_3
# set everything between pos_2 and pos_3 to word_3
# do our thing with adding stuff to dictionary
# make word_1 = word_2, word_2 = word_3, same for positions
# loop from search pos_2 for next space

    chains = {}
    # 
    all_words = text_string.split()
    n_gram_length = 2
    for index in range(0, len(all_words)-n_gram_length):
        n_gram = []
        for word in range(index,index+n_gram_length):
            n_gram.append(all_words[word])
        n_gram = tuple(n_gram)
        next_word = all_words[index+n_gram_length]
        if n_gram in chains:
            chains[n_gram].append(next_word)
        else:
            chains[n_gram] = [next_word]  
    return chains
# empty dictionary
# get 3 words
# put 2 words in dictionary as key and third as value
# get new_word
# word_1 = word_2, then word_2 = word_3, then word_3 = new_word
# see if (word_1, word_2) in dictionary, if not add, if so append
# go until no words left

def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    text = ""
    all_upper_tuples = []
    for a_tuple in chains.keys():
        if a_tuple[0][0].isupper():
            all_upper_tuples.append(a_tuple)
    current_tuple = choice(all_upper_tuples)
    for word in current_tuple:
        text += word + " "

    end_punctuation = [".", "?", "!"]
    while current_tuple in chains and current_tuple[-1][-1] not in end_punctuation:
        rand_word = choice(chains[current_tuple])
        text += rand_word + " "
        #loop in current_tuple to get the words from 1 to len(current_tuple) and add rand_word
        new_tuple = list(current_tuple)
        new_tuple.pop(0)
        new_tuple.append(rand_word)
        current_tuple = tuple(new_tuple)

    return text


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    pass


input_path = sys.argv[1]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

print random_text
