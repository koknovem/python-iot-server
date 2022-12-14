import numpy as np
from os import listdir
from os.path import isfile, join
files = [f for f in listdir("heatmap/") if isfile(join("heatmap/", f))]
def readFile(file):
    return np.loadtxt("heatmap/" + file)
def parseFmtToFloat(fmt):
    pass
def findNumpyDifference(anp, bnp):
    pass
def main():
    for file in files:
        content = readFile(file)
        print(content.amax())

if __name__ == "__main__":
    main()