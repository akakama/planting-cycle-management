package com.planting;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.validation.ValidationAutoConfiguration;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * 智能种植周期管理系统应用主类
 */
@SpringBootApplication(exclude = {ValidationAutoConfiguration.class})
@MapperScan("com.planting.mapper")
@EnableCaching
@EnableAsync
public class PlantingApplication {

    public static void main(String[] args) {
        SpringApplication.run(PlantingApplication.class, args);
        System.out.println("========================================");
        System.out.println("智能种植周期管理系统后端启动成功!");
        System.out.println("API文档地址: http://localhost:8080/api/doc.html");
        System.out.println("========================================");
    }
}
