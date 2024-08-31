import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load and process data
@st.cache_data  # This decorator helps cache the data
def load_accident_data(file):
    df = pd.read_csv(file)
    # Assume the CSV has columns: 'latitude', 'longitude', 'street_name', 'is_drunk_driving'
    return df

# Create heatmap
def create_heatmap(df):
    # Filter for drunk driving accidents
    drunk_driving_accidents = df[df['is_drunk_driving'] == True]
    
    # Group by street and count accidents
    street_counts = drunk_driving_accidents.groupby('street_name').size().reset_index(name='count')
    street_counts = street_counts.sort_values('count', ascending=False)
    
    # Create map centered on the mean coordinates
    map_center = [df['latitude'].mean(), df['longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=12)
    
    # Add markers for top streets
    for _, row in street_counts.head(10).iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['street_name']}: {row['count']} accidents",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    return m

# Streamlit app
def main():
    st.title('Drunk Driving Accident Hotspots')
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Load data
        data = load_accident_data(uploaded_file)
        
        # Display some basic stats
        st.write(f"Total accidents: {len(data)}")
        st.write(f"Drunk driving accidents: {data['is_drunk_driving'].sum()}")
        
        # Create and display map
        st.subheader("Accident Hotspots Map")
        map = create_heatmap(data)
        folium_static(map)
        
        # Display top streets table
        st.subheader("Top 10 Streets with Most Drunk Driving Accidents")
        top_streets = data[data['is_drunk_driving'] == True]['street_name'].value_counts().head(10)
        st.table(top_streets)

if __name__ == "__main__":
    main()
