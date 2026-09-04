import sys
from datetime import datetime
from models import Entry, ShopConfig
import storage
import runway


def parse_date(date_str: str) -> str:
    """দোকানদারের দেওয়া DD-MM-YYYY ফরম্যাটকে সিস্টেমের YYYY-MM-DD ফরম্যাটে রূপান্তর করে"""
    dt = datetime.strptime(date_str.strip(), "%d-%m-%Y")
    return dt.strftime("%Y-%m-%d")


def format_date(date_str: str) -> str:
    """সিস্টেমের YYYY-MM-DD ফরম্যাটকে ডিসপ্লের জন্য DD-MM-YYYY করে দেখায়"""
    dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
    return dt.strftime("%d-%m-%Y")


def add_entry_flow():
    print("\n--- নতুন দৈনিক হিসাব যোগ করুন ---")
    date_input = input("তারিখ দিন (DD-MM-YYYY, যেমন 04-09-2026): ")
    try:
        iso_date = parse_date(date_input)
    except ValueError:
        print("❌ ভুল তারিখের ফরম্যাট! দয়া করে DD-MM-YYYY ফরম্যাটে দিন।")
        return

    try:
        income = float(input("আজকের মোট বিক্রি/নগদ আয় (টাকা): "))
        expense = float(input("আজকের মোট খরচ (ভাড়া/মহাজন/বেতন ইত্যাদি) (টাকা): "))
    except ValueError:
        print("❌ টাকার পরিমাণ অবশ্যই সংখ্যায় হতে হবে!")
        return

    entry = Entry(date=iso_date, income=income, expense=expense)
    storage.save_entry(entry)
    print("✅ হিসাব সফলভাবে সংরক্ষণ করা হয়েছে।")


def view_status_flow():
    print("\n================ দোকানের আর্থিক স্বাস্থ্য ================")
    config = storage.load_config()
    entries = storage.load_entries()

    if not entries:
        print("⚠️ এখনো কোনো দৈনিক হিসাব এন্ট্রি করা হয়নি!")
        return

    avg_net = runway.average_burn(entries, window=7)
    runway_days, status = runway.calculate_runway(config.reserve, avg_net)
    is_critical = runway.check_alert(runway_days, config.alert_threshold)

    print(f"বর্তমান নগদ বাফার (Reserve)   : {config.reserve:,.2f} টাকা")
    print(f"দৈনিক গড় ক্যাশ ফ্লো (৭ দিন)  : {avg_net:,.2f} টাকা/দিন")
    print(f"ব্যবসার স্ট্যাটাস               : {status}")

    if runway_days is not None:
        print(f"আনুমানিক রানওয়ে (Runway)     : {runway_days} দিন")
        if is_critical:
            print(f"\n🚨 সতর্কতা: আপনার রানওয়ে {config.alert_threshold} দিনের নিচে নেমে গেছে! অবিলম্বে খরচ কমান।")
    else:
        print("🚀 চমৎকার! ব্যবসা লাভে বা ব্রেক-ইভেনে আছে, মূল নগদ টাকা অক্ষত।")
    print("==========================================================")


def stress_test_flow():
    print("\n--- স্ট্রেস টেস্টিং (বিক্রি কমে গেলে কী ঘটবে?) ---")
    entries = storage.load_entries()
    config = storage.load_config()

    if not entries:
        print("⚠️ স্ট্রেস টেস্ট করার জন্য আগে কিছু দৈনিক হিসাব যোগ করুন।")
        return

    scenarios = [20, 30, 50]
    print("\n{:<15} {:<22} {:<15}".format("বিক্রি ড্রপ", "নতুন দৈনিক বার্ন", "নতুন রানওয়ে"))
    print("-" * 55)

    for drop in scenarios:
        sim_net, sim_runway = runway.stress_test(entries, config.reserve, drop_percent=drop, window=7)
        burn_display = f"{sim_net:,.2f} টাকা/দিন"
        runway_display = f"{sim_runway} দিন" if sim_runway is not None else "Profitable/Infinite"
        print(f"-{drop}% বিক্রি        {burn_display:<22} {runway_display:<15}")
    print("-" * 55)


def settings_flow():
    print("\n--- দোকান সেটিংস ও বাফার কনফিগারেশন ---")
    config = storage.load_config()
    print(f"বর্তমান নগদ ব্যালেন্স : {config.reserve:,.2f} টাকা")
    print(f"বর্তমান অ্যালার্ট সীমা : {config.alert_threshold} দিন")

    try:
        new_res = input("নতুন নগদ বাফার দিন (পরিবর্তন না করতে Enter চাপুন): ")
        if new_res.strip():
            config.reserve = float(new_res)

        new_thresh = input("নতুন অ্যালার্ট থ্রেশহোল্ড দিন (দিন সংখ্যা, ফাঁকা রাখতে Enter): ")
        if new_thresh.strip():
            config.alert_threshold = int(new_thresh)

        storage.save_config(config)
        print("✅ সেটিংস সফলভাবে আপডেট হয়েছে।")
    except ValueError:
        print("❌ ভুল ইনপুট! পরিবর্তন বাতিল করা হয়েছে।")


def main():
    while True:
        print("\n=== SHOP CASH-RUNWAY TRACKER ===")
        print("1. দৈনিক আয়-ব্যয় যোগ করুন (Add Entry)")
        print("2. রানওয়ে ও আর্থিক স্বাস্থ্য দেখুন (View Status)")
        print("3. রেভিনিউ ড্রপ স্ট্রেস টেস্ট (Stress Test)")
        print("4. বাফার ক্যাশ ও সেটিংস (Settings)")
        print("5. বন্ধ করুন (Exit)")

        choice = input("মেনু সিলেক্ট করুন (১-৫): ").strip()

        if choice == "1":
            add_entry_flow()
        elif choice == "2":
            view_status_flow()
        elif choice == "3":
            stress_test_flow()
        elif choice == "4":
            settings_flow()
        elif choice == "5":
            print("অ্যাপ বন্ধ করা হচ্ছে। ভালো থাকুন!")
            sys.exit(0)
        else:
            print("❌ ভুল অপশন! ১ থেকে ৫-এর মধ্যে নির্বাচন করুন।")


if __name__ == "__main__":
    main()