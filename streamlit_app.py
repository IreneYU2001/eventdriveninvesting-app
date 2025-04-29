# Import Streamlit
import streamlit as st

# **** Page layout setup ****
App_page_0 = st.Page(
    "page0.py",
    title="Know This App",
    default=True
)
App_page_1 = st.Page(
    "page1.py",
    title="Check Your Stock"
)
App_page_2 = st.Page(
    "page2.py",
    title="See Our Process"
)
# **** Set up navigation with section headers ****
pg = st.navigation(
    [
        App_page_0,
        App_page_1,
        App_page_2
    ]
)

# **** Execute the navigation code ****
if __name__ == "__main__":
    pg.run()
