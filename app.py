import time

import streamlit as st
from google import genai
from google.genai import types

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
    http_options=types.HttpOptions(timeout=60000),
)
MODEL = "gemini-3.5-flash-lite"

PROMPTS = {
    "Prompt A: simple": (
        "Here are {stars}-star customer reviews of a beauty product. "
        "Summarise them in one short paragraph. Mention what customers say most often. "
        "Use only what is in the reviews.\n\n{reviews}"
    ),
    "Prompt B: structured": (
        "Here are {stars}-star customer reviews of a beauty product. "
        "Write one paragraph of exactly 3 sentences. "
        "Sentence 1: what customers love most. "
        "Sentence 2: the details they mention most often, such as shade, texture or wear time. "
        "Sentence 3: any small complaints or doubts. "
        "Use only what is in the reviews.\n\n{reviews}"
    ),
    "Prompt C: shopper-focused": (
        "You are helping a shopper in India decide whether to buy a beauty product. "
        "Below are {stars}-star customer reviews. "
        "Write one short paragraph in plain, friendly language that tells the shopper "
        "what real buyers experienced. Do not exaggerate or invent anything. "
        "If reviewers disagree, say so.\n\n{reviews}"
    ),
}


def ask_ai(prompt):
    for attempt in range(3):
        try:
            response = client.models.generate_content(model=MODEL, contents=prompt)
            return response.text
        except Exception as error:
            if attempt == 2:
                return "Something went wrong: " + str(error)
            time.sleep(5)


def summarise(reviews, stars, prompt_name):
    if len(reviews) == 0:
        return "No " + str(stars) + "-star reviews were pasted."

    template = PROMPTS[prompt_name]
    prompt = template.format(stars=stars, reviews="\n".join(reviews))
    return ask_ai(prompt)


def pros_and_cons(all_reviews):
    prompt = (
        "Here are customer reviews of a beauty product. "
        "Write exactly 3 bullet points for the top pros. "
        "Then write a line containing only --- . "
        "Then write exactly 3 bullet points for the top cons. "
        "Use only what is in the reviews. Write nothing else.\n\n"
        + "\n".join(all_reviews)
    )
    return ask_ai(prompt)


st.title("Nykaa review summariser")

product = st.text_input("Product name")

prompt_name = st.selectbox("Which prompt should the AI use?", list(PROMPTS.keys()))

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
        five_summary = summarise(five_star, 5, prompt_name)
        four_summary = summarise(four_star, 4, prompt_name)
        pc_text = pros_and_cons(five_star + four_star)

    st.caption("Prompt used: " + prompt_name)

    st.subheader("5-star summary")
    st.write(five_summary)

    st.subheader("4-star summary")
    st.write(four_summary)

    st.subheader("Highlights")
    parts = pc_text.split("---")
    if len(parts) == 2:
        pros_col, cons_col = st.columns(2)
        with pros_col:
            st.success("**Top 3 pros**\n\n" + parts[0].strip())
        with cons_col:
            st.error("**Top 3 cons**\n\n" + parts[1].strip())
    else:
        st.write(pc_text)
