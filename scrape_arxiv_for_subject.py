"""
this crawls arvix and fetches the subject for each file
"""


import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://arxiv.org/abs/"

def read_in_for_scraper():
    with open('results/file_ids') as f:
        content = f.readlines()
        content = [x.strip() for x in content] 
        content = [x.strip('.tex') for x in content]
        content = [x for x in content if x[0].isdigit() and x[1].isdigit()]
        return content

def pull_subject_single_id(id):
    try:
        req = requests.get(BASE_URL + id)
        c = req.content
        return c
    except:
        print("request didnt complete")
        return None

def pull_subject_from_content(content):
    try:
        soup = BeautifulSoup(content)
        subject = soup.find_all("span", {'class': 'primary-subject'})
        subj_span = subject[0]
        subj_text = subj_span.get_text()
        return subj_text
    except:
        return None

if __name__ == "__main__":
    total = 16862
    id_to_subject = []
    test_ids = read_in_for_scraper()
    test_ids = test_ids[11:20]
    for test_id in test_ids:
        content = pull_subject_single_id(test_id)
        subject = pull_subject_from_content(content)
        if subject != None:
            id_to_subject.append((test_id, subject))
    with open('all_subjects.csv','a') as out:
        csv_out=csv.writer(out)
        for row in id_to_subject:
                csv_out.writerow(row)
