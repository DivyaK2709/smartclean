# gps_utils.py
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import exifread
import io

def _to_degrees(value):
    # value is a tuple of Rational values
    try:
        d = float(value[0].num) / float(value[0].den)
        m = float(value[1].num) / float(value[1].den)
        s = float(value[2].num) / float(value[2].den)
        return d + m / 60.0 + s / 3600.0
    except Exception:
        # fallback
        return None

def get_exif_gps_with_pillow(image_path):
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        if not exif:
            return None
        gps_info = {}
        for tag, val in exif.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in val:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = val[t]
        if 'GPSLatitude' in gps_info and 'GPSLongitude' in gps_info:
            lat = _to_degrees(gps_info['GPSLatitude'])
            lon = _to_degrees(gps_info['GPSLongitude'])
            if gps_info.get('GPSLatitudeRef') == 'S':
                lat = -lat
            if gps_info.get('GPSLongitudeRef') == 'W':
                lon = -lon
            return (lat, lon)
    except Exception:
        return None
    return None

def get_exif_gps_with_exifread(file_bytes):
    try:
        tags = exifread.process_file(io.BytesIO(file_bytes), details=False)
        if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
            def conv(t):
                vals = [float(x.num)/float(x.den) for x in t.values]
                d = vals[0] + vals[1]/60 + vals[2]/3600
                return d
            lat = conv(tags['GPS GPSLatitude'])
            lon = conv(tags['GPS GPSLongitude'])
            if str(tags.get('GPS GPSLatitudeRef')).upper().strip() == 'S':
                lat = -lat
            if str(tags.get('GPS GPSLongitudeRef')).upper().strip() == 'W':
                lon = -lon
            return (lat, lon)
    except Exception:
        return None
    return None

def extract_gps_from_bytes_or_path(file_bytes=None, file_path=None):
    # Try exifread on bytes first, then Pillow path
    if file_bytes:
        g = get_exif_gps_with_exifread(file_bytes)
        if g:
            return g
    if file_path:
        g = get_exif_gps_with_pillow(file_path)
        if g:
            return g
    return None
