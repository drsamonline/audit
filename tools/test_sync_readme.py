#!/usr/bin/env python3
"""Tests for sync_readme.py. Run: python3 tools/test_sync_readme.py"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


class TestSync(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.repo = os.path.join(self.tmp, "repo")
        os.makedirs(os.path.join(self.repo, "state"))
        # the tool finds the repo from its own path, so it must sit in <repo>/tools/
        os.makedirs(os.path.join(self.repo, "tools"))
        shutil.copy(os.path.join(HERE, "sync_readme.py"),
                    os.path.join(self.repo, "tools", "sync_readme.py"))
        self.write_state(3, [["a.yml"], ["b.yml", "c.yml"]], 2)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_state(self, count, workflows, schedules):
        repos = {("r%d" % i): {"workflow_files": w} for i, w in enumerate(workflows)}
        json.dump({"count": count, "repos": repos},
                  open(os.path.join(self.repo, "state", "repos.json"), "w"))
        json.dump({("s%d.yml" % i): {} for i in range(schedules)},
                  open(os.path.join(self.repo, "state", "schedules.json"), "w"))

    def write_readme(self, line):
        open(os.path.join(self.repo, "README.md"), "w").write("# audit\n\n" + line + "\n\nmore\n")

    def call(self, *args):
        return subprocess.run([sys.executable, os.path.join(self.repo, "tools", "sync_readme.py"), *args],
                              capture_output=True, text=True, cwd=self.repo)

    def test_a_stale_line_is_reported_and_the_exit_code_says_so(self):
        self.write_readme("The change log for the drsamonline fleet — **78 repositories, "
                          "105 workflow files, 10 scheduled jobs**.")
        p = self.call()
        self.assertEqual(1, p.returncode)
        self.assertIn("stale", p.stdout)

    def test_write_rewrites_from_the_snapshot(self):
        self.write_readme("The change log for the drsamonline fleet — **78 repositories, "
                          "105 workflow files, 10 scheduled jobs**.")
        p = self.call("--write")
        self.assertEqual(0, p.returncode, p.stderr)
        text = open(os.path.join(self.repo, "README.md")).read()
        # 3 repos, 3 workflow files across them, 2 schedules
        self.assertIn("**3 repositories, 3 workflow files, 2 scheduled jobs**", text)
        self.assertNotIn("78 repositories", text)

    def test_a_current_line_is_left_alone_and_says_so(self):
        self.write_readme("The change log for the drsamonline fleet — **3 repositories, "
                          "3 workflow files, 2 scheduled jobs**.")
        p = self.call()
        self.assertEqual(0, p.returncode)
        self.assertIn("current", p.stdout)

    def test_it_will_not_edit_a_readme_it_does_not_recognise(self):
        self.write_readme("Something else entirely about the fleet.")
        p = self.call("--write")
        self.assertNotEqual(0, p.returncode)
        self.assertIn("will not edit", p.stderr)

    def test_it_refuses_a_zero_repository_snapshot(self):
        self.write_state(0, [], 0)
        self.write_readme("The change log for the drsamonline fleet — **78 repositories, "
                          "105 workflow files, 10 scheduled jobs**.")
        p = self.call("--write")
        self.assertNotEqual(0, p.returncode)
        self.assertIn("failed crawl", p.stderr)

    def test_the_real_readme_in_this_repo_is_current(self):
        p = subprocess.run([sys.executable, os.path.join(HERE, "sync_readme.py")],
                           capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(0, p.returncode, p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
