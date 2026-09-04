# Shop Cash-Runway Tracker

> A lightweight, zero-dependency financial runway predictor and revenue-drop stress-testing engine built for local retail MSMEs.

---

## 🎯 Problem Statement
ক্ষুদ্র ও মাঝারি দোকানের মালিকরা সাধারণত ক্যাশবাক্সের বর্তমান নগদ ব্যালেন্স দেখে ব্যবসার স্বাস্থ্য নির্ধারণ করেন। অ্যাকাউন্টিংয়ের খাতায় লাভ দেখানো সত্ত্বেও আকস্মিক বড় খরচ (দোকান ভাড়া, কর্মচারী বেতন, মহাজনের বকেয়া) আসার সময় লিকুইডিটি ক্রাইসিস তৈরি হয়। ক্যাশ-ইনফ্লো এবং আউটফ্লোর মধ্যে সময়ের অমিলের কারণে অনেক সম্ভাবনাময় ব্যবসা অকালে বন্ধ হয়ে যায়।

---

## 💡 What it Measures
* **Rolling Daily Burn Rate:** যেকোনো আকস্মিক একক বড় খরচের প্রভাবকে স্বাভাবিক করতে ৭ দিনের মুভিং নেট ক্যাশ ফ্লো ($Income - Expense$) হিসাব করে।
* **Cash Runway (in Days):** বর্তমান রিজার্ভ ক্যাশ দিয়ে কোনো বাড়তি সেলস ছাড়াই বর্তমান খরচে দোকান আর ঠিক কতদিন টিকে থাকতে পারবে ($Reserve \div Daily\ Burn$) তা প্রজেক্ট করে।
* **Early Warning Indicator:** রানওয়ে ১৫ দিনের নিচে নামলে টার্মিনালে স্বয়ংক্রিয় বিপদসংকেত ট্রিগার করে।
* **Stress-Testing Engine:** অর্থনৈতিক মন্দা বা পাইকারি সাপ্লাই ডিসরাপশনের কারণে বিক্রি ২০%, ৩০% বা ৫০% কমে গেলে রানওয়ে কত দ্রুত ড্রপ করবে তার রিয়েল-টাইম হোয়াট-ইফ সিমুলেশন।

---

## 🗺️ Project Architecture & Status

```text
shop-runway-tracker/
├── data/               # Persistent JSON storage (ignored by Git)
├── models.py           # Domain Data Contracts (Entry, ShopConfig)
├── storage.py          # Persistence Engine (File I/O & Serialization)
├── runway.py           # Pure Financial Calculation & Stress-Test Logic
├── main.py             # CLI Presentation Layer & Localization Adapter
├── tests/
│   └── test_runway.py  # Automated Unit Test Suite
├── .gitignore
└── README.md