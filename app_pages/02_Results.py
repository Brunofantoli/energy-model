# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 16:56:41 2025

@author: BrunoFantoli
"""

import streamlit as st

st.page_link("app_pages/01_Data.py", label="Click here to add or modify buildings", icon=":material/home:")

if 'buildings' in st.session_state:
    tab1, tab2 = st.tabs([":material/checklist: Results per building", ":material/compare_arrows: Compare buildings"])

    with tab1:
        for idx, b in enumerate(st.session_state.buildings):
            if b.heating_units == []:
                st.error("Please add at least one heating unit to each building")
                break
            b._hourly_energy_balance()

        if st.button(":material/pie_chart: Show heat loss distribution"):
            for idx, b in enumerate(st.session_state.buildings):
                st.write(f"#### {b.name}")
                if b.roofs.empty and b.floors.empty and b.windows.empty and b.walls.empty:
                    st.write("No envelope elements have been added to the building")
                else:
                    envelope = b._show_envelope()
                    st.pyplot(envelope, use_container_width=False)
                    estimations = b._show_estimations()
                    st.pyplot(estimations, use_container_width=False)

        if st.button(":material/list: Show current buildings"):
            for b in st.session_state.buildings:
                st.write(f"{b.name}: {b.surface_area_m2} m², profile: {b.profile}, Electrical bill : {b.hourly_elec_cost_euro.sum():.0f} €, Number of envelope elements : {len(b.roofs)+len(b.walls)+len(b.windows)+len(b.floors)}, number of PV installations : {len(b.pv_installations)}")
                results = b._show_boiler_consumption()
                results

    with tab2:
        building_names = [b.name for b in st.session_state.buildings]

        building_a_name = st.selectbox("Reference building", building_names, key="building_a")
        building_b_name = st.selectbox("Compared building", building_names, key="building_b")

        if building_a_name != building_b_name:
            building_a = next(b for b in st.session_state.buildings if b.name == building_a_name)
            building_b = next(b for b in st.session_state.buildings if b.name == building_b_name)

            if st.button("Compare"):
                result = building_a._compare_buildings(building_b)
                st.markdown(result, unsafe_allow_html=True)
        else:
            st.warning("Please select two different buildings.")
else:
    st.write(":material/error: Create buildings to have results")