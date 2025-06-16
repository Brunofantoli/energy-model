# -*- coding: utf-8 -*-
"""
Created on Fri May  2 15:14:50 2025

@author: BrunoFantoli
"""
import streamlit as st

pages = [
    st.Page("app_pages/01_Data.py", title="Building Description", icon=":material/home:"),
    st.Page("app_pages/02_Results.py", title="Results", icon=":material/bar_chart:")
]

pg = st.navigation(pages, position="sidebar")

pg.run()