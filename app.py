import streamlit as st

st.title("Nykaa review summariser")

product = st.text_input("Product name")

reviews = st.text_area(
    "Paste reviews here (start each line with 5: or 4:)",
    height=250,
)

if st.button("Sort reviews"):
    five_star = []
    four_star = []

    for line in reviews.split("\n"):
        line = line.strip()
        if line.startswith("5:"):
            five_star.append(line[2:].strip())
        elif line.startswith("4:"):
            four_star.append(line[2:].strip())

    st.subheader("5-star reviews (" + str(len(five_star)) + ")")
    for review in five_star:
        st.write("- " + review)

    st.subheader("4-star reviews (" + str(len(four_star)) + ")")
    for review in four_star:
        st.write("- " + review)
