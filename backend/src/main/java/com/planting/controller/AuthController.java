package com.planting.controller;

import com.planting.common.ApiResponse;
import com.planting.dto.LoginRequest;
import com.planting.dto.LoginResponse;
import com.planting.dto.RegisterRequest;
import com.planting.dto.UserInfoResponse;
import com.planting.entity.User;
import com.planting.service.TokenBlacklistService;
import com.planting.service.UserService;
import com.planting.util.JwtUtil;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * 认证控制器
 */
@Slf4j
@RestController
@RequestMapping("/auth")
public class AuthController {

    @Autowired
    private UserService userService;

    @Autowired
    private JwtUtil jwtUtil;

    @Autowired
    private TokenBlacklistService tokenBlacklistService;

    /**
     * 测试注册端点（无验证）
     */
    @PostMapping("/test-register")
    public ApiResponse<String> testRegister(@RequestBody Map<String, String> request) {
        log.info("测试注册请求: {}", request);
        return ApiResponse.success("测试成功", "收到请求: " + request.toString());
    }

    /**
     * 用户注册
     */
    @PostMapping("/register")
    public ApiResponse<Map<String, Object>> register(@RequestBody Map<String, Object> requestMap) {
        log.info("用户注册请求: {}", requestMap);

        try {
            // 手动构建RegisterRequest对象
            RegisterRequest request = new RegisterRequest();
            request.setUsername((String) requestMap.get("username"));
            request.setPassword((String) requestMap.get("password"));
            request.setEmail((String) requestMap.get("email"));
            request.setPhone((String) requestMap.get("phone"));

            log.info("构建的RegisterRequest: {}", request);

            // 注册用户
            User user = userService.register(request);

            // 构建响应
            Map<String, Object> result = new HashMap<>();
            result.put("userId", user.getId());
            result.put("username", user.getUsername());
            result.put("realName", user.getRealName());

            log.info("用户注册成功，用户名: {}", user.getUsername());
            return ApiResponse.success("注册成功", result);
        } catch (Exception e) {
            log.error("注册失败异常: {}", e.getMessage(), e);
            return ApiResponse.error("注册失败: " + e.getMessage());
        }
    }

    /**
     * 用户登录
     */
    @PostMapping("/login")
    public ApiResponse<LoginResponse> login(@Validated @RequestBody LoginRequest request) {
        log.info("用户登录请求，用户名: {}", request.getUsername());

        // 查询用户
        User user = userService.getByUsername(request.getUsername());
        if (user == null) {
            log.warn("用户不存在，用户名: {}", request.getUsername());
            return ApiResponse.error("用户名或密码错误");
        }

        // 检查用户状态
        if (user.getStatus() == 0) {
            log.warn("用户已被禁用，用户名: {}", request.getUsername());
            return ApiResponse.error("用户已被禁用");
        }

        // 验证密码
        if (!userService.verifyPassword(request.getPassword(), user.getPassword())) {
            log.warn("密码错误，用户名: {}", request.getUsername());
            return ApiResponse.error("用户名或密码错误");
        }

        // 生成JWT令牌
        org.springframework.security.core.userdetails.UserDetails userDetails =
                org.springframework.security.core.userdetails.User.builder()
                        .username(user.getUsername())
                        .password(user.getPassword())
                        .authorities(userService.getUserPermissions(user.getId()).toArray(new String[0]))
                        .build();

        String token = jwtUtil.generateToken(userDetails);

        // 获取用户角色
        List<String> roles = userService.getUserRoles(user.getId());

        // 获取用户权限
        List<String> permissions = userService.getUserPermissions(user.getId()).stream().collect(Collectors.toList());

        // 构建响应
        LoginResponse response = LoginResponse.builder()
                .token(token)
                .tokenType("Bearer")
                .userId(user.getId())
                .username(user.getUsername())
                .realName(user.getRealName())
                .roles(roles)
                .permissions(permissions)
                .build();

        log.info("用户登录成功，用户名: {}", user.getUsername());
        return ApiResponse.success(response);
    }

    /**
     * 用户登出
     */
    @PostMapping("/logout")
    public ApiResponse<Void> logout(HttpServletRequest request) {
        // 从请求头中获取JWT令牌
        String token = extractTokenFromRequest(request);
        if (token != null) {
            // 将令牌加入黑名单
            long remainingTime = jwtUtil.getTokenRemainingTime(token);
            if (remainingTime > 0) {
                tokenBlacklistService.addToBlacklist(token, remainingTime);
            }
        }

        // 清除Security上下文
        SecurityContextHolder.clearContext();

        log.info("用户登出成功");
        return ApiResponse.success("登出成功");
    }

    /**
     * 获取当前用户信息
     */
    @GetMapping("/current-user")
    public ApiResponse<UserInfoResponse> getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated()) {
            return ApiResponse.error("未认证");
        }

        String username = authentication.getName();
        User user = userService.getByUsername(username);

        if (user == null) {
            return ApiResponse.error("用户不存在");
        }

        // 获取用户角色
        List<String> roles = userService.getUserRoles(user.getId());

        // 获取用户权限
        List<String> permissions = userService.getUserPermissions(user.getId()).stream().collect(Collectors.toList());

        // 构建响应
        UserInfoResponse response = UserInfoResponse.builder()
                .userId(user.getId())
                .username(user.getUsername())
                .realName(user.getRealName())
                .status(user.getStatus())
                .roles(roles)
                .permissions(permissions)
                .build();

        return ApiResponse.success(response);
    }

    /**
     * 从请求中提取JWT令牌
     */
    private String extractTokenFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
}
