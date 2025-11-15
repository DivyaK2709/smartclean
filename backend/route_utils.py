# route_utils.py
import requests
from geopy.distance import geodesic
import time

OSRM_TABLE = "http://router.project-osrm.org/table/v1/driving/"
OSRM_ROUTE = "http://router.project-osrm.org/route/v1/driving/"

def build_coord_str(lon_lat_list):
    # lon_lat_list: [(lon,lat), ...]
    return ";".join([f"{lon},{lat}" for lon,lat in lon_lat_list])

def compute_osrm_table(coords_lonlat):
    # coords_lonlat: list of (lon,lat)
    coords_str = build_coord_str(coords_lonlat)
    url = OSRM_TABLE + coords_str + "?annotations=distance"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data.get("distances")
    except Exception as e:
        print("OSRM table error:", e)
        return None

def compute_osrm_route_geojson(coords_lonlat):
    if not coords_lonlat or len(coords_lonlat) < 2:
        return None
    coords_str = build_coord_str(coords_lonlat)
    url = OSRM_ROUTE + coords_str + "?overview=full&geometries=geojson"
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        routes = data.get("routes")
        if routes and len(routes) > 0:
            return routes[0].get("geometry")
    except Exception as e:
        print("OSRM route error:", e)
    return None

def greedy_nn_on_matrix(matrix, start_index=0, max_stop=None):
    n = len(matrix)
    visited = [False]*n
    visited[start_index] = True
    cur = start_index
    route = []
    for _ in range(n-1 if max_stop is None else min(max_stop, n-1)):
        nearest = None
        nd = float("inf")
        for j in range(0,n):
            if not visited[j] and matrix[cur][j] is not None:
                if matrix[cur][j] < nd:
                    nd = matrix[cur][j]
                    nearest = j
        if nearest is None:
            break
        visited[nearest] = True
        route.append(nearest)
        cur = nearest
    return route

def greedy_nn_straightline(points_latlon, start_point=None, max_stop=None):
    # points_latlon: [{'id':..., 'latitude':..., 'longitude':...}, ...]
    pts = [(p['_id'], p['latitude'], p['longitude']) for p in points_latlon]
    if not pts:
        return []
    if start_point is None:
        cur = (pts[0][1], pts[0][2])
        remaining = pts[1:]
        route = [pts[0][0]]
    else:
        cur = start_point
        remaining = pts
        route = []
    while remaining:
        nearest=None
        nd = float("inf")
        idx = -1
        for i,(pid,lat,lon) in enumerate(remaining):
            d = geodesic(cur, (lat,lon)).meters
            if d < nd:
                nd = d; nearest = (pid,lat,lon); idx = i
        route.append(nearest[0])
        cur = (nearest[1], nearest[2])
        remaining.pop(idx)
        if max_stop and len(route) >= max_stop:
            break
    return route
