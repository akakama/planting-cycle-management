package com.planting.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.planting.entity.PhenologyRecord;
import com.planting.exception.BusinessException;
import com.planting.mapper.PhenologyRecordMapper;
import com.planting.service.PhenologyRecordService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * 物候期记录服务实现类
 */
@Slf4j
@Service
public class PhenologyRecordServiceImpl extends ServiceImpl<PhenologyRecordMapper, PhenologyRecord>
        implements PhenologyRecordService {

    @Override
    public Page<PhenologyRecord> listPhenologyRecords(Integer page, Integer size, Long planId) {
        Page<PhenologyRecord> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<PhenologyRecord> wrapper = new LambdaQueryWrapper<>();

        if (planId != null) {
            wrapper.eq(PhenologyRecord::getPlanId, planId);
        }

        wrapper.orderByDesc(PhenologyRecord::getRecordDate);
        return page(pageParam, wrapper);
    }

    @Override
    public PhenologyRecord createPhenologyRecord(PhenologyRecord record) {
        save(record);
        log.info("创建物候期记录成功，记录ID: {}", record.getId());
        return record;
    }

    @Override
    public PhenologyRecord updatePhenologyRecord(Long id, PhenologyRecord record) {
        PhenologyRecord existingRecord = getById(id);
        if (existingRecord == null) {
            throw new BusinessException("物候期记录不存在");
        }

        record.setId(id);
        updateById(record);
        log.info("更新物候期记录成功，记录ID: {}", id);
        return record;
    }

    @Override
    public void deletePhenologyRecord(Long id) {
        PhenologyRecord record = getById(id);
        if (record == null) {
            throw new BusinessException("物候期记录不存在");
        }

        removeById(id);
        log.info("删除物候期记录成功，记录ID: {}", id);
    }
}
