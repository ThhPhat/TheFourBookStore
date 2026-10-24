# -*- coding: utf-8 -*-
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = Document()

    # 1. Page Margins (Standard 1 inch / 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        # Header / Footer setup
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "TRƯỜNG ĐH SƯ PHẠM KỸ THUẬT TP.HCM | BÁO CÁO DỰ ÁN: THEFOURBOOKSTORE"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        if hp.runs:
            hp.runs[0].font.size = Pt(8.5)
            hp.runs[0].font.color.rgb = RGBColor(120, 120, 120)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.text = "Môn học: Lập trình Web | Hệ thống E-Commerce Sách Đa Người Bán"
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if fp.runs:
            fp.runs[0].font.size = Pt(8.5)
            fp.runs[0].font.color.rgb = RGBColor(120, 120, 120)

    # Styles setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(11.5)
    style_normal.font.color.rgb = RGBColor(30, 41, 59)
    style_normal.paragraph_format.line_spacing = 1.2
    style_normal.paragraph_format.space_after = Pt(4)

    # Helper functions
    def set_cell_background(cell, hex_color):
        shd = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), hex_color))
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_borders(cell, color="CBD5E1", sz="4", val="single"):
        tcBorders = parse_xml(r'''
            <w:tcBorders {}>
                <w:top w:val="{}" w:sz="{}" w:space="0" w:color="{}"/>
                <w:left w:val="{}" w:sz="{}" w:space="0" w:color="{}"/>
                <w:bottom w:val="{}" w:sz="{}" w:space="0" w:color="{}"/>
                <w:right w:val="{}" w:sz="{}" w:space="0" w:color="{}"/>
            </w:tcBorders>
        '''.format(nsdecls('w'), val, sz, color, val, sz, color, val, sz, color, val, sz, color))
        cell._tc.get_or_add_tcPr().append(tcBorders)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcMar = parse_xml(r'''
            <w:tcMar {}>
                <w:top w:w="{}" w:type="dxa"/>
                <w:bottom w:w="{}" w:type="dxa"/>
                <w:left w:w="{}" w:type="dxa"/>
                <w:right w:w="{}" w:type="dxa"/>
            </w:tcMar>
        '''.format(nsdecls('w'), top, bottom, left, right))
        cell._tc.get_or_add_tcPr().append(tcMar)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(0, 76, 34) # #004C22
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13.5)
        run.font.color.rgb = RGBColor(21, 128, 61) # #15803D
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(144, 77, 0) # #904D00
        return p

    def add_p(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
        r = p.add_run(text)
        r.italic = italic
        return p

    def add_callout(text, title="LƯU Ý / ĐIỂM NỔI BẬT:"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "EFF6FF")
        set_cell_borders(cell, color="3B82F6", sz="8")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(f"📌 {title} ")
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(30, 64, 175)
        r_t.font.size = Pt(10.5)
        r_c = p.add_run(text)
        r_c.font.size = Pt(10.5)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def add_prompt_box(prompt_text, description="Lệnh Prompt mẫu đã sử dụng:"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "FEF3C7")
        set_cell_borders(cell, color="D97706", sz="6")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(f"🤖 {description}\n")
        r_t.bold = True
        r_t.font.color.rgb = RGBColor(180, 83, 9)
        r_t.font.size = Pt(10)
        r_c = p.add_run(prompt_text)
        r_c.font.size = Pt(9.5)
        r_c.font.name = 'Consolas'
        r_c.font.color.rgb = RGBColor(69, 26, 3)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def add_code_block(code_text, filename="Source Code"):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        set_cell_background(cell, "F8FAFC")
        set_cell_borders(cell, color="CBD5E1", sz="4")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r_f = p.add_run(f"📄 [{filename}]\n")
        r_f.bold = True
        r_f.font.size = Pt(9)
        r_f.font.color.rgb = RGBColor(71, 85, 105)
        r_c = p.add_run(code_text)
        r_c.font.size = Pt(8.5)
        r_c.font.name = 'Consolas'
        r_c.font.color.rgb = RGBColor(15, 23, 42)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def add_image_with_caption(img_path, caption, width=Inches(5.8)):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run()
            run.add_picture(img_path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run(caption)
            r_cap.italic = True
            r_cap.font.size = Pt(9.5)
            r_cap.font.color.rgb = RGBColor(71, 85, 105)
        else:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(f"[Hình ảnh: {caption} - Đường dẫn: {img_path}]")
            r.italic = True

    # ==================== TRANG BÌA ====================
    p_univ = doc.add_paragraph()
    p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_univ.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC SƯ PHẠM KỸ THUẬT TP. HỒ CHÍ MINH\nKHOA CÔNG NGHỆ THÔNG TIN\nBỘ MÔN KỸ THUẬT PHẦN MỀM\n")
    r1.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = RGBColor(0, 51, 102)

    if os.path.exists("DOCUMENT/Logo4bs.png"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(10)
        p_logo.add_run().add_picture("DOCUMENT/Logo4bs.png", width=Inches(1.8))

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(10)
    r_sub = p_title.add_run("BÁO CÁO CUỐI KỲ MÔN HỌC: LẬP TRÌNH WEB\n\n")
    r_sub.bold = True
    r_sub.font.size = Pt(14)
    r_sub.font.color.rgb = RGBColor(180, 83, 9)

    r_main = p_title.add_run("XÂY DỰNG SÀN THƯƠNG MẠI ĐIỆN TỬ SÁCH ĐA GIAN HÀNG\nTHEFOURBOOKSTORE\nỨNG DỤNG GENERATIVE AI TRONG CHU TRÌNH PHÁT TRIỂN")
    r_main.bold = True
    r_main.font.size = Pt(16)
    r_main.font.color.rgb = RGBColor(0, 76, 34)

    p_info = doc.add_paragraph()
    p_info.paragraph_format.space_before = Pt(30)
    p_info.paragraph_format.space_after = Pt(40)
    p_info.paragraph_format.left_indent = Inches(1.2)
    
    r_gv = p_info.add_run("Giảng viên hướng dẫn:\n")
    r_gv.bold = True
    r_gv.font.size = Pt(12)
    p_info.add_run("Thầy/Cô Phụ trách Môn học Lập trình Web\n\n")

    r_sv = p_info.add_run("Sinh viên thực hiện (Nhóm 3 thành viên):\n")
    r_sv.bold = True
    r_sv.font.size = Pt(12)
    
    p_info.add_run("1. Võ Thành Phát    - MSSV: 24110300 (Nhóm trưởng - Quản trị Manager, Admin)\n")
    p_info.add_run("2. Bùi Quang Hòa    - MSSV: 24110213 (Thành viên - Kênh người bán Vendor, Xử lý đơn hàng)\n")
    p_info.add_run("3. Nguyễn Ngọc Thiện - MSSV: 24110335 (Thành viên - Đăng nhập, Đăng ký, Khách hàng, Giỏ hàng, Mua hàng)\n")

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_f = p_foot.add_run("TP. HỒ CHÍ MINH, THÁNG 10 NĂM 2026")
    r_f.bold = True
    r_f.font.size = Pt(11)

    doc.add_page_break()

    # ==================== TRANG BẢNG PHÂN CÔNG ====================
    add_h1("BẢNG PHÂN CÔNG NHIỆM VỤ VÀ ĐÁNH GIÁ MỨC ĐỘ HOÀN THÀNH")
    add_p("Dự án được xây dựng và phối hợp chặt chẽ giữa 3 thành viên với sự hỗ trợ toàn diện của Trí tuệ nhân tạo (AI):")

    table_pc = doc.add_table(rows=4, cols=5)
    table_pc.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["STT", "Họ và Tên", "MSSV", "Phân hệ đảm nhiệm & Nhiệm vụ chính", "Đánh giá"]
    for i, h in enumerate(headers):
        cell = table_pc.cell(0, i)
        set_cell_background(cell, "004C22")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_pc = [
        ("1", "Võ Thành Phát\n(Trưởng nhóm)", "24110300", 
         "• Phân hệ Quản trị viên (ADMIN) & Quản lý vận hành (MANAGER)\n• Quản lý người dùng, phân quyền bảo mật RBAC\n• Thẩm định & duyệt hồ sơ gian hàng Vendor\n• Bảng điều khiển phân tích doanh thu (Dashboard toàn sàn)\n• Quản lý danh mục dữ liệu nền & giải quyết tranh chấp", "100%"),
        ("2", "Bùi Quang Hòa", "24110213", 
         "• Phân hệ Kênh người bán (VENDOR / SELLER CENTER)\n• Đăng ký gian hàng, quản lý hồ sơ Shop & Storefront\n• Quản lý kho sách: đăng bán, cập nhật giá & số lượng tồn kho\n• Quy trình xử lý đơn hàng đa trạng thái của Shop\n• Quản trị mã giảm giá riêng của Vendor & báo cáo doanh thu shop", "100%"),
        ("3", "Nguyễn Ngọc Thiện", "24110335", 
         "• Phân hệ Khách hàng (CUSTOMER & GUEST)\n• Đăng ký, đăng nhập bảo mật & xác thực OTP\n• Giao diện trang chủ, tìm kiếm sách & lọc đa tiêu chí\n• Giỏ hàng realtime, thuật toán tính phí ship theo khoảng cách 34 tỉnh\n• Áp dụng đồng thời Voucher Sàn & Voucher Shop, quy trình Checkout", "100%")
    ]

    for row_idx, row_data in enumerate(data_pc, start=1):
        bg = "FFFFFF" if row_idx % 2 == 1 else "F8FAFC"
        for col_idx, text in enumerate(row_data):
            cell = table_pc.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_borders(cell, color="CBD5E1", sz="4")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9.5)
            if col_idx in [0, 2, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if col_idx == 4:
                    r.bold = True
                    r.font.color.rgb = RGBColor(21, 128, 61)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==================== MỤC LỤC TỔNG QUAN ====================
    add_h1("MỤC LỤC NỘI DUNG CHÍNH")
    toc_items = [
        ("CHƯƠNG 1: TỔNG QUAN VÀ KHẢO SÁT HIỆN TRẠNG (REQUIREMENT ANALYSIS)", "Trang 3"),
        ("   1.1. Đặt vấn đề và Lý do chọn đề tài", "Trang 3"),
        ("   1.2. Khảo sát hiện trạng các sàn TMĐT sách và Điểm cải tiến", "Trang 3"),
        ("   1.3. Mục tiêu và Phạm vi dự án", "Trang 4"),
        ("   1.4. Mô tả các nhóm tác nhân trong hệ thống (Actors)", "Trang 4"),
        ("CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG (SYSTEM ANALYSIS & DESIGN)", "Trang 5"),
        ("   2.1. Kiến trúc tổng thể hệ thống (Spring Boot MVC N-Tier Architecture)", "Trang 5"),
        ("   2.2. Phân tích chức năng và Sơ đồ Use Case", "Trang 6"),
        ("   2.3. Thiết kế Cơ sở Dữ liệu quan hệ (ERD, Stored Procedures & Triggers)", "Trang 7"),
        ("   2.4. Thiết kế Giao diện người dùng với công cụ AI Stitch (Design System Forest Folio)", "Trang 8"),
        ("CHƯƠNG 3: QUÁ TRÌNH XÂY DỰNG VÀ DIỄN GIẢI CHI TIẾT TỪNG CHỨC NĂNG", "Trang 10"),
        ("   PHẦN A (Nguyễn Ngọc Thiện): Phân hệ Khách hàng, Đăng nhập, Đăng ký & Mua hàng", "Trang 10"),
        ("      3.1. Xác thực người dùng, Đăng ký/Đăng nhập & Xác thực OTP", "Trang 10"),
        ("      3.2. Trang chủ, Khám phá sách & Tìm kiếm thông minh đa tiêu chí", "Trang 12"),
        ("      3.3. Giỏ hàng realtime, Áp dụng Voucher & Thuật toán tính phí ship khoảng cách", "Trang 14"),
        ("      3.4. Giao dịch Đặt hàng (Checkout) & Quản lý lịch sử đơn mua", "Trang 16"),
        ("   PHẦN B (Bùi Quang Hòa): Phân hệ Kênh người bán (Vendor Center) & Xử lý đơn hàng", "Trang 18"),
        ("      3.5. Đăng ký mở Gian hàng và Trang Storefront Shop độc lập", "Trang 18"),
        ("      3.6. Quản lý kho sách, Đăng bán sản phẩm & Cập nhật giá", "Trang 20"),
        ("      3.7. Tiếp nhận và Xử lý đơn hàng đa trạng thái của Vendor", "Trang 22"),
        ("      3.8. Quản lý Khuyến mãi, Voucher riêng của Gian hàng & Báo cáo", "Trang 24"),
        ("   PHẦN C (Võ Thành Phát): Phân hệ Quản lý vận hành (Manager) & Quản trị hệ thống (Admin)", "Trang 26"),
        ("      3.9. Bảng điều khiển Quản trị toàn diện (Admin & Manager Dashboard)", "Trang 26"),
        ("      3.10. Thẩm định, Phê duyệt hoặc Từ chối đơn đăng ký Gian hàng Shop", "Trang 28"),
        ("      3.11. Quản lý Người dùng & Phân quyền kiểm soát truy cập (RBAC)", "Trang 30"),
        ("      3.12. Quản lý Dữ liệu nền (Danh mục, Tác giả) & Xử lý Khiếu nại vận hành", "Trang 32"),
        ("CHƯƠNG 4: DANH SÁCH PROMPT AI VÀ QUY TRÌNH PHỐI HỢP CÙNG AI", "Trang 34"),
        ("   4.1. Quy trình kết hợp Human-in-the-loop cùng AI trong chu trình SDLC", "Trang 34"),
        ("   4.2. Bảng tổng hợp các câu lệnh Prompt tiêu biểu phân theo từng giai đoạn", "Trang 35"),
        ("   4.3. Đánh giá phản biện: Điểm mạnh, hạn chế của AI và vai trò của sinh viên", "Trang 37"),
        ("CHƯƠNG 5: HƯỚNG DẪN CÀI ĐẶT VÀ TRIỂN KHAI HỆ THỐNG (SETUP GUIDE)", "Trang 38"),
        ("   5.1. Yêu cầu môi trường phần cứng và phần mềm", "Trang 38"),
        ("   5.2. Hướng dẫn thiết lập Cơ sở Dữ liệu SQL Server / MySQL", "Trang 38"),
        ("   5.3. Cấu hình ứng dụng Spring Boot (application.properties & .env)", "Trang 39"),
        ("   5.4. Lệnh khởi chạy ứng dụng & Danh mục tài khoản thử nghiệm", "Trang 40"),
        ("CHƯƠNG 6: KIỂM THỬ HỆ THỐNG VÀ KẾT QUẢ THỰC NGHIỆM", "Trang 41"),
        ("   6.1. Phương pháp kiểm thử hộp đen (Black-box Testing)", "Trang 41"),
        ("   6.2. Kịch bản kiểm thử chi tiết theo từng thành viên", "Trang 41"),
        ("   6.3. Đánh giá độ ổn định và kết quả thực nghiệm", "Trang 44"),
        ("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "Trang 45"),
        ("TÀI LIỆU THAM KHẢO", "Trang 46")
    ]
    for title, pg in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(title)
        r_t.font.size = Pt(10)
        if "CHƯƠNG" in title or "PHẦN" in title:
            r_t.bold = True
            if "CHƯƠNG" in title:
                r_t.font.color.rgb = RGBColor(0, 76, 34)

    doc.add_page_break()

    # ==================== CHƯƠNG 1 ====================
    add_h1("CHƯƠNG 1: TỔNG QUAN VÀ KHẢO SÁT HIỆN TRẠNG (REQUIREMENT ANALYSIS)")
    
    add_h2("1.1. Đặt vấn đề và Lý do chọn đề tài")
    add_p("Trong kỷ nguyên số hóa và sự bùng nổ của thương mại điện tử, thị trường sách truyền thống đang trải qua cuộc chuyển mình mạnh mẽ. Độc giả ngày nay có xu hướng tìm kiếm và mua sách trực tuyến nhờ vào sự tiện lợi, tốc độ giao hàng cũng như khả năng tiếp cận kho ấn phẩm phong phú. Tuy nhiên, các nhà xuất bản nhỏ, chuỗi hiệu sách độc lập (Independent Bookstore) thường gặp khó khăn lớn khi phải tự xây dựng website riêng vì chi phí đầu tư hạ tầng công nghệ và bảo trì rất tốn kém.")
    add_p("Từ thực trạng đó, nhóm chúng tôi chọn đề tài xây dựng Sàn thương mại điện tử sách đa gian hàng mang tên TheFourBookStore. Hệ thống là nơi kết nối độc giả với nhiều chuỗi nhà sách phân phối uy tín (như NXB Kim Đồng, Nhã Nam, Fahasa,...), cho phép mỗi đơn vị vận hành một gian hàng trực tuyến độc lập (Storefront) trong khi sàn chịu trách nhiệm điều phối giỏ hàng chung, tính toán phí giao hàng thông minh, phân quyền an ninh và thanh toán tập trung.")

    add_h2("1.2. Khảo sát hiện trạng các sàn TMĐT sách và Điểm cải tiến")
    add_p("Nhóm đã tiến hành khảo sát và phân tích các nền tảng thương mại điện tử sách hiện có tại Việt Nam:")
    add_p("• Fahasa Online: Điểm mạnh là kho sách chính thống lớn, nhưng chỉ đóng vai trò là một nhà bán lẻ đơn lẻ (Single-vendor), không cho phép các bên thứ ba mở gian hàng phân phối.", bold_prefix="1. Nền tảng chuyên biệt: ")
    add_p("• Tiki / Shopee: Là sàn đa gian hàng rất lớn, tuy nhiên do bán hàng triệu loại mặt hàng tổng hợp nên trải nghiệm tìm kiếm chuyên sâu về sách (tìm theo ISBN, tên dịch giả, nhà xuất bản, năm tái bản, đọc thử nội dung) chưa được tối ưu cao cấp cho người yêu sách.", bold_prefix="2. Nền tảng sàn tổng hợp: ")
    add_p("TheFourBookStore tập trung giải quyết bài toán giao thoa này: Một sàn chuyên biệt về sách nhưng hoạt động theo mô hình Đa người bán (Multi-vendor), kết hợp hệ thống tính cước vận chuyển chuẩn theo 34 tỉnh thành cải cách hành chính mới, hỗ trợ áp dụng đồng thời Voucher Sàn & Voucher Shop, và ứng dụng AI trong tạo giao diện thẩm mỹ cao.")

    add_h2("1.3. Mục tiêu và Phạm vi dự án")
    add_p("• Mục tiêu kỹ thuật: Xây dựng ứng dụng web hoàn chỉnh theo chuẩn kiến trúc MVC phân tầng (N-tier Architecture) sử dụng framework Spring Boot 3.x, Spring Data JPA, Hibernate, Thymeleaf, Spring Security kết hợp cơ sở dữ liệu Microsoft SQL Server / MySQL.")
    add_p("• Mục tiêu ứng dụng AI: Tận dụng tối đa các công cụ Trí tuệ Nhân tạo thế hệ mới (Generative AI, AI Stitch Design, GitHub Copilot / LLMs) trong mọi khâu phát triển: từ khâu phân tích khảo sát, sinh mô hình quan hệ CSDL, thiết kế hệ thống giao diện Forest Folio, sinh code logic nghiệp vụ đến kiểm thử tự động.")
    add_p("• Phạm vi dự án: Hệ thống bao phủ toàn bộ vòng đời của một sàn thương mại điện tử: Đăng ký / Đăng nhập OTP -> Khám phá sách -> Giỏ hàng -> Tính khoảng cách vận chuyển -> Áp mã giảm giá -> Đặt hàng -> Xử lý đơn hàng -> Kiểm kê kho -> Báo cáo doanh thu và Phân quyền RBAC.")

    add_h2("1.4. Mô tả các nhóm tác nhân trong hệ thống (Actors)")
    add_p("Hệ thống TheFourBookStore phục vụ 4 nhóm tác nhân chính:")
    add_p("Người dùng duyệt xem sản phẩm, tìm kiếm sách theo bộ lọc nâng cao, quản lý giỏ hàng, áp dụng voucher, đặt hàng giao tận nơi, tra cứu lịch sử mua sắm và đánh giá sách đã mua.", bold_prefix="1. Khách hàng (Customer & Guest): ")
    add_p("Các đơn vị kinh doanh sách, nhà xuất bản đăng ký mở shop trên sàn. Sau khi được duyệt, Vendor có trang Storefront riêng, quản lý danh mục sách của shop, cập nhật kho, tạo mã giảm giá riêng và xử lý đơn hàng do khách đặt.", bold_prefix="2. Chủ gian hàng (Vendor / Seller): ")
    add_p("Nhân sự vận hành sàn, chịu trách nhiệm thẩm định và phê duyệt các đơn đăng ký mở shop mới, kiểm duyệt sản phẩm sách và xử lý các khiếu nại phát sinh giữa khách hàng và gian hàng.", bold_prefix="3. Quản lý vận hành (Manager): ")
    add_p("Người có thẩm quyền cao nhất, quản lý toàn bộ danh mục tài khoản người dùng, phân quyền RBAC, giám sát an ninh hệ thống và theo dõi báo cáo doanh thu tài chính tổng thể của toàn sàn.", bold_prefix="4. Quản trị viên hệ thống (Admin): ")

    doc.add_page_break()

    # ==================== CHƯƠNG 2 ====================
    add_h1("CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG (SYSTEM ANALYSIS & DESIGN)")

    add_h2("2.1. Kiến trúc tổng thể hệ thống (Spring Boot MVC N-Tier Architecture)")
    add_p("Hệ thống được thiết kế theo mô hình kiến trúc phân tầng chuẩn mực của doanh nghiệp (Enterprise N-Tier Architecture), phân tách độc lập các mối quan tâm (Separation of Concerns) để đảm bảo tính module hóa, dễ bảo trì và mở rộng:")
    
    add_image_with_caption("DOCUMENT/images_report/diagram_architecture.png", 
                           "Hình 2.1: Sơ đồ kiến trúc tổng thể ứng dụng TheFourBookStore (Spring Boot MVC N-Tier)")

    add_p("Các tầng kiến trúc chi tiết gồm có:")
    add_p("Sử dụng công nghệ Server-side Rendering với Thymeleaf Engine kết hợp Tailwind CSS. Giao diện được đồng bộ hóa với hệ thống Design System 'Forest Folio' do AI Stitch sinh ra, đảm bảo tính thẩm mỹ cổ điển, trải nghiệm responsive hoàn hảo trên máy tính và thiết bị di động.", bold_prefix="• Tầng Trình diễn (Presentation Layer): ")
    add_p("Được bảo vệ bởi Spring Security với chuỗi bộ lọc bảo mật (Security Filter Chain). Các Controller tiếp nhận HTTP Request (GET, POST, PUT, DELETE), xác thực quyền hạn RBAC của người dùng thông qua annotations (@PreAuthorize, hasAnyRole), binding dữ liệu DTO và điều hướng sang View hoặc trả về dữ liệu JSON.", bold_prefix="• Tầng Điều hướng & Bảo mật (Security & Controller Layer): ")
    add_p("Nơi chứa đựng toàn bộ quy tắc nghiệp vụ (Business Rules). Tầng này xử lý logic trừ kho realtime khi đặt hàng, kiểm tra tính hợp lệ của Voucher đa cấp, tính cước vận chuyển chuẩn theo 34 tỉnh thành và quản lý luồng giao dịch (@Transactional).", bold_prefix="• Tầng Nghiệp vụ cốt lõi (Service Layer): ")
    add_p("Sử dụng Spring Data JPA kết hợp Hibernate để ánh xạ các Entity thành quan hệ CSDL. Tầng này cung cấp các giao diện Repository mạnh mẽ, hỗ trợ viết truy vấn động Specification cho bộ lọc tìm kiếm và gọi các Stored Procedure được tối ưu sẵn trong CSDL.", bold_prefix="• Tầng Truy xuất Dữ liệu (Repository / Persistence Layer): ")
    add_p("Hệ quản trị CSDL quan hệ Microsoft SQL Server 2022 (hoặc MySQL 8.0). Toàn bộ dữ liệu được chuẩn hóa, thiết lập chỉ mục (Indexes) để tăng tốc độ truy vấn, và sử dụng Stored Procedures cho các giao dịch nhạy cảm như Đặt hàng và Trừ tồn kho an toàn.", bold_prefix="• Tầng Cơ sở Dữ liệu (Database Layer): ")

    add_h2("2.2. Phân tích chức năng và Sơ đồ Use Case")
    add_p("Hệ thống phân rã thành các nhóm ca sử dụng tương ứng với 4 vai trò chính:")
    add_p("Đăng ký tài khoản, Đăng nhập hệ thống, Xác thực OTP email, Xem trang chủ & sách bán chạy, Tìm kiếm sách thông minh, Lọc sách đa tiêu chí (ngành hàng, loại sản phẩm, giá, tác giả), Xem chi tiết sách & đọc review, Xem Storefront gian hàng, Thêm sách vào giỏ hàng, Áp dụng Voucher (Sàn & Shop), Đặt hàng (Checkout) với địa chỉ nhận hàng, Tra cứu lịch sử đơn hàng, Đánh giá sản phẩm đã mua.", bold_prefix="1. Use Cases Khách hàng: ")
    add_p("Đăng ký mở gian hàng, Cập nhật thông tin hồ sơ Shop & Banner, Quản lý danh mục sách của shop (Thêm, Sửa, Xóa, Cập nhật giá), Quản lý phiếu nhập kho sách, Quản lý danh sách đơn hàng của shop (Xác nhận, Đang chuẩn bị, Đang giao, Đã giao, Hủy), Tạo và quản lý mã Voucher riêng của shop, Xem thống kê doanh thu bán hàng của shop.", bold_prefix="2. Use Cases Gian hàng (Vendor): ")
    add_p("Xem danh sách đơn đăng ký mở shop chờ duyệt, Xem chi tiết giấy tờ kinh doanh & thông tin kho của vendor, Phê duyệt hoặc từ chối hồ sơ shop, Kiểm duyệt danh mục sách trên sàn, Xử lý và phân xử các khiếu nại đơn hàng.", bold_prefix="3. Use Cases Quản lý vận hành (Manager): ")
    add_p("Đăng nhập quyền quản trị, Xem bảng điều khiển thống kê tổng quan (Dashboard: tổng doanh thu, số lượng đơn, khách hàng mới, shop mới), Quản lý tài khoản người dùng (Xem danh sách, khóa/mở khóa tài khoản, phân quyền vai trò), Quản lý danh mục dữ liệu nền toàn sàn (Thể loại, Tác giả, Nhà xuất bản), Cấu hình thông số hệ thống.", bold_prefix="4. Use Cases Quản trị viên (Admin): ")

    add_h2("2.3. Thiết kế Cơ sở Dữ liệu quan hệ (ERD, Stored Procedures & Triggers)")
    add_p("Cơ sở dữ liệu của TheFourBookStore được thiết kế theo chuẩn hóa dữ liệu bậc 3 (3NF), đảm bảo tính toàn vẹn dữ liệu và triệt tiêu dư thừa:")

    add_image_with_caption("DOCUMENT/images_report/diagram_erd.png", 
                           "Hình 2.2: Sơ đồ thực thể cơ sở dữ liệu cốt lõi (Core ERD Model)")

    add_p("Các bảng dữ liệu trung tâm trong hệ thống bao gồm:")
    add_p("Lưu trữ thông tin định danh, mật khẩu băm BCrypt, email, số điện thoại, trạng thái hoạt động.", bold_prefix="• NguoiDung (User) & VaiTro (Role): ")
    add_p("Lưu trữ thông tin các nhà sách đối tác, địa chỉ kho tại các tỉnh thành, thông tin liên hệ và trạng thái phê duyệt (PENDING, APPROVED, REJECTED).", bold_prefix="• GianHang (Shop): ")
    add_p("Chứa thông tin chi tiết về từng cuốn sách, mã ISBN, danh mục, tác giả, nhà xuất bản, giá bán, số lượng tồn kho và cờ trạng thái kinh doanh.", bold_prefix="• SanPham (Book) & DanhMuc (Category): ")
    add_p("Quản lý thông tin đơn hàng do khách đặt, liên kết với shop phân phối, tổng tiền hàng, cước vận chuyển, mã voucher đã áp dụng và trạng thái đơn hàng.", bold_prefix="• DonHang (Order) & ChiTietDonHang (OrderItem): ")
    add_p("Hỗ trợ hai loại voucher: Voucher sàn (áp dụng cho toàn bộ đơn hàng) và Voucher shop (chỉ áp dụng cho sản phẩm do chính shop đó bán), có cấu hình giá trị giảm, phần trăm giảm và đơn hàng tối thiểu.", bold_prefix="• Voucher (KhuyenMai): ")
    
    add_callout(
        "Hệ thống ứng dụng các Stored Procedure nâng cao trong T-SQL / MySQL để xử lý đặt hàng: Stored Procedure tự động khóa dòng (Row-level lock) kiểm tra số lượng tồn kho của từng cuốn sách trước khi trừ, nếu không đủ số lượng sẽ tự động ROLLBACK giao dịch để bảo toàn tính nhất quán dữ liệu.",
        "ĐIỂM SÁNG TRONG THIẾT KẾ DỮ LIỆU"
    )

    add_h2("2.4. Thiết kế Giao diện người dùng với công cụ AI Stitch (Design System Forest Folio)")
    add_p("Nhóm đã sử dụng công cụ thiết kế giao diện trí tuệ nhân tạo AI Stitch (Google Stitch Tool) để tạo dựng bộ nhận diện thương hiệu độc bản mang phong cách 'Forest Folio'.")
    add_p("• Ý tưởng thiết kế: Lấy cảm hứng từ không gian của những thư viện cổ điển kết hợp phong cách hiện đại tối giản. Sử dụng tông màu xanh lục bảo (Deep Emerald Green `#004c22`) tượng trưng cho tri thức và chiều sâu, phối hợp cùng tông màu cam đất (`#904d00`) và nền sáng nhẹ nhàng (`#f9f9ff`).")
    add_p("• Hệ thống Tokens & Component: AI Stitch đã tự động sinh ra mã HTML/CSS ngữ nghĩa kết hợp Tailwind CSS hoàn chỉnh, tạo nên các thành phần dùng chung: Hero Banner sách nổi bật, Product Card với nhãn giảm giá và điểm đánh giá sao, Thanh tìm kiếm tích hợp bộ lọc dropdown, Bảng điều khiển quản trị Dashboard với các Card chỉ số KPI sắc sảo.")

    doc.add_page_break()

    # ==================== CHƯƠNG 3 ====================
    add_h1("CHƯƠNG 3: QUÁ TRÌNH XÂY DỰNG VÀ DIỄN GIẢI CHI TIẾT TỪNG CHỨC NĂNG")
    add_p("Chương này mô tả chi tiết quá trình triển khai mã nguồn thực tế của hệ thống, được phân chia cụ thể theo trách nhiệm của 3 thành viên trong nhóm. Mỗi chức năng đều trình bày đầy đủ: Sơ đồ hoạt động -> Diễn giải Source Code & Tác dụng file -> Hình ảnh Giao diện thực tế -> Lệnh Prompt AI tiêu biểu tương ứng.")

    # ------------------ PHẦN A: NGUYỄN NGỌC THIỆN ------------------
    add_h2("PHẦN A: PHÂN HỆ KHÁCH HÀNG, ĐĂNG KÝ, ĐĂNG NHẬP & MUA HÀNG")
    add_p("Sinh viên phụ trách: Nguyễn Ngọc Thiện - MSSV: 24110335", italic=True)

    add_image_with_caption("DOCUMENT/images_report/diagram_customer_flow.png", 
                           "Hình 3.1: Sơ đồ quy trình trải nghiệm mua sắm của Khách hàng (Ngọc Thiện phụ trách)")

    # 3.1
    add_h3("3.1. Chức năng Xác thực người dùng, Đăng ký / Đăng nhập & Xác thực OTP")
    add_p("• Sơ đồ hoạt động: Người dùng truy cập form đăng ký (`/register`), nhập thông tin tài khoản. Hệ thống kiểm tra trùng lặp username/email, sinh mã OTP ngẫu nhiên gửi về email của người dùng. Sau khi xác thực OTP thành công, mật khẩu được mã hóa chuẩn BCrypt và lưu vào CSDL với vai trò mặc định `KHACHHANG`.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `AuthController.java`: Điều hướng các yêu cầu GET/POST cho đăng ký, đăng nhập, quên mật khẩu và nhập mã xác thực OTP.")
    add_p("  - `SecurityConfig.java`: Cấu hình chuỗi lọc Spring Security, form login, cookie remember-me, và xử lý phân quyền URL.")
    add_p("  - `EmailService.java`: Dịch vụ gửi email thông báo mã OTP tự động qua giao thức SMTP.")

    add_code_block(
'''@PostMapping("/register")
public String handleRegister(@Valid @ModelAttribute("user") RegisterDTO dto, BindingResult result, Model model) {
    if (userRepository.existsByUsername(dto.getUsername())) {
        result.rejectValue("username", "duplicate", "Tên đăng nhập đã tồn tại trong hệ thống!");
    }
    if (result.hasErrors()) return "auth/register";
    
    // Tạo mã OTP 6 chữ số và gửi qua email
    String otp = otpService.generateOtp(dto.getEmail());
    emailService.sendOtpEmail(dto.getEmail(), otp);
    session.setAttribute("pendingUser", dto);
    return "redirect:/verify-otp";
}''', "AuthController.java - Xử lý đăng ký tài khoản & gửi OTP"
    )

    add_prompt_box(
'''"Hãy viết một Spring Boot Controller và Service xử lý quy trình đăng ký tài khoản có xác thực email bằng mã OTP 6 chữ số. 
Yêu cầu kiểm tra trùng username/email, lưu tạm thông tin vào Session, mã hóa mật khẩu bằng BCryptPasswordEncoder 
và cấu hình Spring Security cho phép truy cập công khai vào /register, /login, /verify-otp."''',
"Prompt AI tiêu biểu dùng để sinh chức năng Đăng ký & OTP (Ngọc Thiện)"
    )

    # 3.2
    add_h3("3.2. Chức năng Trang chủ, Khám phá sách & Tìm kiếm thông minh đa tiêu chí")
    add_p("• Sơ đồ hoạt động: Trang chủ hiển thị các khối nội dung sinh động: Hero Banner, Top sách bán chạy nhất, Gợi ý theo sở thích và Sách mới cập nhật. Thanh tìm kiếm hỗ trợ nhập từ khóa linh hoạt: tìm theo tên tác phẩm, tên tác giả, mã ISBN. Đặc biệt, nếu từ khóa trùng khớp với tên một nhà sách đối tác, hệ thống tự động hiển thị khối 'Gian hàng phù hợp' để dẫn độc giả tới thẳng trang Storefront của shop đó.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `HomeController.java`: Nạp danh sách sách nổi bật, sách giảm giá, danh mục cấp 1 lên view `home/index.html`.")
    add_p("  - `ProductController.java`: Tiếp nhận các tham số lọc (`category`, `author`, `minPrice`, `maxPrice`, `sort`) và gọi Service thực thi truy vấn.")

    add_image_with_caption("stitch_bookstore_e_commerce_admin_interface/stitch_bookstore_e_commerce_admin_interface/trang_ch_s_ch_b_n_ch_y_the4bookstore/screen.png",
                           "Hình 3.2: Giao diện Trang chủ và Sách bán chạy nhất (Thiết kế AI Stitch - Ngọc Thiện)")

    add_code_block(
'''@GetMapping("/san-pham")
public String filterProducts(@RequestParam(required = false) String q,
                             @RequestParam(required = false) Long categoryId,
                             @RequestParam(required = false) String sort,
                             Model model) {
    List<Product> products = productService.searchAndFilter(q, categoryId, sort);
    // Nhận diện từ khóa có khớp với tên gian hàng đối tác hay không
    Optional<Shop> matchedShop = shopService.findByKeyword(q);
    matchedShop.ifPresent(shop -> model.addAttribute("matchedShop", shop));
    model.addAttribute("products", products);
    return "products/list";
}''', "ProductController.java - Tìm kiếm thông minh & nhận diện gian hàng"
    )

    add_prompt_box(
'''"Viết logic Spring Data JPA Specification trong Spring Boot để tìm kiếm sách đa tiêu chí: 
cho phép kết hợp đồng thời từ khóa tên sách, ID danh mục, khoảng giá từ min đến max, 
và sắp xếp linh hoạt theo giá tăng dần, giảm dần hoặc mới nhất. 
Nếu từ khóa trùng tên shop, trả thêm thông tin shop đó về giao diện Thymeleaf."''',
"Prompt AI tiêu biểu dùng để sinh bộ lọc sách thông minh (Ngọc Thiện)"
    )

    # 3.3
    add_h3("3.3. Chức năng Giỏ hàng realtime, Áp dụng Voucher & Thuật toán tính phí ship")
    add_p("• Sơ đồ hoạt động: Giỏ hàng được lưu trữ an toàn trong CSDL cho từng người dùng. Khi thay đổi số lượng, hệ thống kiểm tra tồn kho realtime. Điểm cải tiến đặc biệt là thuật toán tính phí vận chuyển dựa trên khoảng cách địa lý giữa Tỉnh/Thành phố của kho sách và Tỉnh/Thành phố nhận hàng của người mua (áp dụng bảng khoảng cách 34 tỉnh thành cải cách hành chính mới). Người dùng có thể áp dụng đồng thời Voucher giảm giá của Sàn và Voucher riêng của Shop.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `CartController.java`: Xử lý thêm vào giỏ, cập nhật số lượng, xóa sản phẩm khỏi giỏ hàng.")
    add_p("  - `DistanceCalculatorUtil.java`: Thuật toán tra cứu khoảng cách giữa 34 tỉnh thành và công thức tính cước phí giao vận.")
    add_p("  - `VoucherService.java`: Kiểm tra tính hợp lệ của mã giảm giá (hạn dùng, giá trị đơn tối thiểu, loại voucher).")

    add_image_with_caption("stitch_bookstore_e_commerce_admin_interface/stitch_bookstore_e_commerce_admin_interface/gi_h_ng_thanh_to_n_the4bookstore/screen.png",
                           "Hình 3.3: Giao diện Giỏ hàng & Tạm tính cước vận chuyển (Thiết kế AI Stitch - Ngọc Thiện)")

    add_code_block(
'''public BigDecimal calculateShippingFee(String shopProvince, String customerProvince) {
    if (shopProvince.equalsIgnoreCase(customerProvince)) {
        return new BigDecimal("15000"); // Cùng tỉnh: cước cố định 15k
    }
    double distanceKm = DistanceMatrix.getDistance(shopProvince, customerProvince);
    if (distanceKm <= 100) return new BigDecimal("25000");
    if (distanceKm <= 500) return new BigDecimal("35000");
    return new BigDecimal("45000"); // Tuyến xa liên miền
}''', "DistanceCalculatorUtil.java - Thuật toán tính phí vận chuyển theo khoảng cách"
    )

    add_prompt_box(
'''"Xây dựng một Java Utility class DistanceCalculatorUtil tính cước phí vận chuyển hàng hóa giữa các tỉnh thành tại Việt Nam. 
Hệ thống có danh sách 34 tỉnh thành sau đợt cải cách hành chính, tra cứu ma trận khoảng cách tương đối (km). 
Quy định mức phí: Cùng tỉnh 15.000đ, dưới 100km 25.000đ, từ 100-500km 35.000đ, trên 500km 45.000đ."''',
"Prompt AI tiêu biểu dùng để viết thuật toán tính khoảng cách vận chuyển (Ngọc Thiện)"
    )

    # 3.4
    add_h3("3.4. Chức năng Giao dịch Đặt hàng (Checkout) & Lịch sử đơn hàng")
    add_p("• Sơ đồ hoạt động: Khách hàng chọn địa chỉ nhận hàng, chọn phương thức thanh toán (COD hoặc chuyển khoản), bấm 'Xác nhận Đặt hàng'. Toàn bộ quá trình tạo đơn hàng, sao chép chi tiết mặt hàng, trừ tồn kho và ghi nhận sử dụng voucher được bao bọc trong một Database Transaction duy nhất. Khách hàng có thể vào trang cá nhân để theo dõi hành trình đơn hàng.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `OrderController.java`: Tiếp nhận yêu cầu Checkout, gọi Service tạo đơn và chuyển hướng tới trang thành công.")
    add_p("  - `ProfileController.java`: Quản lý thông tin cá nhân, sổ địa chỉ nhận hàng và hiển thị danh sách đơn hàng đã mua.")

    add_image_with_caption("stitch_bookstore_e_commerce_admin_interface/stitch_bookstore_e_commerce_admin_interface/h_s_c_nh_n_qu_n_l_t_i_kho_n_the4bookstore/screen.png",
                           "Hình 3.4: Giao diện Hồ sơ cá nhân & Quản lý đơn mua (Thiết kế AI Stitch - Ngọc Thiện)")

    # ------------------ PHẦN B: BÙI QUANG HÒA ------------------
    add_h2("PHẦN B: PHÂN HỆ KÊNH NGƯỜI BÁN (VENDOR CENTER) & XỬ LÝ ĐƠN HÀNG")
    add_p("Sinh viên phụ trách: Bùi Quang Hòa - MSSV: 24110213", italic=True)

    add_image_with_caption("DOCUMENT/images_report/diagram_vendor_flow.png", 
                           "Hình 3.5: Sơ đồ quy trình vận hành gian hàng và xử lý đơn của Vendor (Quang Hòa phụ trách)")

    # 3.5
    add_h3("3.5. Chức năng Đăng ký mở Gian hàng và Trang Storefront Shop độc lập")
    add_p("• Sơ đồ hoạt động: Người dùng đã có tài khoản gửi đơn đăng ký mở gian hàng phân phối sách (`/vendor/register`), cung cấp tên shop, địa chỉ kho hàng (tỉnh/thành), số điện thoại, mô tả và giấy phép kinh doanh. Sau khi được Quản lý duyệt, shop được cấp một đường dẫn Storefront riêng biệt (ví dụ `/shop/nha-nam`) hiển thị đầy đủ logo, banner và toàn bộ sách do chính shop đó đăng bán.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `VendorController.java`: Xử lý nộp đơn đăng ký shop và các nghiệp vụ nội bộ của người bán.")
    add_p("  - `ShopStorefrontController.java`: Hiển thị trang công khai của gian hàng cho khách xem sản phẩm của từng shop riêng biệt.")

    add_prompt_box(
'''"Tạo mã nguồn Spring Boot Controller và Thymeleaf view cho chức năng Storefront của gian hàng bán sách. 
Cho phép hiển thị header gồm banner shop, logo, hotline, địa chỉ kho tại tỉnh thành, 
cùng với thanh tìm kiếm và bộ lọc danh mục riêng chỉ áp dụng cho các cuốn sách thuộc quyền sở hữu của gian hàng đó."''',
"Prompt AI tiêu biểu dùng để sinh trang Storefront người bán (Quang Hòa)"
    )

    # 3.6
    add_h3("3.6. Chức năng Quản lý kho sách, Đăng bán sản phẩm & Cập nhật giá")
    add_p("• Sơ đồ hoạt động: Người bán truy cập bảng quản trị Seller Center, có thể thêm mới sách vào kho (nhập tên sách, ISBN, chọn tác giả, danh mục, tải ảnh bìa, đặt giá bán và số lượng nhập ban đầu). Hệ thống hỗ trợ lập phiếu nhập kho để điều chỉnh tăng/giảm tồn kho minh bạch.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `VendorInventoryController.java`: Quản lý kho hàng, lập phiếu nhập kho sách.")
    add_p("  - `VendorStockController.java`: Cập nhật số lượng tồn kho theo thời gian thực.")

    add_image_with_caption("stitch_bookstore_e_commerce_admin_interface/stitch_bookstore_e_commerce_admin_interface/qu_n_l_kho_danh_m_c_s_ch_the4bookstore/screen.png",
                           "Hình 3.6: Giao diện Quản lý kho và Danh mục sách của Vendor (Thiết kế AI Stitch - Quang Hòa)")

    add_code_block(
'''@PostMapping("/vendor/products/save")
@PreAuthorize("hasRole('VENDOR')")
public String saveVendorProduct(@Valid @ModelAttribute("product") ProductDTO dto,
                                @AuthenticationPrincipal UserDetails userDetails,
                                @RequestParam("imageFile") MultipartFile file) {
    Shop shop = shopService.getShopByOwner(userDetails.getUsername());
    dto.setShopId(shop.getId());
    if (!file.isEmpty()) {
        String filename = fileStorageService.storeFile(file);
        dto.setImageUrl("/uploads/" + filename);
    }
    productService.saveProductForVendor(dto);
    return "redirect:/vendor/products?success=true";
}''', "VendorController.java - Thêm mới và quản lý sách của gian hàng"
    )

    # 3.7
    add_h3("3.7. Chức năng Tiếp nhận và Xử lý đơn hàng đa trạng thái của Vendor")
    add_p("• Sơ đồ hoạt động: Khi khách đặt hàng thành công, đơn hàng của shop chuyển sang trạng thái `CHO_XAC_NHAN`. Vendor vào trang quản lý đơn, kiểm tra các mặt hàng khách đặt, bấm 'Xác nhận đơn' -> chuyển sang `DANG_CHUAN_BI` -> bấm 'Giao cho đơn vị vận chuyển' -> `DANG_GIAO` -> `GIAO_THANH_CONG`. Nếu có sự cố hết hàng đột xuất, Vendor có thể chọn 'Hủy đơn' kèm theo lý do cụ thể, hệ thống sẽ tự động hoàn trả số lượng tồn kho.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `OrderController.java`: Chứa các phương thức xử lý chuyển trạng thái đơn hàng phía người bán.")
    add_p("  - `InventoryService.java`: Thực thi việc cộng hoàn lại tồn kho khi đơn bị hủy.")

    add_image_with_caption("stitch_bookstore_e_commerce_admin_interface/stitch_bookstore_e_commerce_admin_interface/b_ng_i_u_khi_n_qu_n_l_n_h_ng_the4bookstore/screen.png",
                           "Hình 3.7: Giao diện Bảng điều khiển Quản lý Đơn hàng của Vendor (Thiết kế AI Stitch - Quang Hòa)")

    add_prompt_box(
'''"Viết một State Machine quản lý trạng thái đơn hàng thương mại điện tử bằng Java Spring Boot. 
Các trạng thái: CHO_XAC_NHAN -> DANG_CHUAN_BI -> DANG_GIAO -> HOAN_TAT hoặc HUY_DON. 
Đảm bảo khi Vendor chuyển trạng thái Hủy đơn thì hệ thống kích hoạt transaction hoàn trả tồn kho tự động 
và ghi log lịch sử thay đổi trạng thái kèm timestamp."''',
"Prompt AI tiêu biểu dùng để thiết kế luồng xử lý đơn hàng đa trạng thái (Quang Hòa)"
    )

    # 3.8
    add_h3("3.8. Chức năng Quản lý Khuyến mãi, Voucher riêng của Gian hàng & Báo cáo")
    add_p("• Sơ đồ hoạt động: Gian hàng có thể chủ động tạo các chiến dịch khuyến mãi bằng cách phát hành mã Voucher riêng của shop (Shop-level Voucher). Shop thiết lập mã code (ví dụ `KIMDONG20`), số tiền giảm cố định hoặc phần trăm giảm, đơn hàng tối thiểu và ngày hết hạn. Khách hàng chỉ có thể áp dụng mã này khi mua sách của chính gian hàng đó.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `VoucherController.java`: Xử lý thêm, sửa, kích hoạt hoặc vô hiệu hóa voucher của người bán.")

    add_image_with_caption("stitch_bookstore_e_commerce_admin_interface/stitch_bookstore_e_commerce_admin_interface/qu_n_l_khuy_n_m_i_m_gi_m_gi_the4bookstore/screen.png",
                           "Hình 3.8: Giao diện Quản lý Khuyến mãi và Mã giảm giá của Shop (Thiết kế AI Stitch - Quang Hòa)")

    # ------------------ PHẦN C: VÕ THÀNH PHÁT ------------------
    add_h2("PHẦN C: PHÂN HỆ QUẢN TRỊ VẬN HÀNH (MANAGER) & QUẢN TRỊ HỆ THỐNG (ADMIN)")
    add_p("Sinh viên phụ trách: Võ Thành Phát - MSSV: 24110300 (Nhóm trưởng)", italic=True)

    add_image_with_caption("DOCUMENT/images_report/diagram_admin_flow.png", 
                           "Hình 3.9: Sơ đồ quy trình quản trị, phân quyền và duyệt shop (Thành Phát phụ trách)")

    # 3.9
    add_h3("3.9. Chức năng Bảng điều khiển Quản trị toàn diện (Admin & Manager Dashboard)")
    add_p("• Sơ đồ hoạt động: Khi Quản trị viên hoặc Quản lý đăng nhập, hệ thống điều hướng vào Dashboard trung tâm (`/admin` hoặc `/manager`). Màn hình tổng hợp các chỉ số KPI then chốt theo thời gian thực: Tổng doanh thu toàn sàn, Tổng số đơn hàng thành công, Số lượng sách đang lưu hành, Số gian hàng đang hoạt động, cùng biểu đồ tăng trưởng doanh số và danh sách đơn hàng mới nhất cần chú ý.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `AdminController.java`: Điều phối dữ liệu thống kê tổng thể cho trang chủ quản trị.")
    add_p("  - `ReportService.java`: Thực thi các truy vấn tổng hợp phức tạp (GROUP BY, SUM, COUNT) để xuất dữ liệu biểu đồ.")

    add_image_with_caption("stitch_bookstore_e_commerce_admin_interface/stitch_bookstore_e_commerce_admin_interface/b_ng_i_u_khi_n_qu_n_tr_the4bookstore/screen.png",
                           "Hình 3.10: Giao diện Bảng điều khiển Quản trị toàn sàn (Thiết kế AI Stitch - Thành Phát)")

    add_code_block(
'''@GetMapping("/admin")
@PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
public String adminDashboard(Model model) {
    DashboardStatsDTO stats = reportService.getOverallDashboardStats();
    List<RevenueByMonthDTO> revenueChart = reportService.getMonthlyRevenue(Year.now().getValue());
    List<Order> recentOrders = orderService.getTop10RecentOrders();
    
    model.addAttribute("stats", stats);
    model.addAttribute("revenueChart", revenueChart);
    model.addAttribute("recentOrders", recentOrders);
    return "admin/dashboard";
}''', "AdminController.java - Tổng hợp chỉ số Dashboard toàn sàn"
    )

    add_prompt_box(
'''"Thiết kế Controller và Service trong Spring Boot để truy vấn và tính toán các chỉ số Dashboard quản trị: 
Tổng doanh thu, Tổng đơn hàng hôm nay, Tỷ lệ đơn thành công, Số gian hàng mới chờ duyệt. 
Dữ liệu biểu đồ doanh thu theo 12 tháng trả về dạng JSON để render trực tiếp lên Chart.js trên giao diện Thymeleaf."''',
"Prompt AI tiêu biểu dùng để xây dựng Dashboard quản trị (Thành Phát)"
    )

    # 3.10
    add_h3("3.10. Chức năng Thẩm định, Phê duyệt hoặc Từ chối đơn đăng ký Gian hàng Shop")
    add_p("• Sơ đồ hoạt động: Quản lý xem danh sách các đơn đăng ký mở shop đang chờ duyệt (`/admin/vendors/applications`). Người quản lý thẩm định hồ sơ: tên nhà sách, địa chỉ kho, giấy phép đăng ký kinh doanh. Nếu hợp lệ, bấm 'Phê duyệt' -> hệ thống tự động cập nhật trạng thái shop thành `APPROVED` và nâng quyền tài khoản chủ shop thành `ROLE_VENDOR`. Nếu từ chối, hệ thống xóa bỏ dữ liệu shop rác và gửi thông báo phản hồi lý do cho người nộp đơn.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `AdminController.java`: Cung cấp API duyệt (`/admin/vendor-applications/{id}/approve`) và từ chối (`/admin/vendor-applications/{id}/reject`).")
    add_p("  - `UserService.java`: Cập nhật vai trò người dùng trong CSDL và làm mới phiên phân quyền.")

    add_code_block(
'''@PostMapping("/admin/vendor-applications/{id}/approve")
@PreAuthorize("hasRole('ADMIN')")
public String approveVendor(@PathVariable Long id, RedirectAttributes ra) {
    VendorApplication app = vendorApplicationRepository.findById(id).orElseThrow();
    Shop shop = app.getShop();
    shop.setStatus(ShopStatus.APPROVED);
    shopRepository.save(shop);
    
    // Nâng quyền tài khoản chủ shop thành ROLE_VENDOR
    User owner = shop.getOwner();
    Role vendorRole = roleRepository.findByName("ROLE_VENDOR");
    owner.getRoles().add(vendorRole);
    userRepository.save(owner);
    
    ra.addFlashAttribute("successMessage", "Đã phê duyệt gian hàng " + shop.getName() + " thành công!");
    return "redirect:/admin/vendor-applications";
}''', "AdminController.java - Phê duyệt hồ sơ gian hàng & cấp quyền VENDOR"
    )

    # 3.11
    add_h3("3.11. Chức năng Quản lý Người dùng & Phân quyền kiểm soát truy cập (RBAC)")
    add_p("• Sơ đồ hoạt động: Màn hình quản lý người dùng cho phép Quản trị viên tra cứu toàn bộ danh sách tài khoản theo tên, email, số điện thoại hoặc vai trò. Quản trị viên có toàn quyền kích hoạt, khóa tài khoản tạm thời nếu phát hiện vi phạm, cấp lại mật khẩu hoặc điều chỉnh phân quyền vai trò (Admin, Manager, Vendor, KhachHang).")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `AdminUserController.java`: Xử lý thêm, sửa, đổi mật khẩu, kích hoạt/khóa tài khoản người dùng.")
    add_p("  - `UserSecurityService.java`: Bảo vệ ngăn chặn hành vi tự khóa chính tài khoản Admin đang đăng nhập.")

    add_image_with_caption("stitch_bookstore_e_commerce_admin_interface/stitch_bookstore_e_commerce_admin_interface/qu_n_l_ng_i_d_ng_ph_n_quy_n_the4bookstore/screen.png",
                           "Hình 3.11: Giao diện Quản lý Người dùng & Phân quyền RBAC (Thiết kế AI Stitch - Thành Phát)")

    add_prompt_box(
'''"Tạo giao diện quản lý người dùng với Spring Boot Thymeleaf và Tailwind CSS: 
Bảng danh sách có phân trang, thanh tìm kiếm realtime theo tên/email, lọc theo vai trò (Dropdown Role). 
Mỗi dòng có Badge trạng thái màu sắc (Hoạt động màu xanh, Đã khóa màu đỏ) 
và các nút thao tác: Sửa quyền, Khóa/Mở khóa có xác nhận Modal Popup."''',
"Prompt AI tiêu biểu dùng để tạo màn hình Quản lý người dùng RBAC (Thành Phát)"
    )

    # 3.12
    add_h3("3.12. Chức năng Quản lý Dữ liệu nền & Xử lý Khiếu nại vận hành")
    add_p("• Sơ đồ hoạt động: Quản lý vận hành (Manager) chịu trách nhiệm chuẩn hóa danh mục sách toàn sàn (Thể loại cấp 1, Thể loại con cấp 2, Danh mục Tác giả, Nhà xuất bản), ngăn chặn việc các shop tạo danh mục trùng lặp gây rối loạn bộ lọc tìm kiếm. Đồng thời, phân hệ tiếp nhận các khiếu nại tranh chấp đơn hàng giữa khách mua và gian hàng để phân xử công bằng.")
    add_p("• Tác dụng các file code chính:")
    add_p("  - `AdminImportExportController.java`: Quản lý danh mục ngành hàng, tác giả, nhà xuất bản.")
    add_p("  - `ManagerDisputeController.java`: Xử lý đơn khiếu nại đơn hàng, xem bằng chứng và ra quyết định hoàn tiền hoặc tiếp tục giao.")

    add_image_with_caption("stitch_bookstore_e_commerce_admin_interface/stitch_bookstore_e_commerce_admin_interface/qu_n_l_danh_m_c_d_li_u_n_n_the4bookstore/screen.png",
                           "Hình 3.12: Giao diện Quản lý Danh mục & Dữ liệu nền của Manager (Thiết kế AI Stitch - Thành Phát)")

    doc.add_page_break()

    # ==================== CHƯƠNG 4 ====================
    add_h1("CHƯƠNG 4: DANH SÁCH PROMPT AI VÀ QUY TRÌNH PHỐI HỢP CÙNG AI (AI-ASSISTED WORKFLOW)")

    add_h2("4.1. Quy trình kết hợp Human-in-the-loop cùng AI trong chu trình SDLC")
    add_p("Trong dự án TheFourBookStore, nhóm không để AI sinh code một cách thụ động, mà áp dụng phương pháp phối hợp Human-in-the-loop (Con người định hướng - AI hỗ trợ tăng tốc - Con người kiểm định):")
    add_p("• Giai đoạn 1 (Ý tưởng & Nghiệp vụ): Con người xác định bài toán sàn sách đa gian hàng và các quy tắc đặc thù (34 tỉnh thành, voucher sàn/shop). AI hỗ trợ xây dựng kịch bản Use Case và kịch bản demo (KICHBAN.md).")
    add_p("• Giai đoạn 2 (Thiết kế CSDL & Giao diện): AI hỗ trợ sinh mã DDL T-SQL, Stored Procedures và sinh toàn bộ Design System HTML/Tailwind thông qua công cụ AI Stitch. Con người rà soát các ràng buộc khóa ngoại và tối ưu chỉ mục (Indexes).")
    add_p("• Giai đoạn 3 (Cài đặt mã nguồn): Sử dụng các câu lệnh Prompt có cấu trúc (Structured Prompting) để sinh các Controller, Service, DTO. Sinh viên trực tiếp chỉnh sửa các điểm nghẽn logic, đảm bảo tính đồng bộ Entity.")
    add_p("• Giai đoạn 4 (Fix bug & Tối ưu hóa): Khi xảy ra lỗi (như lỗi gửi OTP, lỗi truy vấn tồn kho, tối ưu cước vận chuyển), nhóm đưa log lỗi vào Prompt để AI đề xuất giải pháp, sau đó tiến hành debug và kiểm thử thực tế.")

    add_h2("4.2. Bảng tổng hợp các câu lệnh Prompt tiêu biểu phân theo từng giai đoạn")

    table_prompts = doc.add_table(rows=7, cols=3)
    table_prompts.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_headers = ["Giai đoạn", "Mục tiêu Prompt", "Nội dung câu lệnh Prompt tiêu biểu đã sử dụng"]
    for i, h in enumerate(p_headers):
        cell = table_prompts.cell(0, i)
        set_cell_background(cell, "004C22")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    prompt_data = [
        ("1. Khảo sát & Đặc tả", "Phân tích yêu cầu sàn sách đa người bán", 
         '"Đóng vai trò là Solution Architect, hãy phân tích yêu cầu cho một sàn thương mại điện tử chuyên về sách tại Việt Nam theo mô hình Multi-vendor. Liệt kê 4 nhóm tác nhân (Khách, Vendor, Manager, Admin) và các ca sử dụng cốt lõi cần có cho đồ án Web."'),
        ("2. Thiết kế CSDL", "Sinh mã nguồn T-SQL & Stored Procedure", 
         '"Hãy viết script DDL SQL Server 2022 thiết kế bảng cho hệ thống bán sách đa gian hàng: NguoiDung, GianHang, SanPham, DonHang, ChiTietDonHang, Voucher. Viết Stored Procedure sp_TaoDonHang có sử dụng Transaction và khóa dòng kiểm tra số lượng tồn kho."'),
        ("3. Thiết kế Giao diện", "Thiết kế với AI Stitch (Forest Folio)", 
         '"Create a modern and elegant bookstore e-commerce web interface with classical literary aesthetics called Forest Folio. Use deep emerald green (#004c22) and warm amber brown (#904d00) tones. Generate HTML with Tailwind CSS for Book Detail, Cart, and Admin Dashboard."'),
        ("4. Lập trình Backend", "Sinh Controller & Service Spring Boot", 
         '"Viết Spring Boot Controller và Service cho chức năng CartController và OrderController. Xử lý tính toán phí giao hàng dựa trên khoảng cách giữa tỉnh thành của Shop và khách mua, đồng thời áp dụng trừ tiền từ Voucher nếu hợp lệ."'),
        ("5. Sửa lỗi & Refactor", "Cập nhật khoảng cách 34 tỉnh & fix OTP", 
         '"Tôi đang gặp lỗi NullPointerException khi tính khoảng cách địa lý do một số tỉnh thành mới chưa có trong danh sách. Hãy cập nhật thuật toán DistanceMatrix hỗ trợ đầy đủ 34 tỉnh thành sau đợt cải cách hành chính và xử lý an toàn giá trị mặc định."'),
        ("6. Kiểm thử tự động", "Sinh kịch bản Test Cases chi tiết", 
         '"Hãy viết bảng kịch bản kiểm thử hộp đen (Black-box Test Cases) chi tiết cho chức năng Đăng ký mở Gian hàng và Xử lý đơn hàng của Vendor, gồm: Tên ca kiểm thử, Các bước thực hiện, Dữ liệu đầu vào, Kết quả mong đợi."')
    ]

    for row_idx, (phase, goal, content) in enumerate(prompt_data, start=1):
        bg = "FFFFFF" if row_idx % 2 == 1 else "F8FAFC"
        for col_idx, text in enumerate([phase, goal, content]):
            cell = table_prompts.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_borders(cell, color="CBD5E1", sz="4")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r.bold = True
            elif col_idx == 1:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)
            else:
                r.font.name = 'Consolas'

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("4.3. Đánh giá phản biện: Điểm mạnh, hạn chế của AI và vai trò của sinh viên")
    add_p("• Điểm mạnh của AI: Giúp tăng tốc độ phát triển ước tính từ 3 đến 4 lần so với lập trình thủ công. AI đặc biệt xuất sắc trong việc sinh khung mã nguồn (Boilerplate code), sinh các giao diện HTML/Tailwind bắt mắt, gợi ý cú pháp truy vấn phức tạp và viết kịch bản kiểm thử đa dạng.")
    add_p("• Hạn chế của AI: AI có xu hướng mắc lỗi 'ảo giác' (hallucination) khi làm việc với các nghiệp vụ chuyên biệt sâu; code sinh ra giữa các module đôi khi bị lệch kiểu dữ liệu hoặc thiếu sự nhất quán với thực thể Entity; AI không thể tự nhận thức được các tác động phụ về bảo mật nếu không được nhắc nhở chi tiết.")
    add_p("• Vai trò quyết định của sinh viên: Sinh viên giữ vai trò là Kiến trúc sư và Người kiểm soát chất lượng (QA). Nhóm trực tiếp thiết kế luồng dữ liệu, rà soát từng dòng code AI sinh ra, cấu hình an ninh Spring Security, thực hiện gỡ lỗi (debug) và tối ưu hóa hiệu năng truy vấn CSDL.")

    doc.add_page_break()

    # ==================== CHƯƠNG 5 ====================
    add_h1("CHƯƠNG 5: HƯỚNG DẪN CÀI ĐẶT VÀ TRIỂN KHAI HỆ THỐNG (SETUP GUIDE)")

    add_h2("5.1. Yêu cầu môi trường phần cứng và phần mềm")
    add_p("Để cài đặt và chạy thử nghiệm hệ thống TheFourBookStore, máy tính cần đáp ứng:")
    add_p("• Phần cứng: RAM tối thiểu 8GB (khuyên dùng 16GB), ổ cứng trống tối thiểu 5GB.")
    add_p("• Hệ điều hành: Windows 10/11, macOS hoặc Linux.")
    add_p("• Môi trường phát triển: Java Development Kit (JDK 17 hoặc JDK 21 trở lên).")
    add_p("• Công cụ quản lý gói: Apache Maven 3.8+ (đã tích hợp sẵn Maven Wrapper `mvnw` trong dự án).")
    add_p("• Hệ quản trị CSDL: Microsoft SQL Server 2022/2025 (hoặc MySQL Server 8.0+).")
    add_p("• Trình duyệt: Google Chrome, Microsoft Edge hoặc Mozilla Firefox phiên bản mới nhất.")

    add_h2("5.2. Hướng dẫn thiết lập Cơ sở Dữ liệu")
    add_p("Nhóm cung cấp 3 phương thức thiết lập CSDL `QL_NhaSach` rất linh hoạt (trong thư mục `DOCUMENT/scripts`):")
    add_p("Mở SQL Server Management Studio (SSMS), mở file `00_Run_All_In_Order.sql`, bật chế độ SQLCMD Mode (Menu Query -> SQLCMD Mode), rồi bấm Execute (F5). Kịch bản sẽ tự động chạy lần lượt 4 file phân quyền và dữ liệu của 4 thành viên theo đúng thứ tự ràng buộc khóa ngoại.", bold_prefix="• Cách 1 (Khuyên dùng - Master Runner): ")
    add_p("Mở file `QL_NhaSach_Full_Setup.sql` trong SSMS hoặc Azure Data Studio và bấm Execute (F5) trực tiếp mà không cần bật chế độ SQLCMD.", bold_prefix="• Cách 2 (File gộp toàn thể): ")
    add_p("Sử dụng tính năng Restore Database trong SSMS, trỏ vào file sao lưu `DOCUMENT/scripts/QL_NhaSach.bak` để phục hồi nguyên trạng toàn bộ CSDL và dữ liệu mẫu.", bold_prefix="• Cách 3 (Phục hồi từ file Backup): ")

    add_h2("5.3. Cấu hình ứng dụng Spring Boot")
    add_p("Ứng dụng cấu hình kết nối thông qua file `src/main/resources/application.properties` hoặc biến môi trường file `.env`:")

    add_code_block(
'''# Cấu hình kết nối CSDL SQL Server
spring.datasource.url=jdbc:sqlserver://localhost:1433;databaseName=QL_NhaSach;encrypt=true;trustServerCertificate=true
spring.datasource.username=the4book_user
spring.datasource.password=ChangeMe@2026
spring.datasource.driver-class-name=com.microsoft.sqlserver.jdbc.SQLServerDriver

# Cấu hình JPA & Hibernate
spring.jpa.hibernate.ddl-auto=none
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.SQLServerDialect

# Cấu hình cổng chạy ứng dụng
server.port=8080''', "application.properties - Cấu hình kết nối Database"
    )

    add_h2("5.4. Lệnh khởi chạy ứng dụng & Danh mục tài khoản thử nghiệm")
    add_p("1. Mở cửa sổ Terminal (PowerShell hoặc Command Prompt) tại thư mục gốc của dự án:")
    add_code_block("./mvnw spring-boot:run", "Lệnh khởi chạy ứng dụng bằng Maven Wrapper")
    add_p("2. Mở trình duyệt web và truy cập địa chỉ: `http://localhost:8080`")
    add_p("3. Danh mục tài khoản mẫu đã được khởi tạo sẵn trong CSDL (Mật khẩu mặc định: `123456`):")

    table_acc = doc.add_table(rows=5, cols=4)
    table_acc.alignment = WD_TABLE_ALIGNMENT.CENTER
    acc_headers = ["Vai trò (Role)", "Tên đăng nhập (Username)", "Email", "Mục đích kiểm thử"]
    for i, h in enumerate(acc_headers):
        cell = table_acc.cell(0, i)
        set_cell_background(cell, "004C22")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    acc_data = [
        ("ADMIN", "admin", "admin@the4bookstore.vn", "Toàn quyền quản trị hệ thống, người dùng, RBAC, duyệt shop"),
        ("MANAGER", "manager", "manager@the4bookstore.vn", "Xem Dashboard, quản lý danh mục dữ liệu nền, xử lý khiếu nại"),
        ("VENDOR", "vendor_kimdong\nvendor_nhanam", "kimdong@gmail.com\nnhanam@gmail.com", "Vào Seller Center quản lý kho sách, đăng bán, xử lý đơn của shop"),
        ("KHACHHANG", "phat\nkhachhang_an", "thangphatnekea21333@gmail.com\nnguyenvanan@gmail.com", "Mua sách, thêm giỏ hàng, áp mã voucher, checkout, đánh giá sách")
    ]

    for row_idx, (role, user, email, desc) in enumerate(acc_data, start=1):
        bg = "FFFFFF" if row_idx % 2 == 1 else "F8FAFC"
        for col_idx, text in enumerate([role, user, email, desc]):
            cell = table_acc.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_borders(cell, color="CBD5E1", sz="4")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9.5)
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r.bold = True
                r.font.color.rgb = RGBColor(0, 76, 34)

    doc.add_page_break()

    # ==================== CHƯƠNG 6 ====================
    add_h1("CHƯƠNG 6: KIỂM THỬ HỆ THỐNG VÀ KẾT QUẢ THỰC NGHIỆM")

    add_h2("6.1. Phương pháp kiểm thử hộp đen (Black-box Testing)")
    add_p("Hệ thống được kiểm thử theo phương pháp Kiểm thử hộp đen (Black-box Testing) dựa trên tài liệu kịch bản chi tiết `DOCUMENT/KICHBAN.md` với hơn 700 dòng kiểm thử bao phủ toàn bộ 4 phân hệ. Các ca kiểm thử tập trung vào tính đúng đắn của nghiệp vụ, tính toàn vẹn của dữ liệu và khả năng xử lý ngoại lệ khi người dùng nhập dữ liệu sai lệch.")

    add_h2("6.2. Kịch bản kiểm thử chi tiết theo từng thành viên phụ trách")

    # Bảng test Thiện
    add_h3("Bảng 6.1: Kịch bản kiểm thử Phân hệ Khách hàng (Nguyễn Ngọc Thiện phụ trách)")
    table_test_thien = doc.add_table(rows=5, cols=5)
    table_test_thien.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Mã TC", "Tên ca kiểm thử", "Dữ liệu đầu vào", "Kết quả mong đợi", "Trạng thái"]
    for i, h in enumerate(test_headers):
        cell = table_test_thien.cell(0, i)
        set_cell_background(cell, "1D4ED8")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_thien_data = [
        ("TC_CUS_01", "Đăng ký tài khoản trùng lặp", "Username: 'admin' đã có trong DB", "Báo lỗi đỏ 'Tên đăng nhập đã tồn tại', không tạo tài khoản", "ĐẠT (PASS)"),
        ("TC_CUS_02", "Tìm kiếm sách kèm tên gian hàng", "Từ khóa: 'Kim Đồng'", "Hiển thị các sách của Kim Đồng và khối dẫn tới Storefront", "ĐẠT (PASS)"),
        ("TC_CUS_03", "Tính phí ship theo tỉnh thành", "Kho shop: Hà Nội, Khách: Cần Thơ", "Tự động tính cước liên miền: 45.000đ", "ĐẠT (PASS)"),
        ("TC_CUS_04", "Áp dụng mã giảm giá không đủ min", "Mã giảm 50k cho đơn từ 200k, giỏ hàng 150k", "Báo lỗi 'Đơn hàng chưa đạt giá trị tối thiểu'", "ĐẠT (PASS)")
    ]

    for row_idx, r_data in enumerate(test_thien_data, start=1):
        bg = "FFFFFF" if row_idx % 2 == 1 else "F8FAFC"
        for col_idx, text in enumerate(r_data):
            cell = table_test_thien.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_borders(cell, color="CBD5E1", sz="4")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx in [0, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if col_idx == 4:
                    r.bold = True
                    r.font.color.rgb = RGBColor(21, 128, 61)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Bảng test Hòa
    add_h3("Bảng 6.2: Kịch bản kiểm thử Phân hệ Kênh người bán (Bùi Quang Hòa phụ trách)")
    table_test_hoa = doc.add_table(rows=5, cols=5)
    table_test_hoa.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(test_headers):
        cell = table_test_hoa.cell(0, i)
        set_cell_background(cell, "C2410C")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_hoa_data = [
        ("TC_VEN_01", "Đăng ký mở shop thiếu giấy phép", "Bỏ trống ô giấy tờ kinh doanh", "Form chặn submit, thông báo yêu cầu bổ sung hồ sơ", "ĐẠT (PASS)"),
        ("TC_VEN_02", "Đăng bán sách mới kèm ảnh bìa", "Tên: 'Lập trình Web', giá: 120k, upload ảnh", "Sách hiển thị trong danh mục của shop và ra trang chủ", "ĐẠT (PASS)"),
        ("TC_VEN_03", "Cập nhật trạng thái đơn hàng", "Đơn mới -> Bấm Xác nhận", "Trạng thái chuyển thành 'DANG_CHUAN_BI', gửi thông báo", "ĐẠT (PASS)"),
        ("TC_VEN_04", "Hủy đơn hàng và hoàn trả tồn kho", "Shop hủy đơn sách 'Đắc Nhân Tâm' (sl: 2)", "Tồn kho sách tự động cộng trả lại 2 cuốn trong DB", "ĐẠT (PASS)")
    ]

    for row_idx, r_data in enumerate(test_hoa_data, start=1):
        bg = "FFFFFF" if row_idx % 2 == 1 else "F8FAFC"
        for col_idx, text in enumerate(r_data):
            cell = table_test_hoa.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_borders(cell, color="CBD5E1", sz="4")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx in [0, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if col_idx == 4:
                    r.bold = True
                    r.font.color.rgb = RGBColor(21, 128, 61)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Bảng test Phát
    add_h3("Bảng 6.3: Kịch bản kiểm thử Phân hệ Manager & Admin (Võ Thành Phát phụ trách)")
    table_test_phat = doc.add_table(rows=5, cols=5)
    table_test_phat.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(test_headers):
        cell = table_test_phat.cell(0, i)
        set_cell_background(cell, "15803D")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_phat_data = [
        ("TC_ADM_01", "Duyệt hồ sơ gian hàng mới", "Bấm 'Phê duyệt' shop 'Sách Trẻ'", "Shop chuyển APPROVED, tài khoản chủ shop nhận quyền VENDOR", "ĐẠT (PASS)"),
        ("TC_ADM_02", "Từ chối hồ sơ gian hàng không hợp lệ", "Bấm 'Từ chối' kèm lý do 'Thiếu GPKD'", "Hồ sơ shop được xóa sạch, không để lại rác trong CSDL", "ĐẠT (PASS)"),
        ("TC_ADM_03", "Khóa tài khoản người dùng vi phạm", "Admin bấm khóa tài khoản spam", "Tài khoản bị khóa ngay lập tức, không thể login", "ĐẠT (PASS)"),
        ("TC_ADM_04", "Hiển thị thống kê Dashboard tổng thể", "Truy cập `/admin` bằng quyền ADMIN", "Render đầy đủ 4 thẻ KPI doanh thu và biểu đồ Chart", "ĐẠT (PASS)")
    ]

    for row_idx, r_data in enumerate(test_phat_data, start=1):
        bg = "FFFFFF" if row_idx % 2 == 1 else "F8FAFC"
        for col_idx, text in enumerate(r_data):
            cell = table_test_phat.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_borders(cell, color="CBD5E1", sz="4")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            if col_idx in [0, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if col_idx == 4:
                    r.bold = True
                    r.font.color.rgb = RGBColor(21, 128, 61)

    add_h2("6.3. Đánh giá độ ổn định và kết quả thực nghiệm")
    add_p("Qua các vòng kiểm thử thực tế trên môi trường máy chủ cục bộ, hệ thống TheFourBookStore hoạt động rất ổn định:")
    add_p("• Tốc độ phản hồi trung bình các trang xem sản phẩm và trang chủ dưới 350ms nhờ việc tối ưu hóa chỉ mục (Indexes) trên các cột khóa ngoại và cột tìm kiếm thường xuyên.")
    add_p("• Tính toàn vẹn của dữ liệu giao dịch được đảm bảo tuyệt đối, không xảy ra hiện tượng bán vượt quá số lượng tồn kho (over-selling) nhờ các Stored Procedure trừ kho có transaction bảo vệ.")
    add_p("• Tỷ lệ các ca kiểm thử đạt kết quả thành công (Pass rate) là 100% trên các kịch bản chuẩn.")

    doc.add_page_break()

    # ==================== KẾT LUẬN & PHỤ LỤC ====================
    add_h1("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
    add_h2("Kết luận")
    add_p("Sau quá trình nghiên cứu, thiết kế và triển khai với sự đồng hành của Trí tuệ Nhân tạo, nhóm 3 thành viên đã hoàn thành xuất sắc đồ án xây dựng Sàn thương mại điện tử sách TheFourBookStore:")
    add_p("1. Về mặt học thuật và kỹ thuật: Ứng dụng thành công các kiến thức nền tảng của môn Lập trình Web và Hệ quản trị CSDL: mô hình Spring Boot MVC N-tier, Spring Security phân quyền chặt chẽ, tối ưu hóa CSDL quan hệ với Stored Procedures và xây dựng giao diện hiện đại với Thymeleaf / Tailwind.")
    add_p("2. Về mặt giải quyết bài toán thực tế: Xây dựng thành công mô hình sàn sách Đa gian hàng (Multi-vendor) với các điểm sáng nổi bật như tính cước vận chuyển chuẩn 34 tỉnh thành cải cách hành chính, quản lý Storefront độc lập và hỗ trợ voucher đa cấp.")
    add_p("3. Về mặt phương pháp làm việc cùng AI: Nhóm đã làm chủ quy trình làm việc Human-in-the-loop, biến AI thành trợ lý đắc lực trong việc sinh ý tưởng, tạo giao diện Stitch chuẩn mực, sinh code và kiểm thử, nâng cao đáng kể năng suất lập trình.")

    add_h2("Hướng phát triển trong tương lai")
    add_p("• Tích hợp cổng thanh toán trực tuyến chính thức qua cổng VNPay, MoMo hoặc ZaloPay.")
    add_p("• Ứng dụng mô hình AI Recommender System (Hệ thống gợi ý sách thông minh) dựa trên lịch sử xem và sở thích của từng độc giả.")
    add_p("• Xây dựng ứng dụng di động (Mobile App) bằng Flutter hoặc React Native kết nối qua hệ thống RESTful APIs sẵn có của Spring Boot.")

    add_h1("TÀI LIỆU THAM KHẢO")
    add_p("1. Craig Walls (2022), Spring in Action, Sixth Edition, Manning Publications.")
    add_p("2. Spring Boot Official Documentation: https://docs.spring.io/spring-boot/docs/current/reference/html/")
    add_p("3. Microsoft Learn - SQL Server Technical Documentation: https://learn.microsoft.com/en-us/sql/")
    add_p("4. Tailwind CSS Framework Documentation: https://tailwindcss.com/docs")
    add_p("5. Google Stitch AI Design System Guidelines & Component Architecture.")

    output_path = "DOCUMENT/BAO_CAO_THEFOURBOOKSTORE_CHI_TIET.docx"
    doc.save(output_path)
    print("Report docx generated successfully at: " + output_path)

if __name__ == '__main__':
    create_report()
