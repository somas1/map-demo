import streamlit as st
from streamlit_folium import st_folium
import folium
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES
import matplotlib.pyplot as plt
import io
from PIL import Image


def create_map():
    return folium.Map(location=[20, 0], zoom_start=4)


def plot_pretty_map(lat, lon):
    try:
        aoi = get_aoi(address=f"{lat},{lon}", radius=1000, rectangular=False)
        df = get_osm_geometries(aoi=aoi)
        fig = Plot(df=df, aoi_bounds=aoi.bounds, draw_settings=STYLES["Peach"]).plot_all()
        return fig
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def main():
    st.subheader("Pretty Map Drawer")
    st.write("Click on the map to select a point.")

col1, col2 = st.columns(2)
    with col1:
        map_obj = create_map()
        st_data = st_folium(map_obj, width=350, height=350)
        if st_data['last_clicked']:
            lat, lon = st_data['last_clicked']['lat'], st_data['last_clicked']['lng']
            lat_lon_str = f"{lat:.5f} {lon:.5f}"
            st.text_input("Latitude and Longitude", value=lat_lon_str, key="lat_lon_input")
        else:
            st.text_input("Latitude and Longitude", value="", key="lat_lon_input")
        if st.button("Draw Pretty Map"):
            lat_lon_input = st.session_state.lat_lon_input.split()
            if len(lat_lon_input) == 2:
                try:
                    lat, lon = float(lat_lon_input[0]), float(lat_lon_input[1])
                    fig = plot_pretty_map(lat, lon)
                    if fig:
                        buf = io.BytesIO()
                        fig.set_size_inches(10, 10)
                        fig.savefig(buf, format="png", dpi=100)
                        buf.seek(0)
                        img = Image.open(buf)
                        with col2:
                            st.image(img, caption="Pretty Map", use_column_width=True)
                except ValueError:
                    st.error("Invalid latitude and longitude input. Please enter valid numbers.")
                except Exception as e:
                    st.error(f"Error generating map: {e}")
if __name__ == "__main__":
    main(


