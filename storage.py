import json
import os
from typing import List
from models import Entry, ShopConfig

DATA_DIR = "data"
ENTRIES_FILE = os.path.join(DATA_DIR, "entries.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")


def _ensure_data_dir():
    """ডেটা ফোল্ডার না থাকলে স্বয়ংক্রিয়ভাবে তৈরি করবে"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def save_entry(entry: Entry) -> None:
    """নতুন একটি দৈনিক এন্ট্রি entries.json ফাইলে যোগ করবে"""
    _ensure_data_dir()
    entries = load_entries()
    entries.append(entry)
    
    with open(ENTRIES_FILE, "w", encoding="utf-8") as f:
        json.dump([e.to_dict() for e in entries], f, indent=4)


def load_entries() -> List[Entry]:
    """সব এন্ট্রি লোড করে তারিখ অনুযায়ী সাজিয়ে ফেরত দেবে"""
    if not os.path.exists(ENTRIES_FILE):
        return []
    
    with open(ENTRIES_FILE, "r", encoding="utf-8") as f:
        try:
            raw_data = json.load(f)
            return [Entry.from_dict(item) for item in raw_data]
        except json.JSONDecodeError:
            return []


def save_config(config: ShopConfig) -> None:
    """দোকানের ক্যাশ রিজার্ভ ও অ্যালার্ট সেটিংস সংরক্ষণ করবে"""
    _ensure_data_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config.to_dict(), f, indent=4)


def load_config() -> ShopConfig:
    """কনফিগ লোড করবে, না থাকলে ডিফল্ট মান (০ রিজার্ভ, ১৫ দিন অ্যালার্ট) দেবে"""
    if not os.path.exists(CONFIG_FILE):
        return ShopConfig(reserve=0.0, alert_threshold=15)
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            raw_data = json.load(f)
            return ShopConfig.from_dict(raw_data)
        except json.JSONDecodeError:
            return ShopConfig(reserve=0.0, alert_threshold=15)