package com.planting.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.planting.entity.Material;
import com.planting.exception.BusinessException;
import com.planting.mapper.MaterialMapper;
import com.planting.service.MaterialService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

/**
 * 农资服务实现类
 */
@Slf4j
@Service
public class MaterialServiceImpl extends ServiceImpl<MaterialMapper, Material>
        implements MaterialService {

    @Override
    public Page<Material> listMaterials(Integer page, Integer size, String type) {
        Page<Material> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<Material> wrapper = new LambdaQueryWrapper<>();

        if (type != null && !type.isEmpty()) {
            wrapper.eq(Material::getType, type);
        }

        wrapper.orderByDesc(Material::getCreateTime);
        return page(pageParam, wrapper);
    }

    @Override
    @Transactional
    public Material stockIn(Long id, BigDecimal quantity, String remark) {
        Material material = getById(id);
        if (material == null) {
            throw new BusinessException("农资不存在");
        }

        if (quantity.compareTo(BigDecimal.ZERO) <= 0) {
            throw new BusinessException("入库数量必须大于0");
        }

        // 增加库存（使用乐观锁）
        material.setStockQuantity(material.getStockQuantity().add(quantity));
        updateById(material);

        log.info("农资入库成功，农资ID: {}, 入库数量: {}, 当前库存: {}",
                id, quantity, material.getStockQuantity());

        return material;
    }
}
