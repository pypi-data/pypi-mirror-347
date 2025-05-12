from copy import copy
from typing import List

from tqdm import tqdm

from flows.leads_generator_flow.flow.lead_flow import lead_flow
from flows.leads_generator_flow.flow.lead_source import LEADS_QUERY_SOURCES
from flows.leads_generator_flow.leads_filters.filters import leads_filters
from flows.leads_generator_flow.rentcast.fetch_for_sale_properties import fetch_active_for_sale_properties
from property import ForSaleProperty

if __name__ == '__main__':

    print('Main flow - START!')

    # Fetch the active for sale properties
    total_success_count: int = 0
    for lead_source in LEADS_QUERY_SOURCES:
        print(f'Fetching active for sale properties for {lead_source.to_string()}')
        curr_lead_source_properties: List[ForSaleProperty] = fetch_active_for_sale_properties(
            lead_source=lead_source
        )
        print(f'Fetched {len(curr_lead_source_properties)} active for sale properties for {lead_source.to_string()}')

        for_sale_to_filter: List[ForSaleProperty] = copy(curr_lead_source_properties)
        # Filter the leads (active for sale properties)
        for leads_filter in leads_filters:
            for_sale_to_filter: List[ForSaleProperty] = leads_filter.apply_filter(for_sale_to_filter)
            print(f'After applying filter {leads_filter.name}, {len(for_sale_to_filter)} properties left')

        # Iterate over the properties and generate tasks
        for for_sale_property in tqdm(for_sale_to_filter, desc="Processing"):
            try:
                property_link: str = lead_flow(lead_property=for_sale_property)
                if property_link:
                    total_success_count += 1
                    print(f'Property link: {property_link}')
                else:
                    print(f'No task generated for {for_sale_property.address.get_full_address()}')
            except Exception as e:
                print(f'Failed to process property: {for_sale_property.address.get_full_address()} [error={e}]')
