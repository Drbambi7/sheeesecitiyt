import hashlib
import unittest

from sovereign_asset_protection import SovereignAssetProtection


class SovereignAssetProtectionTests(unittest.TestCase):
    def setUp(self):
        self.protection = SovereignAssetProtection()
        self.valid_signature = hashlib.sha256(
            (
                f"{self.protection.owner}:"
                f"{self.protection.encryption_salt}"
            ).encode()
        ).hexdigest()

    def test_verify_ownership_accepts_matching_signature(self):
        self.assertTrue(self.protection.verify_ownership(self.valid_signature))

    def test_verify_ownership_rejects_mismatched_signature(self):
        self.assertFalse(self.protection.verify_ownership("invalid"))
        self.assertFalse(self.protection.verify_ownership(""))
        self.assertFalse(self.protection.verify_ownership("סימן"))
        self.assertFalse(self.protection.verify_ownership(None))

    def test_lock_intellectual_property_returns_protection_metadata(self):
        result = self.protection.lock_intellectual_property()

        self.assertEqual(result["status"], "SECURED_AND_LOCKED")
        self.assertEqual(result["legal_owner"], self.protection.owner)
        self.assertEqual(
            result["ip_rights"],
            "All Rights Reserved - Trade Secret Protection",
        )
        self.assertIsInstance(result["timestamp"], float)
        self.assertIn("Unauthorized replication", result["message"])


if __name__ == "__main__":
    unittest.main()
