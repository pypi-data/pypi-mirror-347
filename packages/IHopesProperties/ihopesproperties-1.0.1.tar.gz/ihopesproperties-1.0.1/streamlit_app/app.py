import sys
import os
sys.path.append(os.path.abspath("src"))
import streamlit as st
from datetime import datetime

from flows.leads_generator_flow.flow.lead_flow import lead_flow

from apify.zillow_scrapers.zillow_detail_scraper.on_the_fly_runner import generate_for_sale_property_from_address

from property import ForSaleProperty

# Simulated database
LEADS = []

def create_lead(address):
    return {
        "id": len(LEADS) + 1,
        "address": address,
        "status": "processing",
        "processedDate": datetime.now().isoformat()
    }

def update_lead(lead, **kwargs):
    lead.update(kwargs)

st.title("🏡 Property Lead Generator - IHopes25To40 🏡")
st.write("Enter a property address to analyze comps and create Asana task.")

if "current_lead" not in st.session_state:
    st.session_state.current_lead = None
if "error" not in st.session_state:
    st.session_state.error = None
if 'current_address' not in st.session_state:
    st.session_state.current_address = None

address = st.text_input("Property Address")
if st.button("Process"):
    if address:
        st.session_state.error = None
        st.session_state.current_address = address
        lead = create_lead(address)
        LEADS.insert(0, lead)
        st.session_state.current_lead = lead

        with st.spinner("Processing property..."):
            try:
                for_sale_property: ForSaleProperty = generate_for_sale_property_from_address(address=address)
                property_link: str = lead_flow(lead_property=for_sale_property)
                update_lead(lead,
                            status="completed",
                            property_link=property_link
                            )
            except Exception as e:
                update_lead(lead, status="failed")
                st.session_state.error = str(e)
    else:
        st.warning("Please enter an address.")

# Show error
if st.session_state.error:
    st.error(f"Error: {st.session_state.error}")

# Show results
if st.session_state.current_lead and st.session_state.current_lead["status"] == "completed":
    lead = st.session_state.current_lead
    if property_link:
        st.success("Processing complete! See link to Asana task below.")
    else:
        st.warning(f"Did not create a new task. Task is probably already exists for {st.session_state.current_address}")
    st.json(lead)

# Recent leads
st.subheader("📜 Recent Leads")
if LEADS:
    st.table([{
        "Address": l["address"],
        "Status": l["status"],
        "Date": l["processedDate"][:10],
        "Asana task": l['property_link']
    }
        for l in LEADS])
else:
    st.info("No leads yet.")
