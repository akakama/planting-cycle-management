package com.planting.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.planting.entity.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

/**
 * 用户Mapper接口
 */
@Mapper
public interface UserMapper extends BaseMapper<User> {

    /**
     * 根据用户名查询用户ID
     *
     * @param username 用户名
     * @return 用户ID
     */
    @Select("SELECT id FROM sys_user WHERE username = #{username} AND deleted = 0")
    Long selectIdByUsername(String username);
}
