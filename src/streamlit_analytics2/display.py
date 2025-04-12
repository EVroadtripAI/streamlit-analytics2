"""
Displays the analytics results within streamlit.
"""

import altair as alt
import pandas as pd
import streamlit as st

from . import utils
from .state import data, session_data  # noqa: F401


def show_results(data, reset_callback, unsafe_password=None):  # noqa: F811
    """Show analytics results in streamlit, asking for password if given."""

    # Show header.
    st.title("Analytics Dashboard")
    st.markdown(
        """
        Psst! 👀 You found a secret section generated by
        [streamlit-analytics2](https://github.com/444B/streamlit-analytics2).
        If you didn't mean to go here, remove `?analytics=on` from the URL.
        """
    )

    # Ask for password if one was given.
    show = True
    if unsafe_password is not None:
        password_input = st.text_input(
            "Enter password to show results", type="password"
        )
        if password_input != unsafe_password:
            show = False
            if len(password_input) > 0:
                st.write("Nope, that's not correct ☝️")

    if show:
        # Show traffic.
        st.header("Traffic")
        st.write(f"since {data['start_time']}")
        col1, col2, col3 = st.columns(3)
        col1.metric(
            "Pageviews",
            data["total_pageviews"],
            help="Every time a user (re-)loads the site.",
        )
        col2.metric(
            "Widget Interactions",
            data["total_script_runs"],
            help="Every time Streamlit reruns upon changes or interactions.",
        )
        col3.metric(
            "Time spent",
            utils.format_seconds(data["total_time_seconds"]),
            help=(
                "Total usage from all users from run to last widget interaction"
            ),  # noqa: E501
        )
        st.write("")

        df = pd.DataFrame(data["per_day"])
        # check if more than one year of data exists
        if pd.to_datetime(df["days"]).dt.year.nunique() > 1:
            x_axis_ticks = "yearmonthdate(days):O"
        else:
            x_axis_ticks = "monthdate(days):O"

        base = alt.Chart(df).encode(
            x=alt.X(x_axis_ticks, axis=alt.Axis(title="", grid=True))
        )
        line1 = base.mark_line(point=True, stroke="#5276A7").encode(
            alt.Y(
                "pageviews:Q",
                axis=alt.Axis(
                    titleColor="#5276A7",
                    tickColor="#5276A7",
                    labelColor="#5276A7",
                    format=".0f",
                    tickMinStep=1,
                ),
                scale=alt.Scale(domain=(0, df["pageviews"].max() + 1)),
            )
        )
        line2 = base.mark_line(point=True, stroke="#57A44C").encode(
            alt.Y(
                "script_runs:Q",
                axis=alt.Axis(
                    title="script runs",
                    titleColor="#57A44C",
                    tickColor="#57A44C",
                    labelColor="#57A44C",
                    format=".0f",
                    tickMinStep=1,
                ),
            )
        )
        layer = (
            alt.layer(line1, line2)
            .resolve_scale(y="independent")
            .configure_axis(titleFontSize=15, labelFontSize=12, titlePadding=10)
        )
        st.altair_chart(layer, use_container_width=True)

        # Show widget interactions.
        st.header("Widget interactions")
        st.markdown(
            """
            Find out how users interacted with your app!
            <br>
            Numbers indicate how often a button was clicked, how often a
            specific text input was given, ...
            <br>
            <sub>Note: Numbers only increase if the state of the widget
            changes, not every time streamlit runs the script.</sub>
            <br>
            If you would like to improve the way the below metrics are
            displayed, please open an issue/PR on
            [streamlit-analytics2](https://github.com/444B/streamlit-analytics2)
            with a clear suggestion
            """,
            unsafe_allow_html=True,
        )

        # This section controls how the tables on individual widgets are shown
        # Before, it was just a json of k/v pairs
        # There is still room for improvement and PRs are welcome
        for i in data["widgets"].keys():
            st.markdown(f"##### `{i}` Widget Usage")
            if type(data["widgets"][i]) is dict:
                st.dataframe(
                    pd.DataFrame(
                        {
                            "widget_name": i,
                            "selected_value": list(data["widgets"][i].keys()),
                            "number_of_interactions": data["widgets"][
                                i
                            ].values(),  # noqa: E501
                        }
                    ).sort_values(by="number_of_interactions", ascending=False)
                )
            else:
                st.dataframe(
                    pd.DataFrame(
                        {
                            "widget_name": i,
                            "number_of_interactions": data["widgets"][i],
                        },
                        index=[0],
                    ).sort_values(by="number_of_interactions", ascending=False)
                )

        # Show button to reset analytics.
        st.header("Danger zone")
        with st.expander("Here be dragons 🐲🔥"):
            st.write(
                """
                Here you can reset all analytics results.
                **This will erase everything tracked so far. You will not be
                able to retrieve it. This will also overwrite any results
                synced to Firestore.**
                """
            )
            reset_prompt = st.selectbox(
                "Continue?",
                [
                    "No idea what I'm doing here",
                    "I'm sure that I want to reset the results",
                ],
            )
            if reset_prompt == "I'm sure that I want to reset the results":
                reset_clicked = st.button("Click here to reset")
                if reset_clicked:
                    reset_callback()
                    st.write("Done! Please refresh the page.")
