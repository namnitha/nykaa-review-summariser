import time

import streamlit as st
from google import genai
from google.genai import types

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
    http_options=types.HttpOptions(timeout=60000),
)
MODEL = "gemini-3.5-flash-lite"


def summarise(reviews, stars):
    if len(reviews) == 0:
        return "No " + str(stars) + "-star reviews were pasted."

    prompt = (
        "Here are " + str(stars) + "-star customer reviews of a beauty product. "
        "Summarise them in one short paragraph. Mention what customers say most often. "
        "Use only what is in the reviews.\n\n" + "\n".join(reviews)
    )

    for attempt in range(3):
        try:
            response = client.models.generate_content(model=MODEL, contents=prompt)
            return response.text
        except Exception as error:
            if attempt == 2:
                return "Something went wrong: " + str(error)
            time.sleep(5)


st.title("Nykaa review summariser")

product = st.text_input("Product name")

reviews = st.text_area(
    "Paste reviews here (start each line with 5: or 4:)",
    height=250,
)

if st.button("Summarise reviews"):
    five_star = []
    four_star = []

    for line in reviews.split("\n"):
        line = line.strip()
        if line.startswith("5:"):
            five_star.append(line[2:].strip())
        elif line.startswith("4:"):
            four_star.append(line[2:].strip())

    with st.spinner("Reading the reviews..."):
        five_summary = summarise(five_star, 5)
        four_summary = summarise(four_star, 4)

    st.subheader("5-star summary")
    st.write(five_summary)

    st.subheader("4-star summary")
    st.write(four_summary)
