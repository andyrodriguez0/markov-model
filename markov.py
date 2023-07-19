
from hashtable import Hashtable
import math

# Initialize constants
HASH_CELLS = 57
TOO_FULL = 0.5
GROWTH_RATIO = 2

class Markov:

    def __init__(self, k, text, use_hashtable):
        '''
        This method specifies the actions to be taken when a Markov model is
        created
        
        Inputs:
            - k (int): an integer representing the order of the model
            - test (str): a string representing the text that will be used to
            build the model
            - use_hashtable (bool): a boolean representing if the Hashtable
            class should be used
        
        Outputs:
            - None
        '''

        # Initialize attributes
        self.k = k
        self.text = text
        self.S = len(set(self.text))

        # Determine with hashtable implementation to use
        if use_hashtable:
            self.hashtable = Hashtable(HASH_CELLS, 0, TOO_FULL, GROWTH_RATIO)
        else:
            self.hashtable = {}
        
        # Populate the hashtable
        for strings in self.generate_strings(self.text, self.k):
            for string in strings:
                if string not in self.hashtable:
                    self.hashtable[string] = 1
                else:
                    self.hashtable[string] += 1

    def log_probability(self, s):
        '''
        This method calculates the log probability of a string, given the
        statistics of character sequences modeled by this Markov model. This
        probability is not normalized by the length of the string.

        Inputs:
            - s (str): a string for which the probability will be calculated
        
        Outputs:
            - probability (float): a float representing the log probability of
            the string
        '''

        # Initialize variables
        probability = 0

        # Iterate through all of the strings of length k and k + 1
        for strings in self.generate_strings(s, self.k):
            
            # Get the occurrences of the string of length k
            if strings[0] in self.hashtable:
                N = self.hashtable[strings[0]]
            else:
                N = 0

            # Get the occurrences of the string of length k + 1
            if strings[1] in self.hashtable:
                M = self.hashtable[strings[1]]
            else:
                M = 0

            # Calculate the log probability and add it to the total probability
            probability += math.log((M + 1) / (N + self.S))

        return probability
    
    def generate_strings(self, string, k):
        '''
        This generator generates all strings of length k and k + 1 in an input
        string

        Inputs:
            string (str): a string for which all strings of length k and k + 1
            will be generated
            k (int): an integer representing the length of the strings to be
            generated
        
        Yields:
            - (tuple): a two-element tuple containing the current strings of
            length k and k + 1
        '''

        # Initialize variables
        n = len(string)

        # Iterate through all of the characters in the string
        for i in range(n):
            
            # Create the k and k + 1 string
            k_string = []
            k_plus_one_string = []

            # Add k characters to each of the strings
            for j in range(k):
                k_string.append(string[(i + j) % n])
                k_plus_one_string.append(string[(i + j) % n])
            
            # Add the last character to the k + 1 string
            k_plus_one_string.append(string[(i + k) % n])

            yield (''.join(k_string), ''.join(k_plus_one_string))


def identify_speaker(speech1, speech2, speech3, k, use_hashtable):
    '''
    This function takes sample text from two speakers (1 and 2), and text from
    an unidentified speaker (3), and return a tuple with the normalized log
    probabilities of each of the speakers uttering that text under an "order"
    character-based Markov model, as well as a conclusion of which speaker
    uttered the unidentified text based on the two probabilities

    Inputs:
        - speech1 (str): a string representing the sample text for the first
        speaker
        - speech2 (str): a string representing the sample text for the second
        speaker
        - speech3 (str): a string representing the text from the unidentified
        speaker
        - k (int): an integer representing the order of the Markov model
        - use_hashtable (bool): a boolean representing if the Hashtable
            class should be used
    '''

    # Create the Markov models
    markov1 = Markov(k, speech1, use_hashtable)
    markov2 = Markov(k, speech2, use_hashtable)

    # Calculate the normalized log probabilities for each model
    probability1 = markov1.log_probability(speech3) / len(speech3)
    probability2 = markov2.log_probability(speech3) / len(speech3)

    # Return the speaker that most likely spoke speech3
    if probability1 >= probability2:
        return (probability1, probability2, 'A')
    else:
        return (probability1, probability2, 'B')