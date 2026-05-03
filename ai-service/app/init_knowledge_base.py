"""
知识库初始化脚本
将农业专业知识添加到 ChromaDB 向量数据库
"""
import chromadb
from sentence_transformers import SentenceTransformer
from app.knowledge.agricultural_knowledge import (
    CROP_KNOWLEDGE_BASE,
    PRICE_TREND_KNOWLEDGE,
    AGRICULTURAL_METEOROLOGY_KNOWLEDGE,
    SOIL_KNOWLEDGE,
    AGRICULTURAL_MATERIAL_KNOWLEDGE,
    PLANTING_CYCLE_KNOWLEDGE
)
import json


def format_crop_knowledge(crop_name: str, data: dict) -> list:
    """格式化作物知识为文本列表"""
    documents = []
    
    # 基础信息
    doc = f"【{crop_name}种植技术大全】\n\n"
    doc += f"品种类型：{', '.join(data.get('品种', []))}\n\n"
    
    # 种植技术
    if '种植技术' in data:
        doc += "种植技术要点：\n"
        for key, value in data['种植技术'].items():
            doc += f"• {key}：{value}\n"
        doc += "\n"
    
    # 施肥方案
    if '施肥方案' in data:
        doc += "科学施肥方案：\n"
        for key, value in data['施肥方案'].items():
            doc += f"• {key}：{value}\n"
        doc += "\n"
    
    # 病虫害防治
    if '病虫害防治' in data:
        doc += "病虫害防治：\n"
        doc += f"• 主要病害：{', '.join(data['病虫害防治'].get('主要病害', []))}\n"
        doc += f"• 主要虫害：{', '.join(data['病虫害防治'].get('主要虫害', []))}\n"
        doc += f"• 防治方法：{data['病虫害防治'].get('防治方法', '')}\n"
        doc += "\n"
    
    # 产量预期
    if '产量预期' in data:
        doc += f"产量预期：{data['产量预期']}\n"
    
    documents.append(doc)
    
    # 单独的病虫害问答
    if '病虫害防治' in data:
        for disease in data['病虫害防治'].get('主要病害', []):
            doc = f"【{crop_name}{disease}防治方法】\n\n"
            doc += f"{crop_name}常见病害：{disease}\n\n"
            doc += f"防治建议：\n"
            doc += f"1. 选用抗病品种\n"
            doc += f"2. 合理轮作倒茬\n"
            doc += f"3. 加强田间管理\n"
            doc += f"4. 发病初期及时喷药防治\n"
            doc += f"5. 注意排水通风，降低田间湿度\n"
            documents.append(doc)
        
        for pest in data['病虫害防治'].get('主要虫害', []):
            doc = f"【{crop_name}{pest}防治方法】\n\n"
            doc += f"{crop_name}常见虫害：{pest}\n\n"
            doc += f"防治建议：\n"
            doc += f"1. 物理防治：灯光诱杀、色板诱杀\n"
            doc += f"2. 生物防治：释放天敌、使用生物农药\n"
            doc += f"3. 化学防治：选用高效低毒农药\n"
            doc += f"4. 农业防治：清洁田园、合理轮作\n"
            documents.append(doc)
    
    # 单独的种植问答
    if '种植技术' in data:
        doc = f"【{crop_name}什么时候种植？】\n\n"
        doc += f"{crop_name}最佳种植时间：\n\n"
        if '播种期' in data['种植技术']:
            doc += f"播种期：{data['种植技术']['播种期']}\n\n"
        doc += f"注意事项：\n"
        doc += f"• 选择适宜当地气候的品种\n"
        doc += f"• 关注天气预报，避开恶劣天气\n"
        doc += f"• 做好播种前准备工作\n"
        documents.append(doc)
    
    return documents


def format_extended_knowledge() -> list:
    """格式化扩展知识"""
    documents = []
    
    # 病虫害诊断知识
    disease_diagnosis = [
        """【病虫害诊断方法】

一、病害识别要点
• 观察病斑形状：圆形、不规则形、条斑等
• 观察病斑颜色：褐色、黑色、黄色、白色等
• 观察发病部位：叶片、茎秆、果实、根系
• 观察发病规律：从下向上、从外向内等

二、虫害识别要点
• 观察虫体形态：大小、颜色、形状
• 观察为害症状：咬食、刺吸、蛀食
• 观察为害部位：叶片、茎秆、果实、根系
• 观察发生时间：季节、生育期

三、诊断步骤
1. 现场调查：了解发病情况、分布特点
2. 症状观察：详细记录病害症状
3. 标本采集：采集典型症状标本
4. 实验室检测：显微镜检查、分离培养
5. 综合判断：结合症状、环境、病原确定""",
        
        """【农药使用原则】

一、科学选药
• 对症下药：根据病虫害种类选择药剂
• 交替用药：避免长期使用同一种农药
• 混配用药：合理混配提高防治效果
• 选用低毒农药：优先选择生物农药

二、适时施药
• 发病初期施药：病害发生初期防治效果好
• 害虫低龄期施药：幼虫期防治效果最佳
• 避开恶劣天气：风雨天不宜施药
• 注意安全间隔期：距采收前停止施药

三、适量施药
• 按推荐剂量：不随意增加用药量
• 均匀喷施：确保全面覆盖
• 足量用药危害：药害、残留、环境污染

四、安全防护
• 穿戴防护用品：口罩、手套、防护服
• 逆风施药：避免农药飘移
• 施药后清洗：及时清洗身体和工具
• 注意警示标识：设置警示标志""",
        
        """【施肥基本原则】

一、测土配方施肥
• 土壤检测：了解土壤养分含量
• 配方设计：根据作物需肥规律设计配方
• 合理施肥：按配方定量施肥

二、有机无机结合
• 增施有机肥：改良土壤、培肥地力
• 配施化肥：满足作物快速生长需求
• 有机肥充分腐熟：防止烧根和病虫害

三、氮磷钾平衡
• 氮肥：促进营养生长，过量易徒长
• 磷肥：促进根系发育和开花结实
• 钾肥：增强抗逆性，提高品质
• 适当补充微量元素

四、分期追肥
• 基肥：播种前施入，打好基础
• 苗肥：促进幼苗生长
• 花果肥：促进开花结果
• 后期补肥：防止早衰""",
        
        """【灌溉管理技术】

一、灌溉原则
• 适时灌溉：根据土壤墒情和作物需求
• 适量灌溉：避免过量造成浪费和涝害
• 节水灌溉：采用滴灌、喷灌等节水技术

二、主要作物需水规律
• 水稻：需水量最大，保持水层
• 小麦：拔节孕穗期需水最多
• 玉米：抽雄吐丝期需水临界期
• 大豆：开花结荚期需水较多

三、灌溉方法
• 沟灌：适用于行距较大的作物
• 漫灌：适用于密植作物
• 滴灌：节水高效，适用于设施农业
• 喷灌：均匀性好，适用于多种作物

四、排水管理
• 雨季排水：防止涝害
• 低洼地排水：深沟高畦
• 设施排水：排水沟配套""",
        
        """【土壤改良技术】

一、酸性土壤改良
• 施用石灰：中和土壤酸性
• 施用草木灰：提高pH值
• 种植绿肥：改良土壤结构
• 施用有机肥：提高缓冲能力

二、碱性土壤改良
• 施用石膏：改良碱化土壤
• 施用硫磺：降低pH值
• 种植耐碱作物：生物改良
• 洗盐排碱：水利改良

三、黏重土壤改良
• 增施有机肥：改善土壤结构
• 深翻松土：打破犁底层
• 掺沙改土：改善质地
• 种植绿肥：增加有机质

四、沙质土壤改良
• 增施有机肥：提高保水保肥能力
• 客土改良：掺入黏土
• 种植绿肥：增加有机质
• 覆盖保墒：减少水分蒸发""",
        
        """【作物轮作倒茬技术】

一、轮作的意义
• 减轻病虫害：打断病虫害传播链
• 培肥地力：不同作物养分需求不同
• 提高产量：改善土壤理化性质
• 降低成本：减少农药化肥使用

二、轮作原则
• 深根浅根搭配：充分利用土壤养分
• 豆科禾本科轮作：固氮养地
• 避免同科连作：减少病虫害
• 经济效益与生态效益兼顾

三、常见轮作模式
• 水稻-小麦轮作：南方常见模式
• 玉米-大豆轮作：东北常见模式
• 小麦-玉米轮作：华北常见模式
• 棉花-小麦轮作：新疆常见模式

四、注意事项
• 轮作周期：一般2-4年
• 土壤准备：轮作前深翻施肥
• 品种选择：选择适宜轮作周期的品种
• 病虫害监测：注意病虫害发生动态"""
    ]
    
    documents.extend(disease_diagnosis)
    
    # 作物生长周期知识
    growth_stages = """【作物生长阶段管理】

一、苗期管理
• 及时查苗补苗：确保全苗
• 间苗定苗：合理密植
• 中耕除草：疏松土壤，清除杂草
• 防治病虫害：苗期病虫害防治

二、生长中期管理
• 追肥：满足快速生长需求
• 灌溉：保证水分供应
• 中耕培土：促进根系发育
• 病虫害防治：重点防治期

三、生殖生长期管理
• 追施花果肥：促进开花结果
• 水分管理：保证水分供应
• 疏花疏果：合理负载
• 防治病虫害：保护花果

四、成熟期管理
• 适时收获：确定最佳收获期
• 停止灌溉：促进成熟
• 防止倒伏：减少损失
• 及时晾晒：防止霉变"""
    
    documents.append(growth_stages)
    
    return documents


def init_knowledge_base():
    """初始化知识库"""
    print("开始初始化知识库...")
    
    # 初始化 ChromaDB
    client = chromadb.PersistentClient(path="./data/chromadb")
    collection = client.get_or_create_collection(name="planting_knowledge")
    
    # 初始化嵌入模型
    print("加载嵌入模型...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 收集所有文档
    all_documents = []
    metadatas = []
    ids = []
    
    doc_id = 0
    
    # 添加作物知识
    print("添加作物知识...")
    for crop_name, data in CROP_KNOWLEDGE_BASE.items():
        docs = format_crop_knowledge(crop_name, data)
        for doc in docs:
            all_documents.append(doc)
            metadatas.append({"crop": crop_name, "type": "crop_knowledge"})
            ids.append(f"crop_{doc_id}")
            doc_id += 1
    
    # 添加价格趋势知识
    print("添加价格趋势知识...")
    for product, data in PRICE_TREND_KNOWLEDGE.items():
        doc = f"【{product}价格趋势分析】\n\n"
        doc += f"季节性规律：{data.get('季节性规律', '')}\n\n"
        doc += f"影响因素：{', '.join(data.get('影响因素', []))}\n\n"
        doc += f"价格区间：{data.get('价格区间', '')}\n"
        all_documents.append(doc)
        metadatas.append({"product": product, "type": "price_trend"})
        ids.append(f"price_{doc_id}")
        doc_id += 1
    
    # 添加农业气象知识
    print("添加农业气象知识...")
    for category, data in AGRICULTURAL_METEOROLOGY_KNOWLEDGE.items():
        doc = f"【农业气象知识-{category}】\n\n"
        for crop, info in data.items():
            doc += f"{crop}：{info}\n"
        all_documents.append(doc)
        metadatas.append({"category": category, "type": "meteorology"})
        ids.append(f"meteorology_{doc_id}")
        doc_id += 1
    
    # 添加土壤知识
    print("添加土壤知识...")
    for category, data in SOIL_KNOWLEDGE.items():
        doc = f"【土壤知识-{category}】\n\n"
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    doc += f"{key}：\n"
                    for k, v in value.items():
                        doc += f"  • {k}：{v}\n"
                else:
                    doc += f"{key}：{value}\n"
        all_documents.append(doc)
        metadatas.append({"category": category, "type": "soil"})
        ids.append(f"soil_{doc_id}")
        doc_id += 1
    
    # 添加农资使用知识
    print("添加农资使用知识...")
    for category, data in AGRICULTURAL_MATERIAL_KNOWLEDGE.items():
        doc = f"【农资使用知识-{category}】\n\n"
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    doc += f"{key}：\n"
                    for k, v in value.items():
                        if isinstance(v, list):
                            doc += f"  • {k}：{', '.join(v)}\n"
                        else:
                            doc += f"  • {k}：{v}\n"
                else:
                    doc += f"{key}：{value}\n"
        all_documents.append(doc)
        metadatas.append({"category": category, "type": "agricultural_material"})
        ids.append(f"material_{doc_id}")
        doc_id += 1
    
    # 添加种植周期知识
    print("添加种植周期知识...")
    for crop, data in PLANTING_CYCLE_KNOWLEDGE.items():
        doc = f"【{crop}种植周期】\n\n"
        for stage, time in data.items():
            doc += f"• {stage}：{time}\n"
        all_documents.append(doc)
        metadatas.append({"crop": crop, "type": "planting_cycle"})
        ids.append(f"cycle_{doc_id}")
        doc_id += 1
    
    # 添加扩展知识
    print("添加扩展知识...")
    extended_docs = format_extended_knowledge()
    for i, doc in enumerate(extended_docs):
        all_documents.append(doc)
        metadatas.append({"type": "extended_knowledge"})
        ids.append(f"extended_{doc_id}")
        doc_id += 1
    
    # 批量添加到向量数据库
    print(f"共生成 {len(all_documents)} 条知识文档")
    print("生成向量嵌入...")
    
    # 分批处理，避免内存溢出
    batch_size = 100
    for i in range(0, len(all_documents), batch_size):
        batch_docs = all_documents[i:i+batch_size]
        batch_metas = metadatas[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        
        # 生成嵌入向量
        embeddings = embedder.encode(batch_docs).tolist()
        
        # 添加到集合
        collection.add(
            documents=batch_docs,
            embeddings=embeddings,
            metadatas=batch_metas,
            ids=batch_ids
        )
        
        print(f"已添加 {min(i+batch_size, len(all_documents))}/{len(all_documents)} 条文档")
    
    print(f"知识库初始化完成！共添加 {len(all_documents)} 条知识")
    print(f"集合信息：{collection.count()} 条记录")
    
    return collection.count()


if __name__ == "__main__":
    count = init_knowledge_base()
    print(f"\n初始化成功！知识库共 {count} 条记录")
