from scraper import *

if __name__ == '__main__':
    args: dict = {
        'limit': 5,
        'base': 'https://www.elfcosmetics.com/face/foundation/?&start=0&sz=999',
        'vendor': 'e.l.f.',
        'next': None,
        'product': (By.CLASS_NAME, 'thumb-link'),
        'swatch': (By.CLASS_NAME, 'swatchanchor'),
        'click': False,
        'brand': None,
        'name': (By.CLASS_NAME, 'product-name'),
        'code': (By.CLASS_NAME, 'swatch_image'),
        'code_attribute': 'alt',
        'img': (By.CLASS_NAME, 'swatch_image'),
        'price': (By.CSS_SELECTOR, "span[itemprop='price']")
    }

    # links: set = {'https://www.elfcosmetics.com/acne-fighting-foundation/300005.html', 'https://www.elfcosmetics.com/halo-glow-liquid-filter/300211.html', 'https://www.elfcosmetics.com/camo-powder-foundation/300205.html', 'https://www.elfcosmetics.com/flawless-satin-foundation/300061.html', 'https://www.elfcosmetics.com/camo-cc-cream/300176.html'}
    # with open('temp.pkl', 'wb') as file:
    #     pickle.dump(links, file)

    test: Scraper = Scraper(args)
    
    test.scrape(4)
    # test.scrape_product('https://www.elfcosmetics.com/camo-cc-cream/300176.html')

    test.to_tsv()