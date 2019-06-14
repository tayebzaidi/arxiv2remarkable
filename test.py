#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "G.J.J. van den Burg"

"""
Unit Tests for arxiv2remarkable

These tests only test two things: whether the filename is generated correctly, 
and whether the retrieved PDF matches what is in the test files archive.  
Uploading to the reMarkable is not tested.
"""

import hashlib
import os
import shutil
import tarfile
import tempfile
import unittest

from diff_pdf_visually import pdfdiff

from arxiv2remarkable import (
    ArxivProvider,
    PMCProvider,
    ACMProvider,
    OpenReviewProvider,
    LocalFileProvider,
    PdfUrlProvider,
)


def md5sum(filename):
    blocksize = 65536
    hasher = hashlib.md5()
    with open(filename, "rb") as fid:
        buf = fid.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = fid.read(blocksize)
    return hasher.hexdigest()


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_dir = os.getcwd()
        cls.test_archive = os.path.abspath("./a2rtestfiles.tar.xz")
        cls.test_files_dir = tempfile.mkdtemp()
        os.chdir(cls.test_files_dir)

        tar = tarfile.open(cls.test_archive)
        tar.extractall()
        tar.close()

        cls.test_files_dir = os.path.join(cls.test_files_dir, "a2rtest")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_files_dir)

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        #shutil.rmtree(self.test_dir)

    def archive_filename(self, name):
        archive_files = os.listdir(self.test_files_dir)
        if not name + ".pdf" in archive_files:
            raise ValueError("Archive doesn't have file for %s" % name)
        return os.path.join(self.test_files_dir, name + ".pdf")

    def _providerTest(self, provider, name, url, exp_fname, filename=None):
        prov = provider(upload=False)
        if filename is None:
            fname = prov.run(url)
        else:
            fname = prov.run(url, filename=filename)
        self.assertEqual(os.path.basename(fname), exp_fname)
        self.assertTrue(
            pdfdiff(fname, self.archive_filename(name), verbosity=2)
        )

    def test_arxiv(self):
        self._providerTest(
            ArxivProvider,
            "arxiv",
            "https://arxiv.org/abs/1811.11242v1",
            "Burg_Nazabal_Sutton_-_Wrangling_Messy_CSV_Files_by_Detecting_Row_and_Type_Patterns_2018.pdf",
        )

    def test_pmc(self):
        self._providerTest(
            PMCProvider,
            "pmc",
            "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3474301/",
            "Hoogenboom_Manske_-_How_to_Write_a_Scientific_Article_2012.pdf",
        )

    def test_acm(self):
        self._providerTest(
            ACMProvider,
            "acm",
            "https://dl.acm.org/citation.cfm?id=3025626",
            "Kery_Horvath_Myers_-_Variolite_Supporting_Exploratory_Programming_by_Data_Scientists_2017.pdf",
        )

    def test_openreview(self):
        self._providerTest(
            OpenReviewProvider,
            "openreview",
            "https://openreview.net/forum?id=S1x4ghC9tQ",
            "Gregor_et_al_-_Temporal_Difference_Variational_Auto-Encoder_2018.pdf",
        )

    def test_local(self):
        local_filename = "test.pdf"
        with open(local_filename, "w") as fp:
            fp.write(
                "%PDF-1.1\n%¥±ë\n\n1 0 obj\n  << /Type /Catalog\n     /Pages 2 0 R\n  >>\nendobj\n\n2 0 obj\n  << /Type /Pages\n     /Kids [3 0 R]\n     /Count 1\n     /MediaBox [0 0 300 144]\n  >>\nendobj\n\n3 0 obj\n  <<  /Type /Page\n      /Parent 2 0 R\n      /Resources\n       << /Font\n           << /F1\n               << /Type /Font\n                  /Subtype /Type1\n                  /BaseFont /Times-Roman\n               >>\n           >>\n       >>\n      /Contents 4 0 R\n  >>\nendobj\n\n4 0 obj\n  << /Length 55 >>\nstream\n  BT\n    /F1 18 Tf\n    0 0 Td\n    (Hello World) Tj\n  ET\nendstream\nendobj\n\nxref\n0 5\n0000000000 65535 f \n0000000018 00000 n \n0000000077 00000 n \n0000000178 00000 n \n0000000457 00000 n \ntrailer\n  <<  /Root 1 0 R\n      /Size 5\n  >>\nstartxref\n565\n%%EOF"
            )
        self._providerTest(
            LocalFileProvider, "local", local_filename, "test_.pdf"
        )

    def test_pdfurl(self):
        self._providerTest(
            PdfUrlProvider,
            "pdfurl",
            "http://www.jmlr.org/papers/volume17/14-526/14-526.pdf",
            "test.pdf",
            filename="test.pdf",
        )


if __name__ == "__main__":
    unittest.main()
