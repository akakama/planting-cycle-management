package com.planting.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.planting.dto.RegisterRequest;
import com.planting.entity.User;
import com.planting.mapper.UserMapper;
import com.planting.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * 用户服务实现类
 */
@Slf4j
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public User getByUsername(String username) {
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(User::getUsername, username);
        return getOne(wrapper);
    }

    @Override
    public boolean verifyPassword(String rawPassword, String encodedPassword) {
        return passwordEncoder.matches(rawPassword, encodedPassword);
    }

    @Override
    public Set<String> getUserPermissions(Long userId) {
        // TODO: 实现从数据库查询用户权限的逻辑
        // 这里先返回一个默认的权限集合，实际应该从sys_permission表和sys_role_permission表查询
        log.info("获取用户权限，用户ID: {}", userId);
        return Set.of(
                "crop:read", "crop:write", "crop:delete",
                "plan:read", "plan:write", "plan:delete",
                "plot:read", "plot:write",
                "phenology:read", "phenology:write",
                "pest:read", "pest:write",
                "material:read", "material:write",
                "harvest:read", "harvest:write",
                "yield:read", "yield:write",
                "ai:chat"
        );
    }

    @Override
    public List<String> getUserRoles(Long userId) {
        // TODO: 实现从数据库查询用户角色的逻辑
        // 这里先返回一个默认的角色列表，实际应该从sys_role表和sys_user_role表查询
        log.info("获取用户角色，用户ID: {}", userId);
        return List.of("ROLE_ADMIN");
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public User register(RegisterRequest request) {
        log.info("用户注册请求，用户名: {}, 邮箱: {}, 手机: {}", request.getUsername(), request.getEmail(), request.getPhone());

        try {
            // 检查用户名是否已存在
            User existingUser = getByUsername(request.getUsername());
            if (existingUser != null) {
                throw new RuntimeException("用户名已存在");
            }

            // 创建新用户
            User user = new User();
            user.setUsername(request.getUsername());
            user.setPassword(passwordEncoder.encode(request.getPassword()));
            user.setRealName(request.getUsername()); // 使用用户名作为真实姓名
            user.setEmail(request.getEmail());
            user.setPhone(request.getPhone());
            user.setStatus(1); // 默认启用
            user.setCreateTime(LocalDateTime.now());
            user.setUpdateTime(LocalDateTime.now());

            // 保存用户
            save(user);
            log.info("用户注册成功，用户ID: {}, 用户名: {}", user.getId(), user.getUsername());

            return user;
        } catch (Exception e) {
            log.error("注册过程中发生异常: {}", e.getMessage(), e);
            throw new RuntimeException("注册失败: " + e.getMessage(), e);
        }
    }
}
