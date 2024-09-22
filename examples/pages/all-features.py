# This is the file to test all the features in streanlit-analytics2
# When making code changes or refactoring, this is the current main way of
# catching breaking changes
# In time, we will use Streamlits AppTest framework 

import streamlit as st
import streamlit_analytics2 as streamlit_analytics

# Example functions for each test
def test_all_widgets():
    with streamlit_analytics.track(verbose=True):
        st.title("Test app with all widgets")
        st.checkbox("checkbox")
        st.button("button")
        st.radio("radio", ("option 1", "option 2"))
        st.selectbox("selectbox", ("option 1", "option 2", "option 3"))
        st.multiselect("multiselect", ("option 1", "option 2"))
        st.slider("slider")
        st.slider("double-ended slider", value=[0, 100])
        st.select_slider("select_slider", ("option 1", "option 2"))
        st.text_input("text_input")
        st.number_input("number_input")
        st.text_area("text_area")
        st.date_input("date_input")
        st.time_input("time_input")
        st.file_uploader("file_uploader")
        st.color_picker("color_picker")
        prompt = st.chat_input("Send a prompt to the bot")
        if prompt:
            st.write(f"User has sent the following prompt: {prompt}")

        st.sidebar.checkbox("sidebar_checkbox")
        st.sidebar.button("sidebar_button")
        st.sidebar.radio("sidebar_radio", ("option 1", "option 2"))
        st.sidebar.selectbox("sidebar_selectbox", ("option 1", "option 2", "option 3"))
        st.sidebar.multiselect("sidebar_multiselect", ("option 1", "option 2"))
        st.sidebar.slider("sidebar_slider")
        st.sidebar.slider("sidebar_double-ended slider", value=[0, 100])
        st.sidebar.select_slider("sidebar_select_slider", ("option 1", "option 2"))
        st.sidebar.text_input("sidebar_text_input")
        st.sidebar.number_input("sidebar_number_input")
        st.sidebar.text_area("sidebar_text_area")
        st.sidebar.date_input("sidebar_date_input")
        st.sidebar.time_input("sidebar_time_input")
        st.sidebar.file_uploader("sidebar_file_uploader")
        st.sidebar.color_picker("sidebar_color_picker")


def test_password_protection():
    with streamlit_analytics.track(verbose=True, unsafe_password=st.secrets["unsafe_password"]):
        st.markdown("""
        Testing password protection.... Please enter '?analytics=on' after the URL   
        There should already be a Key and Value for each widget in Firebase.
        """)



def test_firebase_storage():
    with streamlit_analytics.track(verbose=True, firestore_key_file="firebase-key.json", firestore_collection_name="streamlit-analytics2"):
        st.write("You should see this in your firebase dashboard")
        st.button("Click Me!")


def test_firebase_storage_with_st_secret():
    with streamlit_analytics.track(verbose=True, streamlit_secrets_firestore_key="firebase_key", firestore_project_name=st.secrets["project_name"], firestore_collection_name=st.secrets["collection_secret"]):
        st.write("You should see this in your firebase dashboard")
        st.button("Click Me!")

def test_analytics_track_local_json_storing():
    # requires additional testing to ensure error handling
    with streamlit_analytics.track(verbose=True, save_to_json="path/to/file.json"):
        st.write("Testing analytics tracking with local JSON storing...")
        st.button("Click Me!")


def test_analytics_track_local_json_loading():
    # requires additional testing to ensure error handling
    with streamlit_analytics.track(verbose=True, load_from_json="path/to/file.json"):
        st.write("Testing analytics tracking with local JSON loading...")
        st.button("Click Me!")


# Dropdown menu for selecting the test
option = st.selectbox(
    'Select the functionality to test:',
    ('Test All Widgets', 'Password Protection',  'Firebase Storage', 'Firebase st.secret use',
     'Analytics Track Local JSON Storing', 'Analytics Track Local JSON Loading')
)

# Execute the selected option
if option == 'Test All Widgets':
    test_all_widgets()
elif option == 'Password Protection':
    test_password_protection()
elif option == 'Firebase Storage':
    test_firebase_storage()
elif option == 'Firebase st.secret use':
    test_firebase_storage_with_st_secret()
elif option == 'Analytics Track Local JSON Storing':
    test_analytics_track_local_json_storing()
elif option == 'Analytics Track Local JSON Loading':
    test_analytics_track_local_json_loading()