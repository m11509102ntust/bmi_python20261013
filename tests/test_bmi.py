import unittest

from bmi import BmiCalculationError, bmi_guidance, calculate_bmi, parse_positive_number


class BmiUnitTests(unittest.TestCase):
    def test_parse_positive_number_accepts_finite_positive_values(self):
        self.assertEqual(parse_positive_number("65"), 65)
        self.assertIsNone(parse_positive_number(""))
        self.assertIsNone(parse_positive_number("0"))
        self.assertIsNone(parse_positive_number("inf"))

    def test_calculate_bmi(self):
        self.assertAlmostEqual(calculate_bmi(170, 65), 22.4913, places=3)

    def test_calculate_bmi_rejects_invalid_height_calculation(self):
        with self.assertRaises(BmiCalculationError) as context:
            calculate_bmi(1e-300, 65)
        self.assertEqual(context.exception.field, "height")

    def test_calculate_bmi_rejects_invalid_weight_calculation(self):
        with self.assertRaises(BmiCalculationError) as context:
            calculate_bmi(1, 1e308)
        self.assertEqual(context.exception.field, "weight")

    def test_taiwan_adult_thresholds(self):
        for bmi, category in [
            (18.4, "體重過輕"),
            (18.5, "健康體位"),
            (23.9, "健康體位"),
            (24.0, "體重過重"),
            (26.9, "體重過重"),
            (27.0, "肥胖"),
        ]:
            with self.subTest(bmi=bmi):
                self.assertEqual(bmi_guidance(bmi)["label"], category)


if __name__ == "__main__":
    unittest.main()
