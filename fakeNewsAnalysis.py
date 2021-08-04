'''
    Project Name: fake news analysis
    Name: Zixi Zhong
    Purpose: This program analyzes some recent data about fake news articles
    and identifies what they most commonly focus on. It reads in a
    csv file, cleans it, creates Word objects that it adds to a list from
    from the title words of the articles in the file. It then prints all
    the words with word occurance counts greater than or equal to the count
    of the word object at position n in the sorted linked list.

'''

import csv
import string
import sys


class Word:
    '''
        This class represents information about a word.
        Parameters: self
                    word - a string
        Returns: none, sets value to self._word, self._count
        Pre-condition: A list must exist in order to store the
                       word objects
        Post-condition: The word object will be initialized with a word
                        value, and a count of 1
    '''
    def __init__(self, word):
        self._word = word
        self._count = 1


    def word(self):
        '''
            This method returns self._word.
            Parameters: self
            Returns: self._word
        '''
        return self._word


    def count(self):
        '''
            This method returns self._count.
            Parameters: self
            Returns: self._count
        '''
        return self._count


    def incr(self):
        '''
            This method increments self._count by 1.
            Parameters: self
            Returns: none
        '''
        self._count += 1


    def __str__(self):
        '''
            This method formats the Word object to be
            easily printed wth it's word and count attributes.
            Parameters: self
            Returns: printable format for Word
        '''
        return str(self._word) + ", " + str(self._count)



def merge_sort(word_list):
    '''
        This function sorts the list in of word objects in descending
        order of count by recursively splitting the list, sorting the
        split values, and merging it back together in a helper function.
        This was acquired and modified from the lecture slieds.
        Parameters: self, word_list
        Returns: none
        Pre-condition: The list of Word Objs must contain all the Word
                       objs and have updated counts in order to sort them
        Post-condition: The list will be sorted in descending
                        order, and alphabetical order if counts are equal
    '''
    if len(word_list) <= 1: # Base Case
        return word_list
    else:
        l_split = len(word_list)//2
        L1 = word_list[:l_split] # Splits the list in half
        L2 = word_list[l_split:]
        sortedL1 = merge_sort(L1) # Merges them back in
        sortedL2 = merge_sort(L2) # sorted order
        return merge(sortedL1, sortedL2, [])



def merge(L1, L2, merged):
    '''
        This function sorts two lists and merges them back together
        in sorted order.
        Parameters: self, L1, L2, merged
        Returns: none
        Pre-condition: merge_sort must be run first and lists must be
                       split in order to merge them together
        Post-condition: Pieces of the list will be sorted in descending
                        order until the entire list is sorted
    '''
    if L1 == [] or L2 == []:  # Base case
        return merged + L1 + L2
    else:
        if L1[0].count() > L2[0].count(): # Checks if word objs are not sorted
                                          # by count
            new_merged = merged + [L1[0]] # Creates new list to be sorted
            new_L1 = L1[1:]
            new_L2 = L2
        elif L1[0].count() == L2[0].count(): # If count is same, sorts by
            if L1[0].word() < L2[0].word():  # alphabetical order
                new_merged = merged + [L1[0]] # creates new list to be sorted
                new_L1 = L1[1:]
                new_L2 = L2
            else:
                new_merged = merged + [L2[0]]
                new_L1 = L1
                new_L2 = L2[1:]
        else:
            new_merged = merged + [L2[0]] # If sorted by count, creates new
            new_L1 = L1                   # list to be sorted
            new_L2 = L2[1:]
        return merge(new_L1, new_L2, new_merged)



def ask_print_n(word_list):
    '''
         This function asks the user t input n, finds the word obj
         at the nth position of the list, gets its count, and prints
         all the words with counts equal to or higher than that one.
        Parameters: self, word_list
        Returns: none, prints words with counts k
        Pre-condition: List must be sorted and an n
                       value must be input
        Post-condition: The words with counts k or greater will be
                        printed
    '''
    try:
        n = int(input('N: '))
    except:  # Checks if the input can be read or converted to int
        print("ERROR: Could not read N")
        sys.exit()

    assert n >= 0

    k = word_list[n].count()

    # Creates a list of words with count greater than/equal to k
    k_list = [word for word in word_list if word.count() >= k]

    # Prints words with count greater than/equal to k
    for word in k_list:
        print("{} : {:d}".format(word.word(), word.count()))



def read_file():
    '''
        This function reads and cleans the input csv file,
        collects the cleaned titles, and sends them back to
        main to be processed.
        Parameters: None
        Returns: Cleaned titles list
        Pre-condition: none
        Post-condition: Files will be read and cleaned for
                        the rest of the program to process.
    '''

    file = input("File: ")

    try:
        infile = open(file)
    except:  # Checks if the file can be opened
        print("ERROR: Could not open file " + file)
        sys.exit()

    csvreader = csv.reader(infile)

    titles = []  # List of titles
    for line in csvreader:
        if not line[0].startswith("#"):
            title = line[4]

            # Replaces punctuation with whitespace
            for p in string.punctuation:
                title = title.replace(p, ' ')

            title = title.lower().split()

            # Removes words with length <= 2
            title = [word for word in title if len(word) > 2]

            titles.append(title)
    infile.close()
    return titles



def main():
    '''
        This function reads and cleans a csv file, extracts its titles,
        makes the words in the titles word objs and stores them in a list,
        sorts them by count, and alphabetical order if counts are equal,
        asks for a position form the user, finds the word obj at that
        position in the sorted list, and prints all the words with counts
        equal to or greater than the count of thw word at position n.
        Parameters: None
        Returns: None
        Pre-condition: none
        Post-condition: files will be processed, and all the words
                        with counts greater than or equal to the
                        count of the word at position n will be
                        printed.
        '''
    sys.setrecursionlimit(2500) # Expands limit for recursion

    titles = read_file()

    words = []
    for title in titles:
        for word in title:
            # Checks if the word already exists as an object in the list
            check = next((x for x in words if x.word() == word), None)

            # If word isn't in list, it makes it an obk and appends
            # to the list
            if check == None:
                word_obj = Word(word)
                words.append(word_obj)

            # Increases count if it is in list
            else:
                check.incr()

    word_list = merge_sort(words)

    ask_print_n(word_list)


main()
