import sys
import math
import random

# Global variables assigned with default values
num_permutations_to_print = 1
probability_to_print = 1.0

def generate_permutations(a, n):
    
    if n == 0:
        # Randomly choose permutations to be printed
        if random.random() < probability_to_print:
            print(' '.join(a))
    else:
        for i in range(n):
            generate_permutations(a, n - 1)
            j = 0 if n % 2 == 0 else i
            a[j], a[n] = a[n], a[j]
        generate_permutations(a, n - 1)


def main():

    #if len(sys.argv) != 2:
    #    sys.stderr.write('Exactly one argument is required\n')
    #    sys.exit(1)
    

    if len(sys.argv) != 3:
        sys.stderr.write('Two arguments required: <word>, <approx num of prints>.\n')
        return 1


    # Get command line arguments
    word = sys.argv[1]
    word_len = len(word)
    num_permutations_to_print = int(sys.argv[2])
    
    # Calculate the chance for a permutation to be printed
    # The actual number of prints is approximate to the number passed as command line argument
    global probability_to_print
    probability_to_print = num_permutations_to_print / math.factorial(word_len)

    generate_permutations(list(word), word_len - 1)

    return 0

if __name__ == '__main__':
    sys.exit(main())