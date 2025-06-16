# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 11:31:00 2025

@author: Bruno
"""

## Imports


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt # Permet de générer des graphiques
import streamlit as st
from myClasses import building, heating_unit, hot_water_tank, pv_installation


if 'trigger_rerun' in st.session_state and st.session_state.trigger_rerun:
    st.session_state.trigger_rerun = False
    st.session_state.trigger_rerun = True

load_profiles = ["Office", "Manufacturing processes",	"Trades (non food)", "Trades (food)",	"Education",	"Crop farming and transportation", "Livestock farming", 	"Water supply and telecom",	"Restaurants",	"Food industry", "Wine industry", "Energy supply and rental", "Hotels", "Bakery", "Property management companies", "Hospital", "Recreational and social activities", "Construcion-related activities"]
locations = ["Uccle",	 "Gembloux",	"Ovifat", "Diepenbeek", "Antwerp", "Dessel", "Sint-Katelijne-Waver",	"Gijzenzele",	"Beitem	", "Zeebrugge"]
types_ventilation = ["No ventilation", "Supply", "Exhaust", "Supply and Exhaust"]
ventilation_settings = ["No ventilation", "Demand management, central", "Demand management, local", "Time setting", "No or unknown setting", "Manual"]
optionnal_data = ["Location", "Annual heat consumption", "Average occupation", "Carbon price", "Selected room temperature (comfort)", "Selected room temperature (reduced)", "Leakage rate", "Ventilation system setting", "Heat recovery efficiency of the ventilation", "Typical opening time", "Typical closing time", "Number of opening days per week", "Type of ventilation", "Room height", "Ventilation flow rate", "Electricity price, peak", "Electricity price, off-peak", "Electricity price peak, start time", "Electricity price peak, end time", "Electricity injection price", "Sanitary hot water temperature", "Fuel price", "Fuel carbon intensity", "Electricity carbon intensity"]    
optionnal_data.sort()

optional_fields = {
    "Annual electricity consumption": {
        "label": "Annual electricity consumption [MWh/year]",
        "type": "number_input",
        "attr": "annual_elec_consumption_kwh",
        "topic" : "General info",
        "kwargs": {"format": "%0.0f"}
    },
    "Annual heat consumption": {
        "label": "Annual heat consumption [MWh/year]",
        "type": "number_input",
        "attr": "annual_heat_consumption_kwh",
        "topic" : "General info",
        "kwargs": {"format": "%0.0f"}
    },
    "Average occupation": {
        "label": "Average occupation [number of occupants per day]",
        "type": "number_input",
        "attr": "average_occupation",
        "topic" : "General info",
        "kwargs": {"format": "%0.0f"}
    },
    "Carbon price": {
        "label": "Carbon price [€/ton]",
        "type": "number_input",
        "attr": "co2_cost",
        "topic" : "General info",
        "kwargs": {"format": "%0.0f"}
    },
    "Electricity carbon intensity": {
        "label": "Grid electricity carbon intensity [kg/kWh]",
        "type": "number_input",
        "attr": "carbon_intensity_grid_kg_per_kwh",
        "topic" : "Electricity",
        "kwargs": {"format": "%0.0f"}
    },
    "Electricity injection price": {
        "label": "Electricity injection price [€/kWh]",
        "type": "number_input",
        "attr": "injection_price_euro_per_kwh",
        "topic" : "Electricity",
        "kwargs": {"format": "%0.2f"}
    },
    "Electricity price peak, start time": {
        "label": "Electricity price peak, start time",
        "type": "slider",
        "attr": "peak_start_time",
        "topic" : "Electricity",
        "kwargs": {"min_value": 0.0, "max_value": 24.0, "value": 7.0, "step": 0.5}
    },
    "Electricity price peak, end time": {
        "label": "Electricity price peak, end time",
        "type": "slider",
        "attr": "peak_end_time",
        "topic" : "Electricity",
        "kwargs": {"min_value": 0.0, "max_value": 24.0, "value": 17.0, "step": 0.5}
    },
    "Electricity price, peak": {
        "label": "Electricity price, peak [€/kWh]",
        "type": "number_input",
        "attr": "elec_price_peak_euro_per_kwh",
        "topic" : "Electricity",
        "kwargs": {"format": "%0.2f"}
    },
    "Electricity price, off-peak": {
        "label": "Electricity price, off-peak [€/kWh]",
        "type": "number_input",
        "attr": "elec_price_off_peak_euro_per_kwh",
        "topic" : "Electricity",
        "kwargs": {"format": "%0.2f"}
    },
    "Fuel carbon intensity": {
        "label": "Fuel carbon intensity [kg/kWh]",
        "type": "number_input",
        "attr": "carbon_intensity_fuel_kg_per_kwh",
        "topic" : "Fuel",
        "kwargs": {"format": "%0.0f"}
    },
    "Fuel price": {
        "label": "Fuel price [€/kWh]",
        "type": "number_input",
        "attr": "fuel_price_euro_per_kwh",
        "topic" : "Fuel",
        "kwargs": {"format": "%0.2f"}
    },
    "Heat recovery efficiency of the ventilation": {
        "label": "Heat recovery efficiency of the ventilation [%]",
        "type": "number_input",
        "attr": "vent_recovery_efficiency",
        "topic" : "Ventilation",
        "kwargs": {"format": "%0f"}
    },
    "Leakage rate": {
        "label": "Leakage rate v50 [m3/h/m2]",
        "type": "number_input",
        "attr": "v50",
        "topic" : "Ventilation",
        "kwargs": {"format": "%0.0f"}
    },
    "Location": {
        "label": "Closest location",
        "type": "selectbox",
        "attr": "location",
        "topic" : "General info",
        "kwargs": {"options": locations}
    },
    "Number of opening days per week": {
        "label": "Number of opening days per week",
        "type": "number_input",
        "attr": "opening_days_per_week",
        "topic" : "General info",
        "kwargs": {"format": "%0.0f"}
    },
    "Room height": {
        "label": "Room height [m]",
        "type": "number_input",
        "attr": "room_height",
        "topic" : "General info",
        "kwargs": {"format": "%0.1f"}
    },
    "Sanitary hot water temperature": {
        "label": "Sanitary hot water temperature [°C]",
        "type": "slider",
        "attr": "Temp_shw_degC",
        "topic" : "Heating and SHW",
        "kwargs": {"min_value": 30, "max_value": 90, "value": 60, "step": 1}
    },
    "Selected room temperature (comfort)": {
        "label": "Selected comfort room temperature [°C]",
        "type": "slider",
        "attr": "Temp_in_comfort",
        "topic" : "Heating and SHW",
        "kwargs": {"min_value": 10.0, "max_value": 30.0, "value": 24.0, "step": 0.5}
    },    
    "Selected room temperature (reduced)":{
        "label": "Selected reduced room temperature [°C]",
        "type": "slider",
        "attr": "Temp_in_reduced",
        "topic" : "Heating and SHW",
        "kwargs": {"min_value": 10.0, "max_value": 30.0, "value": 24.0, "step": 0.5}
    },
    "Type of ventilation": {
        "label": "Type of ventilation",
        "type": "selectbox",
        "attr": "type_ventilation",
        "topic" : "Ventilation",
        "kwargs": {"options": types_ventilation}
    },
    "Typical opening time": {
        "label": "Typical opening time",
        "type": "slider",
        "attr": "opening_time",
        "topic" : "General info",
        "kwargs": {"min_value": 0.0, "max_value": 24.0, "value": 7.0, "step": 0.5}
    },
    "Typical closing time": {
        "label": "Typical closing time",
        "type": "slider",
        "attr": "closing_time",
        "topic" : "General info",
        "kwargs": {"min_value": 0.0, "max_value": 24.0, "value": 17.0, "step": 0.5}
    },
    "Ventilation system setting": {
        "label": "Ventilation system setting",
        "type": "selectbox",
        "attr": "ventilation_setting",
        "topic" : "Ventilation",
        "kwargs": {"options": ventilation_settings}
    },
    "Ventilation flow rate": {
        "label": "Ventilation flow rate [m3/h]",
        "type": "number_input",
        "attr": "Q_vent_m3_h",
        "topic" : "Ventilation",
        "kwargs": {"format": "%0.0f"}
    },
}


if 'buildings' not in st.session_state:
    st.session_state.buildings = []

    
st.subheader("Buildings")
#cols = st.columns(2)  # or 3, or more depending on your layout


if st.button(":material/add: Add a new building"):
    new = building(name=f"Building {len(st.session_state.buildings)+1}", surface_area_m2=100)
    st.session_state.buildings.append(new)
    

if st.session_state.buildings:
    tabs = st.tabs([f":material/home: {b.name}" for b in st.session_state.buildings])

    for idx, tab in enumerate(tabs):
        b = st.session_state.buildings[idx]
        with tab:
            st.markdown("#### Building information")
            col1, col2 = st.columns([4, 1])
            with col1:
                b.name = st.text_input(f"Name for building {idx+1}", value=b.name, key=f"name_{idx}")
            with col2:
                if st.button(":material/delete: Delete", key=f"delete_{idx}"):
                    st.session_state.buildings.pop(idx)
                    st.session_state.trigger_rerun = True
            
            b.surface_area_m2 = st.number_input(f"Surface (m²) for building {idx+1}", value=b.surface_area_m2, key=f"surface_{idx}")
                                    
            profile_input_method = st.radio(
                f"Choose profile input method for {b.name}",
                ["Predefined profile", "Upload CSV profile"],
                key=f"profile_method_{idx}",
                horizontal=True
            )
            
            if profile_input_method == "Predefined profile":
                b.profile = st.selectbox(
                    f"Select a predefined profile",
                    options=load_profiles,
                    index=load_profiles.index(b.profile) if b.profile in load_profiles else 0,
                    key=f"profile_select_{idx}"
                )
                b.custom_profile = None  # Clear any previous CSV
            else:
                uploaded_file = st.file_uploader(
                    f"Upload a CSV file with hourly consumption profile for {b.name} (8760 values)",
                    type="csv",
                    key=f"profile_upload_{idx}"
                )
                if uploaded_file:
                    df = pd.read_csv(uploaded_file, header=None)
                    if df.shape[0] == 8760:
                        b.custom_profile = df[0].values  # or .tolist()
                        st.success("Custom profile uploaded and assigned.")
                    else:
                        st.error("The file must contain exactly 8760 rows (one per hour).")
            
            st.divider()  # <— separates required info from optional
            st.markdown("#### Optional parameters")
    
            # 🧠 Add this below the required fields
            known_data = st.multiselect(f"Which optional variables are known for {b.name}?", optional_fields.keys(), key=f"known_{idx}")
    
            for field in known_data:
                if field == "Selected room temperature (comfort)" and "Selected room temperature (reduced)" in known_data:
                    t_comfort, t_reduced = st.slider("Reduced and comfort temperatures [°C]", 10.0, 30.0, (18.0, 24.0), 0.5, key=f"temp_{idx}")
                    b.Temp_in_comfort = t_comfort
                    b.Temp_in_reduced = t_reduced
                elif field in optional_fields:
                    config = optional_fields[field]
                    widget_type = config["type"]
                    label = config["label"]
                    kwargs = config["kwargs"]
                    attr = config["attr"]
    
                    if widget_type == "number_input":
                        value = st.number_input(label, **kwargs, key=f"{attr}_{idx}")
                    elif widget_type == "selectbox":
                        value = st.selectbox(label, **kwargs, key=f"{attr}_{idx}")
                    elif widget_type == "slider":
                        value = st.slider(label, **kwargs, key=f"{attr}_{idx}")
                    else:
                        continue
    
                    if field == "Heat recovery efficiency of the ventilation":
                        value = value / 100
    
                    setattr(b, attr, value)
            # --------------------------
            # 📦 Envelope elements block
            # --------------------------
            
            prefix = f"{b.name}_{idx}"  # unique key for session state
            
            # Initialize envelope lists
            for elem in ["roofs", "walls", "windows", "floors"]:
                key = f"{prefix}_{elem}"
                if key not in st.session_state:
                    st.session_state[key] = []
            
            st.divider()  # <— separates optional from envelope
        
            st.markdown("#### Envelope elements")
            # ➕ Buttons to add elements
            col1, col2, col3, col4 = st.columns(4)
            if col1.button(":material/add: Add roof", key=f"add_roof_{idx}"):
                st.session_state[f"{prefix}_roofs"].append({"surface": 100.0, "U_value": 0.24})
            if col2.button(":material/add: Add wall", key=f"add_wall_{idx}"):
                st.session_state[f"{prefix}_walls"].append({"surface": 100.0, "U_value": 0.24})
            if col3.button(":material/add: Add window", key=f"add_window_{idx}"):
                st.session_state[f"{prefix}_windows"].append({"surface": 100.0, "U_value": 0.24, "solar_factor": 0.6})
            if col4.button(":material/add: Add floor", key=f"add_floor_{idx}"):
                st.session_state[f"{prefix}_floors"].append({"surface": 100.0, "U_value": 0.24})
            
            
            def render_elements(label, key_base, add_method, extra_fields=None):
                st.markdown(f"##### {label}")
                items = st.session_state[key_base]
                for i, item in enumerate(items):
                    st.markdown(f"**{label[:-1]} {i+1}**")
                    cols = st.columns(len(item) + 1)
                    item["surface"] = cols[0].number_input("Surface (m²)", value=item["surface"], key=f"{key_base}_surface_{i}")
                    item["U_value"] = cols[1].number_input("U-value", value=item["U_value"], key=f"{key_base}_uval_{i}")
                    if extra_fields:
                        for j, (field, label_text) in enumerate(extra_fields.items(), start=2):
                            item[field] = cols[j].number_input(label_text, value=item[field], key=f"{key_base}_{field}_{i}")
                    if cols[-1].button(":material/delete:", key=f"del_{key_base}_{i}"):
                        st.session_state[key_base].pop(i)
                        st.session_state.trigger_rerun = True
            
                if st.button(f":material/check: Confirm {label.lower()}", key=f"confirm_{key_base}"):
                    for e in items:
                        if extra_fields:
                            add_method(e["surface"], e["U_value"], **{f: e[f] for f in extra_fields})
                        else:
                            add_method(e["surface"], e["U_value"])
                    st.success(f"{label} added to {b.name}.")
                    st.session_state[key_base] = []
            
            # ⬇️ Render all 4 envelope types
            render_elements("Roofs", f"{prefix}_roofs", b._add_roof)
            render_elements("Walls", f"{prefix}_walls", b._add_wall)
            render_elements("Windows", f"{prefix}_windows", b._add_window, extra_fields={"solar_factor": "Solar factor"})
            render_elements("Floors", f"{prefix}_floors", b._add_floor)
        
            # --------------------------
            # 🔥 Heating + PV systems
            # --------------------------
            
            st.divider()
            st.markdown("#### Heating and PV systems")
            b._distribute_elec_demand()
            # Initialize heating units and PV systems in session state
            for system in ["heaters", "pv_systems"]:
                key = f"{prefix}_{system}"
                if key not in st.session_state:
                    st.session_state[key] = []
            
            # ➕ Add buttons
            col1, col2 = st.columns(2)
            if col1.button(":material/add: Add heating unit", key=f"add_heater_{idx}"):
                st.session_state[f"{prefix}_heaters"].append({
                    "name": f"Unit {len(st.session_state[f'{prefix}_heaters']) + 1}",
                    "heater_type": "Boiler",
                    "heating_power_kw": 100.0,
                    "fuel": "Gas",
                    "efficiency": 0.9,
                    "purpose": "heating"
                })
            
            if col2.button(":material/add: Add PV system", key=f"add_pv_{idx}"):
                st.session_state[f"{prefix}_pv_systems"].append({
                    "peak_power_kw": 10.0,
                    "annual_production_kwh": 0
                })
            
            # 🔁 Render heating units
            st.markdown("##### Heating Units")
            for i, unit in enumerate(st.session_state[f"{prefix}_heaters"]):
                cols = st.columns(6)
                unit["name"] = cols[0].text_input("Name", value=unit["name"], key=f"{prefix}_heater_name_{i}")
                unit["heater_type"] = cols[1].selectbox("Type", ["Boiler", "Heat pump"], index=0 if unit["heater_type"] == "Boiler" else 1, key=f"{prefix}_heater_type_{i}")
                unit["heating_power_kw"] = cols[2].number_input("Heating Power (kW)", value=unit["heating_power_kw"], key=f"{prefix}_heater_power_{i}")
                unit["fuel"] = cols[3].selectbox("Fuel", ["Gas", "Oil", "Elec"], index=["Gas", "Oil", "Elec"].index(unit["fuel"]), key=f"{prefix}_heater_fuel_{i}")
                unit["efficiency"] = cols[4].number_input("Efficiency (or COP)", min_value=0.0, max_value=10.0, step=0.01, value=unit["efficiency"], key=f"{prefix}_heater_eff_{i}")
                if cols[5].button(":material/delete:", key=f"delete_heater_{prefix}_{i}"):
                    st.session_state[f"{prefix}_heaters"].pop(i)
                    st.session_state.trigger_rerun = True
            
            if st.button(":material/check: Confirm heating units", key=f"confirm_heaters_{idx}"):
                for unit in st.session_state[f"{prefix}_heaters"]:
                    heater = heating_unit(
                        heater_type=unit["heater_type"],
                        heating_power_kw=unit["heating_power_kw"],
                        fuel=unit["fuel"],
                        efficiency=unit["efficiency"],
                        name=unit["name"]
                    )
                    b._add_heating_unit(heater)
                st.success("Heating units added.")
                st.session_state[f"{prefix}_heaters"] = []
            
            # 🔁 Render PV systems
            st.markdown("##### PV Installations")
            for i, pv in enumerate(st.session_state[f"{prefix}_pv_systems"]):
                cols = st.columns(3)
                pv["peak_power_kw"] = cols[0].number_input("Peak Power (kW)", value=pv["peak_power_kw"], key=f"{prefix}_pv_power_{i}")
                pv["location"] = b.location
                pv["annual_production_kwh"] = cols[1].number_input("Annual Production (if known) (kWh)", value=0, key=f"{prefix}_pv_production_{i}")
                if cols[2].button(":material/delete:", key=f"delete_pv_{prefix}_{i}"):
                    st.session_state[f"{prefix}_pv_systems"].pop(i)
                    st.session_state.trigger_rerun = True
            
            if st.button(":material/check: Confirm PV systems", key=f"confirm_pv_{idx}"):
                for pv in st.session_state[f"{prefix}_pv_systems"]:
                    pv_obj = pv_installation(
                        peak_power_kw=pv["peak_power_kw"],
                        location=pv["location"],
                        annual_production_kwh=pv["annual_production_kwh"]
                    )                    
                    b._add_pv_installation(pv_obj)

                    
                st.success("PV systems added.")
                st.session_state[f"{prefix}_pv_systems"] = []
                            
                
st.subheader("Results")

st.page_link("app_pages/02_Results.py", label="Click here to view the results", icon=":material/bar_chart:")

