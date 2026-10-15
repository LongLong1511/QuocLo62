"""Chuyen Esri JSON (polygon, he VN-2000 kinh tuyen truc 105°45', mui 3°) sang GeoJSON WGS84.

Cach dung:
    pip install pyproj shapely
    python tools/esrijson_to_geojson.py <vao.json> <ra.geojson>
"""
import json
import sys

from pyproj import Transformer
from shapely.geometry import Polygon, mapping
from shapely.ops import transform, unary_union

VN2000 = (
    "+proj=tmerc +lat_0=0 +lon_0=105.75 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 "
    "+towgs84=-191.90441429,-39.30318279,-111.45032835,-0.00928836,0.01975479,-0.00427372,0.252906278 "
    "+units=m +no_defs"
)


def signed_area(ring):
    return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(ring, ring[1:])) / 2


def main(src, dst):
    data = json.load(open(src, encoding="utf-8-sig"))
    to_wgs84 = Transformer.from_crs(VN2000, "EPSG:4326", always_xy=True)
    features = []
    for f in data["features"]:
        rings = f["geometry"]["rings"]
        # Esri: vong ngoai theo chieu kim dong ho (dien tich am), lo thung nguoc lai
        outers = [r for r in rings if signed_area(r) < 0]
        holes = [r for r in rings if signed_area(r) >= 0]
        polys = []
        for o in outers:
            po = Polygon(o)
            polys.append(Polygon(o, [h for h in holes if po.contains(Polygon(h).representative_point())]))
        geom = unary_union(polys) if len(polys) > 1 else polys[0]
        geom = transform(lambda x, y, z=None: to_wgs84.transform(x, y), geom)
        props = {k: (v.strip() if isinstance(v, str) else v) for k, v in f["attributes"].items()}
        features.append({"type": "Feature", "properties": props, "geometry": mapping(geom)})
    json.dump({"type": "FeatureCollection", "features": features}, open(dst, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"Da ghi {len(features)} doi tuong vao {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
