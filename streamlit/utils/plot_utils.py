import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

def bar_compare(df: pd.DataFrame, x_col: str, y_cols: list[str], y_label="값"):
    fig, ax = plt.subplots()
    df[[x_col] + y_cols].plot(x=x_col, kind="bar", ax=ax)
    ax.set_ylabel(y_label)
    st.pyplot(fig)
    plt.close(fig)
