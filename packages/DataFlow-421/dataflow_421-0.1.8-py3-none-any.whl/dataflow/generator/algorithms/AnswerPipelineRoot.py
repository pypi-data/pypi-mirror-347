# 根节点，用来将数据拆入不同的分支
import pandas as pd
# from dataflow.generator.algorithms.AnswerExtraction_qwenmatheval import UnitTextManager,StringCleaner,AnswerExtractor
from dataflow.utils.utils import get_generator
import logging
from dataflow.utils.registry import GENERATOR_REGISTRY
from dataflow.utils.utils import get_logger

@GENERATOR_REGISTRY.register()
class AnswerPipelineRoot:
    def __init__(self, config: dict):
        self.config = config
        self.input_file = config.get("input_file")
        self.input_answer_key = config.get("input_answer_key")
        self.input_gt_key = config.get("input_gt_key")
        self.output_file_with_gt = config.get("output_file_with_gt")
        self.output_file_without_gt = config.get("output_file_without_gt")
        self.logger = get_logger()

    def run(self):
        # 创建输出目录
        import os
        os.makedirs(os.path.dirname(self.output_file_with_gt), exist_ok=True)
        os.makedirs(os.path.dirname(self.output_file_without_gt), exist_ok=True)

        # 读取输入文件
        df = pd.read_json(self.input_file, lines=True)
        print(f"成功读取输入文件，共 {df.shape[0]} 行数据")
        print(f"数据列: {df.columns.tolist()}")
        
        if self.input_answer_key not in df.columns:
            raise ValueError(f"input_answer_key {self.input_answer_key} not in columns : {df.columns}")

        if self.input_gt_key not in df.columns or self.input_gt_key == "" or self.input_gt_key == None:
            # 直接copy input file 到 output file without gt
            df.to_json(self.output_file_without_gt, orient="records", lines=True)
            print(f"No gt in input file, copy input file to output file without gt")
            return


        # 初始化答案提取器
        unit_text_manager = get_generator("UnitTextManager")
        string_cleaner = get_generator("StringCleaner",unit_text_manager)
        answer_extractor = get_generator("AnswerExtractor",string_cleaner)
        print("成功初始化答案提取器")

        # 如果不存在gt，则用answer传入answer_extractor.extract_answer()提取gt,否则直接使用gt
        def extract_gt(answer,gt):
            try:
                if gt != "" and not pd.isna(gt):
                    return gt
                else:
                    if pd.isna(answer):
                        return None
                    elif answer == "":
                        return None
                    else:
                        return answer_extractor.extract_answer(answer)
            except Exception as e:
                return None
            
        success_count = 0
        fail_count = 0
        for _ in range(df.shape[0]):
            answer = df.loc[_,self.input_answer_key]
            gt = df.loc[_,self.input_gt_key]
            extracted_gt = extract_gt(answer,gt)
            
            if _ < 5:  # 只打印前5条记录的详细信息
                print(f"处理第 {_} 行: answer={answer}, original_gt={gt}, extracted_gt={extracted_gt}")
            
            if extracted_gt is not None:
                success_count += 1
            else:
                fail_count += 1
                
            df.loc[_,self.input_gt_key] = extracted_gt
        
        print(f"GT提取完成: 成功 {success_count} 条, 失败 {fail_count} 条")
        
        # 按有没有gt，将df拆成两个
        df_with_gt = df[df[self.input_gt_key].notna()]
        df_without_gt = df[df[self.input_gt_key].isna()]
        
        print(f"GT列空值数量: {df[self.input_gt_key].isna().sum()}")
        print(f"GT列非空值数量: {df[self.input_gt_key].notna().sum()}")
        
        # 输出
        df_with_gt.to_json(self.output_file_with_gt, orient="records", lines=True)
        df_without_gt.to_json(self.output_file_without_gt, orient="records", lines=True)
        print(f"output {df_with_gt.shape[0]} rows with gt to {self.output_file_with_gt}")
        print(f"output {df_without_gt.shape[0]} rows without gt to {self.output_file_without_gt}")
                
        



        
        