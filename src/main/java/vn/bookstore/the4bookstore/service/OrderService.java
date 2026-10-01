package vn.bookstore.the4bookstore.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import vn.bookstore.the4bookstore.entity.ChiTietDonHang;
import vn.bookstore.the4bookstore.entity.DonHang;
import vn.bookstore.the4bookstore.repository.DonHangRepository;
import vn.bookstore.the4bookstore.repository.SanPhamRepository;

@Service
public class OrderService {
    @Autowired
    private DonHangRepository donHangRepository;

    @Autowired
    private SanPhamRepository sanPhamRepository;

    @Transactional
    public void updateStatus(Long id, String status) {
        DonHang dh = donHangRepository.findById(id.intValue())
            .orElseThrow(() -> new RuntimeException("Không tìm thấy đơn hàng: " + id));

        String oldStatus = dh.getTrangThai();
        dh.setTrangThai(status);

        // Nếu trạng thái chuyển sang Đã hủy và trước đó chưa bị hủy thì hoàn lại tồn kho
        if (("DaHuy".equalsIgnoreCase(status) || "Huy".equalsIgnoreCase(status))
                && !"DaHuy".equalsIgnoreCase(oldStatus) && !"Huy".equalsIgnoreCase(oldStatus)) {
            if (dh.getChiTietDonHangs() != null) {
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
