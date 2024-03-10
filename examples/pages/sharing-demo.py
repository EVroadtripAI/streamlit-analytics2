"""This demo is run through Streamlit Sharing."""

import streamlit as st
import streamlit_analytics2 as streamlit_analytics

with streamlit_analytics.track():
    st.title(
        "👀 Demo app for streamlit-analytics2"
    )
    name = st.text_input("Write your name")
    fav = st.selectbox("Select your favorite", ["cat", "dog", "flower"])
    clicked = st.button("Click me")
    if clicked:
        st.write(
            f"Hello {name}, here's a {fav} for you: :{fav.replace('flower','sunflower')}:"
        )

    st.write(
        "...add `?analytics=on` to the URL to see the analytics dashboard 👀"
    )
