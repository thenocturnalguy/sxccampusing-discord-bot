from bs4 import BeautifulSoup as soup
import requests as req


# Crawler class for getting the job data
class SXCPCCrawler:

    base_url = ''  # Base url of the site to be crawled

    # Constructor to initialize with the default values
    def __init__(self):
        self.base_url = 'https://sxcpc.blogspot.com/'

    # Function to get the page content and convert it into
    # BeautifulSoup object to be parsed later
    def _get_page_content(self, year='', month='', page_name=''):

        url = self.base_url + year + month  # Crafting the url

        response = req.get(url)
        page_html = soup(response.text, 'lxml')

        return page_html

    # Method to extract the required info
    def crawl_archive(self, year='', month=''):

        page_html = self._get_page_content(year, month)

        return [(item['href'], item.text)
                for item in page_html.body.find('div', {
                    'id': 'ArchiveList'
                }).find('ul', {
                    'class': 'posts'
                }).findAll('a')]

        return archive

    def crawl_post(self, year='', month='', page_name=''):
        page_html = self._get_page_content(year, month, page_name)
        full_post = page_html.find('div', {'class': 'blog-posts'})

        post_date = full_post.h2.span.text
        post_name = full_post.h3.text
        post_body = full_post.find('div', {'class': 'post-body'}).text

        return {
            'post_date': post_date,
            'post_name': post_name,
            'post_body': post_body
        }
