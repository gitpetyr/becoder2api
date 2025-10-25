import json
import os
from typing import Dict, Tuple
import random

class OCRStats:
    def __init__(self, stats_file: str = "ocr_stats.json"):
        self.stats_file = stats_file
        self.stats = self._load_stats()
        
    def _load_stats(self) -> Dict[str, Dict[str, int]]:
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                return self._init_stats()
        return self._init_stats()
    
    def _init_stats(self) -> Dict[str, Dict[str, int]]:
        return {
            'ocr1': {'success': 0, 'total': 0},
            'ocr2': {'success': 0, 'total': 0},
            'ocr3': {'success': 0, 'total': 0}
        }
    
    def save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f)
    
    def update_stats(self, ocr_name: str, success: bool):
        self.stats[ocr_name]['total'] += 1
        if success:
            self.stats[ocr_name]['success'] += 1
        self.save_stats()
    
    def get_success_rates(self) -> Dict[str, float]:
        rates = {}
        for ocr_name, stats in self.stats.items():
            total = stats['total']
            if total == 0:
                rates[ocr_name] = 0.33  # 初始默认概率
            else:
                rates[ocr_name] = stats['success'] / total
        return rates
    
    def choose_ocr(self, exploration_rate: float = 0.2) -> str:
        # 随机探索
        if random.random() < exploration_rate:
            return random.choice(['ocr1', 'ocr2', 'ocr3'])
        
        # 选择最佳OCR
        success_rates = self.get_success_rates()
        return max(success_rates.items(), key=lambda x: x[1])[0]