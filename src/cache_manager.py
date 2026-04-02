"""
缓存策略与自动化更新模块
实现智能缓存、数据预取和 N8N 自动化推流
"""
import os
import json
import hashlib
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    data: Any
    created_at: datetime
    expires_at: datetime
    access_count: int = 0
    last_accessed: datetime = None
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return datetime.now() > self.expires_at
    
    def touch(self):
        """更新访问时间"""
        self.last_accessed = datetime.now()
        self.access_count += 1


class SmartCache:
    """智能缓存管理器"""
    
    def __init__(self, cache_dir: str = "./cache", max_size_mb: int = 100):
        self.cache_dir = Path(cache_dir)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.cache_index: Dict[str, CacheEntry] = {}
        
        # 创建缓存目录
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载索引
        self._load_index()
        
        # 缓存策略配置
        self.cache_policies = {
            # 高频更新数据 (赔率、比分) - 短缓存
            "odds": {"ttl_minutes": 5, "priority": "high"},
            "live_scores": {"ttl_minutes": 2, "priority": "high"},
            "fixtures": {"ttl_minutes": 30, "priority": "medium"},
            
            # 中频更新数据 (伤停、新闻) - 中等缓存
            "injuries": {"ttl_minutes": 60, "priority": "medium"},
            "team_news": {"ttl_minutes": 120, "priority": "low"},
            
            # 低频更新数据 (H2H、统计) - 长缓存
            "h2h_stats": {"ttl_hours": 24, "priority": "low"},
            "team_stats": {"ttl_hours": 12, "priority": "low"},
            
            # 静态资源 (球队 Logo、基础信息) - 强缓存
            "team_logos": {"ttl_days": 7, "priority": "low"},
            "player_info": {"ttl_days": 3, "priority": "low"}
        }
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        if key not in self.cache_index:
            return None
        
        entry = self.cache_index[key]
        
        # 检查是否过期
        if entry.is_expired():
            self.delete(key)
            return None
        
        # 更新访问记录
        entry.touch()
        
        # 从文件读取数据
        file_path = self._get_cache_file_path(key)
        if file_path.exists():
            try:
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"⚠️ 读取缓存失败：{e}")
                self.delete(key)
                return None
        
        return None
    
    def set(self, key: str, data: Any, policy_name: str = None) -> bool:
        """设置缓存数据"""
        # 确定缓存策略
        policy = self.cache_policies.get(
            policy_name or self._infer_policy_from_key(key),
            {"ttl_minutes": 30, "priority": "medium"}
        )
        
        # 计算过期时间
        now = datetime.now()
        if "ttl_days" in policy:
            expires = now + timedelta(days=policy["ttl_days"])
        elif "ttl_hours" in policy:
            expires = now + timedelta(hours=policy["ttl_hours"])
        else:
            expires = now + timedelta(minutes=policy.get("ttl_minutes", 30))
        
        # 创建缓存条目
        entry = CacheEntry(
            key=key,
            data=data,
            created_at=now,
            expires_at=expires
        )
        entry.touch()
        
        # 写入文件
        file_path = self._get_cache_file_path(key)
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            
            # 更新索引
            self.cache_index[key] = entry
            self._save_index()
            
            # 检查是否超出容量限制
            self._enforce_size_limit()
            
            return True
            
        except Exception as e:
            print(f"❌ 写入缓存失败：{e}")
            return False
    
    def delete(self, key: str):
        """删除缓存"""
        if key in self.cache_index:
            del self.cache_index[key]
        
        file_path = self._get_cache_file_path(key)
        if file_path.exists():
            file_path.unlink()
        
        self._save_index()
    
    def clear(self, priority: str = None):
        """清空缓存"""
        if priority:
            # 只清空特定优先级的缓存
            keys_to_delete = [
                k for k, v in self.cache_index.items()
                if self.cache_policies.get(v.key.split(":")[0], {}).get("priority") == priority
            ]
            for key in keys_to_delete:
                self.delete(key)
        else:
            # 清空所有缓存
            for key in list(self.cache_index.keys()):
                self.delete(key)
    
    def _get_cache_file_path(self, key: str) -> Path:
        """获取缓存文件路径"""
        # 使用哈希值作为文件名，避免特殊字符问题
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def _infer_policy_from_key(self, key: str) -> str:
        """从键名推断缓存策略"""
        key_lower = key.lower()
        
        if "odds" in key_lower or "price" in key_lower:
            return "odds"
        elif "live" in key_lower or "score" in key_lower:
            return "live_scores"
        elif "fixture" in key_lower or "match" in key_lower:
            return "fixtures"
        elif "injury" in key_lower or "suspension" in key_lower:
            return "injuries"
        elif "h2h" in key_lower or "history" in key_lower:
            return "h2h_stats"
        elif "logo" in key_lower or "image" in key_lower:
            return "team_logos"
        
        return "default"
    
    def _load_index(self):
        """加载缓存索引"""
        index_file = self.cache_dir / "index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r') as f:
                    data = json.load(f)
                
                # 重建索引对象
                for key, entry_data in data.items():
                    entry = CacheEntry(
                        key=entry_data["key"],
                        data=None,  # 延迟加载
                        created_at=datetime.fromisoformat(entry_data["created_at"]),
                        expires_at=datetime.fromisoformat(entry_data["expires_at"]),
                        access_count=entry_data["access_count"],
                        last_accessed=datetime.fromisoformat(entry_data["last_accessed"]) if entry_data.get("last_accessed") else None
                    )
                    
                    # 跳过已过期的索引
                    if not entry.is_expired():
                        self.cache_index[key] = entry
                        
            except Exception as e:
                print(f"⚠️ 加载缓存索引失败：{e}")
                self.cache_index = {}
    
    def _save_index(self):
        """保存缓存索引"""
        index_file = self.cache_dir / "index.json"
        
        # 转换为可序列化的格式
        serializable_index = {}
        for key, entry in self.cache_index.items():
            serializable_index[key] = {
                "key": entry.key,
                "created_at": entry.created_at.isoformat(),
                "expires_at": entry.expires_at.isoformat(),
                "access_count": entry.access_count,
                "last_accessed": entry.last_accessed.isoformat() if entry.last_accessed else None
            }
        
        try:
            with open(index_file, 'w') as f:
                json.dump(serializable_index, f, indent=2)
        except Exception as e:
            print(f"⚠️ 保存缓存索引失败：{e}")
    
    def _enforce_size_limit(self):
        """执行容量限制"""
        try:
            # 计算当前缓存大小
            total_size = sum(
                f.stat().st_size for f in self.cache_dir.glob("*.cache")
            )
            
            # 如果超出限制，删除最久未访问的条目
            while total_size > self.max_size_bytes and self.cache_index:
                # 找到最久未访问的条目
                oldest_key = min(
                    self.cache_index.keys(),
                    key=lambda k: self.cache_index[k].last_accessed or datetime.min
                )
                
                # 删除该条目
                file_path = self._get_cache_file_path(oldest_key)
                if file_path.exists():
                    total_size -= file_path.stat().st_size
                    file_path.unlink()
                
                del self.cache_index[oldest_key]
            
            self._save_index()
            
        except Exception as e:
            print(f"⚠️ 清理缓存失败：{e}")
    
    def get_stats(self) -> Dict:
        """获取缓存统计信息"""
        total_size = sum(
            f.stat().st_size for f in self.cache_dir.glob("*.cache")
        ) if self.cache_dir.exists() else 0
        
        return {
            "total_entries": len(self.cache_index),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "max_size_mb": self.max_size_bytes / (1024 * 1024),
            "hit_rate": self._calculate_hit_rate()
        }
    
    def _calculate_hit_rate(self) -> float:
        """计算命中率"""
        if not self.cache_index:
            return 0.0
        
        total_accesses = sum(e.access_count for e in self.cache_index.values())
        hits = sum(1 for e in self.cache_index.values() if e.access_count > 0)
        
        return hits / len(self.cache_index) if self.cache_index else 0.0


class DataPrefetcher:
    """数据预取器"""
    
    def __init__(self, cache: SmartCache):
        self.cache = cache
        self.prefetch_schedule = {
            "odds": {"interval_minutes": 5, "priority": "high"},
            "fixtures": {"interval_minutes": 30, "priority": "medium"},
            "injuries": {"interval_minutes": 60, "priority": "low"}
        }
    
    def prefetch_all(self, data_collector):
        """预取所有数据类型"""
        print("🔄 开始预取数据...")
        
        # 1. 预取赔率数据 (高优先级)
        try:
            odds_data = data_collector.fetch_casino_odds()
            self.cache.set("odds:latest", odds_data, "odds")
            print(f"✓ 预取赔率数据：{len(odds_data)} 场赛事")
        except Exception as e:
            print(f"⚠️ 预取赔率失败：{e}")
        
        # 2. 预取赛程数据
        try:
            from src.sports_data_api import FootballDataAPI
            football_api = FootballDataAPI()
            fixtures = football_api.get_fixtures(limit=20)
            self.cache.set("fixtures:today", fixtures, "fixtures")
            print(f"✓ 预取赛程数据：{len(fixtures)} 场比赛")
        except Exception as e:
            print(f"⚠️ 预取赛程失败：{e}")
        
        # 3. 预取伤停信息
        try:
            from src.sports_data_api import FootballDataAPI
            football_api = FootballDataAPI()
            injuries = football_api.get_injuries()
            self.cache.set("injuries:latest", injuries, "injuries")
            print(f"✓ 预取伤停信息：{len(injuries)} 条")
        except Exception as e:
            print(f"⚠️ 预取伤停失败：{e}")
        
        print("✅ 数据预取完成")


class N8NAutomation:
    """N8N 自动化推流集成"""
    
    def __init__(self, n8n_webhook_url: str = None):
        self.webhook_url = n8n_webhook_url or os.getenv("N8N_WEBHOOK_URL", "")
    
    def trigger_workflow(self, workflow_id: str, data: Dict = None) -> bool:
        """
        触发 N8N 工作流
        Args:
            workflow_id: 工作流 ID
            data: 传递给工作流的数据
        """
        if not self.webhook_url:
            print("⚠️ 未配置 N8N Webhook URL")
            return False
        
        try:
            import requests
            
            url = f"{self.webhook_url}/{workflow_id}"
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                print(f"✓ 触发 N8N 工作流成功：{workflow_id}")
                return True
            else:
                print(f"⚠️ 触发 N8N 工作流失败：{response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ N8N 触发失败：{e}")
            return False
    
    def send_new_match_alert(self, match_data: Dict):
        """发送新比赛提醒"""
        return self.trigger_workflow("new-match-alert", {
            "match_id": match_data.get("id"),
            "home_team": match_data.get("home_team"),
            "away_team": match_data.get("away_team"),
            "commence_time": match_data.get("commence_time"),
            "sport": match_data.get("sport")
        })
    
    def send_value_bet_alert(self, value_bet_data: Dict):
        """发送价值注提醒"""
        return self.trigger_workflow("value-bet-alert", {
            "match_id": value_bet_data.get("match_id"),
            "bet_type": value_bet_data.get("bet_type"),
            "bookmaker": value_bet_data.get("bookmaker"),
            "odds": value_bet_data.get("odds"),
            "edge_percent": value_bet_data.get("edge", 0) * 100
        })
    
    def update_database(self, data_type: str, records: List[Dict]):
        """更新数据库"""
        return self.trigger_workflow("update-database", {
            "data_type": data_type,
            "records": records,
            "timestamp": datetime.now().isoformat()
        })


# 全局缓存实例
_global_cache: Optional[SmartCache] = None


def get_cache() -> SmartCache:
    """获取全局缓存实例"""
    global _global_cache
    if _global_cache is None:
        _global_cache = SmartCache()
    return _global_cache


if __name__ == "__main__":
    # 测试代码
    print("\n💾 测试缓存与自动化系统\n")
    
    # 1. 测试智能缓存
    cache = SmartCache()
    
    # 设置缓存
    test_data = {"test": "data", "number": 123}
    cache.set("test:key", test_data, "odds")
    print("✓ 写入缓存数据")
    
    # 读取缓存
    cached_data = cache.get("test:key")
    print(f"✓ 读取缓存：{cached_data}")
    
    # 获取统计
    stats = cache.get_stats()
    print(f"✓ 缓存统计：{stats}")
    
    # 2. 测试 N8N 自动化
    n8n = N8NAutomation()
    
    sample_match = {
        "id": "test_123",
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "commence_time": datetime.now().isoformat(),
        "sport": "Football"
    }
    
    # n8n.send_new_match_alert(sample_match)  # 实际使用时取消注释
    
    print("\n✅ 缓存与自动化测试完成")
