import requests
import xml.etree.ElementTree as ET

class Aliexpess_Api:
    REMOTE_FEED_URL = 'https://stripmag.ru/datafeed/p5s_full_stock.xml'
    OUR_FEED_URL = 'http://alitair.1gb.ru/Intim_Ali_allfids_2.xml'
    #your saving path
    SAVING_PATH = 'C:\\Users\\User\\Desktop\\work\\aliexpress_api\\data\\'


    def get_filename_from_url(url, self):
        url = self.url
        url = url.split('/')
        return url[url.__len__() - 1]


    def download_file_from_url(url, file, self):
        self.response = requests.get(self.url)
        with open(file, 'wb') as f_out:
            f_out.write(self.response.content)


    def update_feed(source, destination, self):
        # Get Tree of source file
        self.s_tree = ET.parse(source)
        self.s_root = self.s_tree.getroot()
        self.s_products = self.s_root.findall('product')
        print('Got data from source file')

        # Get tree of destination file
        self.d_tree = ET.parse(destination)
        self.d_root = self.d_tree.getroot()
        self.d_offers = self.d_root.find('shop').find('offers')
        print('Got data from destination file')

        self.counter = 0
        for item in self.s_products:
            self.counter += 1
            if self.counter % 100 == 0:
                print(f'Processed {self.counter} items', flush=True)

            id = item.get('prodID')
            offer = self.d_offers.find(f'offer[@id="{id}"]')
            if offer is None:
                continue

            s_price = item.find('price')
            s_count = item.find('assortiment').find('assort')

            d_price = offer.find('price')
            d_count = offer.find('quantity')

            # Change quantity
            d_count.text = s_count.get('sklad')

            # Change prices
            d_price.set('BaseRetailPrice', s_price.get('BaseRetailPrice'))
            d_price.set('BaseWholePrice', s_price.get('BaseWholePrice'))
            d_price.set('RetailPrice', s_price.get('RetailPrice'))
            d_price.set('WholePrice', s_price.get('WholePrice'))

        print('All tree processed successfuly')
        self.d_tree.write(destination)
        print(f'File saved: {destination}')

if __name__ == '__main__':
    try:
        ali_api = Aliexpess_Api
        # Get file names from url
        remote_file = f'{ali_api.SAVING_PATH}{ali_api.get_filename_from_url(ali_api.REMOTE_FEED_URL)}'
        our_file = f'{ali_api.SAVING_PATH}{ali_api.get_filename_from_url(ali_api.OUR_FEED_URL)}'

        # Download files
        ali_api.download_file_from_url(ali_api.REMOTE_FEED_URL, remote_file)
        ali_api.download_file_from_url(ali_api.OUR_FEED_URL, our_file)

        # Update and save files
        ali_api.update_feed(remote_file, our_file)
    except Exception as ex:
        print(ex)