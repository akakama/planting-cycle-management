package com.planting.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.common.ApiResponse;
import com.planting.entity.PhenologyRecord;
import com.planting.service.PhenologyRecordService;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

/**
 * 物候期记录管理控制器
 */
@Slf4j
@RestController
@RequestMapping("/phenology-records")
public class PhenologyRecordController {

    @Autowired
    private PhenologyRecordService phenologyRecordService;

    /**
     * 获取物候期记录列表
     */
    @GetMapping
    @PreAuthorize("hasAuthority('phenology:read')")
    public ApiResponse<Page<PhenologyRecord>> listPhenologyRecords(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) Long planId) {

        Page<PhenologyRecord> recordPage = phenologyRecordService.listPhenologyRecords(page, size, planId);
        return ApiResponse.success(recordPage);
    }

    /**
     * 添加物候期记录
     */
    @PostMapping
    @PreAuthorize("hasAuthority('phenology:write')")
    public ApiResponse<PhenologyRecord> createPhenologyRecord(@RequestBody PhenologyRecord record) {
        PhenologyRecord createdRecord = phenologyRecordService.createPhenologyRecord(record);
        return ApiResponse.success(createdRecord);
    }

    /**
     * 更新物候期记录
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('phenology:write')")
    public ApiResponse<PhenologyRecord> updatePhenologyRecord(
            @PathVariable Long id,
            @RequestBody PhenologyRecord record) {

        PhenologyRecord updatedRecord = phenologyRecordService.updatePhenologyRecord(id, record);
        return ApiResponse.success(updatedRecord);
    }

    /**
     * 删除物候期记录
     */
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAuthority('phenology:write')")
    public ApiResponse<Void> deletePhenologyRecord(@PathVariable Long id) {
        phenologyRecordService.deletePhenologyRecord(id);
        return ApiResponse.success("删除成功");
    }

    /**
     * AI查询物候期记录
     */
    @GetMapping("/ai/query")
    public ApiResponse<?> queryPhenologyRecordsForAI(
            @RequestParam(required = false) Long planId,
            @RequestParam(required = false) String startDate,
            @RequestParam(required = false) String endDate) {
        // 暂时返回空结果，后续实现
        return ApiResponse.success("功能开发中");
    }
}
