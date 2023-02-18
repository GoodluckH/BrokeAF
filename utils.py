from io import StringIO

import numpy as np
import pandas as pd
import streamlit as st
import tiktoken
from langchain.document_loaders import OnlinePDFLoader, WebBaseLoader
from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.metric_cards import style_metric_cards

from data import MODEL_TO_PRICING

INPUT_TYPES = ["Text", "Single Webpage", "PDF", "Tokens"]


def display_input_zone() -> pd.DataFrame:
    st.title("are you too broke for AI?")
    selected_input = st.selectbox("Select a input type", INPUT_TYPES)

    data = ""
    if selected_input == "Text":
        data = st.text_area("Paste your text here")

    elif selected_input == "Single Webpage":
        data = st.text_input("Enter URL")

    elif selected_input == "PDF":
        data = st.file_uploader("Upload PDF", ["pdf"])

    # elif selected_input == "Online PDF":
    #     data = st.text_input("Enter URL")
    #     st.write("This might take a while...")

    elif selected_input == "Tokens":
        data = st.number_input("Enter number of tokens", min_value=1)

    if not data:
        return None

    st.markdown("""---""")
    with st.spinner("figuring out how much you gonna owe..."):
        df = handle_input(data, selected_input)
    return df


def display_pricing_zone(df: pd.DataFrame):
    if df is not None:
        get_witty_coffee(df)

        for model_type in df["Model Type"].unique():
            st.markdown(f'<h2 style="text-align: center;">{model_type}</h2>',
                        unsafe_allow_html=True)

            cols = st.columns(2) if len(
                df[df["Model Type"] == model_type]) > 1 else st.columns(1)
            for i, row in df[df["Model Type"] == model_type].iterrows():
                with cols[i % 2]:
                    st.metric(
                        label=row["Model"],
                        value=f'${round(row["Price"], 4):,}'
                        if row["Price"] < 1 else f'${round(row["Price"], 2):,}',
                        delta=f'{row["Token Count"]:,} tokens',
                        delta_color="off",
                    )
                    style_metric_cards(border_left_color="None",
                                       border_radius_px=15)
    else:
        st.markdown(f'<h1 style="text-align: center;">not yet...</h1>',
                    unsafe_allow_html=True)
    st.markdown("""---""")


def handle_input(data, selected_input):

    tokens_count_by_model = {}

    if selected_input == "Text":
        tokens_count_by_model = populate_tokens_count(data)

    elif selected_input == "Single Webpage":
        text = ""
        try:
            if data:
                docs = WebBaseLoader(data).load()
                for doc in docs:
                    text += doc.page_content
                tokens_count_by_model = populate_tokens_count(text)
        except Exception as e:
            st.error(e)

    elif selected_input == "PDF":
        try:
            if data is not None:
                string_io = StringIO(data.getvalue().decode('latin-1'))
                text = string_io.read()
                tokens_count_by_model = populate_tokens_count(text)

        except Exception as e:
            st.error(e)

    elif selected_input == "Online PDF":
        text = ""
        try:
            if data:
                docs = OnlinePDFLoader(data).load()
                for doc in docs:
                    text += doc.page_content
                tokens_count_by_model = populate_tokens_count(text)
        except Exception as e:
            st.error(e)

    elif selected_input == "Tokens":
        for model_type, _ in MODEL_TO_PRICING.items():
            for model_name in MODEL_TO_PRICING[model_type]:
                tokens_count_by_model[model_name] = data

    df = pd.DataFrame(
        np.array([[
            model_type,
            model_name,
            MODEL_TO_PRICING[model_type][model_name] *
            tokens_count_by_model[model_name] / 1000,
            tokens_count_by_model[model_name],
        ]
                  for model_type in MODEL_TO_PRICING
                  for model_name in MODEL_TO_PRICING[model_type]]),
        columns=["Model Type", "Model", "Price", "Token Count"],
    )
    df["Price"] = df["Price"].astype(float)
    df["Token Count"] = df["Token Count"].astype(int)
    return df


def populate_tokens_count(text):
    tokens_count_by_model = {}
    for model_type, _ in MODEL_TO_PRICING.items():
        for model_name in MODEL_TO_PRICING[model_type]:
            enc = tiktoken.encoding_for_model(model_name)
            tokens = enc.encode(text)
            tokens_count_by_model[model_name] = len(tokens)
    return tokens_count_by_model


def set_page_config():
    st.set_page_config(
        page_title="BrokeAF",
        page_icon="🍩",
    )
    # hide hosted by Streamlit button
    hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .viewerBadge_container__1QSob {display: none;}
            .viewerBadge_link__1S137 {display: none;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # hide metric card arrow
    st.write(
        """
        <style>
        [data-testid="stMetricDelta"] svg {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def buy_for_me_button():
    button(username="xipu", floating=True, width=221)


def get_witty_coffee(df: pd.DataFrame):
    price = df[df["Model"] == "text-embedding-ada-002"]["Price"].values[0]
    if price > 10000:
        st.markdown(
            f'<p style="text-align: center;">you\'re a billionaire, right? can you buy me coffee for life?</p>',
            unsafe_allow_html=True,
        )
    elif price > 1000:
        st.markdown(
            f'<p style="text-align: center;">you better be VC funded... or you can fund my daily coffee</p>',
            unsafe_allow_html=True,
        )
    elif price > 100:
        st.markdown(
            f'<p style="text-align: center;">wow, that\'s a bit pricey!</p>',
            unsafe_allow_html=True,
        )
    elif price > 50:
        st.markdown(
            f'<p style="text-align: center;">if ur ok with this, buy me a coffee?</p>',
            unsafe_allow_html=True,
        )
    elif price > 10:
        st.markdown(
            f'<p style="text-align: center;">that\'s a lot of tokens!</p>',
            unsafe_allow_html=True,
        )


def get_color(price):
    price = float(price)
    if price < 1:
        return "#4CAF50"
    elif price < 10:
        return "#8BC34A"
    elif price < 100:
        return "#CDDC39"
    elif price < 1000:
        return "#FFEB3B"
    elif price < 10000:
        return "#FFC107"
    elif price < 100000:
        return "#FF9800"
    elif price < 1000000:
        return "#FF5722"
    else:
        return "#F44336"