package com.planting.util;

import org.springframework.beans.BeanUtils;

import java.util.ArrayList;
import java.util.List;

/**
 * Bean拷贝工具类
 */
public class BeanCopyUtils {

    /**
     * 拷贝对象属性
     *
     * @param source 源对象
     * @param target 目标类
     * @param <T>    目标类型
     * @return 目标对象
     */
    public static <T> T copy(Object source, Class<T> target) {
        if (source == null) {
            return null;
        }
        try {
            T instance = target.getDeclaredConstructor().newInstance();
            BeanUtils.copyProperties(source, instance);
            return instance;
        } catch (Exception e) {
            throw new RuntimeException("Bean拷贝失败", e);
        }
    }

    /**
     * 拷贝列表
     *
     * @param sourceList 源列表
     * @param target     目标类
     * @param <S>        源类型
     * @param <T>        目标类型
     * @return 目标列表
     */
    public static <S, T> List<T> copyList(List<S> sourceList, Class<T> target) {
        if (sourceList == null || sourceList.isEmpty()) {
            return new ArrayList<>();
        }
        List<T> targetList = new ArrayList<>(sourceList.size());
        for (S source : sourceList) {
            targetList.add(copy(source, target));
        }
        return targetList;
    }
}
