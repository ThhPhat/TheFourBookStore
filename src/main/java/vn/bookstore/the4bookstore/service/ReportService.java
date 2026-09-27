package vn.bookstore.the4bookstore.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import vn.bookstore.the4bookstore.dto.MonthlyRevenueDTO;
import vn.bookstore.the4bookstore.dto.TopSellingBookDTO;
import vn.bookstore.the4bookstore.repository.ChiTietDonHangRepository;
import vn.bookstore.the4bookstore.repository.DonHangRepository;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.Query;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

@Service
public class ReportService {

    @Autowired
    private DonHangRepository donHangRepository;

    @Autowired
    private ChiTietDonHangRepository chiTietDonHangRepository;

    @PersistenceContext
    private EntityManager entityManager;

    public BigDecimal getRevenueByDate(LocalDate date) {
        LocalDateTime startOfDay = date.atStartOfDay();
        LocalDateTime endOfDay = date.plusDays(1).atStartOfDay();

        Long revenue = donHangRepository.getRevenueByDateRange(startOfDay, endOfDay);
        return revenue != null ? new BigDecimal(revenue) : BigDecimal.ZERO;
    }

    public List<MonthlyRevenueDTO> getRevenueByMonth() {
        String sql = "SELECT YEAR(dh.ngay_hoan_thanh) as nam, MONTH(dh.ngay_hoan_thanh) as thang, SUM(dh.tong_tien) as doanh_thu " +
                     "FROM don_hang dh " +
                     "WHERE dh.trang_thai = 'DaGiao' AND dh.ngay_hoan_thanh IS NOT NULL " +
                     "GROUP BY YEAR(dh.ngay_hoan_thanh), MONTH(dh.ngay_hoan_thanh) " +
                     "ORDER BY nam DESC, thang DESC " +
                     "LIMIT 12";

        Query query = entityManager.createNativeQuery(sql);
        List<Object[]> results = query.getResultList();

        List<MonthlyRevenueDTO> dtos = new ArrayList<>();
        for (Object[] row : results) {
            Integer year = ((Number) row[0]).intValue();
            Integer month = ((Number) row[1]).intValue();
            BigDecimal revenue = new BigDecimal(((Number) row[2]).longValue());
            String monthStr = String.format("%04d-%02d", year, month);
            dtos.add(new MonthlyRevenueDTO(monthStr, revenue));
        }
        return dtos;
    }

    public List<TopSellingBookDTO> getTopSellingBooks() {
        String sql = "SELECT sp.masp, sp.tensp, SUM(ct.so_luong) as so_luong_ban, sp.gia_ban " +
                     "FROM chi_tiet_don_hang ct " +
                     "JOIN don_hang dh ON ct.madh = dh.madh " +
                     "JOIN san_pham sp ON ct.masp = sp.masp " +
                     "WHERE dh.trang_thai = 'DaGiao' " +
                     "GROUP BY sp.masp, sp.tensp, sp.gia_ban " +
                     "ORDER BY so_luong_ban DESC " +
                     "LIMIT 10";

        Query query = entityManager.createNativeQuery(sql);
        List<Object[]> results = query.getResultList();

        List<TopSellingBookDTO> dtos = new ArrayList<>();
        for (Object[] row : results) {
            Long maSP = ((Number) row[0]).longValue();
            String tenSP = (String) row[1];
            Long soLuongBan = ((Number) row[2]).longValue();
            Integer giaBan = row[3] != null ? ((Number) row[3]).intValue() : null;
            dtos.add(new TopSellingBookDTO(maSP, tenSP, soLuongBan, giaBan));
        }
        return dtos;
    }

    public Long getThisMonthOrderCount() {
        LocalDateTime startOfMonth = LocalDate.now().withDayOfMonth(1).atStartOfDay();
        LocalDateTime nextMonth = startOfMonth.plusMonths(1);

        Long count = donHangRepository.getOrderCountByDateRange(startOfMonth, nextMonth);
        return count != null ? count : 0L;
    }

    public Long getTotalBooksSold() {
        Long total = chiTietDonHangRepository.getTotalBooksSold();
        return total != null ? total : 0L;
    }
}
