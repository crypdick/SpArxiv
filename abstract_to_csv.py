import csv
from TexSoup import TexSoup
import os
import subprocess, sys
import re


def main():
    file_abstract = []
    #path = os.listdir('/Akamai_scratch/SpArxiv')
    path = os.listdir('/home/shit/bin/ds_shit/distributed/SpArxiv')
    indir = '/Akamai_scratch/arxiv/outdir3'
    indir = "/home/shit/bin/ds_shit/distributed/SpArxiv"

    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            if ".tex" in f:  # TODO delet
                try:
                    #open file
                    soup = TexSoup(open(os.path.join(root,f)))
                    #find abstract
                    abstract = str(soup.find('abstract'))
                    if abstract is not None:
                        # delete Latex formatting
                        abstract = re.sub(r'\\begin\{.*?}(\[.*?\])?({.*?})?', '', abstract)
                        abstract = re.sub(r'\\end\{.*?}', '', abstract)
                        # remove custom named latex commands while keeping the
                        # stuff inside the braces
                        abstract = re.sub(r'\\.*?{(.*?)}', r'\1', abstract)


                        # make abstract one line before append
                        abstract = abstract.replace('\n', ' ')\
                            .replace('\r', '')\
                            .replace('  ', ' ')


                        file_abstract.append((f, abstract))
                except:
                      pass
    with open('all_abstracts.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['file','abstract'])
        for row in file_abstract:
                csv_out.writerow(row)


if __name__ == '__main__':
    main()
