package com.planting.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.planting.entity.Material;

import java.math.BigDecimal;

/**
 * 农资服务接口
 */
public interface MaterialService extends IService<Material> {

    /**
     * 获取农资列表
     */
    Page<Material> listMaterials(Integer page, Integer size, String type);

    /**
     * 农资入库
     */
    Material stockIn(Long id, BigDecimal quantity, String remark);
}
