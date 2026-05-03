// 病虫害知识库 - 真实数据扩充版
// 包含常见作物病虫害的特征、防治方案等信息
// 数据来源：中国农业科学院、植物保护研究所、农业技术推广中心

export const pestKnowledgeBase = {
  // 水稻病害
  diseases: [
    {
      id: 'rice_blast',
      name: '稻瘟病',
      type: 'disease',
      crop: '水稻',
      severity: '高',
      features: {
        colors: ['褐色', '黑褐色', '灰褐色', '深褐色', '红褐色'],
        shapes: ['椭圆形', '纺锤形', '梭形', '圆形'],
        patterns: ['斑点', '病斑', '坏死斑', '霉层'],
        parts: ['叶片', '叶鞘', '穗颈', '谷粒'],
        symptoms: [
          '叶片出现褐色斑点',
          '病斑呈纺锤形或椭圆形',
          '中心灰白色边缘褐色',
          '严重时病斑连成片',
          '穗颈变黑腐烂'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用三环唑、富士一号、稻瘟灵、咪酰胺等药剂防治。注意：发病初期及时喷药，避免大流行。合理施肥，增施磷钾肥，避免偏施氮肥。',
      prevention: '选用抗病品种，种子消毒，合理密植，科学管水。'
    },
    {
      id: 'rice_bacterial_blight',
      name: '水稻细菌性条斑病',
      type: 'disease',
      crop: '水稻',
      severity: '中',
      features: {
        colors: ['暗绿色', '水浸状', '灰褐色', '暗褐色'],
        shapes: ['条状', '线状', '长条形', '短线状'],
        patterns: ['条斑', '条状病斑', '水渍状'],
        parts: ['叶片', '叶鞘'],
        symptoms: [
          '叶片出现暗绿色水浸状条斑',
          '病斑沿叶脉扩展',
          '后期变为灰褐色',
          '严重时叶片枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.4,
        patternMatch: 0.2
      },
      treatment: '使用农用链霉素、叶枯唑、噻森铜等药剂防治。注意：避免偏施氮肥，合理密植，及时清除病残体。',
      prevention: '选用抗病品种，种子消毒，避免大水漫灌。'
    },
    {
      id: 'rice_sheath_blight',
      name: '水稻纹枯病',
      type: 'disease',
      crop: '水稻',
      severity: '中',
      features: {
        colors: ['灰褐色', '褐色', '暗灰色', '灰白色'],
        shapes: ['云纹状', '不规则形', '椭圆形'],
        patterns: ['云纹', '病斑', '轮纹'],
        parts: ['叶鞘', '茎秆'],
        symptoms: [
          '叶鞘出现云纹状病斑',
          '病斑边缘褐色中间灰白色',
          '严重时茎秆腐烂',
          '植株倒伏'
        ]
      },
      confidenceRules: {
        colorMatch: 0.35,
        shapeMatch: 0.35,
        patternMatch: 0.3
      },
      treatment: '使用井冈霉素、己唑醇、苯醚甲环唑等药剂防治。注意：合理密植，增施钾肥，避免偏施氮肥。',
      prevention: '选用抗病品种，合理管水，及时排水晒田。'
    },
    {
      id: 'rice_false_smut',
      name: '水稻稻曲病',
      type: 'disease',
      crop: '水稻',
      severity: '中',
      features: {
        colors: ['黄色', '橙黄色', '黄绿色', '暗黄色'],
        shapes: ['椭圆形', '球形', '不规则形'],
        patterns: ['曲粒', '孢子', '粉末'],
        parts: ['谷粒', '穗部'],
        symptoms: [
          '谷粒出现黄色或橙黄色病斑',
          '病斑表面有黄绿色粉末',
          '严重时谷粒破裂'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用丙环唑、戊唑醇、己唑醇等药剂防治。注意：在破口前7-10天和齐穗期各喷药一次。',
      prevention: '选用抗病品种，适时播种，避免偏施氮肥。'
    },
    {
      id: 'rice_bacterial_leaf_streak',
      name: '水稻白叶枯病',
      type: 'disease',
      crop: '水稻',
      severity: '高',
      features: {
        colors: ['淡黄色', '黄白色', '灰白色'],
        shapes: ['条状', '线状', '长条形'],
        patterns: ['萎蔫', '枯死', '干枯'],
        parts: ['叶片'],
        symptoms: [
          '叶片从叶尖开始变黄',
          '沿叶脉向下扩展',
          '叶片卷曲枯死',
          '严重时整株枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.4,
        patternMatch: 0.2
      },
      treatment: '使用农用链霉素、叶枯唑、噻森铜等药剂防治。注意：发病初期及时喷药，避免大流行。',
      prevention: '选用抗病品种，种子消毒，避免大水漫灌。'
    },
    {
      id: 'rice_seedling_blight',
      name: '水稻立枯病',
      type: 'disease',
      crop: '水稻',
      severity: '中',
      features: {
        colors: ['黄褐色', '褐色', '黑褐色'],
        shapes: ['条状', '线状'],
        patterns: ['萎蔫', '枯死', '腐烂'],
        parts: ['幼苗', '茎基部'],
        symptoms: [
          '幼苗茎基部变褐',
          '幼苗萎蔫枯死',
          '根茎腐烂',
          '成片枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用恶霉灵、甲霜灵、代森锰锌等药剂防治。注意：做好苗床管理，避免低温高湿。',
      prevention: '种子消毒，苗床消毒，合理控制温湿度。'
    },
    {
      id: 'rice_smut',
      name: '水稻腥黑粉病',
      type: 'disease',
      crop: '水稻',
      severity: '中',
      features: {
        colors: ['黑色', '黑褐色', '灰黑色'],
        shapes: ['椭圆形', '球形'],
        patterns: ['孢子', '黑粉'],
        parts: ['谷粒'],
        symptoms: [
          '谷粒内有黑粉',
          '谷粒破裂散出黑粉',
          '有腥臭味'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用戊唑醇、苯醚甲环唑等药剂拌种。注意：种子消毒，避免带菌种子。',
      prevention: '选用无病种子，种子消毒，轮作倒茬。'
    },
    {
      id: 'rice_dwarf',
      name: '水稻矮缩病',
      type: 'disease',
      crop: '水稻',
      severity: '高',
      features: {
        colors: ['深绿色', '黄绿色'],
        shapes: ['矮化', '畸形'],
        patterns: ['矮缩', '分蘖增多'],
        parts: ['植株', '叶片'],
        symptoms: [
          '植株矮小',
          '分蘖增多',
          '叶片深绿色',
          '不抽穗或少抽穗'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '主要靠防治传毒媒介（褐飞虱、白背飞虱）。注意：及时防治稻飞虱，避免病毒传播。',
      prevention: '选用抗病品种，及时防治稻飞虱，清除田间杂草。'
    },

    // 小麦病害
    {
      id: 'wheat_powdery_mildew',
      name: '小麦白粉病',
      type: 'disease',
      crop: '小麦',
      severity: '中',
      features: {
        colors: ['白色', '灰白色', '乳白色', '浅灰色'],
        shapes: ['圆形', '椭圆形', '不规则'],
        patterns: ['粉状物', '霉层', '白粉'],
        parts: ['叶片正面', '茎秆', '穗部'],
        symptoms: [
          '叶片表面出现白色粉状物',
          '病斑呈圆形或椭圆形',
          '后期出现黑色小点',
          '严重时叶片枯黄'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.2,
        patternMatch: 0.3
      },
      treatment: '使用粉锈宁、多抗霉素、醚菌酯、三唑酮等药剂防治。注意：发病初期及时喷药，避免过度密植。',
      prevention: '选用抗病品种，合理密植，改善田间通风透光条件。'
    },
    {
      id: 'wheat_rust',
      name: '小麦锈病',
      type: 'disease',
      crop: '小麦',
      severity: '高',
      features: {
        colors: ['红褐色', '黄褐色', '橘黄色', '橙红色'],
        shapes: ['圆形', '椭圆形', '短线状'],
        patterns: ['锈孢子', '夏孢子堆', '粉状物'],
        parts: ['叶片正面', '叶鞘', '茎秆'],
        symptoms: [
          '叶片出现红褐色或黄褐色斑点',
          '病斑表面有锈色粉末',
          '严重时叶片枯黄',
          '病斑呈椭圆形或圆形'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.2,
        patternMatch: 0.3
      },
      treatment: '使用三唑酮、烯唑醇、丙环唑、苯醚甲环唑等药剂防治。注意：选用抗病品种，适期播种。',
      prevention: '选用抗病品种，适期播种，避免偏施氮肥。'
    },
    {
      id: 'wheat_head_blight',
      name: '小麦赤霉病',
      type: 'disease',
      crop: '小麦',
      severity: '高',
      features: {
        colors: ['粉红色', '浅红色', '粉白色', '红褐色'],
        shapes: ['椭圆形', '圆形'],
        patterns: ['霉层', '孢子'],
        parts: ['穗部', '小穗'],
        symptoms: [
          '穗部出现粉红色或浅红色霉层',
          '病粒干瘪皱缩',
          '严重时整穗腐烂'
        ]
      },
      confidenceRules: {
        colorMatch: 0.6,
        shapeMatch: 0.2,
        patternMatch: 0.2
      },
      treatment: '使用多菌灵、甲基托布津、咪酰胺、戊唑醇等药剂防治。注意：抽穗扬花期是防治关键期。',
      prevention: '选用抗病品种，及时清除病残体，合理密植。'
    },
    {
      id: 'wheat_smut',
      name: '小麦腥黑穗病',
      type: 'disease',
      crop: '小麦',
      severity: '中',
      features: {
        colors: ['黑色', '黑褐色', '灰黑色'],
        shapes: ['椭圆形', '球形'],
        patterns: ['孢子', '黑粉'],
        parts: ['麦粒'],
        symptoms: [
          '麦粒内有黑粉',
          '麦粒破裂散出黑粉',
          '有腥臭味'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用戊唑醇、苯醚甲环唑等药剂拌种。注意：种子消毒，避免带菌种子。',
      prevention: '选用无病种子，种子消毒，轮作倒茬。'
    },
    {
      id: 'wheat_scab',
      name: '小麦全蚀病',
      type: 'disease',
      crop: '小麦',
      severity: '高',
      features: {
        colors: ['黑褐色', '黑灰色', '灰褐色'],
        shapes: ['条状', '线状'],
        patterns: ['黑根', '腐烂'],
        parts: ['根部', '茎基部'],
        symptoms: [
          '根部变黑腐烂',
          '茎基部变黑',
          '植株枯死',
          '成片枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.4,
        patternMatch: 0.2
      },
      treatment: '使用苯醚甲环唑、丙环唑等药剂灌根。注意：发病初期及时防治。',
      prevention: '选用抗病品种，轮作倒茬，增施有机肥。'
    },
    {
      id: 'wheat_leaf_spot',
      name: '小麦叶斑病',
      type: 'disease',
      crop: '小麦',
      severity: '中',
      features: {
        colors: ['褐色', '黑褐色', '灰褐色'],
        shapes: ['椭圆形', '圆形', '不规则形'],
        patterns: ['斑点', '病斑'],
        parts: ['叶片'],
        symptoms: [
          '叶片出现褐色斑点',
          '病斑呈椭圆形或圆形',
          '严重时病斑连片',
          '叶片枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用代森锰锌、苯醚甲环唑、甲基硫菌灵等药剂防治。注意：发病初期及时喷药。',
      prevention: '选用抗病品种，合理密植，增施钾肥。'
    },

    // 玉米病害
    {
      id: 'corn_southern_leaf_blight',
      name: '玉米南方锈病',
      type: 'disease',
      crop: '玉米',
      severity: '中',
      features: {
        colors: ['红褐色', '橘黄色', '橙褐色', '黄褐色'],
        shapes: ['圆形', '椭圆形', '短线状'],
        patterns: ['锈孢子', '夏孢子堆', '粉状物'],
        parts: ['叶片'],
        symptoms: [
          '叶片出现红褐色或橘黄色斑点',
          '病斑表面有锈色粉末',
          '严重时叶片枯黄'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.2,
        patternMatch: 0.3
      },
      treatment: '使用三唑酮、苯醚甲环唑、丙环唑等药剂防治。注意：选用抗病品种，合理密植。',
      prevention: '选用抗病品种，合理密植，及时清除病残体。'
    },
    {
      id: 'corn_northern_leaf_blight',
      name: '玉米大斑病',
      type: 'disease',
      crop: '玉米',
      severity: '中',
      features: {
        colors: ['褐色', '灰褐色', '深褐色', '黑褐色'],
        shapes: ['长梭形', '椭圆形', '长条形'],
        patterns: ['病斑', '轮纹', '同心轮纹'],
        parts: ['叶片'],
        symptoms: [
          '叶片出现长梭形或椭圆形病斑',
          '病斑灰褐色边缘深褐色',
          '严重时病斑连片'
        ]
      },
      confidenceRules: {
        colorMatch: 0.35,
        shapeMatch: 0.4,
        patternMatch: 0.25
      },
      treatment: '使用代森锰锌、丙环唑、苯醚甲环唑等药剂防治。注意：轮作倒茬，清除病残体。',
      prevention: '选用抗病品种，合理密植，改善通风透光。'
    },
    {
      id: 'corn_gray_spot',
      name: '玉米灰斑病',
      type: 'disease',
      crop: '玉米',
      severity: '中',
      features: {
        colors: ['灰色', '灰褐色', '浅灰色'],
        shapes: ['圆形', '椭圆形', '不规则形'],
        patterns: ['斑点', '霉层'],
        parts: ['叶片'],
        symptoms: [
          '叶片出现圆形或椭圆形病斑',
          '病斑灰色或灰褐色',
          '后期病斑上产生黑色霉层'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用代森锰锌、苯醚甲环唑、丙环唑等药剂防治。注意：合理密植，改善通风透光。',
      prevention: '选用抗病品种，合理密植，增施钾肥。'
    },
    {
      id: 'corn_smut',
      name: '玉米丝黑穗病',
      type: 'disease',
      crop: '玉米',
      severity: '中',
      features: {
        colors: ['黑色', '黑褐色', '灰黑色'],
        shapes: ['椭圆形', '球形'],
        patterns: ['孢子', '黑粉'],
        parts: ['果穗'],
        symptoms: [
          '果穗内有黑粉',
          '果穗破裂散出黑粉',
          '有腥臭味'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用戊唑醇、苯醚甲环唑等药剂拌种。注意：种子消毒，避免带菌种子。',
      prevention: '选用无病种子，种子消毒，轮作倒茬。'
    },
    {
      id: 'corn_stalk_rot',
      name: '玉米茎腐病',
      type: 'disease',
      crop: '玉米',
      severity: '高',
      features: {
        colors: ['红褐色', '褐色', '黑褐色'],
        shapes: ['条状', '线状'],
        patterns: ['腐烂', '软腐'],
        parts: ['茎秆'],
        symptoms: [
          '茎秆变褐腐烂',
          '植株倒伏',
          '叶片枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.4,
        patternMatch: 0.2
      },
      treatment: '使用甲基硫菌灵、多菌灵等药剂灌根。注意：发病初期及时防治。',
      prevention: '选用抗病品种，合理密植，增施钾肥。'
    },
    {
      id: 'corn_ear_rot',
      name: '玉米穗腐病',
      type: 'disease',
      crop: '玉米',
      severity: '高',
      features: {
        colors: ['粉红色', '红色', '白色', '绿色'],
        shapes: ['不规则形', '圆形'],
        patterns: ['霉层', '腐烂'],
        parts: ['果穗'],
        symptoms: [
          '果穗出现霉层',
          '籽粒腐烂',
          '有霉味'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用多菌灵、甲基托布津等药剂防治。注意：及时采收，避免霉变。',
      prevention: '选用抗病品种，适时采收，避免高温高湿。'
    },

    // 棉花病害
    {
      id: 'cotton_blight',
      name: '棉花枯萎病',
      type: 'disease',
      crop: '棉花',
      severity: '高',
      features: {
        colors: ['黄色', '黄绿色', '红褐色', '黑褐色'],
        shapes: ['条状', '线状', '不规则形'],
        patterns: ['维管束变褐', '枯萎'],
        parts: ['叶片', '茎秆', '植株'],
        symptoms: [
          '叶片出现黄色或黄绿色',
          '茎秆维管束变褐色',
          '植株萎蔫枯死',
          '严重时整株死亡'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用咯菌腈、枯草芽孢杆菌等药剂防治。注意：选用抗病品种，合理轮作。',
      prevention: '选用抗病品种，轮作倒茬，增施有机肥。'
    },
    {
      id: 'cotton_fusarium_wilt',
      name: '棉花黄萎病',
      type: 'disease',
      crop: '棉花',
      severity: '高',
      features: {
        colors: ['黄色', '黄绿色', '黄褐色'],
        shapes: ['不规则形', '条状'],
        patterns: ['维管束变褐', '枯萎'],
        parts: ['叶片', '茎秆'],
        symptoms: [
          '叶片出现黄色或黄绿色',
          '茎秆维管束变褐色',
          '植株萎蔫',
          '叶片枯死不脱落'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用枯草芽孢杆菌、哈茨木霉等生物制剂防治。注意：轮作倒茬，增施有机肥。',
      prevention: '选用抗病品种，轮作倒茬，增施有机肥。'
    },
    {
      id: 'cotton_boll_rot',
      name: '棉花红腐病',
      type: 'disease',
      crop: '棉花',
      severity: '中',
      features: {
        colors: ['粉红色', '红色', '红褐色'],
        shapes: ['圆形', '椭圆形'],
        patterns: ['霉层', '腐烂'],
        parts: ['棉铃'],
        symptoms: [
          '棉铃出现粉红色霉层',
          '棉铃腐烂',
          '纤维变红'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用多菌灵、甲基托布津等药剂防治。注意：及时采收，避免霉变。',
      prevention: '选用抗病品种，及时采收，避免高温高湿。'
    },
    {
      id: 'cotton_damping_off',
      name: '棉花立枯病',
      type: 'disease',
      crop: '棉花',
      severity: '中',
      features: {
        colors: ['褐色', '黑褐色'],
        shapes: ['条状', '线状'],
        patterns: ['腐烂', '枯死'],
        parts: ['幼苗', '茎基部'],
        symptoms: [
          '幼苗茎基部变褐',
          '幼苗萎蔫枯死',
          '根茎腐烂'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用恶霉灵、甲霜灵、代森锰锌等药剂防治。注意：做好苗床管理，避免低温高湿。',
      prevention: '种子消毒，苗床消毒，合理控制温湿度。'
    },

    // 大豆病害
    {
      id: 'soybean_frogeye_blight',
      name: '大豆霜霉病',
      type: 'disease',
      crop: '大豆',
      severity: '中',
      features: {
        colors: ['淡绿色', '黄绿色', '灰白色'],
        shapes: ['圆形', '不规则形', '多角形'],
        patterns: ['霉层', '斑点'],
        parts: ['叶片背面'],
        symptoms: [
          '叶片背面出现淡绿色或黄绿色病斑',
          '病斑上产生灰白色霉层',
          '严重时叶片枯黄'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用甲霜灵、代森锰锌、霜脲氰等药剂防治。注意：合理密植，改善田间通风。',
      prevention: '选用抗病品种，合理密植，改善田间通风。'
    },
    {
      id: 'soybean_bacterial_pustule',
      name: '大豆细菌性斑点病',
      type: 'disease',
      crop: '大豆',
      severity: '中',
      features: {
        colors: ['褐色', '黑褐色', '深褐色'],
        shapes: ['圆形', '椭圆形', '不规则形'],
        patterns: ['斑点', '病斑'],
        parts: ['叶片'],
        symptoms: [
          '叶片出现褐色或黑褐色斑点',
          '病斑周围有黄色晕圈',
          '严重时病斑连片'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用链霉素、春雷霉素、中生菌素等药剂防治。注意：种子消毒，及时清除病残体。',
      prevention: '选用抗病品种，种子消毒，及时清除病残体。'
    },
    {
      id: 'soybean_mosaic_virus',
      name: '大豆花叶病毒病',
      type: 'disease',
      crop: '大豆',
      severity: '高',
      features: {
        colors: ['黄绿色', '深绿色', '黄绿色'],
        shapes: ['花叶', '皱缩', '畸形'],
        patterns: ['花叶', '皱缩', '斑驳'],
        parts: ['叶片', '植株'],
        symptoms: [
          '叶片出现黄绿色相间花叶',
          '叶片皱缩畸形',
          '植株矮化',
          '豆粒畸形'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.4,
        patternMatch: 0.2
      },
      treatment: '主要靠种子检疫和防治传毒媒介（蚜虫）。注意：选用抗病品种，及时防治蚜虫。',
      prevention: '选用抗病品种，及时防治蚜虫，清除田间杂草。'
    },
    {
      id: 'soybean_rust',
      name: '大豆锈病',
      type: 'disease',
      crop: '大豆',
      severity: '高',
      features: {
        colors: ['红褐色', '黄褐色', '橘黄色'],
        shapes: ['圆形', '椭圆形'],
        patterns: ['锈孢子', '夏孢子堆', '粉状物'],
        parts: ['叶片背面'],
        symptoms: [
          '叶片背面出现红褐色斑点',
          '病斑表面有锈色粉末',
          '严重时叶片枯黄'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.2,
        patternMatch: 0.3
      },
      treatment: '使用三唑酮、苯醚甲环唑、丙环唑等药剂防治。注意：发病初期及时喷药。',
      prevention: '选用抗病品种，合理密植，及时清除病残体。'
    },
    {
      id: 'soybean_stem_canker',
      name: '大豆茎枯病',
      type: 'disease',
      crop: '大豆',
      severity: '中',
      features: {
        colors: ['褐色', '黑褐色', '灰褐色'],
        shapes: ['条状', '线状'],
        patterns: ['腐烂', '枯死'],
        parts: ['茎秆'],
        symptoms: [
          '茎秆出现褐色病斑',
          '茎秆腐烂',
          '植株枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.4,
        patternMatch: 0.2
      },
      treatment: '使用甲基硫菌灵、多菌灵等药剂防治。注意：发病初期及时喷药。',
      prevention: '选用抗病品种，合理密植，增施钾肥。'
    },

    // 蔬菜病害
    {
      id: 'vegetable_downy_mildew',
      name: '蔬菜霜霉病',
      type: 'disease',
      crop: '蔬菜',
      severity: '中',
      features: {
        colors: ['淡绿色', '黄绿色', '灰白色'],
        shapes: ['圆形', '不规则形', '多角形'],
        patterns: ['霉层', '斑点'],
        parts: ['叶片背面'],
        symptoms: [
          '叶片背面出现淡绿色或黄绿色病斑',
          '病斑上产生灰白色霉层'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用甲霜灵、代森锰锌、霜脲氰等药剂防治。注意：合理密植，改善通风透光。',
      prevention: '选用抗病品种，合理密植，改善通风透光。'
    },
    {
      id: 'vegetable_powdery_mildew',
      name: '蔬菜白粉病',
      type: 'disease',
      crop: '蔬菜',
      severity: '中',
      features: {
        colors: ['白色', '灰白色', '乳白色'],
        shapes: ['圆形', '椭圆形', '不规则'],
        patterns: ['粉状物', '霉层', '白粉'],
        parts: ['叶片正面', '茎秆'],
        symptoms: [
          '叶片表面出现白色粉状物',
          '病斑呈圆形或椭圆形'
        ]
      },
      confidenceRules: {
        colorMatch: 0.6,
        shapeMatch: 0.2,
        patternMatch: 0.2
      },
      treatment: '使用粉锈宁、多抗霉素、醚菌酯等药剂防治。注意：改善通风透光条件。',
      prevention: '选用抗病品种，合理密植，改善通风透光。'
    },
    {
      id: 'vegetable_phytophthora',
      name: '蔬菜疫病',
      type: 'disease',
      crop: '蔬菜',
      severity: '高',
      features: {
        colors: ['暗绿色', '水浸状', '褐色', '黑褐色'],
        shapes: ['不规则形', '大斑', '圆形'],
        patterns: ['病斑', '霉层'],
        parts: ['叶片', '果实', '茎秆'],
        symptoms: [
          '叶片出现暗绿色水浸状病斑',
          '病斑迅速扩大变褐',
          '严重时叶片腐烂'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用甲霜灵、代森锰锌、烯酰吗啉等药剂防治。注意：避免大水漫灌，及时排水。',
      prevention: '选用抗病品种，合理密植，避免大水漫灌。'
    },
    {
      id: 'vegetable_gray_mold',
      name: '蔬菜灰霉病',
      type: 'disease',
      crop: '蔬菜',
      severity: '中',
      features: {
        colors: ['灰色', '灰褐色', '浅灰色'],
        shapes: ['圆形', '椭圆形', '不规则形'],
        patterns: ['霉层', '腐烂'],
        parts: ['叶片', '果实', '花'],
        symptoms: [
          '叶片或果实上出现灰色霉层',
          '病斑呈圆形或不规则形',
          '严重时腐烂'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用嘧霉胺、腐霉利、异菌脲等药剂防治。注意：控制湿度，及时通风。',
      prevention: '选用抗病品种，控制湿度，及时通风。'
    },
    {
      id: 'vegetable_bacterial_spot',
      name: '蔬菜细菌性斑点病',
      type: 'disease',
      crop: '蔬菜',
      severity: '中',
      features: {
        colors: ['褐色', '黑褐色', '深褐色'],
        shapes: ['圆形', '椭圆形', '不规则形'],
        patterns: ['斑点', '病斑'],
        parts: ['叶片', '果实'],
        symptoms: [
          '叶片或果实出现褐色斑点',
          '病斑周围有黄色晕圈',
          '严重时病斑连片'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用链霉素、春雷霉素、中生菌素等药剂防治。注意：种子消毒，及时清除病残体。',
      prevention: '选用抗病品种，种子消毒，及时清除病残体。'
    },
    {
      id: 'vegetable_mosaic_virus',
      name: '蔬菜病毒病',
      type: 'disease',
      crop: '蔬菜',
      severity: '高',
      features: {
        colors: ['黄绿色', '深绿色', '黄色'],
        shapes: ['花叶', '皱缩', '畸形'],
        patterns: ['花叶', '皱缩', '斑驳'],
        parts: ['叶片', '植株'],
        symptoms: [
          '叶片出现黄绿色相间花叶',
          '叶片皱缩畸形',
          '植株矮化'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.4,
        patternMatch: 0.2
      },
      treatment: '主要靠防治传毒媒介（蚜虫、粉虱）。注意：选用抗病品种，及时防治蚜虫。',
      prevention: '选用抗病品种，及时防治蚜虫，清除田间杂草。'
    },
    {
      id: 'vegetable_root_knot',
      name: '蔬菜根结线虫病',
      type: 'disease',
      crop: '蔬菜',
      severity: '高',
      features: {
        colors: ['黄色', '黄绿色', '萎蔫'],
        shapes: ['根结', '瘤状'],
        patterns: ['根结', '萎蔫'],
        parts: ['根部'],
        symptoms: [
          '根部出现根结',
          '根结呈瘤状',
          '植株萎蔫',
          '生长不良'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.5,
        patternMatch: 0.2
      },
      treatment: '使用阿维菌素、噻唑膦等药剂灌根。注意：轮作倒茬，避免连作。',
      prevention: '选用抗病品种，轮作倒茬，土壤消毒。'
    },

    // 果树病害
    {
      id: 'fruit_tree_brown_rot',
      name: '果树褐腐病',
      type: 'disease',
      crop: '果树',
      severity: '高',
      features: {
        colors: ['褐色', '深褐色', '黑褐色'],
        shapes: ['圆形', '不规则形', '软腐状'],
        patterns: ['病斑', '腐烂', '软腐'],
        parts: ['果实'],
        symptoms: [
          '果实出现褐色或深褐色病斑',
          '病斑表面有轮纹或同心轮纹',
          '果实软腐腐烂',
          '有酒糟味'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用多菌灵、甲基托布津、咪酰胺等药剂防治。注意：及时摘除病果，避免果实受伤。',
      prevention: '及时摘除病果，避免果实受伤，合理修剪。'
    },
    {
      id: 'fruit_tree_canker',
      name: '果树腐烂病',
      type: 'disease',
      crop: '果树',
      severity: '高',
      features: {
        colors: ['红褐色', '黑褐色', '深褐色'],
        shapes: ['椭圆形', '不规则形', '溃疡状'],
        patterns: ['病斑', '溃疡', '腐烂'],
        parts: ['枝干', '树皮', '果实'],
        symptoms: [
          '枝干出现红褐色或黑褐色病斑',
          '病斑凹陷溃疡',
          '严重时枝干环腐枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.4,
        patternMatch: 0.2
      },
      treatment: '使用石硫合剂、代森锰锌、多菌灵等药剂防治。注意：及时刮除病斑并涂抹药剂。',
      prevention: '合理修剪，增强树势，及时刮除病斑。'
    },
    {
      id: 'fruit_tree_scab',
      name: '果树疮痂病',
      type: 'disease',
      crop: '果树',
      severity: '中',
      features: {
        colors: ['褐色', '黑褐色', '红褐色'],
        shapes: ['圆形', '椭圆形', '不规则形'],
        patterns: ['疮痂', '病斑', '粗糙'],
        parts: ['果实', '叶片'],
        symptoms: [
          '果实表面出现褐色疮痂',
          '疮痂呈圆形或椭圆形',
          '叶片出现病斑'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用代森锰锌、苯醚甲环唑、甲基托布津等药剂防治。注意：合理修剪，改善通风透光。',
      prevention: '选用抗病品种，合理修剪，改善通风透光。'
    },
    {
      id: 'fruit_tree_powdery_mildew',
      name: '果树白粉病',
      type: 'disease',
      crop: '果树',
      severity: '中',
      features: {
        colors: ['白色', '灰白色', '乳白色'],
        shapes: ['圆形', '椭圆形', '不规则'],
        patterns: ['粉状物', '霉层', '白粉'],
        parts: ['叶片', '果实', '嫩梢'],
        symptoms: [
          '叶片表面出现白色粉状物',
          '病斑呈圆形或椭圆形',
          '果实表面出现白色粉状物'
        ]
      },
      confidenceRules: {
        colorMatch: 0.6,
        shapeMatch: 0.2,
        patternMatch: 0.2
      },
      treatment: '使用粉锈宁、多抗霉素、醚菌酯等药剂防治。注意：合理修剪，改善通风透光。',
      prevention: '选用抗病品种，合理修剪，改善通风透光。'
    },
    {
      id: 'fruit_tree_anthracnose',
      name: '果树炭疽病',
      type: 'disease',
      crop: '果树',
      severity: '高',
      features: {
        colors: ['褐色', '黑褐色', '红褐色'],
        shapes: ['圆形', '椭圆形', '不规则形'],
        patterns: ['病斑', '轮纹', '同心轮纹'],
        parts: ['果实', '叶片'],
        symptoms: [
          '果实出现褐色或黑褐色病斑',
          '病斑表面有轮纹或同心轮纹',
          '严重时果实腐烂'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用多菌灵、甲基托布津、咪酰胺等药剂防治。注意：及时摘除病果，避免果实受伤。',
      prevention: '选用抗病品种，合理修剪，改善通风透光。'
    },
    {
      id: 'fruit_tree_leaf_spot',
      name: '果树叶斑病',
      type: 'disease',
      crop: '果树',
      severity: '中',
      features: {
        colors: ['褐色', '黑褐色', '灰褐色'],
        shapes: ['圆形', '椭圆形', '不规则形'],
        patterns: ['斑点', '病斑'],
        parts: ['叶片'],
        symptoms: [
          '叶片出现褐色斑点',
          '病斑呈圆形或椭圆形',
          '严重时病斑连片',
          '叶片枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用代森锰锌、苯醚甲环唑、甲基硫菌灵等药剂防治。注意：合理修剪，改善通风透光。',
      prevention: '选用抗病品种，合理修剪，改善通风透光。'
    }
  ],
  
  // 虫害
  pests: [
    {
      id: 'rice_planthopper',
      name: '稻飞虱',
      type: 'pest',
      crop: '水稻',
      severity: '高',
      features: {
        colors: ['黄绿色', '淡黄色', '褐黄色', '灰黄色'],
        shapes: ['椭圆形', '卵形', '长椭圆形'],
        patterns: ['虫体', '成虫', '若虫'],
        size: 'small',
        bodyParts: ['成虫', '若虫', '卵'],
        symptoms: [
          '叶片出现黄化',
          '植株矮化',
          '传播病毒病',
          '成虫和若虫在植株下部栖息'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用噻嗪酮、吡虫啉、烯啶虫胺、呋虫胺等药剂防治。注意：统一防治，避免迁飞。飞虱大发生时及时防治。',
      prevention: '选用抗虫品种，合理密植，保护天敌。'
    },
    {
      id: 'rice_leaf_roller',
      name: '稻纵卷叶螟',
      type: 'pest',
      crop: '水稻',
      severity: '中',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['卷曲状', '管状', '筒状'],
        patterns: ['卷叶', '虫体', '粪便'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫', '蛹'],
        symptoms: [
          '叶片卷曲呈筒状',
          '叶片出现白斑',
          '幼虫取食叶片',
          '幼虫吐丝将叶片纵卷'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用阿维菌素、甲维盐、氯虫苯甲酰胺、茚虫威等药剂防治。注意：卵孵化盛期是防治关键期。',
      prevention: '合理密植，保护天敌，适时用药。'
    },
    {
      id: 'rice_stem_borer',
      name: '二化螟',
      type: 'pest',
      crop: '水稻',
      severity: '高',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['虫洞', '隧道', '圆柱形'],
        patterns: ['虫孔', '蛀孔', '隧道'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '茎秆出现虫孔',
          '植株枯心',
          '叶片被蛀食',
          '幼虫在茎秆内蛀食'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用氯虫苯甲酰胺、阿维菌素、甲维盐、杀虫双等药剂防治。注意：在卵孵化盛期和幼虫低龄期防治。',
      prevention: '稻草还田要翻耕深埋，适时用药，保护天敌。'
    },
    {
      id: 'rice_skipper',
      name: '稻弄蝶',
      type: 'pest',
      crop: '水稻',
      severity: '中',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['卷曲状', '筒状'],
        patterns: ['卷叶', '虫体'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '叶片卷曲呈筒状',
          '幼虫取食叶片',
          '幼虫吐丝将叶片纵卷'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用阿维菌素、甲维盐、氯虫苯甲酰胺等药剂防治。注意：卵孵化盛期是防治关键期。',
      prevention: '合理密植，保护天敌，适时用药。'
    },
    {
      id: 'rice_sawfly',
      name: '稻纵叶螟',
      type: 'pest',
      crop: '水稻',
      severity: '中',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['卷曲状', '筒状'],
        patterns: ['卷叶', '虫体', '粪便'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '叶片卷曲呈筒状',
          '幼虫取食叶片',
          '幼虫吐丝将叶片纵卷'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用阿维菌素、甲维盐、氯虫苯甲酰胺等药剂防治。注意：卵孵化盛期是防治关键期。',
      prevention: '合理密植，保护天敌，适时用药。'
    },
    {
      id: 'rice_black_bug',
      name: '稻黑蝽',
      type: 'pest',
      crop: '水稻',
      severity: '中',
      features: {
        colors: ['黑色', '黑褐色', '深褐色'],
        shapes: ['椭圆形', '盾形'],
        patterns: ['虫体', '成虫'],
        size: 'medium',
        bodyParts: ['成虫', '若虫'],
        symptoms: [
          '叶片出现褐色斑点',
          '成虫和若虫吸食汁液',
          '叶片枯萎'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用高效氯氟氰菊酯、阿维菌素等药剂防治。注意：成虫期及时防治。',
      prevention: '选用抗虫品种，合理密植，保护天敌。'
    },
    {
      id: 'wheat_aphid',
      name: '麦蚜',
      type: 'pest',
      crop: '小麦',
      severity: '中',
      features: {
        colors: ['黄绿色', '淡黄色', '绿色', '褐色'],
        shapes: ['椭圆形', '卵形', '小虫体'],
        patterns: ['虫体', '蜜露', '分泌物'],
        size: 'small',
        bodyParts: ['成虫', '若虫', '卵'],
        symptoms: [
          '叶片出现蚜虫',
          '叶片表面有蜜露',
          '叶片发黄',
          '传播病毒病'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用吡虫啉、噻虫嗪、呋虫胺、高效氯氟氰菊酯等药剂防治。注意：保护天敌，避免过度用药。',
      prevention: '适时播种，保护天敌，合理密植。'
    },
    {
      id: 'wheat_armyworm',
      name: '小麦吸浆虫',
      type: 'pest',
      crop: '小麦',
      severity: '高',
      features: {
        colors: ['粉红色', '橙红色', '红褐色'],
        shapes: ['椭圆形', '长椭圆形'],
        patterns: ['虫体', '成虫'],
        size: 'medium',
        bodyParts: ['成虫', '幼虫', '卵'],
        symptoms: [
          '成虫吸食麦粒浆液',
          '麦粒出现虫孔',
          '麦粒干瘪',
          '严重时颗粒不饱满'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用高效氯氟氰菊酯、阿维菌素、毒死蜱等药剂防治。注意：在成虫产卵期和幼虫孵化期防治。',
      prevention: '适时播种，保护天敌，及时收割。'
    },
    {
      id: 'wheat_midge',
      name: '麦秆蝇',
      type: 'pest',
      crop: '小麦',
      severity: '中',
      features: {
        colors: ['黄色', '黄绿色', '褐色'],
        shapes: ['虫洞', '隧道'],
        patterns: ['虫孔', '蛀孔'],
        size: 'small',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '茎秆出现虫孔',
          '幼虫在茎秆内蛀食',
          '植株萎蔫',
          '叶片枯死'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用高效氯氟氰菊酯、阿维菌素等药剂防治。注意：在成虫产卵期和幼虫孵化期防治。',
      prevention: '适时播种，保护天敌，及时收割。'
    },
    {
      id: 'wheat_sawfly',
      name: '小麦叶蜂',
      type: 'pest',
      crop: '小麦',
      severity: '中',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['虫体', '幼虫'],
        patterns: ['虫体', '幼虫'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '幼虫取食叶片',
          '叶片出现缺刻',
          '严重时叶片被吃光'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用高效氯氟氰菊酯、阿维菌素等药剂防治。注意：幼虫低龄期是防治关键期。',
      prevention: '适时播种，保护天敌，合理密植。'
    },
    {
      id: 'corn_borer',
      name: '玉米螟',
      type: 'pest',
      crop: '玉米',
      severity: '高',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['虫洞', '隧道', '圆柱形'],
        patterns: ['虫孔', '蛀孔', '隧道'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '茎秆出现虫孔',
          '植株倒伏',
          '叶片被蛀食',
          '幼虫在茎秆内蛀食'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用氯虫苯甲酰胺、阿维菌素、甲维盐、辛硫磷等药剂防治。注意：在心叶期防治，适时用药。',
      prevention: '选用抗虫品种，处理秸秆，赤眼蜂放蜂。'
    },
    {
      id: 'corn_aphid',
      name: '玉米蚜',
      type: 'pest',
      crop: '玉米',
      severity: '中',
      features: {
        colors: ['黄绿色', '淡黄色', '绿色', '褐色'],
        shapes: ['椭圆形', '小虫体'],
        patterns: ['虫体', '蜜露', '分泌物'],
        size: 'small',
        bodyParts: ['成虫', '若虫', '卵'],
        symptoms: [
          '叶片出现蚜虫',
          '叶片表面有蜜露',
          '叶片发黄',
          '传播病毒病'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用吡虫啉、噻虫嗪、呋虫胺、高效氯氟氰菊酯等药剂防治。注意：保护天敌，避免过度用药。',
      prevention: '适时播种，保护天敌，合理密植。'
    },
    {
      id: 'corn_armyworm',
      name: '玉米粘虫',
      type: 'pest',
      crop: '玉米',
      severity: '高',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['虫体', '幼虫'],
        patterns: ['虫体', '幼虫', '粪便'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '幼虫取食叶片',
          '叶片出现缺刻',
          '严重时叶片被吃光'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用氯虫苯甲酰胺、甲氨基阿维菌素、高效氯氟氰菊酯等药剂防治。注意：幼虫低龄期是防治关键期。',
      prevention: '适时播种，保护天敌，合理密植。'
    },
    {
      id: 'corn_beetle',
      name: '玉米铁甲虫',
      type: 'pest',
      crop: '玉米',
      severity: '中',
      features: {
        colors: ['黑褐色', '深褐色', '黑色'],
        shapes: ['椭圆形', '盾形'],
        patterns: ['虫体', '成虫'],
        size: 'medium',
        bodyParts: ['成虫', '幼虫'],
        symptoms: [
          '成虫取食叶片',
          '叶片出现缺刻',
          '幼虫在叶片内蛀食'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用高效氯氟氰菊酯、阿维菌素等药剂防治。注意：成虫期及时防治。',
      prevention: '适时播种，保护天敌，合理密植。'
    },
    {
      id: 'cotton_bollworm',
      name: '棉铃虫',
      type: 'pest',
      crop: '棉花',
      severity: '高',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['虫洞', '隧道', '圆柱形'],
        patterns: ['虫孔', '蛀孔', '隧道'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '棉铃出现虫孔',
          '棉铃腐烂',
          '幼虫蛀食棉铃',
          '幼虫在棉铃内蛀食'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用氯虫苯甲酰胺、甲氨基阿维菌素、茚虫威、高效氯氟氰菊酯等药剂防治。注意：在卵孵化盛期和幼虫低龄期防治。',
      prevention: '种植抗虫品种，使用性诱剂，保护天敌。'
    },
    {
      id: 'cotton_aphid',
      name: '棉蚜',
      type: 'pest',
      crop: '棉花',
      severity: '中',
      features: {
        colors: ['黄绿色', '淡黄色', '绿色', '褐色'],
        shapes: ['椭圆形', '小虫体'],
        patterns: ['虫体', '蜜露', '分泌物'],
        size: 'small',
        bodyParts: ['成虫', '若虫', '卵'],
        symptoms: [
          '叶片背面出现蚜虫',
          '叶片卷缩',
          '叶片发黄',
          '传播病毒病'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用吡虫啉、噻虫嗪、呋虫胺、高效氯氟氰菊酯等药剂防治。注意：保护天敌，避免过度用药。',
      prevention: '合理密植，保护天敌，及时防治。'
    },
    {
      id: 'cotton_red_bug',
      name: '棉红蜘蛛',
      type: 'pest',
      crop: '棉花',
      severity: '中',
      features: {
        colors: ['红色', '红褐色', '橘红色'],
        shapes: ['小虫体', '椭圆形', '圆形'],
        patterns: ['虫体', '网状丝', '斑点'],
        size: 'tiny',
        bodyParts: ['成虫', '若虫', '卵'],
        symptoms: [
          '叶片出现红褐色斑点',
          '叶片变黄脱落',
          '虫体结网'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用阿维菌素、螺螨酯、哒螨灵、炔螨特等药剂防治。注意：保护天敌，避免过度用药。',
      prevention: '合理密植，保护天敌，及时防治。'
    },
    {
      id: 'cotton_mirid_bug',
      name: '棉盲蝽',
      type: 'pest',
      crop: '棉花',
      severity: '中',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['椭圆形', '长椭圆形'],
        patterns: ['虫体', '成虫'],
        size: 'medium',
        bodyParts: ['成虫', '若虫'],
        symptoms: [
          '叶片出现破叶',
          '叶片边缘呈锯齿状',
          '成虫和若虫吸食汁液'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用高效氯氟氰菊酯、阿维菌素等药剂防治。注意：成虫期及时防治。',
      prevention: '适时播种，保护天敌，合理密植。'
    },
    {
      id: 'soybean_caterpillar',
      name: '大豆食心虫',
      type: 'pest',
      crop: '大豆',
      severity: '高',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['虫洞', '隧道', '圆柱形'],
        patterns: ['虫孔', '蛀孔', '隧道'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '豆粒出现虫孔',
          '豆粒被蛀食',
          '豆粒不完整',
          '幼虫在豆粒内蛀食'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用氯虫苯甲酰胺、阿维菌素、甲维盐、高效氯氟氰菊酯等药剂防治。注意：在成虫产卵期和幼虫孵化期防治。',
      prevention: '适时播种，保护天敌，及时收割。'
    },
    {
      id: 'soybean_aphid',
      name: '大豆蚜',
      type: 'pest',
      crop: '大豆',
      severity: '中',
      features: {
        colors: ['黄绿色', '淡黄色', '绿色', '褐色'],
        shapes: ['椭圆形', '小虫体'],
        patterns: ['虫体', '蜜露', '分泌物'],
        size: 'small',
        bodyParts: ['成虫', '若虫', '卵'],
        symptoms: [
          '叶片背面出现蚜虫',
          '叶片卷缩',
          '叶片发黄',
          '传播病毒病'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用吡虫啉、噻虫嗪、呋虫胺、高效氯氟氰菊酯等药剂防治。注意：保护天敌，避免过度用药。',
      prevention: '合理密植，保护天敌，及时防治。'
    },
    {
      id: 'soybean_webworm',
      name: '大豆卷叶螟',
      type: 'pest',
      crop: '大豆',
      severity: '中',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['卷曲状', '筒状'],
        patterns: ['卷叶', '虫体', '粪便'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '叶片卷曲呈筒状',
          '幼虫取食叶片',
          '幼虫吐丝将叶片纵卷'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用阿维菌素、甲维盐、氯虫苯甲酰胺等药剂防治。注意：卵孵化盛期是防治关键期。',
      prevention: '合理密植，保护天敌，适时用药。'
    },
    {
      id: 'vegetable_plutella',
      name: '小菜蛾',
      type: 'pest',
      crop: '蔬菜',
      severity: '高',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['虫洞', '隧道', '不规则形'],
        patterns: ['虫孔', '蛀孔', '隧道'],
        size: 'small',
        bodyParts: ['幼虫', '成虫', '蛹'],
        symptoms: [
          '叶片出现虫孔',
          '幼虫在叶片内蛀食',
          '叶片被蛀食成网状',
          '幼虫吐丝结网'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用氯虫苯甲酰胺、甲氨基阿维菌素、茚虫威、高效氯氟氰菊酯等药剂防治。注意：在低龄幼虫期防治，避免产生抗药性。',
      prevention: '使用防虫网，保护天敌，及时清理残株。'
    },
    {
      id: 'vegetable_aphid',
      name: '蚜虫',
      type: 'pest',
      crop: '蔬菜',
      severity: '中',
      features: {
        colors: ['黄绿色', '淡黄色', '绿色', '褐色'],
        shapes: ['椭圆形', '小虫体'],
        patterns: ['虫体', '蜜露', '分泌物'],
        size: 'small',
        bodyParts: ['成虫', '若虫', '卵'],
        symptoms: [
          '叶片背面出现蚜虫',
          '叶片卷缩',
          '叶片发黄',
          '传播病毒病'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用吡虫啉、噻虫嗪、呋虫胺、高效氯氟氰菊酯等药剂防治。注意：保护天敌，避免过度用药。',
      prevention: '合理密植，保护天敌，及时防治。'
    },
    {
      id: 'vegetable_armyworm',
      name: '菜青虫',
      type: 'pest',
      crop: '蔬菜',
      severity: '中',
      features: {
        colors: ['绿色', '黄绿色', '褐色'],
        shapes: ['虫体', '幼虫'],
        patterns: ['虫体', '幼虫', '粪便'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '幼虫取食叶片',
          '叶片出现缺刻',
          '严重时叶片被吃光'
        ]
      },
      confidenceRules: {
        colorMatch: 0.3,
        shapeMatch: 0.4,
        patternMatch: 0.3
      },
      treatment: '使用氯虫苯甲酰胺、甲氨基阿维菌素、高效氯氟氰菊酯等药剂防治。注意：幼虫低龄期是防治关键期。',
      prevention: '使用防虫网，保护天敌，及时清理残株。'
    },
    {
      id: 'vegetable_thrips',
      name: '蓟马',
      type: 'pest',
      crop: '蔬菜',
      severity: '中',
      features: {
        colors: ['黄色', '黄褐色', '褐色'],
        shapes: ['小虫体', '椭圆形'],
        patterns: ['虫体', '成虫'],
        size: 'tiny',
        bodyParts: ['成虫', '若虫'],
        symptoms: [
          '叶片出现银白色斑点',
          '叶片卷缩',
          '成虫和若虫吸食汁液'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用吡虫啉、噻虫嗪、呋虫胺等药剂防治。注意：成虫期及时防治。',
      prevention: '使用防虫网，保护天敌，及时防治。'
    },
    {
      id: 'vegetable_whitefly',
      name: '粉虱',
      type: 'pest',
      crop: '蔬菜',
      severity: '中',
      features: {
        colors: ['白色', '灰白色', '淡黄色'],
        shapes: ['小虫体', '椭圆形'],
        patterns: ['虫体', '成虫'],
        size: 'tiny',
        bodyParts: ['成虫', '若虫'],
        symptoms: [
          '叶片背面出现白色小虫',
          '叶片发黄',
          '传播病毒病',
          '分泌蜜露'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用吡虫啉、噻虫嗪、呋虫胺等药剂防治。注意：成虫期及时防治。',
      prevention: '使用防虫网，保护天敌，及时防治。'
    },
    {
      id: 'fruit_tree_moth',
      name: '桃小食心虫',
      type: 'pest',
      crop: '果树',
      severity: '高',
      features: {
        colors: ['粉红色', '浅红色', '褐色'],
        shapes: ['虫洞', '隧道', '圆柱形'],
        patterns: ['虫孔', '蛀孔', '虫粪'],
        size: 'medium',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '果实出现虫孔',
          '果实内部被蛀食',
          '果实内有虫粪',
          '幼虫在果实内蛀食'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用氯虫苯甲酰胺、甲氨基阿维菌、高效氯氟氰菊酯等药剂防治。注意：在成虫产卵期和幼虫孵化期防治。',
      prevention: '使用性诱剂，摘除虫果，保护天敌。'
    },
    {
      id: 'fruit_tree_scale',
      name: '介壳虫',
      type: 'pest',
      crop: '果树',
      severity: '中',
      features: {
        colors: ['褐色', '灰褐色', '红褐色'],
        shapes: ['圆形', '椭圆形', '不规则形'],
        patterns: ['介壳', '斑点', '蜡质'],
        parts: ['枝干', '叶片', '果实'],
        symptoms: [
          '枝干或叶片出现介壳',
          '虫体固定不动',
          '吸食植物汁液',
          '影响植物生长'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用螺螨酯、噻嗪酮、矿物油等药剂防治。注意：保护天敌，避免花期用药。',
      prevention: '合理修剪，保护天敌，及时防治。'
    },
    {
      id: 'fruit_tree_red_spider_mite',
      name: '红蜘蛛',
      type: 'pest',
      crop: '果树',
      severity: '中',
      features: {
        colors: ['红褐色', '橘红色', '红黄色'],
        shapes: ['小虫体', '椭圆形', '圆形'],
        patterns: ['虫体', '网状丝', '斑点'],
        size: 'tiny',
        bodyParts: ['成虫', '若虫', '卵'],
        symptoms: [
          '叶片出现红褐色斑点',
          '叶片变黄脱落',
          '虫体结网',
          '叶片表面有细小斑点'
        ]
      },
      confidenceRules: {
        colorMatch: 0.5,
        shapeMatch: 0.3,
        patternMatch: 0.2
      },
      treatment: '使用阿维菌素、螺螨酯、哒螨灵、炔螨特等药剂防治。注意：保护天敌，避免过度用药。',
      prevention: '合理修剪，保护天敌，及时防治。'
    },
    {
      id: 'fruit_tree_leaf_miner',
      name: '潜叶蛾',
      type: 'pest',
      crop: '果树',
      severity: '中',
      features: {
        colors: ['白色', '灰白色', '淡黄色'],
        shapes: ['隧道', '线状', '弯曲状'],
        patterns: ['隧道', '蛀道'],
        size: 'small',
        bodyParts: ['幼虫', '成虫'],
        symptoms: [
          '叶片出现弯曲隧道',
          '幼虫在叶片内蛀食',
          '叶片枯萎'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.4,
        patternMatch: 0.2
      },
      treatment: '使用阿维菌素、甲维盐等药剂防治。注意：幼虫低龄期是防治关键期。',
      prevention: '合理修剪，保护天敌，及时防治。'
    },
    {
      id: 'fruit_tree_aphid',
      name: '果树蚜虫',
      type: 'pest',
      crop: '果树',
      severity: '中',
      features: {
        colors: ['黄绿色', '淡黄色', '绿色', '褐色'],
        shapes: ['椭圆形', '小虫体'],
        patterns: ['虫体', '蜜露', '分泌物'],
        size: 'small',
        bodyParts: ['成虫', '若虫', '卵'],
        symptoms: [
          '嫩芽或叶片出现蚜虫',
          '叶片卷缩',
          '叶片发黄',
          '传播病毒病'
        ]
      },
      confidenceRules: {
        colorMatch: 0.4,
        shapeMatch: 0.3,
        patternMatch: 0.3
      },
      treatment: '使用吡虫啉、噻虫嗪、呋虫胺、高效氯氟氰菊酯等药剂防治。注意：保护天敌，避免过度用药。',
      prevention: '合理修剪，保护天敌，及时防治。'
    }
  ]
}
