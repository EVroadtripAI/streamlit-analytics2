# streamlit-analytics2 👀
[![PyPi](https://img.shields.io/pypi/v/streamlit-analytics2)](https://pypi.org/project/streamlit-analytics2/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/streamlit-analytics2)](https://pypi.org/project/streamlit-analytics2/)
![Build Status](https://github.com/444B/streamlit-analytics2/actions/workflows/release.yml/badge.svg)

[![CodeFactor](https://www.codefactor.io/repository/github/444b/streamlit-analytics2/badge)](https://www.codefactor.io/repository/github/444b/streamlit-analytics2)
![Coverage](https://codecov.io/gh/444B/streamlit-analytics2/branch/main/graph/badge.svg)

![Known Vulnerabilities](https://snyk.io/test/github/444B/streamlit-analytics2/badge.svg)
[![streamlit-analytics2](https://snyk.io/advisor/python/streamlit-analytics2/badge.svg)](https://snyk.io/advisor/python/streamlit-analytics2)

**Enhanced tracking & visualization for your Streamlit apps.**

Streamlit Analytics2 is a maintained, powerful tool for tracking user interactions and gathering insights from your Streamlit applications. With just a few lines of code, you can start monitoring user behavior and making data-driven decisions to improve your app.

> [!Note]
> This fork is confirmed to fix the deprecation ```st.experimental_get_query_params``` alerts.    [Context](https://docs.streamlit.io/library/api-reference/utilities/st.experimental_get_query_params)  
> It also resolved 25 security issues that exist in the upstream (2 Critical, 11 High, 10 Moderate, 2 Low) 


## Getting Started

1. Install the package:
   ```
   pip install streamlit-analytics2
   ```

2. Import and initialize the tracker in your Streamlit script:
   ```python
   import streamlit as st
   import streamlit_analytics2 as streamlit_analytics

   with streamlit_analytics.track():
      st.write("Hello, World!")
      st.button("Click me")
   ```

3. Run your Streamlit app and append `?analytics=on` to the URL to view the analytics dashboard.

## Contributing

### Session-Level Analytics

We have added a new feature to track session-level analytics. The default behavior of tracking across all sessions of your app is still supported, but now we also enable tracking at the individual session level as well. To do this, simply add a string representing a unique session ID to the track() function (recommended to be a UUID4):

```python
import streamlit as st
import streamlit_analytics2 as streamlit_analytics

with streamlit_analytics.track(session_id="1234567890"):
    main()

def main():
    st.write("Hello, World!")
    st.button("Click me")
```

## Moving Forward


## Upcoming Features

We're currently working on a major breaking release that will introduce exciting new features and enhancements:

- Multi-page tracking: Monitor user interactions across multiple pages of your Streamlit app.
- Improved metrics accuracy: Get more precise and reliable usage metrics.
- Flexible data formats: Choose between CSV or JSON for storing and exporting analytics data.
- Customization screen: Easily configure and customize the analytics settings through a user-friendly interface.

Stay tuned for more updates and join our [community](https://github.com/444B/streamlit-analytics2/discussions) to be part of shaping the future of Streamlit Analytics2!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
