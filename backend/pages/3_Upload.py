# pages/3_Upload.py
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import piexif

API = "http://localhost:8000"

st.set_page_config(page_title="Upload Photo", layout="wide")

# --------- AUTH CHECK ----------
if "token" not in st.session_state:
    st.error("Please login first.")
    st.stop()

st.title("📸 Upload Geo-Tagged Photo")

uploaded = st.file_uploader("Upload an image with GPS EXIF:", type=["jpg", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Preview", use_container_width=True)

    # ---- EXTRACT GPS ----
    try:
        exif_dict = piexif.load(uploaded.getvalue())
        gps = exif_dict.get("GPS")

        if not gps or len(gps.keys()) == 0:
            st.error("❌ No GPS EXIF found in this image. Please upload a geo-tagged photo.")
            st.stop()

        def dms_to_deg(v):
            return float(v[0][0] / v[0][1]) + float(v[1][0] / v[1][1]) / 60 + float(v[2][0] / v[2][1]) / 3600

        lat = dms_to_deg(gps[2])
        if gps[1] == b"S":
            lat = -lat

        lon = dms_to_deg(gps[4])
        if gps[3] == b"W":
            lon = -lon

        st.success(f"📍 Extracted Location: {lat}, {lon}")

    except Exception as e:
        st.error("❌ Unable to read GPS EXIF data. Use a geo-tagged image.")
        st.stop()

    # ---- CONFIRM UPLOAD ----
    if st.button("✅ Confirm Upload"):
        try:
            files = {"file": uploaded.getvalue()}
            data = {
                "user_id": st.session_state["user_id"],
                "latitude": lat,
                "longitude": lon,
                "token": st.session_state["token"]
            }

            r = requests.post(f"{API}/upload/", data=data, files=files)
            if r.status_code == 200:
                st.success("🎉 Upload successful! Redirecting to Map...")

                # NEW Streamlit rerun
                st.session_state["last_upload"] = True
                st.rerun()

            else:
                st.error("Upload failed: " + r.text)

        except Exception as e:
            st.error(f"Error uploading image: {e}")
