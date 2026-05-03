package com.planting.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.planting.common.ApiResponse;
import com.planting.dto.DiagnoseRequest;
import com.planting.dto.DiagnoseResponse;
import com.planting.entity.PestRecord;
import com.planting.service.PestRecordService;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

/**
 * 病虫害记录管理控制器
 */
@Slf4j
@RestController
@RequestMapping("/pest-records")
public class PestRecordController {

    @Autowired
    private PestRecordService pestRecordService;

    /**
     * 获取病虫害记录列表
     */
    @GetMapping
    @PreAuthorize("hasAuthority('pest:read')")
    public ApiResponse<Page<PestRecord>> listPestRecords(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) Long planId) {

        Page<PestRecord> recordPage = pestRecordService.listPestRecords(page, size, planId);
        return ApiResponse.success(recordPage);
    }

    /**
     * 添加病虫害记录
     */
    @PostMapping
    @PreAuthorize("hasAuthority('pest:write')")
    public ApiResponse<PestRecord> createPestRecord(@RequestBody PestRecord record) {
        PestRecord createdRecord = pestRecordService.createPestRecord(record);
        return ApiResponse.success(createdRecord);
    }

    /**
     * 更新病虫害记录
     */
    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('pest:write')")
    public ApiResponse<PestRecord> updatePestRecord(
            @PathVariable Long id,
            @RequestBody PestRecord record) {

        PestRecord updatedRecord = pestRecordService.updatePestRecord(id, record);
        return ApiResponse.success(updatedRecord);
    }

    /**
     * 删除病虫害记录
     */
    @DeleteMapping("/{id}")
    @PreAuthorize("hasAuthority('pest:write')")
    public ApiResponse<Void> deletePestRecord(@PathVariable Long id) {
        pestRecordService.deletePestRecord(id);
        return ApiResponse.success("删除成功");
    }

    /**
     * 病虫害图片识别诊断
     */
    @PostMapping("/diagnose")
    @PreAuthorize("hasAuthority('pest:write')")
    public ApiResponse<DiagnoseResponse> diagnose(@RequestBody DiagnoseRequest request) {
        DiagnoseResponse response = pestRecordService.diagnose(request);
        return ApiResponse.success(response);
    }
}
