import streamlit as st

def ingest_data(doclist):
    for doc in doclist:
        pass

class Session:
    def __init__(self):
        pass

    def render_sidebar(self):
        st.sidebar.markdown("# Collections")
        files = st.sidebar.file_uploader("Files (PDF only now)", accept_multiple_files=True)

        urls = st.sidebar.text_area("Web pages (new line for each url)")

        text = st.sidebar.text_area("Custom message")

        self.documents = [*files, *urls.split('\n'), text]

        if st.button("Generate"):
            pass



    def render(self):
        self.render_sidebar()


session = Session()

session.render()