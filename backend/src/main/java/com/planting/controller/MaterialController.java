package com.planting.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.common.ApiResponse;
import com.planting.entity.Material;
import com.planting.service.MaterialService;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;

/**
 * 农资管理控制器
 */
@Slf4j
@RestController
@RequestMapping("/materials")
public class MaterialController {

    @Autowired
    private MaterialService materialService;

    /**
     * 获取农资列表
     */
    @GetMapping
    @PreAuthorize("hasAuthority('material:read')")
    public ApiResponse<Page<Material>> listMaterials(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) String type) {

        Page<Material> materialPage = materialService.listMaterials(page, size, type);
        return ApiResponse.success(materialPage);
    }

    /**
     * 获取农资详情
     */
    @GetMapping("/{id}")
    @PreAuthorize("hasAuthority('material:read')")
    public ApiResponse<Material> getMaterialById(@PathVariable Long id) {
        Material material = materialService.getById(id);
        if (material == null) {
            return ApiResponse.error("农资不存在");
        }
        return ApiResponse.success(material);
    }

    /**
     * 农资入库
     */
    @PutMapping("/{id}/stock-in")
    @PreAuthorize("hasAuthority('material:write')")
    public ApiResponse<Material> stockIn(
            @PathVariable Long id,
            @RequestParam BigDecimal quantity,
            @RequestParam(required = false) String remark) {

        Material material = materialService.stockIn(id, quantity, remark);
        return ApiResponse.success(material);
    }
}
