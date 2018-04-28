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
                count = 0
                references = soup.find_all('bibitem')
                for reference in references:
                  count +=1
                references = soup.find_all('cite')
                for reference in references:
                  count +=1
                file_abstract.append((f, count))
            except:
                pass
    with open('all_references.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['file','reference_count'])
        for row in file_abstract:
                csv_out.writerow(row)

if __name__ == "__main__":
  main()
