# python

Below are the python script and their related task and chapter:

## pythagorean_triples.py
### Chapter: 101
Task: Modify the program so that it also prints the count of the Pythagorean triples at the end.<br />

## heap_algorithm.py
### Chapter: 110
Task: Modify the script to work with long words. We require that it prints approx. 20 randomly chosen permutations of the input word.
It is important that the printed permutations are chosen at random, but it is not important to print exactly 20 each time.

## bitcoin_price.py
### Chapter: 115
Task: Use the finnhub.io websockets API to retrieve in real-time data the bitcoin price from the Binance exchange. You'll need to following symbol: BINANCE:BTCUSDT. The payload is json, so use the json module in Python to transform the message to dict.
1. Your class should have the optionto output in the console all relevant trades
2. Implement a data structure which calculates time averages. For each one minute period (e.g. 10:00-10:01, 10:01-10:02, etc.) calculate the volume-weighted average priceof trades made during this minute. Keep in mind that there may be late-arriving data, and the messages you receive are not guaranteed to be ordered.

## convert_farenheit_to_celsius.py
### Chapter: 125
Task: There is a file which contains temperatures in Celsius or Fahrenheit, one string per line. The strings are expected to look like this: 10F or -15C.
Write a Python program which asks:
- the user for an input value for the file location
- reads the file line by line
- converts each temperature to Fahrenheit if it is in Celsius
- writes the converted values in a new file
<a/>
The input and output values should be floating-point numbers.
What could make this program crash? What would we need to do to handle this situation more gracefully?

## avg_function.py
### Chapter: 140
Task: Write a function which takes any number of parameters and returns their average.<br />

## decorator_lucas_numbers.py
### Chapter: 140
Task:
- Write a function to calculate Lucas numbers using the naïve recursion. Lucas numbers are very similar to Fibonacci numbers and are defined by L(0)=2, L(1)=1 and L(n)=L(n-1)+L(n-2)
- Use a timing decorator to log how long each call. How long does it take to calculate L(35)? What about L(100)?
- Now add a memoize decorator. Can you calculate L(100) now?
- Write a function which does prime factorization of a number, e.g. 20633239 = 11*29*71*911. Calculate the prime factorization of L(60) and L(61).

## etl_system.py (Contains all classes) etl_system_test.py (Imports etl_system.py and creates objects of the classes)
### Chapter: 150
Task:
You are creating a pseudo-ETL system, which needs to be able to retrieve data from various sources and transmit the data to various sinks. By data, in this case, we mean short json messages with predefined structure. Here is an example
{"key": "A123", "value":"15.6", "ts":'2020-10-07 13:28:43.399620+02:00'}
You need to implement at least the following functionality:
- Data source is Simulation: this source will generate random data.
- Data source is File: the messages are read from an input file which contains a json array of messages.
- Data sink is Console: the consumed messages are printed to stdout.
- Data sink is PostgreSQL: the consumed messages are inserted in a database table in PostgreSQL
<a/>
Messages should be read and transmitted one by one until the source has no more messages. The Simulation source is infinite -it should always have a new message, if asked. The File source is finite, it ends when the whole file is read.
If you write actual code, make your interface as user-friendly as possible, e.g. make it fluent:
ETL().source(source_args).sink(sink_args).run()

## black_jack_deck.py
### Chapter: 151
Task:
Using the following Suit class:
classSuit(str,Enum):
  Club="♣"
  Diamond="♦"
  Heart="♥"
  Spade="♠"
define a BlackJackCard class and a Deck class so that the following code (which draws 3 cards) will work:
d=Deck()
h=Hand_Lazy(d.pop(),d.pop(),d.pop())
print(h.total)

## lamda_func.py
### Chapter: 160
Task:
1. Create a lambda which returns the first item in a list.
2. Map a lambda which applies the logistic functionto the list [-3, -5, 1, 4] . Round each number to 4 decimal places. (ermm…. that's two nested maps)
