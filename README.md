# Shop Cash-Runway Tracker

> A lightweight financial runway predictor & stress-testing engine built for local retail shops.

## 🎯 Problem
ক্ষুদ্র ও মাঝারি দোকানের মালিকরা সাধারণত দিনশেষে ক্যাশবাক্সে নগদ টাকা দেখে ভাবেন ব্যবসা ভালো চলছে। কিন্তু মাসের শেষে যখন হঠাৎ দোকান ভাড়া, কর্মচারীর বেতন বা মহাজনের বকেয়া পরিশোধ করতে হয়, তখন আকস্মিক ক্যাশ ক্রাইসিস তৈরি হয়। অ্যাকাউন্টিংয়ের খাতায় লাভ দেখানো সত্ত্বেও শুধুমাত্র ক্যাশ ফ্লো এবং বার্ন রেট ট্র্যাক না করার কারণে অনেক সম্ভাবনাময় দোকান বন্ধ হয়ে যায়।

## 💡 What it measures
এই টুলটি জটিল অ্যাকাউন্টিং পরিহার করে দোকানদারকে একটি সুনির্দিষ্ট অ্যাকশনেবল সংখ্যা দেয়: *"বর্তমান খরচের ট্রেন্ড অনুযায়ী আমার হাতের নগদ টাকায় দোকান আর কতদিন চলবে?"* এটি রোলিং অ্যাভারেজের মাধ্যমে আকস্মিক খরচের নয়েজ দূর করে প্রকৃত বার্ন রেট বের করে এবং বিক্রি ২০%-৫০% কমে গেলে রানওয়ে কতদিনে নামবে তা সিমুলেট করে আগাম সতর্কতা দেয়।

---

## 🗺️ Project Architecture & Roadmap

- [x] **Phase 0: Setup & Skeleton**
  - Git repository, `.gitignore` (Python standards), directory structure, and initial sync.
- [x] **Phase 1: Data Layer (`models.py`, `storage.py`)**
  - Single Responsibility Principle (SRP): decoupled data contracts from persistence.
  - `Entry` & `ShopConfig` models with serialization logic.
  - File-based JSON persistence engine.
- [ ] **Phase 2: Core Financial Logic (`runway.py`)**
  - Pure, side-effect-free financial calculation functions.
  - 7-day rolling average burn rate to filter out sudden expense spikes.
  - Zero-division prevention for profitable states (`Runway: Infinite/Profitable`).
  - Stress-testing engine for parameterized revenue drops (20%, 30%, 50%).
- [ ] **Phase 3: Automated Testing (`tests/test_runway.py`)**
  - Unit tests for edge cases: break-even, profitable shops, negative burn.
  - Testing stress-test simulations before touching any user interface.
- [ ] **Phase 4: User Interface (`main.py`)**
  - Frictionless CLI menu for daily shop entries.
  - Date localization adapter (`DD-MM-YYYY` for retail users).
  - Terminal alert badges (Runway < 15 days warning).
- [ ] **Phase 5: Technical Deep-Dive & Trade-offs**
  - Documenting architectural trade-offs: Flat expenses vs COGS, JSON vs SQLite.

---

## ⚙️ Design Decisions
*(Detailed write-ups will be added upon Phase 5 completion)*