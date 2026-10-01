package vn.bookstore.the4bookstore.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import vn.bookstore.the4bookstore.entity.ChiTietDonHang;
import vn.bookstore.the4bookstore.entity.DonHang;
import vn.bookstore.the4bookstore.repository.DonHangRepository;
import vn.bookstore.the4bookstore.repository.SanPhamRepository;

import java.time.LocalDateTime;

@Service
public class OrderService {
    @Autowired
    private DonHangRepository donHangRepository;

    @Autowired
    private SanPhamRepository sanPhamRepository;

    public void updateStatus(Long id, String status) {
        updateStatus(id, status, null);
    }

    @Transactional
    public void updateStatus(Long id, String status, String reason) {
        DonHang dh = donHangRepository.findById(id.intValue())
            .orElseThrow(() -> new RuntimeException("Không tìm thấy đơn hàng: " + id));

        String oldStatus = dh.getTrangThai();
        dh.setTrangThai(status);

        if ("DaGiao".equals(status)) {
            if (dh.getNgayHoanThanh() == null) {
                dh.setNgayHoanThanh(LocalDateTime.now());
            }
        } else if ("DaXacNhan".equals(status)) {
            if (dh.getNgayXacNhan() == null) {
                dh.setNgayXacNhan(LocalDateTime.now());
            }
        } else if ("DaHuy".equals(status) || "Huy".equals(status)) {
            if (reason != null && !reason.isBlank()) {
                dh.setLyDoHuy(reason);
            }
            // Hoàn lại số lượng tồn kho nếu đơn chuyển từ trạng thái chưa hủy sang hủy
            if (!"DaHuy".equalsIgnoreCase(oldStatus) && !"Huy".equalsIgnoreCase(oldStatus) && dh.getChiTietDonHangs() != null) {
                for (ChiTietDonHang ct : dh.getChiTietDonHangs()) {
                    if (ct.getSanPham() != null && ct.getSoLuong() != null) {
                        sanPhamRepository.increaseStock(ct.getSanPham().getMaSP(), ct.getSoLuong());
                    }
                }
            }
        }
        donHangRepository.save(dh);
    }
}

