import unittest
from unittest.mock import patch
from jobscraper import JobScraper

class TestJobScraper(unittest.TestCase):
 
    def setUp(self):
        self.test_search1 = JobScraper('Python', 'Test')
        self.test_search2 = JobScraper('Java', 'Test')
        self.test_search3 = JobScraper('Swift', 'Test')
 
    def test_correct_url_format(self):
        self.assertEqual(self.test_search1.url, 'https://www.indeed.co.uk/jobs?q=Python&l=Test')
        self.assertEqual(self.test_search2.url, 'https://www.indeed.co.uk/jobs?q=Java&l=Test')
        self.assertEqual(self.test_search3.url, 'https://www.indeed.co.uk/jobs?q=Swift&l=Test')
    
    
    def test_site_response_code(self):
        with patch('requests.get') as mock_request:
            
            mock_request.return_value.status_code = 200
            
            self.assertTrue(self.test_search1.connect())
            self.assertTrue(self.test_search2.connect())
            self.assertTrue(self.test_search3.connect())
        
    def test_soup_content_on_page_is_appended_to_list(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
