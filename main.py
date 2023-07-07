import sys
from plotter import plotter

def main():
    if (len(sys.argv) < 2):
        print("Error: not enough arguments")
        quit()
    thePlotter = plotter() 
    thePlotter.run(sys.argv[1])
  
main()