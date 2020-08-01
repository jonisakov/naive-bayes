###########################################################################
# Auther: Jonathan isakov
# Date: 31-7-2020
# Description: Naive bayes algorythem for predicting a spam mail from a real
#              mail
###########################################################################

# IMPORTS
import re
import os
import glob
import shutil
import hashlib

# GLOBALS
friends_path    = '.\\friends'
spam_path       = '.\\spam'
sus_path        = '.\\sus'
alpha           = 1 

# Functions
def word_count(path):
    """
    word_count(path to the folder of mails) -> number of mails, a dict of words and accournces,,
    word_count is a algo that reads all the *.txt files in a specfied directory
    and returns the count per word in a dict {word : count} 
    """
    w = {}
    i = 0
    for mail in glob.glob(path +'\\'+ "*.txt"):
        i = i + 1
        m = open(mail, "r+")
        content = m.read()
        content = re.split(r"\W+", content)
        for word in content:
            if word in w:
                w[word] = w[word] + 1
            else:
                w[word] = alpha + 1
        m.close()
    if re.match(r'.*\.txt', path):
        m = open(path, "r+")
        content = m.read()
        w = list(set(re.findall(r"\w+", content)))
        m.close()
    return [i, w]

def dict_combo(dict1, dict2):
    """
    dict_combo(dict1,dict2) --> returns a combined dicted with words at min of alpha,,
    this will return a correct combo list uppon which we can preform the naive bayes algo
    """
    for word in dict2:
        if word not in dict1:
            dict1[word] = alpha
    return dict1
def porb_dict(d):
    """
    num_of_words(dict) --> the number of words in the dict,,
    used to calculate the probability of the word to accour
    """
    count = 0
    for word in d:
        count = count + d[word]
    for word in d:
        d[word] = float(d[word] / count)
    return d

def compare(p_friend, p_spam, friends_words,spam_words, sus_words):
    for word in sus_words:
        if word in friends_words:
            p_friend = p_friend * friends_words[word]
            p_spam = p_spam * spam_words[word]
    print("friend prob: " + str(p_friend))
    print("spam prob: " + str(p_spam))
    if p_friend > p_spam:
        return 'friend'
    return 'spam'
# Main
def main():
    print("collecting all mails")
    a = word_count(friends_path)
    friend_mails = a[0]
    friends_words = a[1]
    a = word_count(spam_path)
    spam_mails = a[0]
    spam_words = a[1]

    print("preparing the naive bayes vars")
    p_friend = friend_mails / (friend_mails + spam_mails)
    p_spam = spam_mails / (friend_mails + spam_mails)
    friends_words = porb_dict(dict_combo(friends_words, spam_words))
    spam_words = porb_dict(dict_combo(spam_words, friends_words))

    print("classifing the new mails and improving algo")
    for mail in glob.glob(sus_path +'\\'+ "*.txt"):
        a = word_count(mail)
        sus_words = a[1]
        state = compare(p_friend, p_spam, friends_words,spam_words, sus_words)
        if state == 'friend':
            name = mail.split('\\')
            shutil.copyfile(mail, friends_path + '\\' + name[2])
            print(mail + " is classified as friend mail")
        else:
            name = mail.split('\\')
            shutil.copyfile(mail, spam_path + '\\' + name[2])
            print(mail + " is classified as spam mail")

        

    


if __name__== "__main__" :
    main()
