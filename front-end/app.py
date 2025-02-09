import streamlit as st
import pandas as pd



df = pd.read_csv("data/brasseries.csv")
st.title("Cafe/bistrot/brasserie research")
st.write(f"There are {df.shape[0]} cafes/bistrots/brasseries available with in this research.")



if st.button('Show mean rating'):
    st.write(df['rating'].mean())


if st.button('Show mean reviews'):
    st.write(df['reviews'].mean())

if st.button('Show mean price_level'):
    st.write(df['price_level'].mean())




