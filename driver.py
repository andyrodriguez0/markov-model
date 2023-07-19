
import sys
from markov import identify_speaker

if __name__ == '__main__':

    # Confirm the appropriate arguments were passed
    if len(sys.argv) != 6:
        print(f'Usage: python3 {sys.argv[0]} <filenameA> <filenameB> ' + \
        '<filenameC> <k> <hashtable-or-dict>')
        sys.exit(1)

    # Extract the parameters from the command line and convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)

    # Confirm the appropriate arguments for hashtable-or-dict was padded
    if hashtable_or_dict not in ('hashtable', 'dict'):
        print('Final parameter must either be \'hashtable\' or \'dict\'')
        sys.exit(1)

    # Open the files
    with open(filenameA) as speech1:
        with open(filenameB) as speech2:
            with open(filenameC) as speech3:

                # Identify the most likely speaker of the third speech
                result = identify_speaker(speech1.read(), speech2.read(), \
                speech3.read(), k, hashtable_or_dict == 'hashtable')

                # Print the results
                print(f'Speaker A: {result[0]}')
                print(f'Speaker B: {result[1]}')
                print(f'Conclusion: Speaker {result[2]} is most likely')