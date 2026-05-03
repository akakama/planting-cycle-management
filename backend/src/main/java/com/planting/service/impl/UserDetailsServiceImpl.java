package com.planting.service.impl;

import com.planting.entity.User;
import com.planting.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * 用户详情服务实现类
 */
@Slf4j
@Service
public class UserDetailsServiceImpl implements UserDetailsService {

    @Autowired
    private UserService userService;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        log.info("加载用户信息，用户名: {}", username);

        // 查询用户信息
        User user = userService.getByUsername(username);
        if (user == null) {
            log.error("用户不存在，用户名: {}", username);
            throw new UsernameNotFoundException("用户不存在: " + username);
        }

        // 检查用户状态
        if (user.getStatus() == 0) {
            log.error("用户已被禁用，用户名: {}", username);
            throw new UsernameNotFoundException("用户已被禁用: " + username);
        }

        // 加载用户角色
        List<String> roles = userService.getUserRoles(user.getId());

        // 加载用户权限
        Set<String> permissions = userService.getUserPermissions(user.getId());

        // 构建权限列表（角色和权限）
        List<SimpleGrantedAuthority> authorities = roles.stream()
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList());

        authorities.addAll(permissions.stream()
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList()));

        log.info("用户信息加载成功，用户名: {}, 角色数: {}, 权限数: {}",
                username, roles.size(), permissions.size());

        // 返回UserDetails对象
        return org.springframework.security.core.userdetails.User.builder()
                .username(user.getUsername())
                .password(user.getPassword())
                .authorities(authorities)
                .accountLocked(false)
                .credentialsExpired(false)
                .disabled(false)
                .accountExpired(false)
                .build();
    }
}
