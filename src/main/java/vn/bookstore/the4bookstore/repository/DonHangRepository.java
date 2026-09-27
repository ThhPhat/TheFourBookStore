package vn.bookstore.the4bookstore.repository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import vn.bookstore.the4bookstore.entity.DonHang;

import java.time.LocalDateTime;

@Repository
public interface DonHangRepository extends JpaRepository<DonHang, Integer> {

    @Query("SELECT SUM(dh.tongTien) FROM DonHang dh WHERE dh.trangThai = 'DaGiao' AND dh.ngayHoanThanh >= :startDate AND dh.ngayHoanThanh < :endDate")
    Long getRevenueByDateRange(@Param("startDate") LocalDateTime startDate, @Param("endDate") LocalDateTime endDate);

    @Query("SELECT COUNT(dh) FROM DonHang dh WHERE dh.trangThai = 'DaGiao' AND dh.ngayHoanThanh >= :startDate AND dh.ngayHoanThanh < :endDate")
    Long getOrderCountByDateRange(@Param("startDate") LocalDateTime startDate, @Param("endDate") LocalDateTime endDate);

    java.util.List<DonHang> findByKhachHangOrderByNgayDatDesc(vn.bookstore.the4bookstore.entity.KhachHang khachHang);

    org.springframework.data.domain.Page<DonHang> findAllByOrderByNgayDatDesc(org.springframework.data.domain.Pageable pageable);
    org.springframework.data.domain.Page<DonHang> findByTrangThaiOrderByNgayDatDesc(String trangThai, org.springframework.data.domain.Pageable pageable);
    org.springframework.data.domain.Page<DonHang> findByTrangThaiInOrderByNgayDatDesc(java.util.List<String> trangThaiList, org.springframework.data.domain.Pageable pageable);

    Long countByKhachHang(vn.bookstore.the4bookstore.entity.KhachHang khachHang);

    Long countByKhachHangAndTrangThai(vn.bookstore.the4bookstore.entity.KhachHang khachHang, String trangThai);
    
    Long countByTrangThai(String trangThai);
    Long countByTrangThaiIn(java.util.List<String> trangThaiList);

    Long countByNgayDatBetween(LocalDateTime startDate, LocalDateTime endDate);
}
