import numpy as np
from os import listdir
from os.path import isfile, join
files = [f for f in listdir("heatmap/") if isfile(join("heatmap/", f))]
def readFile(file):
    return np.loadtxt("heatmap/" + file)
def findNumpyDifference(anp, bnp):
    return np.subtract(anp, bnp)
def main():
    firstHeatmap = readFile(files[0]).tolist()
    for file in files:
        heatmap = readFile(file).tolist()
        diff = findNumpyDifference(firstHeatmap, heatmap)
        print(diff.amax())


if __name__ == "__main__":
    main()