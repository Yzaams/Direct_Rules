#!/usr/bin/env python3
"""
AI规则合并脚本
⚠️ 需要修改的地方已用 ### 标注 ###
"""

import requests
import re
from pathlib import Path
from datetime import datetime

class AIRulesMerger:
    def __init__(self):
        # 🔧 这里可以修改规则来源，添加或删除
        self.sources = {
            'win-update': 'https://raw.githubusercontent.com/ForestL18/rules-dat/main/ai.txt',
            'category-games-cn': 'https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/openai.txt',
            'steamcn': 'https://ruleset.skk.moe/List/domainset/ai.conf',
            'nvidia': 'https://raw.githubusercontent.com/DustinWin/ruleset_geodata/main/rules/ai.txt'
            'cn_site': 'https://raw.githubusercontent.com/ForestL18/rules-dat/main/ai.txt',
            'chinadomains': 'https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/openai.txt',
            ### 如果想添加新的规则源，按照这个格式添加：
            ### 'SourceName': 'https://规则地址.txt',
        }
        
        self.all_domains = set()
        self.all_domain_suffixes = set()
        self.all_domain_keywords = set()
        
    def download_rules(self, url, source_name):
        """下载规则文件"""
        try:
            print(f"正在下载 {source_name} 规则...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"下载 {source_name} 失败: {e}")
            return ""
    
    def parse_rules(self, content, source_name):
        """解析规则内容"""
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 跳过注释和空行
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            # 处理不同格式的规则
            if line.startswith('DOMAIN-SUFFIX,'):
                domain = line.split(',', 1)[1].strip()
                self.all_domain_suffixes.add(domain)
            
            elif line.startswith('DOMAIN,'):
                domain = line.split(',', 1)[1].strip()
                self.all_domains.add(domain)
            
            elif line.startswith('DOMAIN-KEYWORD,'):
                keyword = line.split(',', 1)[1].strip()
                self.all_domain_keywords.add(keyword)
            
            elif line.startswith('.'):
                domain = line.lstrip('.').split(',')[0].strip()
                if domain:
                    self.all_domain_suffixes.add(domain)
            
            elif re.match(r'^[a-zA-Z0-9][-a-zA-Z0-9.]*\.[a-zA-Z]{2,}$', line):
                self.all_domain_suffixes.add(line)
        
        print(f"{source_name}: 找到规则 {len(self.all_domains) + len(self.all_domain_suffixes) + len(self.all_domain_keywords)} 条")
    
    def generate_text_rules(self, output_file='AIs_merged.txt'):
        """生成文本格式规则文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            # 写入头部信息
            f.write("# AI Services Merged Rules\n")
            f.write("# 合并来源: ForestL18, MetaCubeX, Sukka, DustinWin\n")
            f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# 统计: DOMAIN={len(self.all_domains)}, ")
            f.write(f"DOMAIN-SUFFIX={len(self.all_domain_suffixes)}, ")
            f.write(f"DOMAIN-KEYWORD={len(self.all_domain_keywords)}\n\n")
            
            # 写入规则
            for domain in sorted(self.all_domains):
                f.write(f"DOMAIN,{domain}\n")
            
            for domain in sorted(self.all_domain_suffixes):
                f.write(f"DOMAIN-SUFFIX,{domain}\n")
            
            for keyword in sorted(self.all_domain_keywords):
                f.write(f"DOMAIN-KEYWORD,{keyword}\n")
        
        print(f"\n✅ 文本规则已保存到: {output_file}")
        return output_file
    
    def run(self):
        """执行合并流程"""
        print("=" * 50)
        print("开始合并 AI 规则...")
        print("=" * 50)
        
        # 下载并解析所有规则
        for source_name, url in self.sources.items():
            content = self.download_rules(url, source_name)
            if content:
                self.parse_rules(content, source_name)
        
        # 统计结果
        total = len(self.all_domains) + len(self.all_domain_suffixes) + len(self.all_domain_keywords)
        print("\n" + "=" * 50)
        print("合并完成！")
        print(f"完整域名: {len(self.all_domains)} 条")
        print(f"域名后缀: {len(self.all_domain_suffixes)} 条")
        print(f"域名关键词: {len(self.all_domain_keywords)} 条")
        print(f"总规则数: {total} 条")
        print("=" * 50)
        
        # 生成文本规则
        text_file = self.generate_text_rules()
        return text_file


if __name__ == "__main__":
    merger = AIRulesMerger()
    merger.run()
