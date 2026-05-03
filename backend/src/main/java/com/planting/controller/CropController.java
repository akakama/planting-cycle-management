package com.planting.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.common.ApiResponse;
import com.planting.common.PageResult;
import com.planting.dto.CreateCropRequest;
import com.planting.dto.CropDTO;
import com.planting.dto.UpdateCropRequest;
import com.planting.entity.Crop;
import com.planting.service.CropService;
import com.planting.util.BeanCopyUtils;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

/**
 * 作物管理控制器
 */
@Slf4j
@RestController
@RequestMapping("/crops")
public class CropController {

    @Autowired
    private CropService cropService;

    /**
     * 获取作物列表
     */
    @GetMapping
    @PreAuthorize("hasAuthority('crop:read')")
    public ApiResponse<PageResult<CropDTO>> listCrops(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) String keyword) {

        Page<Crop> cropPage = cropService.listCrops(page, size, keyword);
        PageResult<CropDTO> pageResult = PageResult.of(
                cropPage.getTotal(),
                BeanCopyUtils.copyList(cropPage.getRecords(), CropDTO.class)
        );

        return ApiResponse.success(pageResult);
    }

    /**
     * 获取作物详情
     */
    @GetMapping("/{id}")
    @PreAuthorize("hasAuthority('crop:read')")
    public ApiResponse<CropDTO> getCropById(
            @PathVariable Long id) {

        Crop crop = cropService.getCropById(id);
        CropDTO cropDTO = new CropDTO();
        BeanUtils.copyProperties(crop, cropDTO);

        return ApiResponse.success(cropDTO);
    }

    /**
     * 添加作物
     */
    @PostMapping
    @PreAuthorize("hasAuthority('crop:write')")
    public ApiResponse<CropDTO> createCrop(@Validated @RequestBody CreateCropRequest request) {
        Crop crop = cropService.createCrop(request);

        CropDTO cropDTO = new CropDTO();
        BeanUtils.copyProperties(crop, cropDTO);

        return ApiResponse.success(cropDTO);
    }

    /**
     * 更新作物
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('crop:write')")
    public ApiResponse<CropDTO> updateCrop(
            @PathVariable Long id,
            @Validated @RequestBody UpdateCropRequest request) {

        Crop crop = cropService.updateCrop(id, request);

        CropDTO cropDTO = new CropDTO();
        BeanUtils.copyProperties(crop, cropDTO);

        return ApiResponse.success(cropDTO);
    }

    /**
     * 删除作物
     */
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAuthority('crop:delete')")
    public ApiResponse<Void> deleteCrop(@PathVariable Long id) {
        cropService.deleteCrop(id);
        return ApiResponse.success("删除成功");
    }
}
