from time import sleep
from numpy.random import normal

class Scraper:
    base: str
    element: dict = {
        '': None
    }

    products: set

    data: dict = {
        'name': None,
        'url': None,
        'vendor': None,
        'red': None,
        'green': None,
        'blue': None
    }


    def __init__(self, base, args: dict) -> None:
        """Requires a base url and dictionary with all keys in the 'element' dictionary"""
        missing: set = self.element.keys() - args.keys()

        if missing != set():
            print(f'[ERROR]\tScraper object missing {missing} in constructor')
            exit()
        
        for key in self.element.keys():
            self.element[key] = args[key]


    def __random_sleep(mu: float):
        """Some sites don't like web scraping and this ensures the scraper doesn't get blacklisted"""

        # This should make the 90% confidence interval close to [mu - 0.25, mu + 0.25]
        sigma: float = 0.25
        sigma /= 1.644854

        length: float = normal(mu, sigma)
        if length < 0:
            length = 0
        
        sleep(length)


    def __scrape_links(self, rate_limit: float = 0) -> None:
        self.products.add()

    def __scrape_name(self) -> None:
        self.data['name'] = None


    def __scrape_url(self) -> None:
        self.data['url'] = None


    def __scrape_vendor(self) -> None:
        self.data['vendor'] = None
    

    def __scrape_rgb(self) -> None:
        self.data['red'] = None
        self.data['green'] = None
        self.data['blue'] = None
    

    def scrape_data(self, rate_limit: float = 0) -> None:
        return


    def get_data(self) -> dict | None:
        if None in self.data.values():
            return None
        
        return self.data


test: Scraper = Scraper({'next': 2})