from pyspark import SparkContext

import os


def main():
    sc = SparkContext(appName='SparkWordCount')
    path = os.listdir('/Akamai_scratch/SpArxiv')
    print(path)
    temp_file = sc.textFile(os.path.join(os.getcwd(), path[1])).flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    indir = '/Akamai_scratch/arxiv/outdir3'
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            try:
                input_file = sc.textFile(os.path.join(root, f))
                counts = input_file.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
                temp_file.union(counts)
            except:
                pass
    counts.saveAsTextFile('/Akamai_scratch/spArxiv/results/all.wordcount.csv')
    sc.stop()

if __name__ == '__main__':
    main()
