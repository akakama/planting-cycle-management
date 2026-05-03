package com.planting.exception;

import lombok.Getter;

/**
 * 业务异常类
 */
@Getter
public class BusinessException extends RuntimeException {

    private static final long serialVersionUID = 1L;

    /**
     * 错误码
     */
    private Integer code;

    /**
     * 错误消息
     */
    private String message;

    public BusinessException(String message) {
        super(message);
        this.code = 500;
        this.message = message;
    }

    public BusinessException(Integer code, String message) {
        super(message);
        this.code = code;
        this.message = message;
    }

    public BusinessException(String message, Throwable cause) {
        super(message, cause);
        this.code = 500;
        this.message = message;
    }

    public BusinessException(Integer code, String message, Throwable cause) {
        super(message, cause);
        this.code = code;
        this.message = message;
    }

    /**
     * 用户名或密码错误
     */
    public static BusinessException invalidCredentials() {
        return new BusinessException(1001, "用户名或密码错误");
    }

    /**
     * JWT令牌无效或过期
     */
    public static BusinessException invalidToken() {
        return new BusinessException(1002, "JWT令牌无效或过期");
    }

    /**
     * 权限不足
     */
    public static BusinessException accessDenied() {
        return new BusinessException(1003, "权限不足");
    }

    /**
     * 数据已存在
     */
    public static BusinessException dataExists(String message) {
        return new BusinessException(1004, message);
    }

    /**
     * 数据不存在
     */
    public static BusinessException dataNotFound(String message) {
        return new BusinessException(1005, message);
    }

    /**
     * 库存不足
     */
    public static BusinessException insufficientStock() {
        return new BusinessException(1006, "库存不足");
    }

    /**
     * 状态转换不合法
     */
    public static BusinessException invalidStatusTransition() {
        return new BusinessException(1007, "状态转换不合法");
    }

    /**
     * 数据被使用,无法删除
     */
    public static BusinessException dataInUse() {
        return new BusinessException(1008, "数据被使用,无法删除");
    }
}
