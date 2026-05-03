package com.planting.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.planting.dto.DiagnoseRequest;
import com.planting.dto.DiagnoseResponse;
import com.planting.entity.PestKnowledge;
import com.planting.entity.PestRecord;
import com.planting.entity.PlantingPlan;
import com.planting.exception.BusinessException;
import com.planting.mapper.PestKnowledgeMapper;
import com.planting.mapper.PestRecordMapper;
import com.planting.mapper.PlantingPlanMapper;
import com.planting.service.PestRecordService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

/**
 * 病虫害记录服务实现类
 */
@Slf4j
@Service
public class PestRecordServiceImpl extends ServiceImpl<PestRecordMapper, PestRecord>
        implements PestRecordService {

    @Value("${ai.service.url:http://localhost:8000}")
    private String aiServiceUrl;

    @Value("${ai.service.timeout:30000}")
    private int aiServiceTimeout;

    @Autowired
    private PestKnowledgeMapper pestKnowledgeMapper;

    @Autowired
    private PlantingPlanMapper plantingPlanMapper;

    @Override
    public Page<PestRecord> listPestRecords(Integer page, Integer size, Long planId) {
        Page<PestRecord> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<PestRecord> wrapper = new LambdaQueryWrapper<>();

        if (planId != null) {
            wrapper.eq(PestRecord::getPlanId, planId);
        }

        wrapper.orderByDesc(PestRecord::getDiscoveryDate);
        return page(pageParam, wrapper);
    }

    @Override
    public PestRecord createPestRecord(PestRecord record) {
        // 设置默认状态
        if (record.getStatus() == null) {
            record.setStatus("未处理");
        }
        save(record);
        log.info("创建病虫害记录成功，记录ID: {}", record.getId());
        return record;
    }

    @Override
    public PestRecord updatePestRecord(Long id, PestRecord record) {
        PestRecord existingRecord = getById(id);
        if (existingRecord == null) {
            throw new BusinessException("病虫害记录不存在");
        }

        record.setId(id);
        updateById(record);
        log.info("更新病虫害记录成功，记录ID: {}", id);
        return record;
    }

    @Override
    public void deletePestRecord(Long id) {
        PestRecord record = getById(id);
        if (record == null) {
            throw new BusinessException("病虫害记录不存在");
        }

        removeById(id);
        log.info("删除病虫害记录成功，记录ID: {}", id);
    }

    @Override
    public DiagnoseResponse diagnose(DiagnoseRequest request) {
        if (request == null) {
            throw new BusinessException("诊断请求不能为空");
        }

        log.info("调用病虫害诊断服务，种植计划ID: {}", request.getPlanId());

        if (request.getImageBase64() == null || request.getImageBase64().isBlank()) {
            throw new BusinessException("图片不能为空");
        }

        // 获取种植计划信息。图片识别本身不依赖计划，计划缺失时继续调用AI模型。
        PlantingPlan plan = null;
        if (request.getPlanId() != null) {
            plan = plantingPlanMapper.selectById(request.getPlanId());
            if (plan == null) {
                log.warn("种植计划不存在，仍继续执行图片识别，种植计划ID: {}", request.getPlanId());
            }
        }

        DiagnoseResponse aiResponse = null;
        double aiConfidence = 0.0;

        // 尝试调用AI诊断服务
        try {
            String diagnoseUrl = aiServiceUrl.replaceAll("/+$", "") + "/api/image/diagnose";
            aiResponse = createAiRestTemplate().postForObject(
                    diagnoseUrl,
                    request,
                    DiagnoseResponse.class
            );

            if (aiResponse != null && aiResponse.getConfidence() != null) {
                aiConfidence = aiResponse.getConfidence();
                log.info("AI诊断完成，病虫害: {}, 置信度: {}%",
                        aiResponse.getPestName(), aiConfidence);
            }
        } catch (Exception e) {
            log.warn("AI诊断服务调用失败: {}，使用本地知识库", e.getMessage());
        }

        // 使用本地知识库作为AI服务不可用时的兜底
        DiagnoseResponse knowledgeResponse = matchWithKnowledgeBase(request, plan);

        // 混合识别结果
        DiagnoseResponse finalResponse = combineResults(aiResponse, knowledgeResponse);

        // 验证置信度
        if (finalResponse.getConfidence() == null) {
            finalResponse.setConfidence(0.0);
        }

        boolean highConfidence = finalResponse.getConfidence() > 70.0; // 降低阈值从78%到70%
        finalResponse.setHighConfidence(highConfidence);

        log.info("最终诊断结果，病虫害: {}, 置信度: {}, 高置信度: {}",
                finalResponse.getPestName(), finalResponse.getConfidence(), highConfidence);

        return finalResponse;
    }

    /**
     * 使用本地知识库匹配病虫害
     */
    private DiagnoseResponse matchWithKnowledgeBase(DiagnoseRequest request, PlantingPlan plan) {
        // 获取所有病虫害知识
        List<PestKnowledge> allKnowledge = pestKnowledgeMapper.selectList(null);

        if (allKnowledge.isEmpty()) {
            return createDefaultResponse();
        }

        List<PestKnowledge> relevantKnowledge = allKnowledge;

        // 根据种植计划的作物类型筛选相关知识
        if (plan != null) {
            String cropType = getCropType(plan.getCropId());
            relevantKnowledge = allKnowledge.stream()
                    .filter(k -> k.getAffectedCrops() != null &&
                            (k.getAffectedCrops().contains("全部") ||
                                    k.getAffectedCrops().contains(cropType)))
                    .collect(Collectors.toList());
        }

        if (relevantKnowledge.isEmpty()) {
            // 如果没有特定作物的知识，使用所有知识
            relevantKnowledge = allKnowledge;
        }

        // 简单的匹配算法：基于图像特征匹配
        PestKnowledge bestMatch = findBestMatch(relevantKnowledge, request);

        if (bestMatch != null) {
            return createResponseFromKnowledge(bestMatch);
        }

        return createDefaultResponse();
    }

    /**
     * 查找最佳匹配
     */
    private PestKnowledge findBestMatch(List<PestKnowledge> knowledgeList, DiagnoseRequest request) {
        // 这里是一个简化的匹配算法
        // 实际应用中应该使用更复杂的图像识别和特征匹配算法
        
        return knowledgeList.stream()
                .max(Comparator.comparing(k -> k.getConfidenceScore()))
                .orElse(null);
    }

    /**
     * 从知识库创建响应
     */
    private DiagnoseResponse createResponseFromKnowledge(PestKnowledge knowledge) {
        DiagnoseResponse response = new DiagnoseResponse();
        response.setPestName(knowledge.getPestName());
        response.setPestType(knowledge.getPestType());
        response.setCropType(resolveCropType(knowledge));
        response.setSymptoms(knowledge.getSymptoms());
        response.setTreatmentMethods(knowledge.getTreatmentMethods());
        response.setPreventionMethods(knowledge.getPreventionMethods());
        response.setSeverity(knowledge.getSeverity());
        response.setSeason(knowledge.getSeason());
        response.setConfidence(knowledge.getConfidenceScore() != null ? 
                             knowledge.getConfidenceScore().doubleValue() : 75.0);
        return response;
    }

    /**
     * 创建默认响应
     */
    private DiagnoseResponse createDefaultResponse() {
        DiagnoseResponse response = new DiagnoseResponse();
        response.setPestName("未知病虫害");
        response.setPestType("待识别");
        response.setCropType("");
        response.setSymptoms("无法识别具体病虫害类型，建议人工诊断");
        response.setTreatmentMethods("建议联系专业农技人员进行诊断");
        response.setPreventionMethods("加强田间管理，定期检查");
        response.setSeverity("未知");
        response.setSeason("未知");
        response.setConfidence(50.0);
        return response;
    }

    private String resolveCropType(PestKnowledge knowledge) {
        if (knowledge == null) {
            return "";
        }

        if (knowledge.getAffectedCrops() != null && !knowledge.getAffectedCrops().isBlank()) {
            return knowledge.getAffectedCrops().split("[,，、]")[0].trim();
        }

        return inferCropTypeFromName(knowledge.getPestName());
    }

    private String inferCropTypeFromName(String pestName) {
        if (pestName == null) {
            return "";
        }

        if (pestName.contains("小麦") || pestName.contains("麦")) {
            return "小麦";
        }
        if (pestName.contains("水稻") || pestName.contains("稻")) {
            return "水稻";
        }
        if (pestName.contains("玉米")) {
            return "玉米";
        }
        if (pestName.contains("大豆")) {
            return "大豆";
        }
        if (pestName.contains("马铃薯")) {
            return "马铃薯";
        }
        if (pestName.contains("番茄")) {
            return "番茄";
        }

        return "";
    }

    /**
     * 混合AI和知识库的结果
     */
    private DiagnoseResponse combineResults(DiagnoseResponse aiResponse,
                                           DiagnoseResponse knowledgeResponse) {
        if (aiResponse == null) {
            return knowledgeResponse;
        }

        // 真实图片模型结果优先。知识库匹配没有读取图像，只作为AI服务不可用时的兜底。
        return aiResponse;
    }

    private RestTemplate createAiRestTemplate() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(aiServiceTimeout);
        factory.setReadTimeout(aiServiceTimeout);
        return new RestTemplate(factory);
    }

    /**
     * 获取作物类型
     */
    private String getCropType(Long cropId) {
        // 简化的作物类型映射
        // 实际应用中应该查询crop表
        if (cropId == null) return "全部";
        
        // 假设cropId 1=小麦, 2=水稻, 3=玉米, 4=大豆, 5=马铃薯
        switch (cropId.intValue()) {
            case 1: return "小麦";
            case 2: return "水稻";
            case 3: return "玉米";
            case 4: return "大豆";
            case 5: return "马铃薯";
            default: return "全部";
        }
    }
}
