import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('DOCUMENT/images_report', exist_ok=True)

# Set common font and style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# 1. Architecture Diagram
def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=200)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Title
    ax.text(6, 6.6, "KIẾN TRÚC TỔNG THỂ HỆ THỐNG THE4BOOKSTORE (SPRING BOOT MVC N-TIER)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#004C22')

    # Layers
    layers = [
        ("1. Presentation Layer (Giao diện người dùng)", 5.2, "#E0F2FE", "#0369A1", 
         "Client Browser (Chrome, Edge)\nThymeleaf Templates + Tailwind CSS + Responsive UI\nAI Stitch Generated Components (Design System Forest Folio)"),
        ("2. Security & Controller Layer (Xác thực & Điều hướng)", 3.8, "#DCFCE7", "#15803D", 
         "Spring Security (RBAC: ADMIN, MANAGER, VENDOR, KHACHHANG)\nControllers: AuthController, HomeController, ProductController, CartController,\nVendorController, AdminController, ManagerDisputeController"),
        ("3. Business Logic & Service Layer (Nghiệp vụ cốt lõi)", 2.4, "#FEF3C7", "#B45309", 
         "Services: ProductService, OrderService, VoucherService, ShopChainService, UserService\nBusiness Rules: Khoảng cách 34 tỉnh thành, Voucher đa cấp, Trừ tồn kho an toàn"),
        ("4. Data Access & Persistence Layer (Truy xuất CSDL)", 1.0, "#F3E8FF", "#7E22CE", 
         "Spring Data JPA / Hibernate Repositories\nMicrosoft SQL Server 2022 / MySQL 8.0\nStored Procedures (Đặt hàng, Trừ kho, Thống kê doanh thu), Triggers, Indexes")
    ]

    for title, y, bg_col, border_col, desc in layers:
        rect = patches.FancyBboxPatch((0.8, y - 0.45), 10.4, 0.9, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor=bg_col, edgecolor=border_col, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(1.1, y + 0.22, title, fontsize=10, fontweight='bold', color=border_col)
        ax.text(1.1, y - 0.12, desc, fontsize=8.5, color='#1E293B', va='center')

    # Connectors
    for y in [4.55, 3.15, 1.75]:
        ax.annotate('', xy=(6, y - 0.2), xytext=(6, y + 0.2),
                    arrowprops=dict(arrowstyle="<|-|>", color="#475569", lw=2))

    plt.tight_layout()
    plt.savefig('DOCUMENT/images_report/diagram_architecture.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("Architecture diagram created.")

# 2. ERD Summary Diagram
def create_erd_diagram():
    fig, ax = plt.subplots(figsize=(13, 8), dpi=200)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    ax.text(6.5, 7.6, "SƠ ĐỒ THỰC THỂ CƠ SỞ DỮ LIỆU CỐT LÕI (CORE ERD MODEL)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#004C22')

    tables = [
        ("NguoiDung (User)", 1.5, 5.8, ["id (PK)", "username", "password", "email", "so_dien_thoai", "vai_tro_id (FK)"], "#DBEAFE", "#1D4ED8"),
        ("VaiTro (Role)", 1.5, 2.5, ["id (PK)", "ten_vai_tro", "mo_ta"], "#E0E7FF", "#4338CA"),
        ("GianHang (Shop)", 4.8, 5.8, ["id (PK)", "ten_gian_hang", "chu_shop_id (FK)", "tinh_thanh", "dia_chi", "trang_thai"], "#DCFCE7", "#15803D"),
        ("SanPham (Book)", 4.8, 2.5, ["id (PK)", "ten_san_pham", "shop_id (FK)", "danh_muc_id (FK)", "gia_ban", "so_luong_ton"], "#FEF3C7", "#B45309"),
        ("DanhMuc (Category)", 8.2, 2.5, ["id (PK)", "ten_danh_muc", "slug", "parent_id (FK)"], "#FCE7F3", "#BE185D"),
        ("DonHang (Order)", 8.2, 5.8, ["id (PK)", "khach_hang_id (FK)", "shop_id (FK)", "voucher_id (FK)", "tong_tien", "trang_thai"], "#FFEDD5", "#C2410C"),
        ("ChiTietDonHang (Item)", 11.2, 5.8, ["id (PK)", "don_hang_id (FK)", "san_pham_id (FK)", "so_luong", "don_gia"], "#FEE2E2", "#B91C1C"),
        ("Voucher (KhuyenMai)", 11.2, 2.5, ["id (PK)", "ma_code", "giam_gia", "don_toi_thieu", "shop_id (FK)", "ngay_het_han"], "#F3E8FF", "#7E22CE"),
    ]

    for name, x, y, fields, bg, border in tables:
        rect = patches.FancyBboxPatch((x - 1.3, y - 1.1), 2.6, 2.0, boxstyle="round,pad=0.1,rounding_size=0.1",
                                      facecolor=bg, edgecolor=border, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y + 0.65, name, ha='center', va='center', fontsize=9.5, fontweight='bold', color=border)
        ax.axhline(0, color=border) # dummy
        field_text = "\n".join(fields)
        ax.text(x - 1.1, y - 0.2, field_text, fontsize=8, color='#1E293B', va='center', family='monospace')

    # Draw relations
    def draw_rel(x1, y1, x2, y2, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5, ls='--'))
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, label, fontsize=7.5, ha='center', color='#475569')

    draw_rel(1.5, 4.7, 1.5, 3.5, "1:N")
    draw_rel(2.8, 5.8, 3.5, 5.8, "1:1 (Vendor)")
    draw_rel(4.8, 4.7, 4.8, 3.5, "1:N (Books)")
    draw_rel(6.9, 2.5, 6.1, 2.5, "N:1")
    draw_rel(2.8, 6.3, 6.9, 6.3, "1:N (Customer)")
    draw_rel(6.1, 5.8, 6.9, 5.8, "1:N (Shop)")
    draw_rel(9.5, 5.8, 9.9, 5.8, "1:N (Items)")
    draw_rel(9.9, 2.5, 8.2, 4.7, "N:1 (Voucher)")
    draw_rel(6.1, 2.5, 11.2, 4.7, "N:1 (Product)")

    plt.tight_layout()
    plt.savefig('DOCUMENT/images_report/diagram_erd.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("ERD diagram created.")

# 3. Customer Flow (Thien)
def create_customer_flow():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    ax.text(6, 5.5, "QUY TRÌNH MUA HÀNG VÀ THANH TOÁN (PHÂN HỆ KHÁCH HÀNG - NGỌC THIỆN)", 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#004C22')

    steps = [
        (1.2, 3.5, "1. Duyệt & Tìm kiếm\nTrang chủ, Bộ lọc sách,\nXem Storefront"),
        (3.6, 3.5, "2. Thêm giỏ hàng\nChọn số lượng,\nKiểm tra tồn kho"),
        (6.0, 3.5, "3. Áp dụng Ưu đãi\nNhập mã Voucher,\nTính phí ship 34 tỉnh"),
        (8.4, 3.5, "4. Đặt hàng & OTP\nNhập địa chỉ giao,\nXác thực mã OTP"),
        (10.8, 3.5, "5. Hoàn tất & Đánh giá\nTheo dõi đơn hàng,\nViết review sách")
    ]

    for x, y, text in steps:
        rect = patches.FancyBboxPatch((x - 1.0, y - 0.7), 2.0, 1.4, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, color='#1E293B')

    for i in range(len(steps)-1):
        x1 = steps[i][0] + 1.0
        x2 = steps[i+1][0] - 1.0
        ax.annotate('', xy=(x2, 3.5), xytext=(x1, 3.5),
                    arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=2))

    # Note
    ax.text(6, 1.2, "Điểm nổi bật: Tự động tính cước vận chuyển chuẩn theo khoảng cách địa lý 34 tỉnh thành cải cách hành chính,\náp dụng đồng thời Voucher giảm giá sàn và Voucher gian hàng.", 
            ha='center', va='center', fontsize=9, style='italic', color='#475569',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FEF3C7", edgecolor="#F59E0B", lw=1))

    plt.tight_layout()
    plt.savefig('DOCUMENT/images_report/diagram_customer_flow.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("Customer flow created.")

# 4. Vendor Flow (Hoa)
def create_vendor_flow():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    ax.text(6, 5.5, "QUY TRÌNH VẬN HÀNH GIAN HÀNG & XỬ LÝ ĐƠN HÀNG (PHÂN HỆ VENDOR - QUANG HÒA)", 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#904D00')

    steps = [
        (1.2, 3.5, "1. Đăng ký Gian hàng\nĐiền hồ sơ shop,\nKho hàng & Giấy tờ"),
        (3.6, 3.5, "2. Quản lý Sản phẩm\nĐăng bán sách,\nCập nhật giá & tồn kho"),
        (6.0, 3.5, "3. Nhận đơn hàng mới\nThông báo realtime,\nKiểm tra trạng thái"),
        (8.4, 3.5, "4. Đóng gói & Giao vận\nChuyển Đang giao,\nIn phiếu xuất kho"),
        (10.8, 3.5, "5. Doanh thu & Thống kê\nĐối soát tài chính,\nQuản lý Voucher shop")
    ]

    for x, y, text in steps:
        rect = patches.FancyBboxPatch((x - 1.0, y - 0.7), 2.0, 1.4, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor="#FFF7ED", edgecolor="#EA580C", linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, color='#1E293B')

    for i in range(len(steps)-1):
        x1 = steps[i][0] + 1.0
        x2 = steps[i+1][0] - 1.0
        ax.annotate('', xy=(x2, 3.5), xytext=(x1, 3.5),
                    arrowprops=dict(arrowstyle="-|>", color="#EA580C", lw=2))

    ax.text(6, 1.2, "Điểm nổi bật: Quản lý kho sách theo thời gian thực (real-time inventory lock),\nxử lý đơn hàng đa trạng thái và phân tách doanh thu tự động theo từng shop.", 
            ha='center', va='center', fontsize=9, style='italic', color='#475569',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFEDD5", edgecolor="#F97316", lw=1))

    plt.tight_layout()
    plt.savefig('DOCUMENT/images_report/diagram_vendor_flow.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("Vendor flow created.")

# 5. Admin & Manager Flow (Phat)
def create_admin_flow():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')

    ax.text(6, 5.5, "QUY TRÌNH QUẢN TRỊ & VẬN HÀNH SÀN (PHÂN HỆ ADMIN & MANAGER - THÀNH PHÁT)", 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#15803D')

    steps = [
        (1.2, 3.5, "1. Giám sát Dashboard\nDoanh thu toàn sàn,\nLượng đơn & Tăng trưởng"),
        (3.6, 3.5, "2. Duyệt Đăng ký Shop\nThẩm định hồ sơ,\nCấp quyền VENDOR"),
        (6.0, 3.5, "3. Quản lý Người dùng\nPhân quyền RBAC,\nKhóa/mở tài khoản"),
        (8.4, 3.5, "4. Dữ liệu nền & Sách\nQuản lý danh mục,\nKiểm duyệt tác phẩm"),
        (10.8, 3.5, "5. Xử lý Khiếu nại\nGiải quyết tranh chấp,\nBảo mật hệ thống")
    ]

    for x, y, text in steps:
        rect = patches.FancyBboxPatch((x - 1.0, y - 0.7), 2.0, 1.4, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor="#F0FDF4", edgecolor="#16A34A", linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8.5, color='#1E293B')

    for i in range(len(steps)-1):
        x1 = steps[i][0] + 1.0
        x2 = steps[i+1][0] - 1.0
        ax.annotate('', xy=(x2, 3.5), xytext=(x1, 3.5),
                    arrowprops=dict(arrowstyle="-|>", color="#16A34A", lw=2))

    ax.text(6, 1.2, "Điểm nổi bật: Phân quyền đa cấp nghiêm ngặt (Admin - Manager - Vendor - Customer),\nBáo cáo trực quan với chỉ số phân tích chuyên sâu và tự động hóa quy trình hậu kiểm.", 
            ha='center', va='center', fontsize=9, style='italic', color='#475569',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#DCFCE7", edgecolor="#22C55E", lw=1))

    plt.tight_layout()
    plt.savefig('DOCUMENT/images_report/diagram_admin_flow.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("Admin flow created.")

if __name__ == '__main__':
    create_architecture_diagram()
    create_erd_diagram()
    create_customer_flow()
    create_vendor_flow()
    create_admin_flow()
    print("All 5 diagrams successfully generated!")
