from collections import Counter
import streamlit as st
from wordfreq import top_n_list
import config


@st.cache_data
def read(path):
    """read words from the file"""
    with open(path, "r") as file:
        # read the word from file
        return [line.strip().lower() for line in file if len(line.strip()) == 5]


top_words = top_n_list(config.DEFAULT_LANGUAGE, 100000)


def get_rank(word):
    try:
        return top_words.index(word) + 1
    except ValueError:
        return None  # not found in list


# logic for gray, green, yellow


def freq(words):
    """letter frequencies"""
    count = Counter()
    for word in words:
        for char in word:
            count[char] += 1
    return count


def filter(words, correct_letters, remove_letters, remove_posn_letters):
    """filters green, grey and yellow words"""
    remove_letters_set = set(remove_letters)
    print("Green : ", correct_letters)
    print("Grey : ", remove_letters_set)
    print("Yellow : ", remove_posn_letters)

    # green
    green_words = []
    for word in words:
        match = True
        for posn, char in correct_letters.items():
            if word[posn] != char:
                match = False
                break
        if match:
            green_words.append(word)

    print("Words after applying green letter criteria:", len(green_words))

    # yellow
    yellow_words = []
    for word in green_words:
        match = True
        for letter, posn in remove_posn_letters.items():
            if letter not in word:
                match = False
                break
            if any(word[pos] == letter for pos in posn):
                match = False
                break
        if match:
            yellow_words.append(word)

    print("Words after applying yellow letter criteria:", len(yellow_words))

    # grey
    final_words = []
    for word in yellow_words:
        match = True
        for i, char in enumerate(word):
            if i in correct_letters and correct_letters[i] == char:  # green
                continue

            # yellow posn
            if char in remove_posn_letters:
                yellow_count = len(remove_posn_letters[char])
                word_count = word.count(char)
                green_count = sum(1 for pos, c in correct_letters.items() if c == char)
                # if we have right number of this letter (yellow + green)
                if word_count <= (yellow_count + green_count):
                    continue

            # char is in remove_letters
            if char in remove_letters_set:  # not dups
                match = False
                print(f"Excluding {word} due to grey letter '{char}' at position {i}")
                break
        if match:
            final_words.append(word)

    return final_words


def score(words, freq, remove_posn):
    """Algorithm for scoring  (Update this to word_pred * entropy = score) for better results"""

    def wordScore(word):
        score = 0
        initial_score = sum(
            freq[char] for i, char in enumerate(word) if i not in remove_posn
        )

        # no word ends with s
        s_score = 1
        if word[-1] == "s":
            s_score = 0.1

        # diverse vowels
        vowel_score = 0
        vowels = set("aeiou")
        uniq = set(word) & vowels
        vowel_score += len(uniq) * 1000

        # duplicates : penalty
        duplicate_score = 1
        duplicate_count = len(word) - len(set(word))
        if duplicate_count > 0:
            duplicate_score = 0.5

        rank_score = 0
        rank = get_rank(word)
        if rank:
            rank_score += (10000 / rank) * 10
        else:
            penalty_rank = -5000
            rank_score += penalty_rank

        score = initial_score * duplicate_score * s_score + vowel_score + rank_score
        return score

    return sorted(words, key=wordScore, reverse=True)
