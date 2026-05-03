package com.planting.common;

import com.baomidou.mybatisplus.core.metadata.IPage;
import lombok.Data;

import java.io.Serializable;
import java.util.List;

/**
 * 分页结果类
 * @param <T> 数据类型
 */
@Data
public class PageResult<T> implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 总记录数
     */
    private Long total;

    /**
     * 记录列表
     */
    private List<T> records;

    /**
     * 当前页码
     */
    private Long current;

    /**
     * 每页数量
     */
    private Long size;

    /**
     * 总页数
     */
    private Long pages;

    public PageResult() {
    }

    public PageResult(Long total, List<T> records) {
        this.total = total;
        this.records = records;
    }

    public PageResult(Long total, List<T> records, Long current, Long size, Long pages) {
        this.total = total;
        this.records = records;
        this.current = current;
        this.size = size;
        this.pages = pages;
    }

    /**
     * 从MyBatis-Plus分页结果转换
     * @param page MyBatis-Plus分页结果
     * @param <T> 数据类型
     * @return PageResult
     */
    public static <T> PageResult<T> of(IPage<T> page) {
        PageResult<T> pageResult = new PageResult<>();
        pageResult.setTotal(page.getTotal());
        pageResult.setRecords(page.getRecords());
        pageResult.setCurrent(page.getCurrent());
        pageResult.setSize(page.getSize());
        pageResult.setPages(page.getPages());
        return pageResult;
    }

    /**
     * 构建分页结果
     * @param total 总记录数
     * @param records 记录列表
     * @param current 当前页码
     * @param size 每页数量
     * @param <T> 数据类型
     * @return PageResult
     */
    public static <T> PageResult<T> build(Long total, List<T> records, Long current, Long size) {
        PageResult<T> pageResult = new PageResult<>();
        pageResult.setTotal(total);
        pageResult.setRecords(records);
        pageResult.setCurrent(current);
        pageResult.setSize(size);
        pageResult.setPages((total + size - 1) / size);
        return pageResult;
    }

    /**
     * 构建分页结果(简化版)
     * @param total 总记录数
     * @param records 记录列表
     * @param <T> 数据类型
     * @return PageResult
     */
    public static <T> PageResult<T> of(Long total, List<T> records) {
        PageResult<T> pageResult = new PageResult<>();
        pageResult.setTotal(total);
        pageResult.setRecords(records);
        pageResult.setCurrent(1L);
        pageResult.setSize(records.size() > 0 ? (long) records.size() : 10L);
        pageResult.setPages((total + pageResult.getSize() - 1) / pageResult.getSize());
        return pageResult;
    }
}
