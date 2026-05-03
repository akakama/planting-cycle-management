"""
LoRA微调服务
用于对Qwen2.5-7B模型进行农业领域微调
"""
import os
import json
import torch
from typing import List, Dict, Optional
from pathlib import Path
from loguru import logger
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType
)
from datasets import Dataset


class LoRAFineTuningService:
    """LoRA微调服务类"""

    def __init__(self, model_path: str, output_dir: str = "./lora_output"):
        """
        初始化LoRA微调服务

        Args:
            model_path: 基础模型路径
            output_dir: 输出目录
        """
        self.model_path = model_path
        self.output_dir = output_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        self.lora_model = None

        logger.info(f"LoRA微调服务初始化完成, 设备: {self.device}")

    def load_model(self):
        """加载基础模型和tokenizer"""
        try:
            logger.info("正在加载基础模型...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32,
                device_map="auto" if self.device.type == "cuda" else None
            )

            if self.device.type == "cpu":
                self.model = self.model.to(self.device)

            logger.info("基础模型加载完成")
        except Exception as e:
            logger.error(f"加载模型失败: {str(e)}")
            raise

    def prepare_lora_model(
        self,
        r: int = 8,
        lora_alpha: int = 32,
        lora_dropout: float = 0.05,
        target_modules: Optional[List[str]] = None,
        bias: str = "none"
    ):
        """
        准备LoRA模型

        Args:
            r: LoRA秩
            lora_alpha: LoRA alpha
            lora_dropout: LoRA dropout
            target_modules: 目标模块
            bias: bias设置
        """
        if self.model is None:
            raise ValueError("请先加载基础模型")

        try:
            logger.info("正在准备LoRA模型...")

            # 如果是量化模型,需要准备
            if hasattr(self.model, "is_quantized") and self.model.is_quantized:
                self.model = prepare_model_for_kbit_training(self.model)

            # 默认目标模块(针对Qwen模型)
            if target_modules is None:
                target_modules = [
                    "q_proj",
                    "k_proj",
                    "v_proj",
                    "o_proj",
                    "gate_proj",
                    "up_proj",
                    "down_proj"
                ]

            # LoRA配置
            lora_config = LoraConfig(
                task_type=TaskType.CAUSAL_LM,
                r=r,
                lora_alpha=lora_alpha,
                lora_dropout=lora_dropout,
                target_modules=target_modules,
                bias=bias,
                inference_mode=False
            )

            # 应用LoRA
            self.lora_model = get_peft_model(self.model, lora_config)

            # 打印可训练参数
            self.lora_model.print_trainable_parameters()

            logger.info("LoRA模型准备完成")

        except Exception as e:
            logger.error(f"准备LoRA模型失败: {str(e)}")
            raise

    def load_training_data(self, data_path: str) -> Dataset:
        """
        加载训练数据

        Args:
            data_path: 数据文件路径(JSON格式)

        Returns:
            训练数据集
        """
        try:
            logger.info(f"正在加载训练数据: {data_path}")

            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 转换为HuggingFace Dataset格式
            dataset = Dataset.from_list(data)

            logger.info(f"训练数据加载完成, 共 {len(dataset)} 条")
            return dataset

        except Exception as e:
            logger.error(f"加载训练数据失败: {str(e)}")
            raise

    def preprocess_data(self, dataset: Dataset, max_length: int = 512) -> Dataset:
        """
        预处理数据

        Args:
            dataset: 原始数据集
            max_length: 最大长度

        Returns:
            处理后的数据集
        """
        def tokenize_function(examples):
            # 构建训练文本
            texts = []
            for i in range(len(examples['instruction'])):
                instruction = examples['instruction'][i]
                input_text = examples.get('input', [''])[i]
                output_text = examples['output'][i]

                # 构建提示词格式
                if input_text:
                    text = f"<|im_start|>user\n{instruction}\n{input_text}<|im_end|>\n<|im_start|>assistant\n{output_text}<|im_end|>"
                else:
                    text = f"<|im_start|>user\n{instruction}<|im_end|>\n<|im_start|>assistant\n{output_text}<|im_end|>"

                texts.append(text)

            # Tokenize
            tokenized = self.tokenizer(
                texts,
                truncation=True,
                max_length=max_length,
                padding="max_length",
                return_tensors=None
            )

            # 设置labels(用于计算loss)
            tokenized["labels"] = tokenized["input_ids"].copy()

            return tokenized

        try:
            logger.info("正在预处理数据...")
            tokenized_dataset = dataset.map(
                tokenize_function,
                batched=True,
                remove_columns=dataset.column_names
            )
            logger.info("数据预处理完成")
            return tokenized_dataset

        except Exception as e:
            logger.error(f"数据预处理失败: {str(e)}")
            raise

    def train(
        self,
        dataset: Dataset,
        num_train_epochs: int = 3,
        per_device_train_batch_size: int = 4,
        gradient_accumulation_steps: int = 4,
        learning_rate: float = 2e-4,
        warmup_steps: int = 100,
        logging_steps: int = 10,
        save_steps: int = 500,
        eval_steps: int = 500
    ):
        """
        训练LoRA模型

        Args:
            dataset: 训练数据集
            num_train_epochs: 训练轮数
            per_device_train_batch_size: 每设备批次大小
            gradient_accumulation_steps: 梯度累积步数
            learning_rate: 学习率
            warmup_steps: 预热步数
            logging_steps: 日志步数
            save_steps: 保存步数
            eval_steps: 评估步数
        """
        if self.lora_model is None:
            raise ValueError("请先准备LoRA模型")

        try:
            logger.info("开始训练LoRA模型...")

            # 训练参数
            training_args = TrainingArguments(
                output_dir=self.output_dir,
                num_train_epochs=num_train_epochs,
                per_device_train_batch_size=per_device_train_batch_size,
                gradient_accumulation_steps=gradient_accumulation_steps,
                learning_rate=learning_rate,
                warmup_steps=warmup_steps,
                logging_steps=logging_steps,
                save_steps=save_steps,
                eval_steps=eval_steps,
                save_total_limit=3,
                load_best_model_at_end=True,
                metric_for_best_model="loss",
                greater_is_better=False,
                fp16=self.device.type == "cuda",
                dataloader_num_workers=4,
                remove_unused_columns=False,
                report_to="none"
            )

            # 数据整理器
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False
            )

            # 创建Trainer
            trainer = Trainer(
                model=self.lora_model,
                args=training_args,
                train_dataset=dataset,
                data_collator=data_collator
            )

            # 开始训练
            trainer.train()

            # 保存模型
            trainer.save_model(self.output_dir)
            self.tokenizer.save_pretrained(self.output_dir)

            logger.info(f"LoRA模型训练完成, 保存至: {self.output_dir}")

            # 打印训练统计
            train_stats = trainer.state.log_history[-1]
            logger.info(f"训练损失: {train_stats.get('train_loss', 'N/A')}")
            logger.info(f"训练步数: {train_stats.get('step', 'N/A')}")

        except Exception as e:
            logger.error(f"训练失败: {str(e)}")
            raise

    def save_lora_adapter(self, output_path: str):
        """
        保存LoRA适配器

        Args:
            output_path: 输出路径
        """
        if self.lora_model is None:
            raise ValueError("没有可保存的LoRA模型")

        try:
            logger.info(f"正在保存LoRA适配器至: {output_path}")
            self.lora_model.save_pretrained(output_path)
            logger.info("LoRA适配器保存完成")
        except Exception as e:
            logger.error(f"保存LoRA适配器失败: {str(e)}")
            raise

    def load_lora_adapter(self, adapter_path: str):
        """
        加载LoRA适配器

        Args:
            adapter_path: 适配器路径
        """
        if self.model is None:
            raise ValueError("请先加载基础模型")

        try:
            logger.info(f"正在加载LoRA适配器: {adapter_path}")
            from peft import PeftModel
            self.lora_model = PeftModel.from_pretrained(self.model, adapter_path)
            logger.info("LoRA适配器加载完成")
        except Exception as e:
            logger.error(f"加载LoRA适配器失败: {str(e)}")
            raise

    def merge_lora_weights(self):
        """合并LoRA权重到基础模型"""
        if self.lora_model is None:
            raise ValueError("没有可合并的LoRA模型")

        try:
            logger.info("正在合并LoRA权重...")
            merged_model = self.lora_model.merge_and_unload()
            logger.info("LoRA权重合并完成")
            return merged_model
        except Exception as e:
            logger.error(f"合并LoRA权重失败: {str(e)}")
            raise

    def generate_text(self, prompt: str, max_length: int = 512) -> str:
        """
        使用微调后的模型生成文本

        Args:
            prompt: 提示词
            max_length: 最大长度

        Returns:
            生成的文本
        """
        if self.lora_model is None:
            raise ValueError("请先加载或训练LoRA模型")

        try:
            # 构建输入
            input_text = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)

            # 生成
            with torch.no_grad():
                outputs = self.lora_model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )

            # 解码
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # 提取assistant的回复
            if "<|im_start|>assistant\n" in generated_text:
                generated_text = generated_text.split("<|im_start|>assistant\n")[-1]
            if "<|im_end|>" in generated_text:
                generated_text = generated_text.split("<|im_end|>")[0]

            return generated_text.strip()

        except Exception as e:
            logger.error(f"生成文本失败: {str(e)}")
            raise

    def cleanup(self):
        """清理资源"""
        if self.model is not None:
            del self.model
        if self.lora_model is not None:
            del self.lora_model
        if self.tokenizer is not None:
            del self.tokenizer

        # 清理GPU缓存
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        logger.info("资源清理完成")


def create_sample_training_data(output_path: str = "./training_data.json"):
    """
    创建示例训练数据

    Args:
        output_path: 输出文件路径
    """
    sample_data = [
        {
            "instruction": "如何防治稻瘟病?",
            "input": "",
            "output": "稻瘟病的防治方法包括:\n1. 选用抗病品种,种子消毒\n2. 合理密植,科学施肥,避免过量施氮肥\n3. 发病初期使用三环唑、富士一号等药剂防治,隔7-10天施药一次,连续施药2-3次\n4. 及时清除病残体,减少病源\n5. 加强田间管理,保持田间通风透光"
        },
        {
            "instruction": "水稻什么时候施肥最合适?",
            "input": "",
            "output": "水稻施肥的关键时期:\n1. 基肥:在耕地或整地时施用,以有机肥为主,配合适量氮磷钾肥\n2. 分蘖肥:在移栽后7-10天施用,促进分蘖\n3. 穗肥:在幼穗分化期施用,促进穗大粒多\n4. 粒肥:在抽穗开花后施用,提高结实率和千粒重\n\n施肥原则:前重、中控、后补,避免后期氮肥过多导致贪青晚熟。"
        },
        {
            "instruction": "小麦锈病应该用什么药?",
            "input": "",
            "output": "小麦锈病的防治药剂:\n1. 预防:使用戊唑醇、苯醚甲环唑等杀菌剂进行种子处理\n2. 发病初期:使用三唑酮、烯唑醇等药剂喷雾防治\n3. 严重时:使用戊唑醇、丙环唑等药剂,间隔7-10天喷施2-3次\n\n注意事项:轮换使用不同作用机制的药剂,避免产生抗药性。"
        },
        {
            "instruction": "玉米大斑病的症状是什么?",
            "input": "",
            "output": "玉米大斑病的症状:\n1. 叶片症状:主要危害叶片,从下部叶片开始发病\n2. 病斑特征:病斑长梭形,灰褐色或黄褐色,边缘不明显\n3. 病斑大小:长5-10厘米,宽1-2厘米\n4. 严重时:多个病斑连片,导致叶片枯死\n5. 环境影响:高温高湿条件下发病严重"
        },
        {
            "instruction": "如何提高水稻产量?",
            "input": "",
            "output": "提高水稻产量的措施:\n1. 选用高产优质品种\n2. 培育壮秧,适时移栽\n3. 合理密植,保证基本苗数\n4. 科学施肥,平衡氮磷钾\n5. 合理灌溉,浅水勤灌\n6. 综合防治病虫害\n7. 适时收获,减少损失\n\n关键技术:测土配方施肥、节水灌溉、病虫害综合防治。"
        }
    ]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)

    logger.info(f"示例训练数据已保存至: {output_path}")


if __name__ == "__main__":
    # 创建示例数据
    create_sample_training_data("./agriculture_training_data.json")

    # 初始化LoRA微调服务
    lora_service = LoRAFineTuningService(
        model_path="./models/Qwen2.5-7B-Instruct",
        output_dir="./lora_output"
    )

    # 加载模型
    lora_service.load_model()

    # 准备LoRA模型
    lora_service.prepare_lora_model(
        r=8,
        lora_alpha=32,
        lora_dropout=0.05
    )

    # 加载训练数据
    dataset = lora_service.load_training_data("./agriculture_training_data.json")

    # 预处理数据
    tokenized_dataset = lora_service.preprocess_data(dataset, max_length=512)

    # 训练模型
    lora_service.train(
        dataset=tokenized_dataset,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4
    )

    # 清理资源
    lora_service.cleanup()
