ELEMENT_KEYS: set = {
    'next'
}

class Scraper:
    element: dict = {}

    data: dict = {
        'name': None,
        'url': None,
        'vendor': None,
        'red': None,
        'green': None,
        'blue': None
    }

    def __init__(self, args: dict) -> None:
        """Requires a dictionary including keys within ELEMENT_KEYS"""
        missing: set = ELEMENT_KEYS - args.keys()

        if missing != set():
            print(f'[ERROR]\tScraper object missing {missing} in constructor')
            exit()
        
        self.element = args
        

    def __get_name(self) -> None:
        self.data['name'] = None

    def __get_url(self) -> None:
        self.data['url'] = None

    def __get_vendor(self) -> None:
        self.data['vendor'] = None
    
    def __get_rgb(self) -> None:
        self.data['red'] = None
        self.data['green'] = None
        self.data['blue'] = None
    
    def scrape_data(self, rate_limit: int = 0) -> None:
        return

    def get_data(self) -> dict | None:
        if None in self.data.values():
            return None
        
        return self.data


test: Scraper = Scraper({'next': 2})