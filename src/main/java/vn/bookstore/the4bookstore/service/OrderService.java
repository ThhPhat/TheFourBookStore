package vn.bookstore.the4bookstore.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import vn.bookstore.the4bookstore.entity.DonHang;
import vn.bookstore.the4bookstore.repository.DonHangRepository;

@Service
public class OrderService {
    @Autowired
    private DonHangRepository donHangRepository;

    public void updateStatus(Long id, String status) {
        DonHang dh = donHangRepository.findById(id.intValue())
            .orElseThrow(() -> new RuntimeException("Không tìm thấy đơn hàng: " + id));
        dh.setTrangThai(status);
        if ("DaGiao".equals(status)) {
            dh.setNgayHoanThanh(java.time.LocalDateTime.now());
        } else if ("DaXacNhan".equals(status)) {
            if (dh.getNgayXacNhan() == null) {
                dh.setNgayXacNhan(java.time.LocalDateTime.now());
            }
        }
        donHangRepository.save(dh);
    }
}
