from typing import List

from apify.zillow_scrapers.zillow_detail_scraper.on_the_fly_runner import generate_for_sale_property_from_address
from flows.leads_generator_flow.flow.lead_flow import lead_flow
from google_drive.authenticator import get_google_services
from property import ForSaleProperty, PropertyAddress

if __name__ == '__main__':

    addresses: List[str] = [
        '211 Ohio St, Monroeville, PA 15146',
    ]

    print('Authenticating...')
    get_google_services()
    print('Authenticated successfully.')

    for address in addresses:
        print(f'Working on address: {address}')
        for_sale_property: ForSaleProperty = generate_for_sale_property_from_address(address=address)
        lead_flow(lead_property=for_sale_property)
