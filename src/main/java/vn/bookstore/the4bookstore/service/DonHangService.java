package vn.bookstore.the4bookstore.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import vn.bookstore.the4bookstore.entity.*;
import vn.bookstore.the4bookstore.repository.*;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class DonHangService {

    private final DonHangRepository donHangRepository;
    private final ChiTietDonHangRepository chiTietDonHangRepository;
    private final SanPhamRepository sanPhamRepository;
    private final ThanhToanRepository thanhToanRepository;
    private final GioHangService gioHangService;
    private final KhuyenMaiRepository khuyenMaiRepository;

    public DonHangService(DonHangRepository donHangRepository,
                          ChiTietDonHangRepository chiTietDonHangRepository,
                          SanPhamRepository sanPhamRepository,
                          ThanhToanRepository thanhToanRepository,
                          GioHangService gioHangService,
                          KhuyenMaiRepository khuyenMaiRepository) {
        this.donHangRepository = donHangRepository;
        this.chiTietDonHangRepository = chiTietDonHangRepository;
        this.sanPhamRepository = sanPhamRepository;
        this.thanhToanRepository = thanhToanRepository;
        this.gioHangService = gioHangService;
        this.khuyenMaiRepository = khuyenMaiRepository;
    }

    /**
     * Tạo đơn hàng từ giỏ hàng của khách hàng (có thể chọn lọc danh sách sản phẩm cần mua và áp mã giảm giá).
     */
    @Transactional
    public DonHang createOrder(KhachHang khachHang, String diaChiGiao,
                               String soDienThoaiGiao, String phuongThuc, String ghiChu) {
        return createOrder(khachHang, diaChiGiao, soDienThoaiGiao, phuongThuc, ghiChu, null, null);
    }

    @Transactional
    public DonHang createOrder(KhachHang khachHang, String diaChiGiao,
                               String soDienThoaiGiao, String phuongThuc, String ghiChu,
                               List<Integer> selectedProductIds) {
        return createOrder(khachHang, diaChiGiao, soDienThoaiGiao, phuongThuc, ghiChu, selectedProductIds, null);
    }

    @Transactional
    public DonHang createOrder(KhachHang khachHang, String diaChiGiao,
                               String soDienThoaiGiao, String phuongThuc, String ghiChu,
                               List<Integer> selectedProductIds,
                               String maVoucher) {

        // 1. Lấy giỏ hàng
        List<ChiTietGioHang> allCartItems = gioHangService.getCartItems(khachHang);
        if (allCartItems.isEmpty()) {
            throw new RuntimeException("Giỏ hàng trống, không thể đặt hàng!");
        }

        // Lọc theo các sản phẩm được tích chọn (nếu có chỉ định)
        List<ChiTietGioHang> cartItems;
        if (selectedProductIds != null && !selectedProductIds.isEmpty()) {
            cartItems = allCartItems.stream()
                    .filter(ct -> selectedProductIds.contains(ct.getSanPham().getMaSP()))
                    .toList();
        } else {
            cartItems = allCartItems;
        }

        if (cartItems.isEmpty()) {
            throw new RuntimeException("Vui lòng chọn ít nhất một sản phẩm để đặt hàng!");
        }

        // 2. Kiểm tra tồn kho
        for (ChiTietGioHang ct : cartItems) {
            SanPham sp = ct.getSanPham();
            if (sp.getSoLuongTon() < ct.getSoLuong()) {
                throw new RuntimeException("Sản phẩm \"" + sp.getTenSP() + "\" chỉ còn " 
                        + sp.getSoLuongTon() + " cuốn trong kho!");
            }
        }

        // 3. Tạo đơn hàng
        DonHang donHang = new DonHang();
        donHang.setKhachHang(khachHang);
        donHang.setNgayDat(LocalDateTime.now());
        donHang.setDiaChiGiao(diaChiGiao);
        donHang.setSoDienThoaiGiao(soDienThoaiGiao);
        donHang.setTrangThai("ChoXuLy");
        donHang.setTienGiam(0);

        // Lưu đơn hàng trước để lấy maDH
        donHang = donHangRepository.save(donHang);

        // 4. Tạo chi tiết đơn hàng và tính tổng tiền
        int tongTien = 0;
        List<ChiTietDonHang> chiTietList = new ArrayList<>();

        for (ChiTietGioHang ctGH : cartItems) {
            SanPham sp = ctGH.getSanPham();

            ChiTietDonHang ctDH = new ChiTietDonHang();
            ctDH.setDonHang(donHang);
            ctDH.setSanPham(sp);
            ctDH.setSoLuong(ctGH.getSoLuong());
            ctDH.setDonGia(sp.getGiaBan());

            chiTietDonHangRepository.save(ctDH);
            chiTietList.add(ctDH);

            // 5. Trừ tồn kho
            sp.setSoLuongTon(sp.getSoLuongTon() - ctGH.getSoLuong());
            sanPhamRepository.save(sp);

            tongTien += sp.getGiaBan() * ctGH.getSoLuong();
        }

        // 6. Xử lý giảm giá từ mã khuyến mãi (nếu có)
        int tienGiam = 0;
        KhuyenMai khuyenMai = null;
        if (maVoucher != null && !maVoucher.isBlank()) {
            Optional<KhuyenMai> kmOpt = khuyenMaiRepository.findByMaCode(maVoucher.trim());
            if (kmOpt.isPresent() && "HoatDong".equalsIgnoreCase(kmOpt.get().getTrangThai())) {
                khuyenMai = kmOpt.get();
                if ("PhanTram".equalsIgnoreCase(khuyenMai.getLoaiGiam())) {
                    tienGiam = (int) Math.round(tongTien * (khuyenMai.getGiaTriGiam() / 100.0));
                    if (khuyenMai.getGiamToiDa() != null && tienGiam > khuyenMai.getGiamToiDa()) {
                        tienGiam = khuyenMai.getGiamToiDa();
                    }
                } else {
                    tienGiam = khuyenMai.getGiaTriGiam();
                }
                khuyenMai.setSoLuongDaDung(khuyenMai.getSoLuongDaDung() != null ? khuyenMai.getSoLuongDaDung() + 1 : 1);
                khuyenMaiRepository.save(khuyenMai);
            } else if ("THE4BOOK15".equalsIgnoreCase(maVoucher.trim()) || "BOOK15".equalsIgnoreCase(maVoucher.trim()) || "SALE15".equalsIgnoreCase(maVoucher.trim())) {
                tienGiam = (int) Math.round(tongTien * 0.15);
            }
        }

        int finalTotal = Math.max(0, tongTien - tienGiam);
        donHang.setTongTien(finalTotal);
        donHang.setTienGiam(tienGiam);
        donHang.setKhuyenMai(khuyenMai);
        donHang.setChiTietDonHangs(chiTietList);
        donHang = donHangRepository.save(donHang);

        // 7. Tạo bản ghi thanh toán
        ThanhToan thanhToan = new ThanhToan();
        thanhToan.setDonHang(donHang);
        thanhToan.setPhuongThuc(phuongThuc != null ? phuongThuc : "COD");
        thanhToan.setTrangThai("ChoThanhToan");
        thanhToan.setSoTien(finalTotal);
        thanhToan.setNoiDung("Thanh toán đơn hàng #" + donHang.getMaDH());
        thanhToanRepository.save(thanhToan);

        // 8. Xóa các món đã đặt khỏi giỏ hàng
        for (ChiTietGioHang ctGH : cartItems) {
            gioHangService.removeFromCart(khachHang, ctGH.getSanPham().getMaSP());
        }

        return donHang;
    }

    /**
     * Lấy danh sách đơn hàng của khách hàng, sắp xếp theo ngày đặt giảm dần
     */
    public List<DonHang> getOrdersByKhachHang(KhachHang khachHang) {
        return donHangRepository.findByKhachHangOrderByNgayDatDesc(khachHang);
    }

    /**
     * Lấy đơn hàng theo ID
     */
    public DonHang getOrderById(Integer maDH) {
        return donHangRepository.findById(maDH)
                .orElseThrow(() -> new RuntimeException("Không tìm thấy đơn hàng: " + maDH));
    }

    /**
     * Hủy đơn hàng (chỉ khi trạng thái là ChoXuLy).
     * Hoàn lại số lượng tồn kho.
     */
    @Transactional
    public void cancelOrder(Integer maDH, KhachHang khachHang, String lyDoHuy) {
        DonHang donHang = donHangRepository.findById(maDH)
                .orElseThrow(() -> new RuntimeException("Không tìm thấy đơn hàng: " + maDH));

        // Kiểm tra quyền sở hữu
        if (!donHang.getKhachHang().getMaKH().equals(khachHang.getMaKH())) {
            throw new RuntimeException("Bạn không có quyền hủy đơn hàng này!");
        }

        // Chỉ cho phép hủy khi trạng thái là ChoXuLy
        if (!"ChoXuLy".equals(donHang.getTrangThai())) {
            throw new RuntimeException("Chỉ có thể hủy đơn hàng ở trạng thái 'Chờ xử lý'!");
        }

        // Hoàn lại tồn kho
        if (donHang.getChiTietDonHangs() != null) {
            for (ChiTietDonHang ct : donHang.getChiTietDonHangs()) {
                SanPham sp = ct.getSanPham();
                sp.setSoLuongTon(sp.getSoLuongTon() + ct.getSoLuong());
                sanPhamRepository.save(sp);
            }
        }

        donHang.setTrangThai("DaHuy");
        donHang.setLyDoHuy(lyDoHuy != null && !lyDoHuy.isBlank() ? lyDoHuy : "Khách hàng tự hủy");
        donHangRepository.save(donHang);
    }
}
