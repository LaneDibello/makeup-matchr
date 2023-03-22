import pickle
import re
from io import BytesIO
from multiprocessing.pool import ThreadPool
from os.path import isfile
from time import sleep

from colorthief import ColorThief
from numpy.random import normal
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# Amount of time to sleep before timing out
TIMEOUT: int = 30

# Sleep length 90% CI: [limit - SLEEP_JITTER, limit + SLEEP_JITTER]
SLEEP_JITTER: float = 0.25

# Makes Selenium run in headless mode and disables log prints
OPTIONS = Options()
OPTIONS.headless = False
OPTIONS.add_extension('./uBlock-Origin.crx')
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

    price: float = None

    red: int = None
    green: int = None
    blue: int = None

    def __str__(self) -> str:
        output: str = f'Vendor:  {self.vendor}\n'
        output += f'URL:  {self.url}\n'
        
        output += f'Brand:  {self.brand}\n'
        output += f'Product Name:  {self.name}\n'
        output += f'Color Code:  {self.code}\n'
        output += f'Price:  {self.price}\n'

        output += f'(R, G, B):  ({self.red}, {self.green}, {self.blue})'

        return output

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

    def __validate_price(self) -> bool:
        if self.price <= 0:
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

    def validate(self) -> bool:
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
        
        if not self.__validate_price():
            warn('Invalid price "{self.price}" ({self.url})')
            valid = False
        
        if not self.__validate_rgb():
            warn('Invalid (R, G, B) value ({self.red}, {self.green}, {self.blue}) ({self.url})')
            valid = False
        
        return valid

    def to_list(self) -> list:
        self.__clean()
        self.validate()

        product: list = [
            self.name,
            self.vendor,
            self.red,
            self.green,
            self.blue,
            self.url,
            self.brand,
            self.code,
            self.price
        ]

        return product


class Scraper:
    # __rate_limit: float = None

    __args: dict = {
        'limit': None,
        'base': None,
        'vendor': None,
        'next': None,
        'product': None,
        'swatch': None,
        'click': None,
        'brand': None,
        'name': None,
        'code': None,
        'code_attribute': None,
        'price': None
    }

    __product_links: set[str] = set()
    __products: list[Product] = list()

    def __init__(self, args: dict) -> None:
        """Requires a dictionary with all keys in the '__args' dictionary"""
        missing: set = self.__args.keys() - args.keys()

        if missing != set():
            print(f'[ERROR]\tScraper object missing {missing} in constructor')
            exit()
        
        for key in self.__args.keys():
            self.__args[key] = args[key]


    def __random_sleep(self):
        """Some sites don't like web scraping and this ensures the scraper doesn't get blacklisted"""

        # This should make the 90% confidence interval close to [mu - 0.25, mu + 0.25]
        sigma: float = SLEEP_JITTER / 1.644854

        length: float = normal(self.__args['limit'], sigma)
        if length < 0:
            length = 0
        
        sleep(length)
    
    def __get_color(self, img: bytes) -> tuple[int, int, int]:
        color_thief: ColorThief = ColorThief(BytesIO(img))

        return color_thief.get_color(quality=1)

    def __scrape_links(self) -> None:
        with webdriver.Chrome(options=OPTIONS) as driver:            
            driver.get(self.__args['base'])
            driver.maximize_window()
            driver.set_page_load_timeout(30)

            wait: WebDriverWait = WebDriverWait(driver, TIMEOUT)

            is_next: bool = True
            while is_next:
                is_next = False

                page_height: int = int(driver.execute_script("return document.body.scrollHeight"))
                window_height: int = driver.get_window_size()['height']
                
                for i in range(int(page_height / window_height) + 1):
                    self.__random_sleep()
                    driver.execute_script(f'window.scrollTo(0, {i * window_height});')

                    wait.until(ec.element_to_be_clickable(self.__args['product']))
                    elements: list[WebElement] = driver.find_elements(*self.__args['product'])

                    for element in elements:
                        href: str = element.get_attribute('href')
                        href = href.split('?')[0]
                        self.__product_links.add(href)
                    
                try:
                    driver.find_element(*self.__args['next']).click()
                    is_next = True
                except:
                    pass
                
        print(self.__product_links)
        print(len(self.__product_links))

    def scrape_product(self, product_link: str) -> Product:
        self.__random_sleep()
        products: set[Product] = set()

        try:
            with webdriver.Chrome(options=OPTIONS) as driver:
                driver.get(product_link)
                driver.maximize_window()
                driver.set_page_load_timeout(30)

                wait: WebDriverWait = WebDriverWait(driver, TIMEOUT)

                wait.until(ec.element_to_be_clickable(self.__args['swatch']))
                swatches: list[WebElement] = driver.find_elements(*self.__args['swatch'])

                for swatch in swatches:
                    product: Product = Product()

                    if self.__args['click']:
                        try:
                            swatch.click()
                        except:
                            continue

                    self.__random_sleep()

                    # Get URL
                    if self.__args['click']:
                        product.url = driver.current_url
                    else:
                        product.url = swatch.get_attribute('href')

                    # Set vendor
                    product.vendor = self.__args['vendor']

                    # Get brand
                    if not self.__args['brand']:
                        product.brand = self.__args['vendor']
                    else:
                        wait.until(ec.visibility_of_element_located(self.__args['brand']))
                        element: WebElement = driver.find_element(*self.__args['brand'])
                        product.brand = element.text

                    # Get product name
                    wait.until(ec.visibility_of_element_located(self.__args['name']))
                    element = driver.find_element(*self.__args['name'])
                    product.name = element.text

                    # Get product price
                    wait.until(ec.visibility_of_element_located(self.__args['price']))
                    element = driver.find_element(*self.__args['price'])
                    price: float = float(element.text.replace('$', ''))
                    product.price = price

                    # Get color code
                    wait.until(ec.visibility_of_element_located(self.__args['code']))
                    if self.__args['click']:
                        element: WebElement = driver.find_element(*self.__args['code'])
                    else:
                        element: WebElement = swatch.find_element(*self.__args['code'])

                    code: str = element.get_attribute(self.__args['code_attribute'])

                    # Clean up the received text
                    code = code.split(': ')[-1]
                    code = code.split('-')[0]
                    product.code = code.strip()

                    # Get product color
                    # NOTE: Color may be incorrect if screenshot has none swatch colors in it
                    driver.execute_script("arguments[0].scrollIntoView();", swatch)
                    (product.red, product.green, product.blue) = self.__get_color(swatch.screenshot_as_png)

                    products.add(product)
        except Exception as e:
            print(e)

        return products
    
    def scrape(self, processes: int = 1) -> None:
        # self.__rate_limit = self.__args['limit'] * processes

        link_file = f'{self.__args["vendor"]}_links.pkl'
        if isfile(link_file):
            with open(link_file, 'rb') as file:
                self.__product_links = pickle.load(file)
        else:
            self.__scrape_links()

            with open(link_file, 'wb') as file:
                pickle.dump(self.__product_links, file)
        
        with ThreadPool(processes) as p:
            self.__products = p.map(self.scrape_product, self.__product_links)
        
        with open(f'{self.__args["vendor"]}_products.pkl', 'wb') as file:
            pickle.dump(self.__products, file)

        products: set[Product] = set()
        for product_set in self.__products:
            for product in product_set:
                products.add(product)
        
        self.__products = products
    
    def to_tsv(self) -> None:
        with open(f'{self.__args["vendor"]}.tsv', 'w') as file:
            for product in self.__products:
                line = '\t'.join([str(elem) for elem in product.to_list()])
                line += '\n'
                file.write(line)
