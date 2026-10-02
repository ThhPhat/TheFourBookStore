package vn.bookstore.the4bookstore;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;

@SpringBootApplication
@EnableCaching
public class The4BookStoreApplication {

    public static void main(String[] args) {
        SpringApplication.run(The4BookStoreApplication.class, args);
    }

}
