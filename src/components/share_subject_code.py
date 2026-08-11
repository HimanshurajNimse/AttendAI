import streamlit as st

import segno
import io




@st.dialog("Share Class Link")
def share_subject_code(subject_name, subject_code):
    app_domain="http://localhost:8501/"
    join_url=f"{app_domain}/?join={subject_code}"

    st.markdown(f"""<h2 style="text-align:center;">Scan to Join</h2>""",unsafe_allow_html=True)

    qr=segno.make(join_url, error='H', micro=False)

    out=io.BytesIO()

    qr.save(out, kind='png', scale=10,border=1)

    col1,col2=st.columns(2)

    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language='text')
        st.code(subject_code, language='text')
        st.info("Share this link or code with your students to allow them to join the class.", icon="ℹ️")

    with col2:
        st.markdown("### Scan QR Code")
        st.image(out.getvalue(), width='content', caption="Scan this QR code to join the class.")
        