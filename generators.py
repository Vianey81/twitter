

def read_file_with_generator(file_path):
    with open(file_path) as input_file:
        for line in input_file:
            yield line


def make_chains_with_generator(input_path):
    a_line_of_input = read_file_with_generator(input_path)
    chains = {}

    text_string = a_line_of_input.next()

    start_pos = 0
    end_pos = text_string.find(" ")
    word_1 = text_string[start_pos:end_pos]

    start_pos = end_pos+1
    end_pos = text_string.find(" ", start_pos)
    word_2 = text_string[start_pos:end_pos]

    start_pos = end_pos+1
    end_pos = text_string.find(" ", start_pos)
    word_3 = text_string[start_pos:end_pos]
    
    while True:
        try:
            text_string = a_line_of_input.next()
        except (StopIteration):
            break
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
    return chains