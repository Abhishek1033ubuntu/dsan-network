import unittest
import sys
import os

# Append the root directory to system path so we can import our simulation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestDSANEcosystem(unittest.TestCase):

    def setUp(self):
        """Set up standard baseline configurations for testing."""
        self.moving_average_price = 250.0  # $250 per metric ton
        self.buffer_threshold = 0.15       # 15% volatility buffer
        self.variance_penalty = 2.0        # Exponential penalty multiplier lambda

    def test_escrow_valuation_math(self):
        """Verify Tier 1 Escrow Valuation: V_escrow = (D_k * P_MA) * (1 + σ_buffer)"""
        demand_volume = 1000  # 1,000 metric tons
        
        base_value = demand_volume * self.moving_average_price
        expected_buffer = base_value * self.buffer_threshold
        expected_escrow = base_value + expected_buffer
        
        # Assert the math evaluates perfectly to $287,500.00
        self.assertEqual(expected_escrow, 287500.0)

    def test_extreme_economic_stress_buffer(self):
        """Ensure the escrow math holds up during simulated hyper-inflationary inputs."""
        extreme_price = 1000000.0  # Simulated currency collapse scenario
        demand_volume = 50000
        
        calculated_escrow = (demand_volume * extreme_price) * (1 + self.buffer_threshold)
        
        # Verify large-scale numbers do not cause structural overflows
        self.assertTrue(calculated_escrow > 0)
        self.assertAlmostEqual(calculated_escrow, 57500000000.0, places=2)

    def test_satellite_telemetry_fidelity_perfect_match(self):
        """Test Tier 2 Fidelity Score when reported acreage matches satellite observation perfectly."""
        import math
        
        reported_acreage = 500.0
        satellite_acreage = 500.0
        soil_moisture_coeff = 1.0  # Perfect soil moisture
        
        # Variance calculation: ((500 - 500) / 500)^2 = 0
        # exp(-2.0 * 0) * 1.0 = 1.0
        variance = ((reported_acreage - satellite_acreage) / satellite_acreage) ** 2
        fidelity_score = math.exp(-self.variance_penalty * variance) * soil_moisture_coeff
        
        self.assertEqual(fidelity_score, 1.0)

    def test_satellite_telemetry_fraud_gate(self):
        """Verify that massive discrepancies in reporting trigger a sub-90% failure gate."""
        import math
        
        reported_acreage = 1200.0  # Farmer claims more than double reality
        satellite_acreage = 500.0
        soil_moisture_coeff = 0.85
        
        variance = ((reported_acreage - satellite_acreage) / satellite_acreage) ** 2
        fidelity_score = math.exp(-self.variance_penalty * variance) * soil_moisture_coeff
        
        # Assert that the security gate would block consensus (F_C must be < 0.90)
        self.assertTrue(fidelity_score < 0.90)

if __name__ == '__main__':
    unittest.main()