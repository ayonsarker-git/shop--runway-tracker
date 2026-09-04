import unittest
from models import Entry
from runway import daily_net, average_burn, calculate_runway, check_alert, stress_test


class TestRunwayCalculations(unittest.TestCase):

    def setUp(self):
        """প্রতিটি টেস্টের জন্য কিছু ডামি সেলস/এক্সপেন্স ডেটা"""
        self.entries = [
            Entry(date="2026-09-01", income=5000, expense=7000),  # Net: -2000
            Entry(date="2026-09-02", income=6000, expense=8000),  # Net: -2000
            Entry(date="2026-09-03", income=4000, expense=6000),  # Net: -2000
        ]
        self.reserve = 60000.0  # ৬০,০০০ টাকা নগদ বাফার

    def test_daily_net(self):
        entry = Entry(date="2026-09-01", income=5000, expense=3000)
        self.assertEqual(daily_net(entry), 2000.0)

    def test_average_burn_negative(self):
        # প্রতিদিন গড়ে ২০০০ টাকা ক্যাশ লস হচ্ছে
        burn = average_burn(self.entries, window=3)
        self.assertEqual(burn, -2000.0)

    def test_runway_burning_cash(self):
        # ৬০,০০০ টাকা রিজার্ভ, প্রতিদিন লস ২০০০ -> রানওয়ে ৩০ দিন
        runway_days, status = calculate_runway(self.reserve, -2000.0)
        self.assertEqual(runway_days, 30.0)
        self.assertEqual(status, "Burning Cash")

    def test_runway_profitable_edge_case(self):
        # ব্যবসা লাভে থাকলে রানওয়ে None হবে (জিরো ডিভিশন হবে না)
        runway_days, status = calculate_runway(self.reserve, 1500.0)
        self.assertIsNone(runway_days)
        self.assertEqual(status, "Profitable")

    def test_alert_threshold(self):
        # রানওয়ে ১০ দিন, থ্রেশহোল্ড ১৫ দিন -> অ্যালার্ট True হওয়া উচিত
        self.assertTrue(check_alert(10.0, 15))
        # রানওয়ে ২০ দিন, থ্রেশহোল্ড ১৫ দিন -> অ্যালার্ট False হওয়া উচিত
        self.assertFalse(check_alert(20.0, 15))

    def test_stress_test(self):
        # বিক্রি ২০% কমে গেলে নতুন লস ও রানওয়ে সিমুলেশন
        # গড় ইনকাম ৫০০০ এর ২০% ড্রপ = ৪০০০, খরচ ৭০০০ -> নেট -৩০০০
        simulated_net, simulated_runway = stress_test(self.entries, self.reserve, drop_percent=20, window=3)
        self.assertEqual(simulated_net, -3000.0)
        self.assertEqual(simulated_runway, 20.0)


if __name__ == "__main__":
    unittest.main()