import requests
from bs4 import BeautifulSoup
import re


class JobScraper:
    results = []
    page_count = 0

    def __init__(self, job, location):
        self.job = job
        self.location = location
        self.url = f'https://www.indeed.co.uk/jobs?q={self.job}&l={self.location}'

    def connect(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            return res
        return None

    def search(self):
        print(f'Searching for {self.job} jobs in {self.location}')
        self.__indeed_soup_contents()
        
    def __indeed_soup_contents(self):
        indeed_soup = BeautifulSoup(self.connect().text, 'lxml')
        jobs = indeed_soup.find_all('div', {'class': 'jobsearch-SerpJobCard unifiedRow row result'})
        for i in jobs:
            title = i.find('h2', {'class': 'title'}).text.splitlines()
            company = i.find('div', {'class': 'sjcl'}).text.splitlines()
            formatted_company = ("".join(company).replace(f'{self.location}', f'\n{self.location}'))
            summary = i.find('div', {'class': 'summary'}).text.splitlines()
            job_links = i.find('h2', {'class': 'title'}).a['href']

            print("\n".join(title))
            print(re.sub(r'[0-9]+', '', formatted_company))
            print("".join(summary))
            print(f'Click to see more: https://indeed.co.uk{job_links:.40}')
        while True:
            print("\nWould you like to view the next or previous page? ('Next'/'Previous')")
            user_input = input('>>>> ')
            if user_input.lower() == 'next':
                self.__next_page()
            elif user_input.lower() == 'previous' and self.page_count != 0:
                self.__previous_page()
            print('You are currently on the first page'
                  'and cannot go back any more')

    def __next_page(self):
        self.page_count += 10
        self.url = f'https://www.indeed.co.uk/jobs?q={self.job}&l={self.location}&start={self.page_count}'
        print(self.url)
        self.connect()
        self.search()

    def __previous_page(self):
        self.page_count -= 10
        self.url = f'https://www.indeed.co.uk/jobs?q={self.job}&l={self.location}&start={self.page_count}'
        print(self.url)
        self.connect()
        self.search()


if __name__ == "__main__":
    user_location = input("Where would you like to look for jobs?\n")
    user_job = input("Enter a job\n")
    user_search = JobScraper(user_job, user_location)
    user_search.connect()
    user_search.search()