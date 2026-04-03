import streamlit as st
import pickle
import pandas as pd
import random

# ---------------- TITLE ----------------
st.title("🔐 WSN Intrusion Detection System")
st.write("AI-based system to detect network intrusions using Machine Learning.")

# ---------------- LOAD FILES ----------------
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

# ---------------- FEATURE DESCRIPTIONS ----------------
feature_info = {
    "protocol type tcp": "Transmission Control Protocol (Reliable, connection-based)",
    "protocol type udp": "User Datagram Protocol (Fast, connectionless)",
    "service http": "Web traffic (HTTP protocol)",
    "service ftp": "File Transfer Protocol",
    "flag sf": "Connection successful",
}

# ---------------- HELPER FUNCTIONS ----------------
def clean_name(name):
    return name.replace("_", " ").title()

def get_description(name):
    return feature_info.get(name.lower(), "No description available")

def generate_data():
    return [random.uniform(0, 100) for _ in range(len(columns))]

# ---------------- BUTTON ----------------
if st.button("🚀 Generate Network Data"):

    # Generate data
    data = generate_data()

    df = pd.DataFrame([data], columns=columns)

    # Prediction
    prediction = model.predict(df)

    # ---------------- DISPLAY TABLE ----------------
    st.subheader("📡 Network Features")

    display_df = pd.DataFrame({
        "Feature": [clean_name(col) for col in columns[:15]],
        "Value": data[:15]
    })

    st.dataframe(display_df)

    # ---------------- GRAPH ----------------
    st.subheader("📊 Feature Visualization")
    st.bar_chart(display_df.set_index("Feature"))

    # ---------------- FEATURE DETAILS ----------------
    st.subheader("📖 Feature Explanation")

    for i in range(10):
        name = clean_name(columns[i])
        desc = get_description(name)

        st.markdown(f"🔹 **{name}**: {round(data[i],2)}")
        st.caption(desc)

    # ---------------- RESULT ----------------
    st.subheader("🔍 Prediction Result")

    if prediction[0] == "normal":
        st.success("✅ Normal Network Traffic")
    else:
        st.error("🚨 Intrusion Detected!")

    # ---------------- INFO ----------------
    st.info("The model analyzes multiple network parameters and classifies the traffic behavior.")