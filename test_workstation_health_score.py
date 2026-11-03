import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import score


def row(disk=50, idle=50, updates=0, reboot=5):
    return {"host": "h", "disk_free_pct": str(disk), "cpu_idle_pct": str(idle),
            "pending_updates": str(updates), "last_reboot_days": str(reboot)}


class TestHealthScore(unittest.TestCase):
    def test_clean_host_is_100(self):
        self.assertEqual(score(row()), (100, "HEALTHY"))

    def test_full_disk_costs_30(self):
        self.assertEqual(score(row(disk=5))[0], 70)

    def test_update_penalty_capped(self):
        self.assertEqual(score(row(updates=50))[0], 80)

    def test_many_problems_mean_action(self):
        self.assertEqual(score(row(disk=5, idle=5, updates=10, reboot=40))[1], "ACTION")
