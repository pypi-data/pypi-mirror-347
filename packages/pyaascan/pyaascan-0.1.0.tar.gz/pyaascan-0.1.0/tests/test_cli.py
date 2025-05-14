import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from unittest.mock import patch, mock_open
from argparse import Namespace
from pyaascan.cli import parse_args, read_sequence


class TestCLI(unittest.TestCase):
    @patch(
        "sys.argv",
        [
            "cli.py",
            "-s",
            "test_sequence.txt",
            "-c",
            "10",
            "-m",
            "5",
            "--codon1",
            "ATG",
            "--codon2",
            "TAA",
            "--codon3",
            "TAG",
            "--codon4",
            "TGA",
            "--minlen",
            "20",
            "--maxlen",
            "50",
            "--minGCcl",
            "3",
            "--mintm",
            "55.0",
            "--maxtm",
            "65.0",
            "-o",
            "short",
            "-v",
        ],
    )
    def test_parse_args(self):
        expected = Namespace(
            sequencefile="test_sequence.txt",
            codonpos=10,
            mutpos=5,
            codon1="ATG",
            codon2="TAA",
            codon3="TAG",
            codon4="TGA",
            minlen=20,
            maxlen=50,
            minGCcl=3,
            mintm=55.0,
            maxtm=65.0,
            outputmode="short",
            verbose=True,
        )
        args = parse_args()
        self.assertEqual(args, expected)

    @patch("builtins.open", new_callable=mock_open, read_data="ATGCGT\nGCA\n")
    def test_read_sequence(self, mock_file):
        filename = "test_sequence.txt"
        expected_sequence = "ATGCGTGCA"
        sequence = read_sequence(filename)
        mock_file.assert_called_once_with(filename, "r")
        self.assertEqual(sequence, expected_sequence)


if __name__ == "__main__":
    unittest.main()
