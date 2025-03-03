import streamlit as st

import streamlit_analytics2 as streamlit_analytics

tab1, tab2 = st.tabs(["Classic", "Advanced"])


# classic firestore load
with tab1:
    st.header("Classic")

    if st.button("Test Classic"):

        with streamlit_analytics.track(
            firestore_key_file="pages/firebase-key.json",
            firestore_collection_name="streamlit_analytics2",
            firestore_document_name="data",
            firestore_project_name="streamlit-analtyics2",
            verbose=True,
        ):

            st.text_input("Write something")
            st.button("Click me")


# Advanced storing of key in secrets.toml
with tab2:
    st.header("Advanced")
    # if st.button("Test Advanced"):

    #     with streamlit_analytics.track(
    #         firestore_collection_name="streamlit-analytics-secrets-approach",
    #         streamlit_secrets_firestore_key="firebase",
    #         firestore_project_name="firestore_project_name",
    #         session_id="test_session_id",
    #         verbose=True):

    #         st.text_input("Write something", key="text_input2")
    #         st.button("Click me", key="button2")

    #         st.write("# Aggregate Stats")
    #         st.write(streamlit_analytics.data)
    #         st.write("# Session Stats")
    #         st.write(streamlit_analytics.session_data)
