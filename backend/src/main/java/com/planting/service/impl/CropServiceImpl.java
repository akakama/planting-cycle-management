package com.planting.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.planting.dto.CreateCropRequest;
import com.planting.dto.UpdateCropRequest;
import com.planting.entity.Crop;
import com.planting.exception.BusinessException;
import com.planting.mapper.CropMapper;
import com.planting.service.CropService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeanUtils;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

/**
 * 作物服务实现类
 */
@Slf4j
@Service
public class CropServiceImpl extends ServiceImpl<CropMapper, Crop> implements CropService {

    @Override
    public Page<Crop> listCrops(Integer page, Integer size, String keyword) {
        Page<Crop> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<Crop> wrapper = new LambdaQueryWrapper<>();

        if (StringUtils.hasText(keyword)) {
            wrapper.and(w -> w.like(Crop::getName, keyword)
                    .or()
                    .like(Crop::getVariety, keyword));
        }

        wrapper.orderByDesc(Crop::getCreateTime);
        return page(pageParam, wrapper);
    }

    @Override
    @Cacheable(value = "crop", key = "#id")
    public Crop getCropById(Long id) {
        Crop crop = getById(id);
        if (crop == null) {
            throw new BusinessException("作物不存在");
        }
        return crop;
    }

    @Override
    @CacheEvict(value = "crop", allEntries = true)
    public Crop createCrop(CreateCropRequest request) {
        // 检查作物名称是否已存在
        Crop existingCrop = baseMapper.selectByName(request.getName());
        if (existingCrop != null) {
            throw new BusinessException("作物名称已存在");
        }

        Crop crop = new Crop();
        BeanUtils.copyProperties(request, crop);
        save(crop);

        log.info("创建作物成功，作物ID: {}, 作物名称: {}", crop.getId(), crop.getName());
        return crop;
    }

    @Override
    @CacheEvict(value = "crop", key = "#id")
    public Crop updateCrop(Long id, UpdateCropRequest request) {
        Crop crop = getById(id);
        if (crop == null) {
            throw new BusinessException("作物不存在");
        }

        // 如果修改了名称，检查新名称是否已存在
        if (!crop.getName().equals(request.getName())) {
            Crop existingCrop = baseMapper.selectByName(request.getName());
            if (existingCrop != null && !existingCrop.getId().equals(id)) {
                throw new BusinessException("作物名称已存在");
            }
        }

        BeanUtils.copyProperties(request, crop);
        updateById(crop);

        log.info("更新作物成功，作物ID: {}", id);
        return crop;
    }

    @Override
    @CacheEvict(value = "crop", key = "#id")
    public void deleteCrop(Long id) {
        // 检查作物是否存在
        Crop crop = getById(id);
        if (crop == null) {
            throw new BusinessException("作物不存在");
        }

        // 检查作物是否被使用
        if (isCropUsed(id)) {
            throw new BusinessException("该作物已被种植计划使用，无法删除");
        }

        removeById(id);
        log.info("删除作物成功，作物ID: {}", id);
    }

    @Override
    public boolean isCropUsed(Long id) {
        Long count = baseMapper.countUsageByCropId(id);
        return count != null && count > 0;
    }
}
