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
    test_ids = read_in_for_scraper()
    indexes = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000]
    for index in indexes:
        print(str(index) + " is the starting index")
        id_to_subject = []
        current_ids = test_ids[index:index + 500]
        for current_id in current_ids:
            print(str(current_id) + " is the current ID")
            content = pull_subject_single_id(current_id)
            subject = pull_subject_from_content(content)
            if subject != None:
                id_to_subject.append((current_id, subject))
        with open('all_subjects.csv','a') as out:
            csv_out=csv.writer(out)
            for row in id_to_subject:
                    csv_out.writerow(row)
