import streamlit as st

# **** Page layout setup ****
App_page_0 = st.Page(
    "page0.py",
    title="Know This App",
)
App_page_1 = st.Page(
    "page1.py",
    title="Everything You Want to Know"
)
App_page_2 = st.Page(
    "page2.py",
    title="How to Get Information"
)
App_page_4 = st.Page(
    "page4.py",
    title="Core Model Overview"
)
App_page_5 = st.Page(
    "page-1.py",
    title="See Our Reference"
)

# **** Set up navigation with invisible section headers ****
pg = st.navigation(
    {
        "  ": [App_page_0],   # 上面第一个空白标题
        "Check Your Stock": [App_page_1, App_page_2, App_page_4],
        "       ": [App_page_5],  # 下面第二个空白标题（两个零宽空格，避免冲突）
    }
)

# **** Execute the navigation code ****
if __name__ == "__main__":
    pg.run()