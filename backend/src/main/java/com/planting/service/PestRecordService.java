package com.planting.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.planting.dto.DiagnoseRequest;
import com.planting.dto.DiagnoseResponse;
import com.planting.entity.PestRecord;

/**
 * 病虫害记录服务接口
 */
public interface PestRecordService extends IService<PestRecord> {

    /**
     * 获取病虫害记录列表
     */
    Page<PestRecord> listPestRecords(Integer page, Integer size, Long planId);

    /**
     * 创建病虫害记录
     */
    PestRecord createPestRecord(PestRecord record);

    /**
     * 更新病虫害记录
     */
    PestRecord updatePestRecord(Long id, PestRecord record);

    /**
     * 删除病虫害记录
     */
    void deletePestRecord(Long id);

    /**
     * AI诊断
     */
    DiagnoseResponse diagnose(DiagnoseRequest request);
}
