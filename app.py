import streamlit as st

def calculate_skin_metrics(temp, humidity):
    """Simulates the biophysical skin barrier reaction to environmental stress."""
    humidity_deficit = max(0, 60 - humidity)
    projected_tewl = 12.0 + (humidity_deficit * 0.4) + (max(0, temp - 70) * 0.1)
    projected_ph = min(7.0, 5.0 + (humidity_deficit * 0.03))
    return round(projected_tewl, 2), round(projected_ph, 2)

# --- WEB PAGE LAYOUT SETTINGS ---
st.set_page_config(page_title="AURA Diagnostic Engine", layout="centered")

st.title("🧬 AURA: Atopic Uncertainty & Risk Analyzer")
st.markdown("### *Predicting Skin Barrier Vulnerability Using Live Environmental Dynamics*")
st.write("This prototype simulates atmospheric stress impacts on biological thresholds using PubChem & RIFM toxicological parameters.")

st.divider()

# --- SIDEBAR INPUTS ---
st.sidebar.header("📥 User Input Interface")
user_zip = st.sidebar.text_input("Enter Zip Code:", value="92612")

# Let the user play with the climate to test different simulation rules
st.sidebar.subheader("🌤️ Environmental Conditions")
temp = st.sidebar.slider("Ambient Temperature (°F):", min_value=30.0, max_value=110.0, value=72.5)
humidity = st.sidebar.slider("Relative Humidity (%):", min_value=5.0, max_value=100.0, value=20.0)

# Product formulation selector
st.sidebar.subheader("🧴 Product Chemical Profile")
user_ing = st.sidebar.selectbox(
    "Select Ingredient to Test:", 
    ["Fragrance", "Phenoxyethanol", "Linalool", "Limonene", "Paraben", "Ceramide NP", "Hyaluronic Acid"]
)
user_conc = st.sidebar.number_input("Enter Concentration Percentage (%):", min_value=0.0, max_value=10.0, value=0.15, step=0.05)

# --- BACKEND PROCESSING ---
tewl, ph = calculate_skin_metrics(temp, humidity)

if tewl > 15.0:
    decay_factor = 0.5
    barrier_status = "COMPROMISED (High Dehydration Risk)"
    status_color = "inverse"
else:
    decay_factor = 1.0
    barrier_status = "HEALTHY / STABLE"

# PubChem / RIFM Registry Maximum Limits
toxicology_registry = {
    "fragrance": 0.1,          
    "phenoxyethanol": 1.0,    
    "linalool": 0.2,          
    "limonene": 0.3,          
    "paraben": 0.4,           
    "ceramide np": 5.0,       
    "hyaluronic acid": 3.0    
}

# --- MAIN DASHBOARD DISPLAY ---
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🧬 Projected TEWL Score", value=f"{tewl} g/m²/h")
with col2:
    st.metric(label="🧪 Projected Skin pH", value=ph)

if tewl > 15.0:
    st.error(f"🛡️ Skin Barrier Status: {barrier_status}")
else:
    st.success(f"🛡️ Skin Barrier Status: {barrier_status}")

st.divider()

# --- DECISION ENGINE LOGIC ---
st.subheader("🔎 In Silico Compliance Assessment")

ing_clean = user_ing.lower()
baseline_nesil = toxicology_registry[ing_clean]
adjusted_limit = baseline_nesil * decay_factor

st.write(f"**Ingredient Selected:** {user_ing}")
st.write(f"**Submitted Concentration:** {user_conc}%")
st.write(f"**Climate-Adjusted Maximum Limit:** {round(adjusted_limit, 3)}% *(Standard Baseline: {baseline_nesil}%)*")

st.divider()

# Final Determination Banners
if user_conc > adjusted_limit:
    st.error("🔴 FINAL DETERMINATION: UNSAFE / RISK OF FLARE-UP")
    if decay_factor < 1.0:
        st.warning(
            f"⚠️ **Toxicological Violation:** Your local environment has introduced atmospheric stress, "
            f"cutting your biological safety margin in half (from {baseline_nesil}% down to {round(adjusted_limit, 2)}%). "
            f"The submitted concentration of {user_conc}% is dangerous for compromised skin."
        )
    else:
        st.warning(f"⚠️ **Toxicological Violation:** This concentration exceeds standard industrial baseline limits.")
else:
    st.success("🟢 FINAL DETERMINATION: SAFE TO APPLY")
    st.write("✅ This chemical formulation is completely safe to utilize under your current localized climate conditions.")
