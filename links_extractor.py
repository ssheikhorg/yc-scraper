import json
import re
from time import sleep

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from tqdm import tqdm


class YCLinksExtractor:
    def __init__(self) -> None:
        self.driver = self.make_driver()
        self.page = "https://www.ycombinator.com/companies"

    def make_driver(self):
        service = Service(executable_path="D:\\webdrivers\\geckodriver.exe")
        return Firefox(service=service, options=Options())

    def get_page_source(self):
        """Returns the source of the current page."""
        self.driver.get(self.page)

    def click_see_all_options(self):
        """Clicks 'See all options' button to load checkboxes for all batches."""
        sleep(3)
        see_all_options = self.driver.find_element(By.LINK_TEXT, 'See all options')
        see_all_options.click()

    def compile_batches(self):
        """Returns elements of checkboxes from all batches."""
        pattern = re.compile(r'^(W|S|IK)[012]')
        bx = self.driver.find_elements(By.XPATH, '//label')
        for element in bx:
            if pattern.match(element.text):
                yield element

    def scroll_to_bottom(self):
        """Scrolls to the bottom of the page."""

        # get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # wait to load page
            sleep(3)

            # calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def fetch_url_paths(self):
        """Returns a generator with url paths for all companies."""
        # contains 'companies' but not 'founders'
        elements = self.driver.find_elements(
            By.XPATH, ('//a[contains(@href,"/companies/") and not(contains(@href,"founders"))]'))
        for url in elements:
            yield url.get_attribute('href')

    def write_urls_to_file(ul: list):
        """Appends a list of company urls to a csv file."""
        import csv
        with open('./scrapy-project/ycombinator/start_urls.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(ul)

    def yc_links_extractor(self):
        """Run the main script to write all start urls to a file."""
        print(f"Attempting to scrape links from {self.page}.")
        self.get_page_source()
        self.click_see_all_options()
        # compile an array of batches (checkbox elements)
        batches = self.compile_batches()
        # get only one batch
        one_batch = next(batches)
        count = len(list(one_batch))
        ulist = []

        # for b in tqdm(list(batches)):
        for b in tqdm(list(batches)):
            # filter companies
            b.click()

            # scroll down to load all companies
            self.scroll_to_bottom()

            # fetch links and append them to ulist
            urls = [u for u in self.fetch_url_paths()]
            ulist.extend(urls)

            # uncheck the batch checkbox
            b.click()

        self.write_urls_to_file(ulist)
        self.driver.quit()


if __name__ == '__main__':
    extractor = YCLinksExtractor()
    extractor.yc_links_extractor()
    print("Done.")
