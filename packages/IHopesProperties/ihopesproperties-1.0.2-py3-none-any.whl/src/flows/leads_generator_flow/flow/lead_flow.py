from typing import List

from comps_extractor.comps_generator import generate_comps
from my_asana.tasks_generator import generate_new_property_task
from my_asana.utils import is_task_exists
from property import ForSaleProperty, SoldProperty


def lead_flow(lead_property: ForSaleProperty) -> str:
    address: str = lead_property.address.get_full_address()
    print(f'Working on property: {address}')

    if is_task_exists(lead_property):
        print(f"Task already exists for: {address}")
        print(f'Stopping the process')
        return ''

    # if is_in_no_comps_list(address):
    #     print(f"No comps for property: {address}. Skipping fetch.")
    #     return ''

    comps: List[SoldProperty] = generate_comps(
        for_sale_property=lead_property,
        test_mode=False
    )

    if not comps:  # If no comps found, add to the no-comps list
        print(f"No comps found for property: {address}. Adding to no-comps list.")
        # add_to_no_comps_list(address)
        #return ''

    property_link: str = generate_new_property_task(
        for_sale_property=lead_property,
        comps=comps
    )

    return property_link
