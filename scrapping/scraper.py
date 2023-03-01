import re
from multiprocessing import Pool
from time import sleep

from numpy.random import normal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# Sleep length 90% CI: [limit - SLEEP_JITTER, limit + SLEEP_JITTER]
SLEEP_JITTER: float = 0.25

# Makes Selenium run in headless mode and disables log prints
OPTIONS = Options()
OPTIONS.headless = False
OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])

def error(msg: str, quit: bool = True) -> None:
    print(f'[ERROR]\t{msg}')

    if quit:
        exit()

def warn(msg: str) -> None:
    print(f'[WARN]\t{msg}')

class Product:
    vendor: str = None
    url: str = None

    brand: str = None
    name: str = None
    code: str = None

    red: int = None
    green: int = None
    blue: int = None

    def __clean(self) -> None:
        self.vendor = self.vendor.strip().replace('\t', ' ')
        self.url = self.url.strip()

        self.brand = self.brand.strip().replace('\t', ' ')
        self.name = self.name.strip().replace('\t', ' ')
        self.code = self.code.strip().replace('\t', ' ')

    def __validate_vendor(self) -> bool:
        if not self.vendor:
            return False
        
        if len(self.vendor) > 128:
            return False
        
        return True
    
    def __validate_url(self) -> bool:
        if not self.url:
            return False

        if len(self.url) > 2048:
            return False

        # https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not regex.match(self.url):
            return False
        
        return True
    
    def __validate_brand(self) -> bool:
        if not self.brand:
            return False

        if len(self.brand) > 256:
            return False
        
        return True
    
    def __validate_name(self) -> bool:
        if not self.name:
            return False
        
        if len(self.name) > 128:
            return False

        return True
    
    def __validate_code(self) -> bool:
        if not self.code:
            return False
        
        if len(self.code) > 128:
            return False

        return True

    def __validate_rgb(self) -> bool:
        if not self.red in range(256):
            return False
        
        if not self.green in range(256):
            return False
        
        if not self.blue in range(256):
            return False
        
        return True

    def __validate(self) -> bool:
        valid: bool = True

        if not self.__validate_vendor():
            warn('Invalid vendor "{self.vendor}" ({self.url})')
            valid = False
        
        if not self.__validate_url():
            warn('Invalid URL "{self.url}" ({self.url})')

        if not self.__validate_brand():
            warn('Invalid brand "{self.brand}" ({self.url})')
            valid = False
        
        if not self.__validate_name():
            warn('Invalid name "{self.name}" ({self.url})')
            valid = False
        
        if not self.__validate_code():
            warn('Invalid color code "{self.code}" ({self.url})')
            valid = False
        
        if not self.__validate_rgb():
            warn('Invalid (R, G, B) value ({self.red}, {self.green}, {self.blue}) ({self.url})')
            valid = False
        
        return valid

    def to_list(self) -> list:
        self.__clean()
        self.__validate()

        product: list = [
            self.name,
            self.vendor,
            self.red,
            self.green,
            self.blue,
            self.url,
            self.brand,
            self.code
        ]

        return product


class Scraper:
    __args: dict = {
        'base': None
    }

    __product_links: set

    __product_template: dict  = {
        'name': None,
        'url': None,
        'vendor': None,
        'red': None,
        'green': None,
        'blue': None
    }

    __products: dict


    def __init__(self, args: dict) -> None:
        """Requires a dictionary with all keys in the '__args' dictionary"""
        missing: set = self.__args.keys() - args.keys()

        if missing != set():
            print(f'[ERROR]\tScraper object missing {missing} in constructor')
            exit()
        
        for key in self.__args.keys():
            self.__args[key] = args[key]


    def __random_sleep(mu: float):
        """Some sites don't like web scraping and this ensures the scraper doesn't get blacklisted"""

        # This should make the 90% confidence interval close to [mu - 0.25, mu + 0.25]
        sigma: float = SLEEP_JITTER / 1.644854

        length: float = normal(mu, sigma)
        if length < 0:
            length = 0
        
        sleep(length)


    def __scrape_links(self, rate_limit: float = 0) -> None:
        self.__product_links.add()


    def __scrape_name(self) -> None:
        self.__data['name'] = None


    def __scrape_url(self) -> None:
        self.__data['url'] = None


    def __scrape_vendor(self) -> None:
        self.__data['vendor'] = None
    

    def __scrape_rgb(self) -> None:
        self.__data['red'] = None
        self.__data['green'] = None
        self.__data['blue'] = None
    

    def scrape_data(self, rate_limit: float = 0) -> None:
        return


    def get_data(self) -> dict | None:
        if None in self.__data.values():
            return None
        
        if not self.__data['red'] in range(256):
            return None
        
        if not self.__data['green'] in range(256):
            return None
        
        if not self.__data['blue'] in range(256):
            return None

        return self.__data


test: Scraper = Scraper({})