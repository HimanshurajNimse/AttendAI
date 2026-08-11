import streamlit as st


def subject_card(
    name,
    code,
    section,
    stats,
    footer_callback=None
):

    card_html = f"""
    <div style="
        background: #ffffff;
        border: 1px solid #9ca3af;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-family: Arial, sans-serif;
    ">

        <div style="
            font-size: 19px;
            font-weight: 700;
            color: #202124;
            margin-bottom: 16px;
        ">
            {name}
        </div>

        <div style="
            font-size: 14px;
            color: #555;
            margin-bottom: 16px;
        ">
            Code:
            <span style="
                background: #e8e9ff;
                color: #6670d8;
                padding: 4px 8px;
                border-radius: 6px;
                font-weight: 600;
            ">
                {code}
            </span>

            <span style="
                margin-left: 8px;
                color: #777;
            ">
                | Section: {section}
            </span>
        </div>

        <div style="
            display: flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
        ">
            {"".join(
                f'''
                <div style="
                    background: #f7f7fa;
                    border-radius: 8px;
                    padding: 7px 10px;
                    font-size: 13px;
                    color: #333;
                ">
                    {stat[0]} <b>{stat[2]}</b> {stat[1]}
                </div>
                '''
                for stat in stats
            )}
        </div>

    </div>
    """

    st.html(card_html)

    if footer_callback:
        footer_callback()