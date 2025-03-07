#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "G.J.J. van den Burg"

"""Tests"""

import unittest
import tempfile
import hashlib
import shutil
import os

from arxiv2remarkable import (
    ACM,
    Arxiv,
    LocalFile,
    OpenReview,
    PdfUrl,
    Pubmed,
    Springer,
)

VERBOSE = False


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

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_arxiv(self):
        prov = Arxiv(upload=False, verbose=VERBOSE)
        url = "https://arxiv.org/abs/1811.11242v1"
        exp_filename = "Burg_Nazabal_Sutton_-_Wrangling_Messy_CSV_Files_by_Detecting_Row_and_Type_Patterns_2018.pdf"
        filename = prov.run(url)
        self.assertEqual(exp_filename, os.path.basename(filename))

    def test_pmc(self):
        prov = Pubmed(upload=False, verbose=VERBOSE)
        url = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3474301/"
        exp_filename = (
            "Hoogenboom_Manske_-_How_to_Write_a_Scientific_Article_2012.pdf"
        )
        filename = prov.run(url)
        self.assertEqual(exp_filename, os.path.basename(filename))

    def test_acm(self):
        prov = ACM(upload=False, verbose=VERBOSE)
        url = "https://dl.acm.org/citation.cfm?id=3025626"
        exp_filename = "Kery_Horvath_Myers_-_Variolite_Supporting_Exploratory_Programming_by_Data_Scientists_2017.pdf"
        filename = prov.run(url)
        self.assertEqual(exp_filename, os.path.basename(filename))

    def test_openreview(self):
        prov = OpenReview(upload=False, verbose=VERBOSE)
        url = "https://openreview.net/forum?id=S1x4ghC9tQ"
        exp_filename = "Gregor_et_al_-_Temporal_Difference_Variational_Auto-Encoder_2018.pdf"
        filename = prov.run(url)
        self.assertEqual(exp_filename, os.path.basename(filename))

    def test_springer(self):
        prov = Springer(upload=False, verbose=VERBOSE)
        url = "https://link.springer.com/article/10.1007/s10618-019-00631-5"
        exp_filename = "Mauw_Ramirez-Cruz_Trujillo-Rasua_-_Robust_Active_Attacks_on_Social_Graphs_2019.pdf"
        filename = prov.run(url)
        self.assertEqual(exp_filename, os.path.basename(filename))

    def test_local(self):
        local_filename = "test.pdf"
        with open(local_filename, "w") as fp:
            fp.write(
                "%PDF-1.1\n%¥±ë\n\n1 0 obj\n  << /Type /Catalog\n     /Pages 2 0 R\n  >>\nendobj\n\n2 0 obj\n  << /Type /Pages\n     /Kids [3 0 R]\n     /Count 1\n     /MediaBox [0 0 300 144]\n  >>\nendobj\n\n3 0 obj\n  <<  /Type /Page\n      /Parent 2 0 R\n      /Resources\n       << /Font\n           << /F1\n               << /Type /Font\n                  /Subtype /Type1\n                  /BaseFont /Times-Roman\n               >>\n           >>\n       >>\n      /Contents 4 0 R\n  >>\nendobj\n\n4 0 obj\n  << /Length 55 >>\nstream\n  BT\n    /F1 18 Tf\n    0 0 Td\n    (Hello World) Tj\n  ET\nendstream\nendobj\n\nxref\n0 5\n0000000000 65535 f \n0000000018 00000 n \n0000000077 00000 n \n0000000178 00000 n \n0000000457 00000 n \ntrailer\n  <<  /Root 1 0 R\n      /Size 5\n  >>\nstartxref\n565\n%%EOF"
            )
        prov = LocalFile(upload=False, verbose=VERBOSE)
        filename = prov.run(local_filename)
        self.assertEqual("test_.pdf", os.path.basename(filename))

    def test_pdfurl(self):
        prov = PdfUrl(upload=False, verbose=VERBOSE)
        url = "http://www.jmlr.org/papers/volume17/14-526/14-526.pdf"
        filename = prov.run(url, filename="test.pdf")
        self.assertEqual("test.pdf", os.path.basename(filename))


if __name__ == "__main__":
    unittest.main()
