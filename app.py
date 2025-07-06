import streamlit as st
import pandas as pd
import altair as alt
from backend.utils.image_utils import get_base64_image
from backend.utils.ars_utils import calculate_ars, color_score


# --- PAGE CONFIG ---
st.set_page_config(page_title="Acquisition Readiness Dashboard", layout="wide")
# Add after st.set_page_config()
with open("static/styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- LOGO ---
encoded_logo = get_base64_image("static/logo_horizontal.png")
st.markdown(f"""
    <div style="padding: 1rem 2rem; background-color: #1e293b; border-radius: 12px; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{encoded_logo}" width="160" style="margin-right: 20px;" />
            <div>
                <h1 style="color: #10b981; font-size: 2.5rem; margin-bottom: 0.2rem;">🔍 Acquisition Readiness Dashboard</h1>
                <p style="font-size: 1.1rem; color: #cbd5e1;">
                    Score and prioritize acquisition targets using company metadata, credibility signals, and smart filters.
                </p>
            </div>
        </div>
       
    </div>
""", unsafe_allow_html=True)

# --- DATA ---
df = pd.read_csv("data/standardized_company_data_from_linkedin.csv")
valid_states = set([
    'AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN',
    'IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV',
    'NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN',
    'TX','UT','VT','VA','WA','WV','WI','WY'
])

df['State'] = df['State'].apply(lambda x: x if x in valid_states else None)


# --- SIDEBAR WEIGHTS ---
st.sidebar.markdown("### 🧮 Customize ARS Weights")
weight_age = st.sidebar.slider("Company Age", 0, 100, 20, step=5)
weight_website = st.sidebar.slider("Website Present", 0, 100, 10, step=5)
weight_linkedin = st.sidebar.slider("LinkedIn Present", 0, 100, 10, step=5)
weight_owner_contact = st.sidebar.slider("Owner Info Present", 0, 100, 10, step=5)
weight_address = st.sidebar.slider("City & State Present", 0, 100, 10, step=5)
weight_bbb = st.sidebar.slider("BBB Rating", 0, 100, 15, step=5)
weight_industry = st.sidebar.slider("Attractive Industry", 0, 100, 15, step=5)
weight_team_size = st.sidebar.slider("Employees Count / Revenue Proxy", 0, 100, 10, step=5)

weights = {"age": weight_age, "website": weight_website, "linkedin": weight_linkedin,
           "owner": weight_owner_contact, "address": weight_address, "bbb": weight_bbb,
           "industry": weight_industry, "team": weight_team_size}

weight_sum = sum(weights.values())
weights = {k: v/weight_sum for k,v in weights.items()}

# --- SCORING ---
df['ARS'] = df.apply(lambda row: calculate_ars(row, weights), axis=1)
df['ARS Level'] = df['ARS'].apply(color_score)

# --- FILTERS ---
st.sidebar.markdown("### 🎚️ ARS Range")
ars_min, ars_max = st.sidebar.slider("Select ARS Range", 0, 100, (50, 100), step=1)

selected_state = st.sidebar.multiselect("Choose States:", sorted(df['State'].dropna().unique()))

filtered_df = df[(df['ARS'] >= ars_min) & (df['ARS'] <= ars_max)]
if selected_state:
    filtered_df = filtered_df[filtered_df['State'].isin(selected_state)]

# --- TABLE ---
st.subheader("📊 Company Table")
st.dataframe(filtered_df[['Company Name', 'Industry', 'City', 'State', 'Employees Count', 'ARS', 'ARS Level']], use_container_width=True)

st.download_button("📥 Download CSV", data=filtered_df.to_csv(index=False), file_name="filtered_companies.csv")

# --- INSIGHTS ---
st.markdown("### 📈 ARS Insights")
for label, color in zip(['🟢 High', '🟡 Medium', '🔴 Low'], ['#34d399', '#facc15', '#f87171']):
    count = filtered_df[filtered_df['ARS Level'] == label].shape[0]
    st.markdown(f"""
        <div style='text-align:center; margin-bottom: 10px;'>
            <p style='color:{color}; font-size: 1.1rem; font-weight:600;'>{label} ARS Companies</p>
            <p style='font-size: 2.5rem; color: white; font-weight: bold;'>{count}</p>
        </div>
    """, unsafe_allow_html=True)

# --- CHART ---
binned_df = pd.cut(filtered_df['ARS'], bins=[0, 30, 60, 100], labels=['🔴 Low (0-30)', '🟡 Medium (31-60)', '🟢 High (61-100)'])
chart_data = pd.DataFrame(binned_df.value_counts().sort_index()).reset_index()
chart_data.columns = ['ARS Category', 'Company Count']

chart = alt.Chart(chart_data).mark_bar(color="#38bdf8").encode(
    x=alt.X('ARS Category', title='ARS Score Range', axis=alt.Axis(labelColor='#e2e8f0', titleColor='#e2e8f0')),
    y=alt.Y('Company Count', title='Number of Companies', axis=alt.Axis(labelColor='#e2e8f0', titleColor='#e2e8f0')),
    tooltip=['ARS Category', 'Company Count']
).properties(width=600, height=300, background="#0f172a")

st.altair_chart(chart, use_container_width=True)
