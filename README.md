# Y Combinator Directory Scraper

YC-Scraper is a tool designed to compile a comprehensive dataset of all companies listed in the [Y Combinator directory](https://www.ycombinator.com/companies/). This directory allows users to search for companies based on industry, region, company size, and more.

## About Y Combinator

Y Combinator is a startup accelerator that has invested in over 4,000 companies with a combined valuation exceeding $600 billion. Its primary goal is to help startups achieve significant growth.

## Requirements

To use this scraper, you need to have [Firefox](https://www.mozilla.org/en-US/firefox/new/) and [geckodriver](https://github.com/mozilla/geckodriver/releases) installed. You can install `geckodriver` by running `brew install geckodriver`.

The following Python packages are required:

- [Scrapy](https://scrapy.org)
- [Selenium](https://www.selenium.dev/documentation/)
- [tqdm](https://tqdm.github.io)
- [Pandas](https://pandas.pydata.org) (optional)

## Usage

1. Clone this repository.
2. Navigate to the `yc-scraper` directory.
