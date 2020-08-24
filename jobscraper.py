import requests
from bs4 import BeautifulSoup

class JobScraper:
    
    results = []
    
    
    def __init__(self, job, location):
        self.job = job
        self.location = location
        self.url = f'https://www.indeed.co.uk/jobs?q={self.job}&l={self.location}'
        
    
    def connect(self):
        self.res = self.res = requests.get(self.url)
        if self.res.status_code == 200:
            return self.res
        return None
    
    def search(self):
        self.__soup_contents()
    
    def __soup_contents(self):
        self.soup = BeautifulSoup(self.connect().text, 'lxml')
        self.jobs = self.soup.find_all('td', {'id': 'resultsCol'})
        for job in self.jobs:
            self.results.append(job.text)
        print(self.results)


test = JobScraper('Python', 'Southampton')
test.connect()
test.search()



