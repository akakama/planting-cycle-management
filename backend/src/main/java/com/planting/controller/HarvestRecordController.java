package com.planting.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.common.ApiResponse;
import com.planting.entity.HarvestRecord;
import com.planting.service.HarvestService;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

/**
 * 采收记录管理控制器
 */
@Slf4j
@RestController
@RequestMapping("/harvest-records")
public class HarvestRecordController {

    @Autowired
    private HarvestService harvestService;

    /**
     * 获取采收记录列表
     */
    @GetMapping
    @PreAuthorize("hasAuthority('harvest:read')")
    public ApiResponse<Page<HarvestRecord>> listHarvestRecords(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) Long planId) {

        Page<HarvestRecord> recordPage = harvestService.listHarvestRecords(page, size, planId);
        return ApiResponse.success(recordPage);
    }

    /**
     * 添加采收记录
     */
    @PostMapping
    @PreAuthorize("hasAuthority('harvest:write')")
    public ApiResponse<HarvestRecord> createHarvestRecord(@RequestBody HarvestRecord record) {
        HarvestRecord createdRecord = harvestService.createHarvestRecord(record);
        return ApiResponse.success(createdRecord);
    }

    /**
     * 更新采收记录
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('harvest:write')")
    public ApiResponse<HarvestRecord> updateHarvestRecord(
            @PathVariable Long id,
            @RequestBody HarvestRecord record) {

        HarvestRecord updatedRecord = harvestService.updateHarvestRecord(id, record);
        return ApiResponse.success(updatedRecord);
    }

    /**
     * 删除采收记录
     */
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAuthority('harvest:write')")
    public ApiResponse<Void> deleteHarvestRecord(@PathVariable Long id) {
        harvestService.deleteHarvestRecord(id);
        return ApiResponse.success("删除成功");
    }
}
