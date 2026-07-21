import streamlit as st

def base_style_layout():

    st.markdown("""
        <style>
                
                @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');

                .stApp{
                    background:#0F1117;
                    color:#F8FAFC;  }
                /* Hide top bar of streamlit */
                    #MainMenu,footer,header{
                        visibility:hidden;
                }
                .block-container{
                        padding-top:1.5rem !important;
                    }
                h1{
                    font-family: "Bebas Neue", sans-serif !important;
                    font-size:3.5rem !important;
                    line-height:1.1 !important;
                    margin-bottom:0rem !important;}
                h2{
                    font-family: "Bebas Neue", sans-serif !important;
                    font-size:2rem !important;
                    line-height:1.1 !important;
                    margin-bottom:0rem !important;}
                
                h3,h4,p{
                    font-family: "Outfit", sans-serif;
                    }
                .stButton > button{
                    width:100%;
                    border-radius:15px;
                    background:linear-gradient(90deg,#2563EB,#4F46E5);
                    color:white;
                    font-weight:600;
                    border:none;
                    padding:0.8rem;
                }

                .stButton > button:hover{
                    transform:translateY(-2px);
                }
                
                button{
                    border-radius:1.5rem !important;
                    
                    colour: white !important;
                    padding:10px 20px !important;
                    border: None !important;
                    trasition: transform 0.25s ease-in-out !important    
                }
                button:hover{
                    transform:scale(1.05)}
                
        </style>

    
        """ 
        ,unsafe_allow_html=True
    )


def background():
    st.markdown("""
    <style>

    div[data-testid="stColumn"] > div{
        background:#181E2C;
        border-radius:24px;
        padding:1rem;
        text-align:center;
        border:1px solid rgba(255,255,255,.08);
        min-height:420px;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
    }

    </style>
    """, unsafe_allow_html=True)