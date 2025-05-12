from typing import List

from apify.zillow_scrapers.zillow_detail_scraper.on_the_fly_runner import generate_for_sale_property_from_address
from flows.leads_generator_flow.flow.lead_flow import lead_flow
from property import ForSaleProperty, PropertyAddress

if __name__ == '__main__':

    addresses: List[str] = [
        '2725 Connecticut Avenue, Dormont, PA 15216',
        '439 William St, PA 15210'
    ]

    for address in addresses:
        print(f'Working on address: {address}')
        for_sale_property: ForSaleProperty = generate_for_sale_property_from_address(address=address)
        lead_flow(lead_property=for_sale_property)
