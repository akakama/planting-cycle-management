package com.planting.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.planting.entity.HarvestRecord;
import com.planting.exception.BusinessException;
import com.planting.mapper.HarvestRecordMapper;
import com.planting.service.HarvestService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * 采收服务实现类
 */
@Slf4j
@Service
public class HarvestServiceImpl extends ServiceImpl<HarvestRecordMapper, HarvestRecord>
        implements HarvestService {

    @Override
    public Page<HarvestRecord> listHarvestRecords(Integer page, Integer size, Long planId) {
        Page<HarvestRecord> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<HarvestRecord> wrapper = new LambdaQueryWrapper<>();

        if (planId != null) {
            wrapper.eq(HarvestRecord::getPlanId, planId);
        }

        wrapper.orderByDesc(HarvestRecord::getHarvestDate);
        return page(pageParam, wrapper);
    }

    @Override
    public HarvestRecord createHarvestRecord(HarvestRecord record) {
        save(record);
        log.info("创建采收记录成功，记录ID: {}", record.getId());
        return record;
    }

    @Override
    public HarvestRecord updateHarvestRecord(Long id, HarvestRecord record) {
        HarvestRecord existingRecord = getById(id);
        if (existingRecord == null) {
            throw new BusinessException("采收记录不存在");
        }

        record.setId(id);
        updateById(record);
        log.info("更新采收记录成功，记录ID: {}", id);
        return record;
    }

    @Override
    public void deleteHarvestRecord(Long id) {
        HarvestRecord record = getById(id);
        if (record == null) {
            throw new BusinessException("采收记录不存在");
        }

        removeById(id);
        log.info("删除采收记录成功，记录ID: {}", id);
    }
}
