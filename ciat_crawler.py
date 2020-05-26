import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Crawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.inner_urls = set()
        self.inner_page_info = []
        self.item_urls = set()
        self.items = []

    def _get_web_driver(self, CHROME_PATH, headless=False):
        """
        Create a Webdriver
        """
        options = Options()
        if headless:
            options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options,
                                       executable_path=CHROME_PATH)

    def check_page_link(self, url):
        """
        check if this page is what we need
        """
        try:
            self.driver.get(url)
            assert "No results found." not in self.driver.page_source
        except TimeoutException as error:
            print(url, error)

    def get_inner_links(self):
        """
        collect links to the necessary internal pages
        Add links in to iinner_pages_links Set
        """
        url = self.start_url
        self.check_page_link(url, driver)
        self.driver.get(url)
        self.inner_urls.add('')

    def parse_inner_page(self, inner_url):
        """
        Recive internal pages url and
        collect info to the necessary internal pages
        and add item links
        """
        url = inner_url
        self.check_page_link(url)
        self.driver.get(url)
        time.sleep(2)
        self.inner_page_info.append('')
        self.item_urls.add('')
        """
        pagination block needed
        """

    def parse_item_page(self, item_url):
        """
        collect info for item
        """
        url = item_url
        self.check_page_link(url)
        self.driver.get(url)
        time.sleep(2)
        self.items.append('')


def main():
    START_URL = ''
    CHROME_PATH = os.path.join(__location__, 'chromedriver')
    crawler = Crawler(START_URL)
    crawler._get_web_driver(CHROME_PATH, headless=True)
    crawler.get_inner_links()
    for inner_url in crawler.inner_urls:
        crawler.parse_inner_page(inner_url)
        time.sleep(3)
    for item_url in crawler.item_urls:
        crawler.parse_item_page(item_url)
        time.sleep(3)


if __name__ == "__main__":
    main()
