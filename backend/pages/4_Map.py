# pages/4_Map.py
import streamlit as st
from database import query_points
from route_utils import compute_osrm_table, compute_osrm_route_geojson, greedy_nn_straightline
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Map - SmartClean")
st.title("Map & Optimized Route")

if not st.session_state.get("logged_in"):
    st.warning("You must login first. Go to Login page.")
    st.stop()

pts = query_points(limit=1000)
if not pts:
    st.info("No reports yet — go to Upload.")
    st.stop()

# create folium map centered at average
avg_lat = sum([p["latitude"] for p in pts]) / len(pts)
avg_lon = sum([p["longitude"] for p in pts]) / len(pts)
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=13)

# add markers
for p in pts:
    popup_html = ""
    # display image if exists on disk
    path = p.get("image_path") or p.get("image_url")
    if path:
        # If using saved local path under uploads/
        try:
            fname = path.split("/")[-1]
            fpath = os.path.join("uploads", fname)
            if os.path.exists(fpath):
                popup_html += f'<img src="file://{os.path.abspath(fpath)}" width="200"><br>'
        except Exception:
            pass
    popup_html += f"<b>Reported:</b> {p.get('created_at', '')}"
    folium.Marker([p["latitude"], p["longitude"]], popup=popup_html).add_to(m)

st.write("Total reports:", len(pts))

# compute OSRM route (municipal center can be changed)
municipal_center_latlon = (12.9716, 77.5946)  # lat, lon for map display
# build OSRM coords list (lon,lat)
coords = [(77.5946, 12.9716)] + [(p["longitude"], p["latitude"]) for p in pts]
dist_matrix = compute_osrm_table(coords)
if dist_matrix:
    order_idx = []
    # greedy starting at index 0
    visited = [False]*len(dist_matrix)
    visited[0] = True
    cur = 0
    for _ in range(len(dist_matrix)-1):
        nearest = None
        nd = float("inf")
        for j in range(1, len(dist_matrix)):
            if not visited[j] and dist_matrix[cur][j] is not None:
                if dist_matrix[cur][j] < nd:
                    nd = dist_matrix[cur][j]; nearest = j
        if nearest is None:
            break
        visited[nearest] = True
        order_idx.append(nearest)
        cur = nearest
    # ordered coordinates for route geometry
    ordered_coords = [(coords[i][0], coords[i][1]) for i in order_idx]  # lon,lat
    full_seq = [coords[0]] + ordered_coords
    geom = compute_osrm_route_geojson(full_seq)
    if geom and geom.get("coordinates"):
        # convert to latlon pairs
        latlon = [[c[1], c[0]] for c in geom["coordinates"]]
        folium.PolyLine(latlon, color="blue", weight=4).add_to(m)
    else:
        # fallback: draw simple polyline through points
        latlngs = [[p["latitude"], p["longitude"]] for p in pts]
        folium.PolyLine(latlngs, color="blue", weight=3, opacity=0.6).add_to(m)
else:
    # fallback greedy straight-line
    route_ids = greedy_nn_straightline(pts, start_point=(municipal_center_latlon[0], municipal_center_latlon[1]))
    ordered_pts = [next((p for p in pts if p["_id"]==rid), None) for rid in route_ids]
    latlngs = [[p["latitude"], p["longitude"]] for p in ordered_pts if p]
    if latlngs:
        folium.PolyLine(latlngs, color="blue", weight=3, opacity=0.6).add_to(m)

# show map
st_folium(m, width=900, height=700)
