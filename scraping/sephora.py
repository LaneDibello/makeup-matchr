from scraper import *

if __name__ == '__main__':
    args: dict = {
        'limit': 5,
        'base': 'https://www.sephora.com/shop/foundation-makeup',
        'vendor': 'Sephora',
        'next': (By.CLASS_NAME, 'css-bk5oor'),
        'product': (By.CLASS_NAME, 'css-klx76'),
        'swatch': (By.CLASS_NAME, 'css-10zyrsm'),
        'click': True,
        'brand': (By.CLASS_NAME, 'css-1gyh3op'),
        'name': (By.CLASS_NAME, 'css-1pgnl76'),
        'code': (By.CLASS_NAME, 'css-15ro776'),
        'code_attribute': 'text',
        'price': (By.CLASS_NAME, 'css-18jtttk')
    }

    test: Scraper = Scraper(args)

    test.scrape()

    test.to_tsv()