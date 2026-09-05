import unittest
from unittest.mock import patch

import scout


class ScoutCoreTests(unittest.TestCase):
    def test_greenhouse_source_parsing(self):
        self.assertEqual(scout.parse_source_url("https://boards.greenhouse.io/acme"), ("greenhouse", "acme"))

    def test_lever_source_parsing(self):
        self.assertEqual(scout.parse_source_url("https://jobs.lever.co/acme"), ("lever", "acme"))

    def test_ashby_source_parsing(self):
        self.assertEqual(scout.parse_source_url("https://jobs.ashbyhq.com/acme"), ("ashby", "acme"))

    def test_unknown_source_is_rejected(self):
        with self.assertRaises(ValueError):
            scout.parse_source_url("https://example.com/careers")

    def test_keyword_score_penalizes_senior_job(self):
        job = scout.Job("x", "Example", "1", "Senior Data Engineering Manager", "", "", "Python SQL data analytics")
        with patch.object(scout, "load_candidate_profile", return_value={"verified_skills": ["Python", "SQL"]}):
            score, _ = scout.keyword_score(job)
        self.assertLess(score, 70)


if __name__ == "__main__":
    unittest.main()
