import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

toilets = pd.DataFrame([
    {"Name": "Toilet 1", "Lat": 8.5241, "Lon": 76.9366, "Paid": True, "Hygiene Rating": 4.5, "Wheelchair Accessible": True, "Family Friendly": False, "Showers": False},
    {"Name": "Toilet 2", "Lat": 8.5245, "Lon": 76.9370, "Paid": False, "Hygiene Rating": 3.8, "Wheelchair Accessible": False, "Family Friendly": True, "Showers": True},
    {"Name": "Toilet 3", "Lat": 8.5250, "Lon": 76.9350, "Paid": True, "Hygiene Rating": 4.0, "Wheelchair Accessible": True, "Family Friendly": True, "Showers": False},
])

st.title("Find Nearby Toilets")

st.sidebar.header("Filters")
paid_filter = st.sidebar.selectbox("Paid/Free", ["All", "Paid", "Free"])
rating_filter = st.sidebar.slider("Minimum Hygiene Rating", 0.0, 5.0, 3.0)
accessibility_filter = st.sidebar.checkbox("Wheelchair Accessible")
family_filter = st.sidebar.checkbox("Family Friendly")
showers_filter = st.sidebar.checkbox("Showers Available")

filtered_toilets = toilets.copy()
if paid_filter == "Paid":
    filtered_toilets = filtered_toilets[filtered_toilets["Paid"] == True]
elif paid_filter == "Free":
    filtered_toilets = filtered_toilets[filtered_toilets["Paid"] == False]

filtered_toilets = filtered_toilets[filtered_toilets["Hygiene Rating"] >= rating_filter]

if accessibility_filter:
    filtered_toilets = filtered_toilets[filtered_toilets["Wheelchair Accessible"] == True]
if family_filter:
    filtered_toilets = filtered_toilets[filtered_toilets["Family Friendly"] == True]
if showers_filter:
    filtered_toilets = filtered_toilets[filtered_toilets["Showers"] == True]

st.header("Toilet Locations")
map_center = [8.5241, 76.9366]
toilet_map = folium.Map(location=map_center, zoom_start=15)

for _, toilet in filtered_toilets.iterrows():
    popup_info = f"""
    <b>{toilet['Name']}</b><br>
    Hygiene Rating: {toilet['Hygiene Rating']}<br>
    Paid: {'Yes' if toilet['Paid'] else 'No'}<br>
    Wheelchair Accessible: {'Yes' if toilet['Wheelchair Accessible'] else 'No'}<br>
    Family Friendly: {'Yes' if toilet['Family Friendly'] else 'No'}<br>
    Showers: {'Yes' if toilet['Showers'] else 'No'}
    """
    folium.Marker([toilet["Lat"], toilet["Lon"]], popup=popup_info).add_to(toilet_map)

st_folium(toilet_map, width=700, height=500)

st.header("Submit a Review")
selected_toilet = st.selectbox("Select a Toilet", toilets["Name"].tolist())
user_rating = st.slider("Your Hygiene Rating", 0.0, 5.0, 3.0)
user_review = st.text_area("Your Review")

if st.button("Submit Review"):
    st.success(f"Thank you for reviewing {selected_toilet}!")
