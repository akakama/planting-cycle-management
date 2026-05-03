package com.planting.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.planting.entity.PhenologyRecord;

/**
 * 物候期记录服务接口
 */
public interface PhenologyRecordService extends IService<PhenologyRecord> {

    /**
     * 获取物候期记录列表
     */
    Page<PhenologyRecord> listPhenologyRecords(Integer page, Integer size, Long planId);

    /**
     * 创建物候期记录
     */
    PhenologyRecord createPhenologyRecord(PhenologyRecord record);

    /**
     * 更新物候期记录
     */
    PhenologyRecord updatePhenologyRecord(Long id, PhenologyRecord record);

    /**
     * 删除物候期记录
     */
    void deletePhenologyRecord(Long id);
}
