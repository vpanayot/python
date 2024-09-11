import sys
import os

def convert_to_celsius(fahrenheit):
    '''
    Converts Fahrenheit tempreture value to Celsius.
    '''

    # Strings ending with 'F' are considered valid values
    # In case of invalid values the function returns None
    if fahrenheit[-1].upper() == 'F':
        try:
            fahrenheit = float(fahrenheit[:-1])
            celsius = (fahrenheit - 32) * 5.0/9.0
            return celsius
        except ValueError:
            return None
    else:
        return None

def read_from_file(filepath):
    '''
    Reads data from a text file returns a list of the lines.
    '''
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file]

    except FileNotFoundError:
        print(f'Error: File "{filepath}" not found.')


def write_to_file(filepath, data):
    '''
    Writes data from a sequence to a text file.
    '''
    try:
        with open(filepath, 'w') as file:
            for item in data:
                file.write(str(item) + '\n')
    except FileNotFoundError:
        print(f'Error: File "{filepath}" not found.')

def main():
    
    # Get source filepath from command line and set target filepath
    src_filepath = input('Please provide filepath location: ')
    trg_filepath = 'celsius.txt'

    # Create a list with converted tempretures read from the source file
    # Invalid Fahrenheit values are filtered out
    celsius = [convert_to_celsius(fahrenheit) for fahrenheit in read_from_file(src_filepath) if convert_to_celsius(fahrenheit) is not None]

    write_to_file(trg_filepath, celsius)

    return 0

if __name__ == '__main__':
    sys.exit(main())