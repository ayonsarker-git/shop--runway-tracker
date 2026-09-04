from typing import List, Optional, Tuple
from models import Entry


def daily_net(entry: Entry) -> float:
    """একদিনের নেট ক্যাশ ফ্লো (বিক্রি - খরচ)"""
    return entry.income - entry.expense


def average_burn(entries: List[Entry], window: int = 7) -> float:
    """
    শেষ N দিনের (ডিফল্ট ৭ দিন) গড় দৈনিক নেট ক্যাশ ফ্লো বের করে।
    নেগেটিভ মান মানে ব্যবসা ক্যাশ লস করছে (Burn)।
    """
    if not entries:
        return 0.0

    # তারিখ অনুযায়ী সাজিয়ে শেষ 'window' সংখ্যক দিনের ডেটা নেওয়া
    recent = sorted(entries, key=lambda x: x.date)[-window:]
    total_net = sum(daily_net(e) for e in recent)
    return round(total_net / len(recent), 2)


def calculate_runway(reserve: float, avg_net: float) -> Tuple[Optional[float], str]:
    """
    রিজার্ভ ও গড় নেটের ওপর ভিত্তি করে রানওয়ে দিন হিসাব করে।
    রিটার্ন: (দিন সংখ্যা বা None, স্ট্যাটাস মেসেজ)
    """
    if avg_net > 0:
        return None, "Profitable"

    if avg_net == 0:
        return None, "Breakeven"

    # ক্যাশ বার্ন হচ্ছে (avg_net নেগেটিভ)
    daily_burn = abs(avg_net)
    runway_days = reserve / daily_burn
    return round(runway_days, 1), "Burning Cash"


def check_alert(runway_days: Optional[float], threshold: int) -> bool:
    """রানওয়ে বিপদসীমার (Threshold) নিচে নামলে সতর্কবার্তা ট্রিগার করবে"""
    if runway_days is None:
        return False  # লাভে থাকলে কোনো অ্যালার্টের প্রয়োজন নেই
    return runway_days < threshold


def stress_test(
    entries: List[Entry], 
    reserve: float, 
    drop_percent: float, 
    window: int = 7
) -> Tuple[float, Optional[float]]:
    """
    বিক্রি নির্দিষ্ট হারে কমে গেলে (যেমন: ২০%, ৫০%) নতুন বার্ন রেট ও রানওয়ে সিমুলেট করে।
    রিটার্ন: (সিমুলেটেড গড় নেট, নতুন রানওয়ে)
    """
    if not entries:
        return 0.0, None

    recent = sorted(entries, key=lambda x: x.date)[-window:]
    multiplier = 1.0 - (drop_percent / 100.0)

    # ইনকাম কমিয়ে খরচ অপরিবর্তিত রেখে নতুন নেট ফ্লো হিসাব
    simulated_nets = [(e.income * multiplier) - e.expense for e in recent]
    simulated_avg_net = round(sum(simulated_nets) / len(simulated_nets), 2)

    simulated_runway, _ = calculate_runway(reserve, simulated_avg_net)
    return simulated_avg_net, simulated_runway