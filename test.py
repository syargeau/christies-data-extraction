"""
Unit tests.

This module includes all unit tests for the program. These are
ran through Travis CI when pushed to Git.
"""

import unittest

from main import find_dimensions, get_usd_price
import config

class DataPrepTest(unittest.TestCase):
    """Tests that ensure data is prepared as expected."""

    def test_find_dimensions(self):
        dimension_case_1 = 'Height: 6 7/8 in. (17.5 cm.)\nLength: 21 5/8 in. (55 cm.)\n'
        dimensions = find_dimensions(dimension_case_1)
        self.assertEqual(dimensions['height'], 17.5)
        self.assertEqual(dimensions['width'], 55)

        dimension_case_2 = 'oil on canvas\n5 3/8 x 7 in. (13.7 x 17.8 cm.)\n'
        dimensions = find_dimensions(dimension_case_2)
        self.assertEqual(dimensions['height'], 13.7)
        self.assertEqual(dimensions['width'], 17.8)

    def test_get_usd_price(self):
        usd_price = get_usd_price('$12,000')
        self.assertEqual(usd_price, 12000)
        gbp_price = get_usd_price('£12,000')
        self.assertEqual(gbp_price, 12000 * config.GBP_TO_USD_EXCHANGE_RATE)


if __name__ == '__main__':
    unittest.main()
