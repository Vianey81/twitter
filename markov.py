from random import choice
import sys
import twitter
import os
from generators import make_chains_with_generator


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

   # BUILD DICTIONARY BY PARSING LINES OF INPUT FILE

    start_pos = 0
    end_pos = text_string.find(" ")
    word_1 = text_string[start_pos:end_pos]

    start_pos = end_pos+1
    end_pos = text_string.find(" ", start_pos)
    word_2 = text_string[start_pos:end_pos]

    start_pos = end_pos+1
    end_pos = text_string.find(" ", start_pos)
    word_3 = text_string[start_pos:end_pos]
 
    chains = {}
    while True:
        bi_gram = (word_1, word_2)
        if bi_gram in chains:
            chains[bi_gram].append(word_3)
        else:
            chains[bi_gram] = [word_3]
        word_1 = word_2
        word_2 = word_3
        start_pos = end_pos+1
        end_pos = text_string.find(" ", start_pos)
        if end_pos != -1:
            word_3 = text_string[start_pos:end_pos]
        else:
            break

    # BUILD DICTIONARY USING LIST OF ALL WORDS IN INPUT FILE        

    # all_words = text_string.split()
    # n_gram_length = 2
    # for index in range(0, len(all_words)-n_gram_length):
    #     n_gram = []
    #     for word in range(index,index+n_gram_length):
    #         n_gram.append(all_words[word])
    #     n_gram = tuple(n_gram)
    #     next_word = all_words[index+n_gram_length]
    #     if n_gram in chains:
    #         chains[n_gram].append(next_word)
    #     else:
    #         chains[n_gram] = [next_word]  

    return chains


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
    while current_tuple in chains:
        rand_word = choice(chains[current_tuple])
        if len(text) + len(rand_word) < 140:
            text += rand_word + " "
            #loop in current_tuple to get the words from 1 to len(current_tuple) and add rand_word
            if len(text) > 8 and text[-2] in end_punctuation:
                return text   
            new_tuple = list(current_tuple)
            new_tuple.pop(0)
            new_tuple.append(rand_word)
            current_tuple = tuple(new_tuple)

        else:
            return text


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    
    api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    tweet_again = ""
    while tweet_again.lower() != "q":
        new_tweet = make_text(chains)
        status = api.PostUpdate(new_tweet)
        print status.text
        tweet_again = raw_input("Press 'q' to Quit, or any key to tweet again. ")

    our_tweets = api.GetUserTimeline("vk_markov")
    print our_tweets
    single_tweet = api.GetStatus(687369511612186624)
    print single_tweet


input_path = sys.argv[1]

# Open the file and turn it into one long string
#input_text = open_and_read_file(input_path)

# Get a Markov chain
#chains = make_chains(input_text)

# Produce random text
#random_text = make_text(chains)

#tweet(chains)

#print random_text

chains = make_chains_with_generator(input_path)
tweet(chains)