
import streamlit as st
import pandas as pd
from analyzer import analyze_inquiries
import hashlib

st.set_page_config(
    page_title="InquiryFlow",
    page_icon="📨",
    layout="wide"
)

st.title("📨 InquiryFlow")
st.write("Organize customer inquiries using AI.")

uploaded_file = st.file_uploader(
    "Upload your customer inquiries",
    type=["csv"]
)


if uploaded_file is not None:
    file_hash = hashlib.sha256(uploaded_file.getvalue()).hexdigest()

    if st.session_state.get("file_hash") != file_hash:
        st.session_state["file_hash"] = file_hash
        st.session_state.pop("results", None)
else:
    st.session_state.pop("file_hash", None)
    st.session_state.pop("results", None)


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success(f"Loaded {len(df)} customer inquiries!")

    st.subheader("Original Inquiries")
    st.dataframe(df, use_container_width=True)

    
if st.button("Analyze Inquiries"):

    required_columns = {"id", "customer", "message"}

    if df.empty:
        st.error("The CSV file is empty.")

    elif not required_columns.issubset(df.columns):
        st.error("Missing required columns: id, customer, message.")

    elif df[["id", "customer", "message"]].isna().any().any():
        st.error("Some customer records have missing values.")

    elif df["message"].astype(str).str.strip().eq("").any():
        st.error("Some customer messages are blank.")

    elif df["customer"].astype(str).str.strip().eq("").any():
        st.error("Some customer names are blank.")

    else:
        with st.spinner("Analyzing inquiries..."):
            try:
                results_df = analyze_inquiries(df)
                st.session_state["results"] = results_df
                st.success("Analysis complete!")

            except Exception:
                st.error(
                    "Analysis failed. Please check your API "
                    "connection and try again."
                )
    
    if "results" in st.session_state:
        st.subheader("AI Analysis Results")

        results_df = st.session_state["results"]

        st.dataframe(
            results_df,
            use_container_width=True
    )

        csv_data = results_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Analyzed CSV",
            data=csv_data,
            file_name="analyzed_inquiries.csv",
            mime="text/csv"
        )

