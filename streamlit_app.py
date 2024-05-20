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

