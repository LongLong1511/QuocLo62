# Bản đồ ảnh hưởng mở rộng Quốc lộ 62, xã Thạnh Hóa, tỉnh Tây Ninh

Đơn vị thực hiện: **Công ty TNHH Đo đạc nhà đất Hưng Phú**

Trang web tĩnh (HTML + JavaScript, không cần server riêng) thể hiện phạm vi mở rộng QL62 và mức ảnh hưởng tới từng thửa đất lân cận trên nền ảnh vệ tinh.

## Tính năng

- Các lớp: tim đường QL62, phạm vi (chỉ giới) mở rộng, thửa đất trước khi cắt, phần thửa thuộc quy hoạch.
- Diện tích thu hồi lấy theo cột `DTThuocQH` của file thửa đã cắt; nếu không có file này thì tự tính bằng phép giao thửa với phạm vi mở rộng (Turf.js).
- Viền thửa theo mức ảnh hưởng: thu hồi toàn bộ (đỏ), một phần (cam), không ảnh hưởng (xanh).
- Nền thửa tô theo loại đất, bảng màu lấy từ `Thua_CanGio.lyr` (BHK dùng màu HNK, COC màu trắng nhạt).
- Popup hiện toàn bộ thông tin có trong file và phần thuộc quy hoạch của thửa.
- Bảng tổng hợp, danh sách thửa có tìm kiếm, xuất CSV (mở bằng Excel), link chia sẻ tới từng thửa.
- Nền bản đồ: Vệ tinh, Vệ tinh + nhãn, OSM. Dùng được trên điện thoại.

## Cấu trúc

```
QL62/
├── index.html                         Trang bản đồ (toàn bộ giao diện và code)
├── data/
│   ├── QL62_phamvi_morong.geojson     Phạm vi mở rộng (từ RanhQL.json)
│   ├── Thuadat.geojson                Thửa trước khi cắt (từ Manh1.json)
│   ├── Thuadat_ThuocQL62.geojson      Thửa đã cắt theo quy hoạch (từ Manh1_ThuocQL62.json)
│   └── QL62_timduong.geojson          Tim đường (chưa có)
├── tools/
│   └── esrijson_to_geojson.py         Chuyển Esri JSON hệ VN-2000 sang GeoJSON WGS84
├── .nojekyll                          Cho GitHub Pages phục vụ file nguyên trạng
├── .gitignore
└── README.md
```

Các file gốc (`RanhQL.json`, `Manh1*.json`, `*.lyr`) và thư mục `_du_lieu_cu_Long_Huong/` được `.gitignore` bỏ qua, không đưa lên GitHub.

## Chạy trên máy

- **XAMPP**: thư mục dự án ở `C:\xampp\htdocs\QL62`. Bật Apache rồi mở `http://localhost/QL62/`.
- **Python**: trong thư mục này chạy `python -m http.server 8000`, mở `http://localhost:8000`.
- **Mở thẳng `index.html`**: trình duyệt chặn đọc file, dùng mục **Nạp dữ liệu** ở cuối thanh bên để chọn file.

## Đưa lên GitHub và GitHub Pages

> ⚠️ **Lưu ý dữ liệu cá nhân:** file thửa đất có tên chủ sử dụng và địa chỉ. Repository **public** và GitHub Pages ai cũng xem được. Nên tạo repo **Private**; GitHub Pages cho repo private cần gói GitHub trả phí (Pro/Team). Nếu buộc phải public, hãy bỏ trường `TENCHU`, `DIACHI` khỏi file trong `data/` trước khi đẩy lên.

1. Tạo repository mới trên GitHub, ví dụ `QL62` (không tạo sẵn README).
2. Mở Git Bash / Terminal tại `C:\xampp\htdocs\QL62` và chạy:

   ```bash
   git init
   git add .
   git commit -m "Ban do anh huong mo rong QL62 - xa Thanh Hoa"
   git branch -M main
   git remote add origin https://github.com/<ten-tai-khoan>/QL62.git
   git push -u origin main
   ```

3. Trên GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, chọn `main` và thư mục `/ (root)`, bấm **Save**.
4. Sau 1–2 phút trang có tại `https://<ten-tai-khoan>.github.io/QL62/`.

Cập nhật về sau:

```bash
git add .
git commit -m "Cap nhat du lieu"
git push
```

## Chuẩn bị dữ liệu mới

Trang chỉ đọc **GeoJSON hệ WGS84 (EPSG:4326)**. File xuất từ ArcGIS dạng Esri JSON hệ VN-2000 (kinh tuyến trục 105°45', múi 3°) chuyển bằng:

```bash
pip install pyproj shapely
python tools/esrijson_to_geojson.py Manh1.json data/Thuadat.geojson
```

| File trong `data/` | Hình học | Nội dung |
|--------------------|----------|----------|
| `QL62_timduong.geojson` | LineString | Tim đường QL62 hiện hữu |
| `QL62_phamvi_morong.geojson` | Polygon | Phạm vi / chỉ giới sau mở rộng |
| `Thuadat.geojson` | Polygon | Thửa đất trước khi cắt (cần trường `FID`) |
| `Thuadat_ThuocQL62.geojson` | Polygon | Thửa đã cắt: `FID_Manh1` trỏ về `FID` thửa gốc, `QH` khác rỗng là phần thuộc quy hoạch, `DTThuocQH` là diện tích |

Tên trường thửa đất được nhận: số tờ `SHBANDO`/`So_To`, số thửa `SHTHUA`/`Sothua`, chủ `TENCHU`/`Chusudung`, loại đất `KH2003`/`Loaidat`, địa chỉ `DIACHI`/`Diachi`. Đổi tên file, tên trường, bảng màu loại đất trong phần `CẤU HÌNH` đầu thẻ `<script>` của `index.html`.
