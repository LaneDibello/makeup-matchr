from scraper import *

if __name__ == '__main__':
    args: dict = {
        'limit': 5,
        'base': 'https://www.sephora.com/shop/foundation-makeup',
        'vendor': 'Sephora',
        'next': (By.CLASS_NAME, 'css-bk5oor'),
        'product': (By.CLASS_NAME, 'css-klx76'),
        'swatch': (By.XPATH, "//button[@aria-describedby='colorSwatch']"),
        'click': True,
        'brand': (By.XPATH, "//a[@data-at='brand_name']"),
        'name': (By.XPATH, "//span[@data-at='product_name']"),
        'code': (By.XPATH, "//div[@data-at='sku_name_label']/span"),
        'code_attribute': None,
        'img': (By.XPATH, "//button[@data-at='selected_swatch']/div/img"),
        'price': (By.XPATH, "//p[@data-comp='Price ']/span/span[1]/b")
    }

    test: Scraper = Scraper(args)
    test.scrape(4)

    test.to_tsv()