import requests
from bs4 import BeautifulSoup
import re


class JobScraper:
    results = []
    page_count = 0

    def __init__(self, job, location):
        self.job = job
        self.location = location
        self.url = [f'https://www.indeed.co.uk/jobs?q={self.job}&l={self.location}',
                    f'https://www.monster.co.uk/jobs/search/?q={self.job}&where={self.location}&client=power&cy=uk&rad=25']

    def connect(self):
        for website in self.url:
            res = requests.get(website)
            if res.status_code == 200:
                return res
            return None

    def search(self):
        print(f'Searching for {self.job} jobs in {self.location}')
        # self.__indeed_soup_contents()
        self.__monster_soup_contents()

    def __indeed_soup_contents(self):
        indeed_soup = BeautifulSoup(self.connect().text, 'lxml')
        jobs = indeed_soup.find_all('div', {'class': 'jobsearch-SerpJobCard unifiedRow row result'})
        for i in jobs:
            title = i.find('h2', {'class': 'title'}).text.splitlines()
            company = i.find('div', {'class': 'sjcl'}).text.splitlines()
            formatted_company = ("".join(company).replace(f'{self.location}', ' '))
            summary = i.find('div', {'class': 'summary'}).text.splitlines()
            job_links = i.find('h2', {'class': 'title'}).a['href']

            print("\n".join(title))
            print(re.sub(r'[0-9]+', '', formatted_company))
            print("".join(summary))
            print(f'Click to see more: https://indeed.co.uk{job_links}')
        # while True:
        #     print("\nWould you like to view the next or previous page? ('Next'/'Previous')")
        #     user_input = input('>>>> ')
        #     if user_input.lower() == 'next':
        #         self.__next_page()
        #     elif user_input.lower() == 'previous' and self.page_count != 0:
        #         self.__previous_page()
        #
        #     print('You are currently on the first page and cannot go back anymore')

    def __monster_soup_contents(self):
        monster_soup = BeautifulSoup(self.connect().text, 'lxml')
        jobs = monster_soup.find_all('div', {'class': 'summary'})
        for job in jobs:
            print(job)

    def __next_page(self):
        self.page_count += 10
        self.url = f'https://www.indeed.co.uk/jobs?q={self.job}&l={self.location}&start={self.page_count}'
        self.connect()
        self.search()

    def __previous_page(self):
        self.page_count -= 10
        self.url = f'https://www.indeed.co.uk/jobs?q={self.job}&l={self.location}&start={self.page_count}'
        self.connect()
        self.search()


test = JobScraper('Python', 'Southampton')
test.connect()
test.search()
