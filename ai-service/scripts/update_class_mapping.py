"""
更新类别映射脚本
从Kaggle训练输出的class_mapping.json更新image_service.py中的类别映射
"""
import json
import os

def update_class_mapping():
    """从class_mapping.json更新类别映射"""
    
    class_mapping_file = "models/class_mapping.json"
    
    if not os.path.exists(class_mapping_file):
        print(f"错误: 找不到 {class_mapping_file}")
        print("请先从Kaggle下载 class_mapping.json 到 models/ 目录")
        return
    
    with open(class_mapping_file, 'r') as f:
        kaggle_mapping = json.load(f)
    
    print(f"加载了 {len(kaggle_mapping)} 个类别")
    print("\nKaggle类别映射:")
    for idx in sorted(kaggle_mapping.keys(), key=lambda x: int(x)):
        print(f"  {idx}: {kaggle_mapping[idx]}")
    
    base_mapping = {
        "Apple___Apple_scab": {"name": "苹果疮痂病", "name_en": "Apple Scab", 
            "treatment": "喷施多菌灵或代森锰锌，及时清除病叶病果"},
        "Apple___Black_rot": {"name": "苹果黑腐病", "name_en": "Apple Black Rot",
            "treatment": "剪除病枝病果，喷施甲基硫菌灵或戊唑醇"},
        "Apple___Cedar_apple_rust": {"name": "苹果锈病", "name_en": "Apple Cedar Rust",
            "treatment": "喷施三唑酮或腈菌唑，清除附近柏树"},
        "Apple___healthy": {"name": "苹果健康", "name_en": "Apple Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Blueberry___healthy": {"name": "蓝莓健康", "name_en": "Blueberry Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Cherry_(including_sour)___Powdery_mildew": {"name": "樱桃白粉病", "name_en": "Cherry Powdery Mildew",
            "treatment": "喷施三唑酮或腈菌唑，加强通风透光"},
        "Cherry_(including_sour)___healthy": {"name": "樱桃健康", "name_en": "Cherry Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {"name": "玉米灰斑病", "name_en": "Corn Gray Leaf Spot",
            "treatment": "选用抗病品种，喷施苯醚甲环唑或吡唑醚菌酯"},
        "Corn_(maize)___Common_rust_": {"name": "玉米锈病", "name_en": "Corn Common Rust",
            "treatment": "喷施三唑酮或腈菌唑，及时清除病叶"},
        "Corn_(maize)___Northern_Leaf_Blight": {"name": "玉米大斑病", "name_en": "Corn Northern Leaf Blight",
            "treatment": "喷施苯醚甲环唑，加强田间管理，合理密植"},
        "Corn_(maize)___healthy": {"name": "玉米健康", "name_en": "Corn Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Grape___Black_rot": {"name": "葡萄黑腐病", "name_en": "Grape Black Rot",
            "treatment": "清除病果病叶，喷施甲基硫菌灵或代森锰锌"},
        "Grape___Esca_(Black_Measles)": {"name": "葡萄黑痘病", "name_en": "Grape Esca",
            "treatment": "剪除病枝，喷施戊唑醇或苯醚甲环唑"},
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {"name": "葡萄叶枯病", "name_en": "Grape Leaf Blight",
            "treatment": "清除病叶，喷施代森锰锌或百菌清"},
        "Grape___healthy": {"name": "葡萄健康", "name_en": "Grape Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Orange___Haunglongbing_(Citrus_greening)": {"name": "柑橘黄龙病", "name_en": "Orange Huanglongbing",
            "treatment": "立即挖除病树，防治木虱，严格检疫"},
        "Peach___Bacterial_spot": {"name": "桃细菌性穿孔病", "name_en": "Peach Bacterial Spot",
            "treatment": "喷施农用链霉素或噻唑锌，避免伤口"},
        "Peach___healthy": {"name": "桃健康", "name_en": "Peach Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Pepper,_bell___Bacterial_spot": {"name": "辣椒细菌性斑点病", "name_en": "Pepper Bacterial Spot",
            "treatment": "喷施农用链霉素或噻唑锌，加强通风"},
        "Pepper,_bell___healthy": {"name": "辣椒健康", "name_en": "Pepper Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Potato___Early_blight": {"name": "马铃薯早疫病", "name_en": "Potato Early Blight",
            "treatment": "喷施代森锰锌或百菌清，及时清除病叶"},
        "Potato___Late_blight": {"name": "马铃薯晚疫病", "name_en": "Potato Late Blight",
            "treatment": "喷施甲霜灵或烯酰吗啉，及时清除病株"},
        "Potato___healthy": {"name": "马铃薯健康", "name_en": "Potato Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Raspberry___healthy": {"name": "树莓健康", "name_en": "Raspberry Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Soybean___healthy": {"name": "大豆健康", "name_en": "Soybean Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Squash___Powdery_mildew": {"name": "南瓜白粉病", "name_en": "Squash Powdery Mildew",
            "treatment": "喷施三唑酮或腈菌唑，加强通风透光"},
        "Strawberry___Leaf_scorch": {"name": "草莓叶焦病", "name_en": "Strawberry Leaf Scorch",
            "treatment": "清除病叶，喷施代森锰锌或百菌清"},
        "Strawberry___healthy": {"name": "草莓健康", "name_en": "Strawberry Healthy",
            "treatment": "无病害，继续做好预防管理"},
        "Tomato___Bacterial_spot": {"name": "番茄细菌性斑点病", "name_en": "Tomato Bacterial Spot",
            "treatment": "喷施农用链霉素或噻唑锌，避免伤口"},
        "Tomato___Early_blight": {"name": "番茄早疫病", "name_en": "Tomato Early Blight",
            "treatment": "喷施代森锰锌或百菌清，及时清除病叶"},
        "Tomato___Late_blight": {"name": "番茄晚疫病", "name_en": "Tomato Late Blight",
            "treatment": "喷施甲霜灵或烯酰吗啉，降低田间湿度"},
        "Tomato___Leaf_Mold": {"name": "番茄叶霉病", "name_en": "Tomato Leaf Mold",
            "treatment": "加强通风降湿，喷施多菌灵或甲基硫菌灵"},
        "Tomato___Septoria_leaf_spot": {"name": "番茄叶斑病", "name_en": "Tomato Septoria Leaf Spot",
            "treatment": "清除病叶，喷施代森锰锌或百菌清"},
        "Tomato___Spider_mites Two-spotted_spider_mite": {"name": "番茄红蜘蛛", "name_en": "Tomato Spider Mites",
            "treatment": "喷施阿维菌素或螺螨酯，注意轮换用药"},
        "Tomato___Target_Spot": {"name": "番茄斑点病", "name_en": "Tomato Target Spot",
            "treatment": "喷施苯醚甲环唑或吡唑醚菌酯"},
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {"name": "番茄黄化曲叶病毒病", "name_en": "Tomato Yellow Leaf Curl Virus",
            "treatment": "防治烟粉虱，拔除病株，选用抗病品种"},
        "Tomato___Tomato_mosaic_virus": {"name": "番茄花叶病毒病", "name_en": "Tomato Mosaic Virus",
            "treatment": "防治蚜虫，拔除病株，避免接触传染"},
        "Tomato___healthy": {"name": "番茄健康", "name_en": "Tomato Healthy",
            "treatment": "无病害，继续做好预防管理"}
    }
    
    new_mapping = {}
    for idx_str, class_name in kaggle_mapping.items():
        idx = int(idx_str)
        if class_name in base_mapping:
            new_mapping[idx] = base_mapping[class_name]
        else:
            parts = class_name.replace('___', ' ').replace('_', ' ').split()
            disease_name = ' '.join(parts[1:]) if len(parts) > 1 else class_name
            new_mapping[idx] = {
                "name": disease_name,
                "name_en": class_name,
                "treatment": "建议咨询农业专家"
            }
            print(f"\n警告: 找到新类别 '{class_name}'，使用默认映射")
    
    output_file = "models/class_mapping_updated.json"
    output_data = {str(k): v for k, v in new_mapping.items()}
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 已生成更新后的类别映射: {output_file}")
    print("\n请手动将以下内容复制到 image_service.py 的 _load_class_mapping 方法中:")
    print("-" * 80)
    
    for idx in sorted(new_mapping.keys()):
        info = new_mapping[idx]
        print(f'            {idx}: {{"name": "{info["name"]}", "name_en": "{info["name_en"]}",')
        print(f'                "treatment": "{info["treatment"]}"}},')

if __name__ == "__main__":
    update_class_mapping()
