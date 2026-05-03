package com.planting.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.planting.entity.HarvestRecord;

/**
 * 采收服务接口
 */
public interface HarvestService extends IService<HarvestRecord> {

    /**
     * 获取采收记录列表
     */
    Page<HarvestRecord> listHarvestRecords(Integer page, Integer size, Long planId);

    /**
     * 创建采收记录
     */
    HarvestRecord createHarvestRecord(HarvestRecord record);

    /**
     * 更新采收记录
     */
    HarvestRecord updateHarvestRecord(Long id, HarvestRecord record);

    /**
     * 删除采收记录
     */
    void deleteHarvestRecord(Long id);
}
