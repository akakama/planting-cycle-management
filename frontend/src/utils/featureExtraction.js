// 增强的特征提取和知识库匹配模块
import { pestKnowledgeBase } from '@/data/pestKnowledgeBase'

/**
 * 增强的特征提取
 * 提取更丰富的图片特征用于知识库匹配
 */
export const extractEnhancedFeatures = (data, width, height) => {
  // 基础特征
  const basicFeatures = {
    colors: extractColorFeatures(data),
    texture: extractTextureFeatures(data, width, height),
    brightness: extractBrightnessFeatures(data)
  }
  
  // 增强特征
  const enhancedFeatures = {
    // 颜色分布分析
    colorDistribution: analyzeColorDistribution(data),
    
    // 形状特征
    shapeFeatures: analyzeShapeFeatures(data, width, height),
    
    // 模式特征
    patternFeatures: analyzePatternFeatures(data, width, height),
    
    // 对比度特征
    contrastFeatures: analyzeContrastFeatures(data),
    
    // 边缘特征
    edgeFeatures: analyzeEdgeFeatures(data, width, height),
    
    // 植物特征
    plantFeatures: analyzePlantFeatures(data),
    
    // 病害特征
    diseaseFeatures: analyzeDiseaseFeatures(data)
  }
  
  return { ...basicFeatures, ...enhancedFeatures }
}

/**
 * 颜色分布分析
 */
const analyzeColorDistribution = (data) => {
  const colorCounts = {}
  let totalPixels = data.length / 4
  
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i]
    const g = data[i + 1]
    const b = data[i + 2]
    
    // 简化颜色分类
    let colorName = 'other'
    
    if (r > 200 && g > 200 && b > 200) {
      colorName = 'white'
    } else if (r < 50 && g < 50 && b < 50) {
      colorName = 'black'
    } else if (g > r && g > b) {
      if (g > 150) {
        colorName = 'green'
      } else if (g > 100) {
        colorName = 'dark_green'
      } else {
        colorName = 'yellow_green'
      }
    } else if (r > g && r > b) {
      if (g > 150 && b < 100) {
        colorName = 'yellow'
      } else if (r > 150 && g > 100) {
        colorName = 'orange'
      } else if (r > 150 && g < 100 && b < 100) {
        colorName = 'red'
      } else if (r > 100 && g < 100 && b < 100) {
        colorName = 'brown'
      } else if (r > 100 && g < 100 && b > 100) {
        colorName = 'purple'
      } else {
        colorName = 'pink'
      }
    } else if (b > r && b > g) {
      if (b > 150) {
        colorName = 'blue'
      } else {
        colorName = 'dark_blue'
      }
    } else if (r > 150 && g > 150 && b < 100) {
      colorName = 'yellow'
    } else if (r < 100 && g > 100 && b < 100) {
      colorName = 'green'
    }
    
    colorCounts[colorName] = (colorCounts[colorName] || 0) + 1
  }
  
  // 计算颜色比例
  const colorDistribution = {}
  for (const [color, count] of Object.entries(colorCounts)) {
    colorDistribution[color] = count / totalPixels
  }
  
  return colorDistribution
}

/**
 * 形状特征分析
 */
const analyzeShapeFeatures = (data, width, height) => {
  const shapes = []
  const colorDistribution = analyzeColorDistribution(data)
  
  // 根据颜色分布推断形状特征
  if (colorDistribution.green > 0.3) {
    if (colorDistribution.green > 0.7) {
      shapes.push('大面积绿色')
    } else {
      shapes.push('部分绿色')
    }
  }
  
  if (colorDistribution.yellow > 0.05 || colorDistribution.orange > 0.05) {
    shapes.push('斑点状')
  }
  
  if (colorDistribution.brown > 0.05) {
    shapes.push('斑块状')
  }
  
  if (colorDistribution.red > 0.05) {
    shapes.push('红色斑点')
  }
  
  return shapes
}

/**
 * 模式特征分析
 */
const analyzePatternFeatures = (data, width, height) => {
  const patterns = []
  const colorDistribution = analyzeColorDistribution(data)
  
  // 检测病害相关模式
  if (colorDistribution.brown > 0.05) {
    patterns.push('病斑', '坏死')
  }
  
  if (colorDistribution.yellow > 0.05) {
    patterns.push('黄化', '斑点')
  }
  
  if (colorDistribution.white > 0.05 && colorDistribution.green > 0.3) {
    patterns.push('霉层', '粉状物')
  }
  
  if (colorDistribution.red > 0.05) {
    patterns.push('锈孢子', '红斑')
  }
  
  return patterns
}

/**
 * 对比度特征分析
 */
const analyzeContrastFeatures = (data) => {
  let contrastSum = 0
  let contrastCount = 0
  
  for (let i = 0; i < data.length - 4; i += 4) {
    const brightness1 = (data[i] + data[i + 1] + data[i + 2]) / 3
    const brightness2 = (data[i + 4] + data[i + 5] + data[i + 6]) / 3
    const contrast = Math.abs(brightness1 - brightness2)
    contrastSum += contrast
    contrastCount++
  }
  
  const avgContrast = contrastSum / contrastCount
  
  return {
    avgContrast,
    hasHighContrast: avgContrast > 30
  }
}

/**
 * 边缘特征分析
 */
const analyzeEdgeFeatures = (data, width, height) => {
  let edgeCount = 0
  let totalEdges = 0
  
  for (let y = 0; y < height - 1; y++) {
    for (let x = 0; x < width - 1; x++) {
      const idx = (y * width + x) * 4
      const rightIdx = (y * width + (x + 1)) * 4
      const bottomIdx = ((y + 1) * width + x) * 4
      
      const brightness = (data[idx] + data[idx + 1] + data[idx + 2]) / 3
      const rightBrightness = (data[rightIdx] + data[rightIdx + 1] + data[rightIdx + 2]) / 3
      const bottomBrightness = (data[bottomIdx] + data[bottomIdx + 1] + data[bottomIdx + 2]) / 3
      
      const horizontalDiff = Math.abs(brightness - rightBrightness)
      const verticalDiff = Math.abs(brightness - bottomBrightness)
      
      if (horizontalDiff > 20 || verticalDiff > 20) {
        edgeCount++
      }
      
      totalEdges++
    }
  }
  
  return {
    edgeRatio: edgeCount / totalEdges,
    hasEdges: edgeCount / totalEdges > 0.15
  }
}

/**
 * 植物特征分析
 */
const analyzePlantFeatures = (data) => {
  const colorDistribution = analyzeColorDistribution(data)
  
  const features = []
  
  // 检测植物特征
  if (colorDistribution.green > 0.2) {
    features.push('绿色叶片')
  }
  
  if (colorDistribution.dark_green > 0.1) {
    features.push('深绿色')
  }
  
  if (colorDistribution.yellow_green > 0.1) {
    features.push('黄绿色')
  }
  
  return features
}

/**
 * 病害特征分析
 */
const analyzeDiseaseFeatures = (data) => {
  const colorDistribution = analyzeColorDistribution(data)
  
  const features = []
  
  // 检测病害特征
  if (colorDistribution.yellow > 0.05) {
    features.push('黄色', '黄化')
  }
  
  if (colorDistribution.brown > 0.05) {
    features.push('褐色', '坏死')
  }
  
  if (colorDistribution.red > 0.05) {
    features.push('红色', '锈病')
  }
  
  if (colorDistribution.white > 0.05 && colorDistribution.green > 0.2) {
    features.push('白色', '霉层')
  }
  
  if (colorDistribution.black > 0.05 && colorDistribution.green > 0.2) {
    features.push('黑色', '霉斑')
  }
  
  return features
}

/**
 * 基础颜色特征提取
 */
const extractColorFeatures = (data) => {
  let greenPixels = 0
  let yellowPixels = 0
  let brownPixels = 0
  let redPixels = 0
  let whitePixels = 0
  let totalPixels = data.length / 4
  
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i]
    const g = data[i + 1]
    const b = data[i + 2]
    
    // 检测绿色（健康叶片）
    if (g > r && g > b && g > 100) {
      greenPixels++
    }
    
    // 检测黄色（病害症状）
    if (r > 200 && g > 180 && b < 100) {
      yellowPixels++
    }
    
    // 检测褐色（坏死斑点）
    if (r > 100 && r < 180 && g > 80 && g < 150 && b < 100) {
      brownPixels++
    }
    
    // 检测红色（锈病）
    if (r > 180 && g > 100 && g < 180 && b < 100) {
      redPixels++
    }
    
    // 检测白色（霉层）
    if (r > 200 && g > 200 && b > 200) {
      whitePixels++
    }
  }
  
  return {
    greenRatio: greenPixels / totalPixels,
    yellowRatio: yellowPixels / totalPixels,
    brownRatio: brownPixels / totalPixels,
    redRatio: redPixels / totalPixels,
    whiteRatio: whitePixels / totalPixels,
    totalPixels
  }
}

/**
 * 基础纹理特征提取
 */
const extractTextureFeatures = (data, width, height) => {
  let edgeCount = 0
  let contrastSum = 0
  
  for (let y = 1; y < height - 1; y++) {
    for (let x = 1; x < width - 1; x++) {
      const idx = (y * width + x) * 4
      const brightness = (data[idx] + data[idx + 1] + data[idx + 2]) / 3
      
      const rightIdx = (y * width + (x + 1)) * 4
      const rightBrightness = (data[rightIdx] + data[rightIdx + 1] + data[rightIdx + 2]) / 3
      
      const diff = Math.abs(brightness - rightBrightness)
      contrastSum += diff
      
      if (diff > 30) {
        edgeCount++
      }
    }
  }
  
  return {
    edgeRatio: edgeCount / (width * height),
    avgContrast: contrastSum / (width * height)
  }
}

/**
 * 基础亮度特征提取
 */
const extractBrightnessFeatures = (data) => {
  let totalBrightness = 0
  let darkPixels = 0
  let brightPixels = 0
  
  for (let i = 0; i < data.length; i += 4) {
    const brightness = (data[i] + data[i + 1] + data[i + 2]) / 3
    totalBrightness += brightness
    
    if (brightness < 50) {
      darkPixels++
    } else if (brightness > 200) {
      brightPixels++
    }
  }
  
  const avgBrightness = totalBrightness / (data.length / 4)
  
  return {
    avgBrightness,
    darkRatio: darkPixels / (data.length / 4),
    brightRatio: brightPixels / (data.length / 4)
  }
}

/**
 * 知识库匹配
 * 将提取的图片特征与知识库进行匹配
 */
export const matchWithKnowledgeBase = (imageFeatures) => {
  const allResults = []
  
  // 转换图片特征为知识库可识别的格式
  const featureColors = convertToKnowledgeBaseColors(imageFeatures)
  const featureShapes = convertToKnowledgeBaseShapes(imageFeatures)
  const featurePatterns = convertToKnowledgeBasePatterns(imageFeatures)
  
  // 匹配病害
  pestKnowledgeBase.diseases.forEach(disease => {
    const matchScore = calculateDiseaseMatchScore(
      featureColors,
      featureShapes,
      featurePatterns,
      disease
    )
    
    if (matchScore > 0.25) { // 降低阈值，提高召回率
      allResults.push({
        id: disease.id,
        name: disease.name,
        type: 'disease',
        crop: disease.crop,
        confidence: Math.round(matchScore * 100),
        severity: disease.severity,
        treatment: disease.treatment,
        prevention: disease.prevention,
        matchedFeatures: getMatchedFeatures(
          featureColors,
          featureShapes,
          featurePatterns,
          disease
        )
      })
    }
  })
  
  // 匹配虫害
  pestKnowledgeBase.pests.forEach(pest => {
    const matchScore = calculatePestMatchScore(
      featureColors,
      featureShapes,
      featurePatterns,
      pest
    )
    
    if (matchScore > 0.25) { // 降低阈值，提高召回率
      allResults.push({
        id: pest.id,
        name: pest.name,
        type: 'pest',
        crop: pest.crop,
        confidence: Math.round(matchScore * 100),
        severity: pest.severity,
        treatment: pest.treatment,
        prevention: pest.prevention,
        matchedFeatures: getMatchedFeatures(
          featureColors,
          featureShapes,
          featurePatterns,
          pest
        )
      })
    }
  })
  
  // 按置信度排序
  return allResults.sort((a, b) => b.confidence - a.confidence).slice(0, 5)
}

/**
 * 转换颜色特征到知识库格式
 */
const convertToKnowledgeBaseColors = (imageFeatures) => {
  const colors = []
  
  if (imageFeatures.colorDistribution) {
    const distribution = imageFeatures.colorDistribution
    
    if (distribution.green > 0.1) colors.push('绿色')
    if (distribution.dark_green > 0.1) colors.push('深绿色')
    if (distribution.yellow_green > 0.1) colors.push('黄绿色')
    if (distribution.yellow > 0.05) colors.push('黄色')
    if (distribution.orange > 0.05) colors.push('橙黄色')
    if (distribution.brown > 0.05) colors.push('褐色')
    if (distribution.red > 0.05) colors.push('红褐色')
    if (distribution.white > 0.05) colors.push('白色')
    if (distribution.gray > 0.05) colors.push('灰褐色')
  }
  
  // 如果没有检测到颜色，使用基础特征
  if (colors.length === 0) {
    if (imageFeatures.colors && imageFeatures.colors.greenRatio > 0.1) {
      colors.push('绿色')
    }
    if (imageFeatures.colors && imageFeatures.colors.yellowRatio > 0.05) {
      colors.push('黄色')
    }
    if (imageFeatures.colors && imageFeatures.colors.brownRatio > 0.05) {
      colors.push('褐色')
    }
    if (imageFeatures.colors && imageFeatures.colors.redRatio > 0.05) {
      colors.push('红褐色')
    }
    if (imageFeatures.colors && imageFeatures.colors.whiteRatio > 0.05) {
      colors.push('白色')
    }
  }
  
  return colors
}

/**
 * 转换形状特征到知识库格式
 */
const convertToKnowledgeBaseShapes = (imageFeatures) => {
  const shapes = []
  
  if (imageFeatures.shapeFeatures) {
    shapes.push(...imageFeatures.shapeFeatures)
  }
  
  if (imageFeatures.patternFeatures) {
    if (imageFeatures.patternFeatures.includes('斑点')) {
      shapes.push('圆形', '椭圆形')
    }
    if (imageFeatures.patternFeatures.includes('坏死')) {
      shapes.push('不规则形')
    }
  }
  
  return shapes
}

/**
 * 转换模式特征到知识库格式
 */
const convertToKnowledgeBasePatterns = (imageFeatures) => {
  const patterns = []
  
  if (imageFeatures.patternFeatures) {
    patterns.push(...imageFeatures.patternFeatures)
  }
  
  if (imageFeatures.diseaseFeatures) {
    patterns.push(...imageFeatures.diseaseFeatures)
  }
  
  return patterns
}

/**
 * 计算病害匹配分数
 */
const calculateDiseaseMatchScore = (featureColors, featureShapes, featurePatterns, disease) => {
  const rules = disease.confidenceRules
  let score = 0
  let matchCount = 0
  
  // 颜色匹配
  const colorMatch = disease.features.colors.some(color =>
    featureColors.some(fc => fc.includes(color) || color.includes(fc))
  )
  if (colorMatch) {
    score += rules.colorMatch
    matchCount++
  }
  
  // 形状匹配
  const shapeMatch = disease.features.shapes.some(shape =>
    featureShapes.some(fs => fs.includes(shape) || shape.includes(fs))
  )
  if (shapeMatch) {
    score += rules.shapeMatch
    matchCount++
  }
  
  // 模式匹配
  const patternMatch = disease.features.patterns.some(pattern =>
    featurePatterns.some(fp => fp.includes(pattern) || pattern.includes(fp))
  )
  if (patternMatch) {
    score += rules.patternMatch
    matchCount++
  }
  
  // 调整分数：至少匹配2个特征才认为相关
  if (matchCount >= 2) {
    return score
  } else if (matchCount === 1) {
    return score * 0.6 // 单个特征匹配，降低分数
  } else {
    return 0
  }
}

/**
 * 计算虫害匹配分数
 */
const calculatePestMatchScore = (featureColors, featureShapes, featurePatterns, pest) => {
  const rules = pest.confidenceRules
  let score = 0
  let matchCount = 0
  
  // 颜色匹配
  const colorMatch = pest.features.colors.some(color =>
    featureColors.some(fc => fc.includes(color) || color.includes(fc))
  )
  if (colorMatch) {
    score += rules.colorMatch
    matchCount++
  }
  
  // 形状匹配
  const shapeMatch = pest.features.shapes.some(shape =>
    featureShapes.some(fs => fs.includes(shape) || shape.includes(fs))
  )
  if (shapeMatch) {
    score += rules.shapeMatch
    matchCount++
  }
  
  // 模式匹配
  const patternMatch = pest.features.patterns.some(pattern =>
    featurePatterns.some(fp => fp.includes(pattern) || pattern.includes(fp))
  )
  if (patternMatch) {
    score += rules.patternMatch
    matchCount++
  }
  
  // 调整分数
  if (matchCount >= 2) {
    return score
  } else if (matchCount === 1) {
    return score * 0.6
  } else {
    return 0
  }
}

/**
 * 获取匹配的特征
 */
const getMatchedFeatures = (featureColors, featureShapes, featurePatterns, item) => {
  const matched = []
  
  // 匹配的颜色
  item.features.colors.forEach(color => {
    if (featureColors.some(fc => fc.includes(color) || color.includes(fc))) {
      matched.push({ type: '颜色', value: color })
    }
  })
  
  // 匹配的形状
  item.features.shapes.forEach(shape => {
    if (featureShapes.some(fs => fs.includes(shape) || shape.includes(fs))) {
      matched.push({ type: '形状', value: shape })
    }
  })
  
  // 匹配的模式
  item.features.patterns.forEach(pattern => {
    if (featurePatterns.some(fp => fp.includes(pattern) || pattern.includes(fp))) {
      matched.push({ type: '模式', value: pattern })
    }
  })
  
  return matched
}

/**
 * 评估图片相关性（增强版）
 */
export const evaluateEnhancedRelevance = (imageFeatures) => {
  const { colors, texture, brightness, colorDistribution, plantFeatures, diseaseFeatures } = imageFeatures
  
  // 规则1：图片应该有一定的绿色（植物叶片）
  const hasVegetation = colors.greenRatio > 0.2 || 
                        (colorDistribution && colorDistribution.green > 0.1)
  
  // 规则2：应该有一些病害症状的颜色（黄色、褐色、红色、白色）
  const hasDiseaseSymptoms = colors.yellowRatio > 0.03 || 
                             colors.brownRatio > 0.03 ||
                             colors.redRatio > 0.03 ||
                             (colorDistribution && (
                               colorDistribution.yellow > 0.03 ||
                               colorDistribution.brown > 0.03 ||
                               colorDistribution.red > 0.03
                             ))
  
  // 规则3：图片不能太暗或太亮
  const properLighting = brightness.avgBrightness > 50 && brightness.avgBrightness < 220
  
  // 规则4：应该有一定的纹理（叶片、斑点等）
  const hasTexture = texture.edgeRatio > 0.08
  
  // 规则5：不能是纯色图片
  const notSolidColor = colors.greenRatio < 0.95
  
  // 规则6：应该有植物特征
  const hasPlantFeatures = plantFeatures && plantFeatures.length > 0
  
  // 规则7：应该有病害特征（但不强制要求，因为健康植物也可能被识别）
  const hasDiseaseFeatures = diseaseFeatures && diseaseFeatures.length > 0
  
  // 综合判断
  const relevanceScore = 
    (hasVegetation ? 1 : 0) * 0.25 +
    (hasDiseaseSymptoms ? 1 : 0) * 0.25 +
    (properLighting ? 1 : 0) * 0.15 +
    (hasTexture ? 1 : 0) * 0.15 +
    (notSolidColor ? 1 : 0) * 0.1 +
    (hasPlantFeatures ? 1 : 0) * 0.05 +
    (hasDiseaseFeatures ? 1 : 0) * 0.05
  
  return {
    isRelevant: relevanceScore > 0.35, // 降低阈值
    score: relevanceScore,
    details: {
      hasVegetation,
      hasDiseaseSymptoms,
      properLighting,
      hasTexture,
      notSolidColor,
      hasPlantFeatures,
      hasDiseaseFeatures
    }
  }
}
