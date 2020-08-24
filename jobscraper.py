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
        self.jobs = self.soup.find('tbody', {'id': 'resultsBodyContent'})
        self.title = self.jobs.find_all('h2', {'class': 'title'})
        self.company = self.jobs.find_all('div', {'class': 'sjcl'})
        self.salary = self.jobs.find_all('div', {'class': 'salarySnippet salarySnippetDemphasizeholisticSalary'})
        self.summary = self.jobs.find_all('div', {'class': 'summary'})
        self.results.append(self.title + self.company + self.salary + self.salary + self.summary)
        

            
test = JobScraper('Python', 'Southampton')
test.connect()
test.search()



