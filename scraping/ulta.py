from scraper import *

if __name__ == '__main__':
    args: dict = {
        'limit': 5,
        'base': 'https://www.ulta.com/shop/makeup/face/foundation',
        'vendor': 'Ulta',
        'next': (By.XPATH, "//div[@class='LoadContent']/button"),
        'product': (By.XPATH, "//div[@class='ProductCard']/a"),
        'swatch': (By.XPATH, "//div[@class='ProductSwatches']//span[@class='Swatch__image']"),
        'click': True,
        'brand': (By.XPATH, "//div[@class='ProductInformation']/h1/span[1]/a"),
        'name': (By.XPATH, "//div[@class='ProductInformation']/h1/span[2]"),
        'code': (By.XPATH, "//div[@class='SwatchDropDown__nameDescription']/span"),
        'code_attribute': None,
        'img': (By.XPATH, "//div[@class='ProductSwatches']//button[@aria-current='true']/span/img"),
        'price': (By.XPATH, "//div[@class='ProductHero__content']/div[@class='ProductPricing']/span")
    }

    test: Scraper = Scraper(args)
    test.scrape()

    test.to_tsv()
