
from markov import identify_speaker
import pandas as pd
import seaborn as sns
import sys
import time

if __name__ == "__main__":

    # Confirm the appropriate arguments were passed
    if len(sys.argv) != 6:
        print(f'Usage: python3 {sys.argv[0]} <filenameA> <filenameB> ' + \
        '<filenameC> <max-k> <runs>')
        sys.exit(1)

    # Extract the parameters from the command line and convert types
    filenameA, filenameB, filenameC, k, runs = sys.argv[1:]
    k = int(k)
    runs = int(runs)

    # Open the files
    with open(filenameA) as speech1:
        with open(filenameB) as speech2:
            with open(filenameC) as speech3:

                # Initialize variables
                options = [True, False]
                results = []
                speech1_text = speech1.read()
                speech2_text = speech2.read()
                speech3_text = speech3.read()

                # Run the performance tests
                for option in options:
                    for k in range(1, k + 1):
                        for run in range(1, runs + 1):

                            # Start the timer, run the test, and end the timer
                            start = time.perf_counter()
                            identify_speaker(speech1_text, speech2_text, \
                            speech3_text, k,option)
                            elapsed = time.perf_counter() - start

                            # Set the implementation
                            if option:
                                implementation = 'hashtable'
                            else:
                                implementation = 'dict'
                            
                            # Add the result to the results
                            results.append((implementation, k, run, elapsed))
                
                # Create the dataframe from the results
                columns = ['Implementation', 'K', 'Run', 'Time']
                dataframe = pd.DataFrame(results, columns = columns)

                # Take the average time for each K and each Implementation
                dataframe = dataframe.groupby(['K', 'Implementation'])\
                ['Time'].mean().reset_index()

                # Plot the results and save the plot
                sns.set_theme()
                plot = sns.pointplot(data = dataframe, x = 'K', y = 'Time', \
                hue = 'Implementation', linestyle = '-', marker = 'o')
                plot.set(ylabel = f'Average Time ({runs} Runs)', \
                title = 'Python Dictionary vs Hashtable')
                plot.figure.savefig('execution_graph.png')