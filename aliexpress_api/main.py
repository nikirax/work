import requests
import xml.etree.ElementTree as ET


REMOTE_FEED_URL = 'https://stripmag.ru/datafeed/p5s_full_stock.xml'
OUR_FEED_URL = 'http://alitair.1gb.ru/Intim_Ali_allfids_2.xml'
SAVING_PATH = 'C:\\Users\\User\\Desktop\\work\\aliexpress_api\\data\\'


def get_filename_from_url(url):
    url = url.split('/')
    return url[url.__len__() - 1]


def download_file_from_url(url, file):
    response = requests.get(url)
    with open(file, 'wb') as f_out:
        f_out.write(response.content)


def update_feed(source, destination):
    # Get Tree of source file
    s_tree = ET.parse(source)
    s_root = s_tree.getroot()
    s_products = s_root.findall('product')
    print('Got data from source file')

    # Get tree of destination file
    d_tree = ET.parse(destination)
    d_root = d_tree.getroot()
    d_offers = d_root.find('shop').find('offers')
    print('Got data from destination file')

    counter = 0
    for item in s_products:
        counter += 1
        if counter % 100 == 0:
            print(f'Processed {counter} items', flush=True)

        id = item.get('prodID')
        offer = d_offers.find(f'offer[@id="{id}"]')
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
    d_tree.write(destination)
    print(f'File saved: {destination}')

if __name__ == '__main__':
    try:
        # Get file names from url
        remote_file = f'{SAVING_PATH}{get_filename_from_url(REMOTE_FEED_URL)}'
        our_file = f'{SAVING_PATH}{get_filename_from_url(OUR_FEED_URL)}'

        # Download files
        download_file_from_url(REMOTE_FEED_URL, remote_file)
        download_file_from_url(OUR_FEED_URL, our_file)

        # Update and save files
        update_feed(remote_file, our_file)
    except Exception as ex:
        print(ex)