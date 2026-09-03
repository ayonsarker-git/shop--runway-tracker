from dataclasses import dataclass, asdict


@dataclass
class Entry:
    date: str          # ফরম্যাট: YYYY-MM-DD
    income: float      # মোট বিক্রি বা ক্যাশ ইনফ্লো
    expense: float     # মোট পরিচালন খরচ

    def to_dict(self):
        """JSON ফাইলে সেভ করার উপযোগী ডিকশনারি তৈরি করে"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        """ডিকশনারি/JSON ডেটা থেকে Entry অবজেক্ট তৈরি করে"""
        return cls(
            date=data["date"],
            income=float(data["income"]),
            expense=float(data["expense"])
        )


@dataclass
class ShopConfig:
    reserve: float              # বর্তমান নগদ বাফার (ক্যাশ + ব্যাংক)
    alert_threshold: int = 15   # রানওয়ে কত দিনের নিচে নামলে ওয়ার্নিং দেবে

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            reserve=float(data["reserve"]),
            alert_threshold=int(data.get("alert_threshold", 15))
        )