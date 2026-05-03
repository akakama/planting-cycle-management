package com.planting.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.IService;
import com.planting.dto.CreateCropRequest;
import com.planting.dto.UpdateCropRequest;
import com.planting.entity.Crop;

/**
 * 作物服务接口
 */
public interface CropService extends IService<Crop> {

    /**
     * 获取作物列表（分页、搜索）
     *
     * @param page    页码
     * @param size    每页大小
     * @param keyword 搜索关键词
     * @return 作物分页列表
     */
    Page<Crop> listCrops(Integer page, Integer size, String keyword);

    /**
     * 获取作物详情
     *
     * @param id 作物ID
     * @return 作物详情
     */
    Crop getCropById(Long id);

    /**
     * 创建作物
     *
     * @param request 创建作物请求
     * @return 创建的作物
     */
    Crop createCrop(CreateCropRequest request);

    /**
     * 更新作物
     *
     * @param id      作物ID
     * @param request 更新作物请求
     * @return 更新后的作物
     */
    Crop updateCrop(Long id, UpdateCropRequest request);

    /**
     * 删除作物
     *
     * @param id 作物ID
     */
    void deleteCrop(Long id);

    /**
     * 检查作物是否被使用
     *
     * @param id 作物ID
     * @return true-被使用，false-未被使用
     */
    boolean isCropUsed(Long id);
}
