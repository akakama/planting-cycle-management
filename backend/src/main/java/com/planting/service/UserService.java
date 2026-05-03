package com.planting.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.planting.dto.RegisterRequest;
import com.planting.entity.User;

import java.util.List;
import java.util.Set;

/**
 * 用户服务接口
 */
public interface UserService extends IService<User> {

    /**
     * 根据用户名查询用户
     *
     * @param username 用户名
     * @return 用户信息
     */
    User getByUsername(String username);

    /**
     * 验证密码
     *
     * @param rawPassword     原始密码
     * @param encodedPassword 加密后的密码
     * @return true-密码正确，false-密码错误
     */
    boolean verifyPassword(String rawPassword, String encodedPassword);

    /**
     * 获取用户权限列表
     *
     * @param userId 用户ID
     * @return 权限列表
     */
    Set<String> getUserPermissions(Long userId);

    /**
     * 获取用户角色列表
     *
     * @param userId 用户ID
     * @return 角色列表
     */
    List<String> getUserRoles(Long userId);

    /**
     * 用户注册
     *
     * @param request 注册请求
     * @return 注册结果
     */
    User register(RegisterRequest request);
}
