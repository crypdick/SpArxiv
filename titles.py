import csv
from TexSoup import TexSoup
import os


def main():
    file_abstract = []
    path = os.listdir('/Akamai_scratch/SpArxiv')
    indir = '/Akamai_scratch/arxiv/outdir3'
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            try:
                #open file
                soup = TexSoup(open(os.path.join(root,f)))
                #find abstract
                title = soup.find('title').string
                file_abstract.append((f, title))
            except:
                pass
    with open('all_titles.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['file','title'])
        for row in file_abstract:
                csv_out.writerow(row)

if __name__ == "__main__":
  main()
