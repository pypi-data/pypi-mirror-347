from openai import OpenAI
import os
import pandas as pd
from tqdm import tqdm
import concurrent.futures
import warnings
import pickle
warnings.filterwarnings('ignore')
import json

class P_chat_to_excel:
    def __init__(self,
                 name,
                 api_key ,
                 base_url):
        self.help = '''
# Chat-to-Excel 智能表格分析工具

通过大模型（如通义千问）自动解析Excel文本数据，支持智能分析、结果保存与Prompt配置持久化

---

## 📌 核心亮点

### **Prompt配置持久化** 🔄
- **自动保存**：每次通过`info_collect()`设置的prompt/inquiry等参数，将自动保存至本地`prompt_tomb`目录
- **按名称隔离**：通过`name`参数创建不同实例，实现多组独立配置共存（如客服质检/舆情分析等场景）
- **断点续用**：重启程序时自动加载同名实例的历史配置，无需重复输入参数
- **灵活管理**：通过例如`info_collect(param='prompt')`可单独修改特定参数，保留其他配置不变

---

## 🚀 主要功能

### 1. 大模型交互
- 支持Qwen系列模型（默认qwen-plus）
- 多线程并发处理（自动适配CPU核心数）
- 错误自动重试机制（单条数据最大重试2次）

### 2. 数据预处理
- 通话记录结构化解析（JSON→角色/内容）
- 非人工对话内容过滤（如系统提示音）

### 3. 灵活分析模式
- **全量分析**：处理完整数据集
- **抽样调试**：通过`data_sample()`抽取小样本测试Prompt效果
- **单/多字段**：支持单列独立分析或多列联合分析

### 4. 结果输出
- 自动插入分析结果列
- 保留原始数据结构
- 支持xlsx格式导出

---
 
'''
        self.df = None
        self.api_key = api_key
        self.base_url = base_url
        self.client = OpenAI(
            api_key = api_key,
            base_url= base_url,
        )
        self.model = 'qwen-plus'
        self.name = name
        self.__tomb_directory = 'prompt_tomb'
        if os.path.exists(rf'prompt_tomb\{name}_tomb.pkl'):
            with open(rf'prompt_tomb\{name}_tomb.pkl', 'rb') as f:
                self.prompt = pickle.load(f)
        else:
            self.prompt = ''

    def excel_info(self,path,column):
        df = pd.read_excel(path)
        df_filter = df.filter(column)
        self.df = df_filter

    def data_parsing(self,column,truncate_word = '为您服务'):
        list_total = []
        self.df[column] = self.df[column].str.replace('excel单元格限制长度可能有截取：','')
        for x in self.df[column].tolist():
            trigger = False
            try:
                list_context = []
                for i in json.loads(x):
                    if not trigger:
                        if i['text'].find(truncate_word) > -1 and i['text'].find('为了更好') == -1:
                            trigger = True
                            dict_ = {}
                            dict_['role'] = i['role']
                            dict_['text'] = i['text']
                            list_context.append(dict_)
                        else:
                            pass
                    else:
                        dict_ = {}
                        dict_['role'] = i['role']
                        dict_['text'] = i['text']
                        list_context.append(dict_)
                list_total.append(list_context)
            except:
                list_total.append({})
        self.df[column] = list_total
        self.df = self.df[self.df[column] != '[]']
        print('解析完成')

    def concat(self,column):
        for i in column:
            self.df[f'column{i}'] = i + '：' + self.df[i]
        columns_to_combine = self.df.filter(regex='^column').columns
        self.df['combined'] = self.df[columns_to_combine].agg('；'.join, axis=1)
        self.df = self.df.drop(columns=columns_to_combine)

    def __save_to_hell(self):
        os.makedirs(self.__tomb_directory, exist_ok=True)
        with open(rf'prompt_tomb\{self.name}_tomb.pkl', 'wb') as f:
            pickle.dump(self.prompt, f)

    def data_sample(self,num):
        df_sample = self.df.sample(num)
        self.df_sample = df_sample
        print(f'已随机抽取{num}行，请调用df_sample属性查看')

    def info_collect(self,param = None):
        if param:
            if hasattr(self, param):
                replace = input(f'{param}:')
                setattr(self, param, replace)
            else:
                print(f'类中没有名为 {param} 的属性。')
        else:
            if len(self.prompt) == 0 :
                self.prompt = input('prompt（AI的人设）:\n')
            self.inquiry = input('inquiry（询问的内容）：\n')
            self.column = input('column（表格中的目标字段）：\n')
            self.result_column_name = input('result_column_name（结果字段的名称）：\n')
            self.file_path = input('file_path（结果保存到本地的地址）：\n')
        self.__save_to_hell()

    def __chat_single(self,sample = False):
        def chat_prepare(i):
            retries = 0
            try:
                result = []
                completion = self.client.chat.completions.create(
                    model= self.model,
                    messages=[
                        {'role': 'system', 'content': self.prompt},
                        {'role': 'user', 'content': f'这有一段文本：{i}。{self.inquiry}。'}]
                )
                reply = completion.choices[0].message.content
                result.append(reply)
                return result[0]
            except Exception as e:
                while retries < 2:
                    try:
                        retries += 1
                        print(f'出错：{e}，正在进行第{retries}次重试，最大重试次数：2')
                        result = []
                        completion = self.client.chat.completions.create(
                            model= self.model,
                            messages=[
                                {'role': 'system', 'content': self.prompt},
                                {'role': 'user', 'content': f'这有一段文本：{i}。{self.inquiry}。'}]
                        )
                        reply = completion.choices[0].message.content
                        result.append(reply)
                        return result[0]
                        retries = 2
                    except:
                        retries += 1
                        print(f'出错：{e}，正在进行第{retries}次重试，最大重试次数：2')
                        result = []
                        completion = self.client.chat.completions.create(
                            model= self.model,
                            messages=[
                                {'role': 'system', 'content': self.prompt},
                                {'role': 'user', 'content': f'这有一段文本：{i}。{self.inquiry}。'}]
                        )
                        reply = completion.choices[0].message.content
                        result.append(reply)
                        return result[0]
        if not sample:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(tqdm(executor.map(chat_prepare, self.df[self.column]), total=len(self.df[self.column])))
                self.results = results
            self.df[self.result_column_name] = results
            self.df.to_excel(self.file_path,index = False)
            print('done')
        else:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = list(tqdm(executor.map(chat_prepare, self.df_sample[self.column]), total=len(self.df_sample[self.column])))
                self.results = results
            self.df_sample[self.result_column_name] = results
            self.df_sample.to_excel(self.file_path,index = False)
            print('done')

    def __chat_multiple(self,axis = 1,sample = False):
        columns = self.df.columns
        def chat_prepare(i):
            retries = 0
            try:
                result = []
                completion = self.client.chat.completions.create(
                    model= self.model,
                    messages=[
                        {'role': 'system', 'content': self.prompt},
                        {'role': 'user', 'content': f'这有一段文本：{i}。{self.inquiry}。'}]
                )
                reply = completion.choices[0].message.content
                result.append(reply)
                return result[0]
            except Exception as e:
                while retries < 2:
                    try:
                        retries += 1
                        print(f'出错：{e}，正在进行第{retries}次重试，最大重试次数：2')
                        result = []
                        completion = self.client.chat.completions.create(
                            model= self.model,
                            messages=[
                                {'role': 'system', 'content': self.prompt},
                                {'role': 'user', 'content': f'这有一段文本：{i}。{self.inquiry}。'}]
                        )
                        reply = completion.choices[0].message.content
                        result.append(reply)
                        return result[0]
                        retries = 2
                    except:
                        retries += 1
                        print(f'出错：{e}，正在进行第{retries}次重试，最大重试次数：2')
                        result = []
                        completion = self.client.chat.completions.create(
                            model= self.model,
                            messages=[
                                {'role': 'system', 'content': self.prompt},
                                {'role': 'user', 'content': f'这有一段文本：{i}。{self.inquiry}。'}]
                        )
                        reply = completion.choices[0].message.content
                        result.append(reply)
                        return result[0]
        if axis == 1:
            for target_column in tqdm(columns):
                self.target_column = target_column
                if not sample:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = list(tqdm(executor.map(chat_prepare, self.df[self.target_column]), total=len(self.df[self.target_column])))
                        self.results = results
                    target_index = self.df.columns.get_loc(target_column)
                    self.df.insert(target_index + 1, f'{target_column}-{self.result_column_name}', results)
                    self.df.to_excel(self.file_path,index = False)
                    print('done')
                else:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = list(tqdm(executor.map(chat_prepare, self.df_sample[self.target_column]), total=len(self.df_sample[self.target_column])))
                        self.results = results
                    target_index = self.df_sample.columns.get_loc(target_column)
                    self.df_sample.insert(target_index + 1, f'{target_column}-{self.result_column_name}', results)
                    self.df_sample.to_excel(self.file_path,index = False)
                    print('done')
        else:
            self.results = []
            column_content = []
            for target_column in tqdm(columns):
                self.target_column = target_column
                if not sample:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = list(tqdm(executor.map(chat_prepare, self.df[self.target_column]), total=len(self.df[self.target_column])))
                        self.results.extend(results)
                    column_content.extend([target_column]*len(self.df[self.target_column]))
                else:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        results = list(tqdm(executor.map(chat_prepare, self.df_sample[self.target_column]), total=len(self.df_sample[self.target_column])))
                        self.results.extend(results)
                    column_content.extend([target_column]*len(self.df_sample[self.target_column]))
            pd.DataFrame({'目标内容':column_content,self.result_column_name: self.results}).to_excel(self.file_path,index = False)
            print('done')

    def chat(self,sample=False,axis=None):
        if axis:
            self.__chat_multiple(axis = axis,sample = sample)
        else:
            self.__chat_single(sample = sample)





