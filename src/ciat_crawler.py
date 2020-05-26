import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from data_output import Output

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Crawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.inner_urls = []
        self.inner_page_info = []
        self.item_urls = set('')
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
        url = 'https://ciat.org.uk/page-types/find_a_practice/loadMore/?\
               itemclass=.member-item&maxrows=20&practice_specialism&\
               searchby=location&q&page={}&startRow={}'
        self.inner_urls.append(url.format(1, 1))
        for page, row in zip(range(2, 78), range(21, 1512, 20)):
            self.inner_urls.append(url.format(page, row))
        self.inner_urls.append(url.format(77, 1511))

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

        def get_email(row):
            try:
                email = row.find_element_by_xpath('./div[3]/p[3]/a').text
                return email
            except NoSuchElementException:
                return 'No email'

        for row in self.driver.find_elements_by_xpath(
                            '//div[@class="row member-item"]'):
            title = row.find_element_by_xpath('./div[1]/h3/a').text
            company_name = title.split('/')[0]
            if len(title.split('/')) > 1:
                name = title.split('/')[1].strip()
            else:
                name = 'None'
            email = get_email(row)
            inner_page_info = [company_name, name, email]
            self.inner_page_info.append(inner_page_info)


def main():
    START_URL = 'https://ciat.org.uk/find-a-practice.html?\
                 q=&search_by=location'
    CHROME_PATH = os.path.join(__location__, 'chromedriver')
    crawler = Crawler(START_URL)
    crawler._get_web_driver(CHROME_PATH, headless=True)
    crawler.get_inner_links()
    for inner_url in crawler.inner_urls[:2]:
        crawler.parse_inner_page(inner_url)
        time.sleep(2)
    Output(crawler.inner_page_info).to_csv()


if __name__ == "__main__":
    main()
