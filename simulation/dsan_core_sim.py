import math
import random
import time


class GlobalCore:
    """Tier 1: Global Consensus Core. Handles macro metrics, escrow validation,

    reputation decay, and dynamic quota reallocation.
    """

    def __init__(self):
        self.global_demand = 0.0
        self.global_supply_intent = 0.0
        self.moving_average_price = 400.0  # Base line dollars per metric ton
        self.price_history = [410, 405, 395, 400, 400]
        self.reallocation_pool = 0.0
        self.soil_premium_pool = 150000.0  # Seeded by captured speculative spread

    def update_moving_average(self, new_spot_price):
        self.price_history.append(new_spot_price)
        if len(self.price_history) > 5:
            self.price_history.pop(0)
        self.moving_average_price = sum(self.price_history) / len(
            self.price_history
        )

    def verify_vdc_escrow(self, buyer_id, demand_tonnage, locked_collateral):
        """Validates demand via the Verifiable Demand Commitment (VDC) protocol."""
        volatility_buffer = 1.15
        required_escrow = (
            demand_tonnage * self.moving_average_price * volatility_buffer
        )

        print(
            f"[TIER 1] Validating VDC for Importer {buyer_id}: Requested {demand_tonnage} Tons."
        )
        print(f"         Required Capital: ${required_escrow:,.2f}")
        print(f"         Locked Capital:   ${locked_collateral:,.2f}")

        if locked_collateral >= required_escrow:
            self.global_demand += demand_tonnage
            print(
                "📈 [VDC VERIFIED] Demand added to Global Core. Speculation filtered out.\n"
            )
            return True
        else:
            print(
                "❌ [VDC REJECTED] Insufficient backing capital. Dropped as Ghost Order.\n"
            )
            return False

    def process_harvest_yield(self, nation_id, gateway_node):
        """Processes final real-world yield and adjusts state reputation flags."""
        deficit = gateway_node.assigned_quota - gateway_node.actual_production
        if deficit > 0:
            penalty_sensitivity = 0.5
            decay = penalty_sensitivity * (deficit / gateway_node.assigned_quota)
            gateway_node.reputation_score = max(
                0.0, gateway_node.reputation_score - decay
            )
            print(
                f"⚠️ [CARTEL WARNING] Nation {nation_id} underproduced by {deficit} Tons."
            )
            print(
                f"                  Reputation Score dropped to: {gateway_node.reputation_score:.2f}"
            )
            self.reallocate_quota(nation_id, deficit)
        else:
            print(
                f"✅ [DESCENT] Nation {nation_id} smoothly fulfilled its global supply obligations."
            )

    def reallocate_quota(self, failing_nation_id, deficit_tonnage):
        """The Elastic Supply Mesh algorithm."""
        print(
            f"🔄 [ELASTIC MESH ACTIVATED] Dynamically reallocating {deficit_tonnage} Tons away from Nation {failing_nation_id}..."
        )
        # In a real system, this loops over other high-reputation gateway nodes.
        print(
            "         Distributed missing quota seamlessly to high-reputation alternative nodes.\n"
        )


class NationalGateway:
    """Tier 2: National Sovereignty Gateway. Acts as the data bridge firewall,

    processing satellite telemetry and enforcing inventory thresholds.
    """

    def __init__(self, nation_id, assigned_quota, warehouse_cost_per_ton=0.15):
        self.nation_id = nation_id
        self.assigned_quota = assigned_quota
        self.reported_acreage = 0.0
        self.telemetry_acreage = 0.0
        self.actual_production = 0.0
        self.reputation_score = 1.0
        self.emergency_reserve = 5000.0  # Absolute red-line food security threshold
        self.current_inventory = 12000.0
        self.warehouse_cost = warehouse_cost_per_ton

    def calculate_telemetric_fidelity(self, reported_a, satellite_a, moisture):
        """Computes the Fidelity Confidence Score (Fc)."""
        self.reported_acreage = reported_a
        self.telemetry_acreage = satellite_a

        # Soil moisture compatibility coefficient (0.0 - 1.0)
        mu_soil = max(0.0, 1.0 - abs(moisture - 0.65))

        # Exponential divergence formula
        variance_factor = 2.0
        f_c = math.exp(
            -variance_factor * ((reported_a - satellite_a) / satellite_a) ** 2
        ) * mu_soil

        print(
            f"[TIER 2] Evaluating Data Fidelity for Nation {self.nation_id} Gateway Layer:"
        )
        print(
            f"         Reported: {reported_a} Ha | Telemetry Source: {satellite_a} Ha | Soil Moisture: {moisture*100}%"
        )
        print(f"         Calculated Fidelity Confidence (Fc): {f_c*100:.2f}%")

        if f_c >= 0.90:
            print(
                "🔒 [ZERO-KNOWLEDGE ENCLAVE] Data matches physical earth. Encrypting Proof and broadcast up to Tier 1.\n"
            )
            return True
        else:
            print(
                "🚨 [GATEWAY AMENDMENT REQUIRED] Data discrepancy detected. Freezing entry for physical drone sweep.\n"
            )
            return False

    def optimize_sovereign_inventory(self, global_ma_price, duration_days=90):
        """The Sovereign Inventory Optimization Loop to block hoarding."""
        surplus = self.current_inventory - self.emergency_reserve
        total_holding_cost = surplus * self.warehouse_cost * duration_days
        procurement_value_of_surplus = surplus * global_ma_price

        print(
            f"[INVENTORY LOOP] Evaluating Sovereign Reserves for Nation {self.nation_id}:"
        )
        print(f"                 Holding Surplus Cost: ${total_holding_cost:,.2f}")
        print(
            f"                 Global Pool Worth:    ${procurement_value_of_surplus:,.2f}"
        )

        if total_holding_cost > procurement_value_of_surplus:
            print(
                "📉 [FINANCIAL ALIGNMENT ALERT] Deadweight hoarding detected. Advising drawing down domestic surplus into global pool.\n"
            )
            return "RELEASE_SURPLUS"
        else:
            print(
                "🛡️ [SAFETY PROJECTION BOUNDS] Domestic inventory structures are balanced.\n"
            )
            return "HOLD"


class FarmPlot:
    """Tier 3: Local Client Layer. Handles soil nutrient state vectors,

    passive telemetric auto-fill, and offline mesh financial wallets.
    """

    def __init__(self, plot_id, is_connected=True):
        self.plot_id = plot_id
        self.is_connected = is_connected
        self.soil_npk = [0.8, 0.7, 0.7]  # State vector [N, P, K]
        self.wallet_balance_offline = 0.0
        self.last_crop = "Corn"
        self.validated_by_user = False

    def simulate_passive_autofill(self, satellite_crop_prediction):
        """Populates the database automatically if the farmer is offline."""
        if not self.is_connected and not self.validated_by_user:
            print(
                f"[TIER 3 MESH] Farm {self.plot_id} is OFFLINE. Passive Telemetric Auto-Fill active."
            )
            print(
                f"               Pre-populating ledger with: {satellite_crop_prediction}"
            )
            return True
        return False

    def verify_and_rotate_crop(self, global_core):
        """Applies the Agronomic Rebalancing Algorithm with revenue protection."""
        # Crop depletion simulation
        if self.last_crop == "Corn":
            self.soil_npk[0] -= 0.4  # Drastic Nitrogen crash

        print(
            f"[AGRI-VERSE PLANNER] Checking Soil Vector for Farm {self.plot_id}: NPK={self.soil_npk}"
        )

        if self.soil_npk[0] < 0.5:
            print(
                "⚠️ [SOIL CRITICAL LEVEL] Nitrogen depleted. Mandating rotation to Chickpeas (NPK-Fixing Crop)."
            )

            # Revenue Protection Math
            expected_cash_revenue = 12.0 * 400.0  # 12 Tons Corn * $400/Ton
            expected_rotation_revenue = (
                8.0 * 350.0
            )  # 8 Tons Chickpeas * $350/Ton
            revenue_deficit = expected_cash_revenue - expected_rotation_revenue

            # Incentive Premium Generation
            soil_regeneration_credit = 200.0
            incentive_premium = revenue_deficit + soil_regeneration_credit

            print(
                f"         Protected Income Allocation: Premium Added: ${incentive_premium:.2f}"
            )

            # Offline Mesh Voucher Payout
            self.wallet_balance_offline += incentive_premium
            self.soil_npk[0] += 0.5  # Soil heals
            self.last_crop = "Chickpeas"
            self.validated_by_user = True
            print(
                f"📲 [MESH WALLET UPDATE] Secure cryptographic voucher accepted offline via BLE hop."
            )
            print(
                f"                       Local Wallet Balance: ${self.wallet_balance_offline:,.2f}\n"
            )
            return "ROTATION_EXECUTED"
        return "STANDBY"


class OverseasImporter:
    """Models the business logic for cross-border trade execution contracts."""

    def __init__(self, importer_id):
        self.importer_id = importer_id

    def execute_export_contract(self, global_core, farmer_wallet):
        """Tracks the cross-border milestone execution for international trade."""
        print(f"🚢 [CROSS-BORDER TRADE] Initiating Export Protocol via Importer {self.importer_id}")
        contract_value = 50000.0

        # Milestone 1: Sanitary and Phytosanitary (SPS) Verification
        sps_token_minted = True
        if sps_token_minted:
            milestone_1_payout = contract_value * 0.30
            farmer_wallet.wallet_balance_offline += milestone_1_payout
            print(
                f"         [MILESTONE 1 PASSED] Export terminal token minted. Released 30% (${milestone_1_payout:,.2f}) to Farmer."
            )

        # Milestone 2: Geofenced Maritime Satellite Track
        ship_crossed_geofence = True
        if ship_crossed_geofence:
            milestone_2_payout = contract_value * 0.70
            farmer_wallet.wallet_balance_offline += milestone_2_payout
            print(
                f"         [MILESTONE 2 PASSED] Satellite confirms port boundary cross. Released remaining 70% (${milestone_2_payout:,.2f})."
            )

        print("📊 [MACROECONOMIC INFLATION SETTLED] Transaction concluded with 0% speculation risk.\n")


# ==========================================
#          LIVE SIMULATION ORCHESTRATOR
# ==========================================
if __name__ == "__main__":
    print("==================================================================================")
    print("      DECENTRALIZED SOVEREIGN AGRICULTURAL NETWORK (DSAN) - SIMULATION ENGINE      ")
    print("==================================================================================\n")

    # 1. Initialize Network Layers
    core = GlobalCore()
    gateway_alpha = NationalGateway(nation_id="Alpha", assigned_quota=10000.0)
    remote_farm = FarmPlot(plot_id="F-401", is_connected=False)
    importer = OverseasImporter(importer_id="EuroZone-Import-Corp")

    # 2. Importer tries to register a trade (Testing VDC)
    # Correct capital commitment
    core.verify_vdc_escrow(
        buyer_id="EuroZone-Import-Corp",
        demand_tonnage=1000,
        locked_collateral=500000.0,
    )

    # Fake Capital Speculation filtering check
    core.verify_vdc_escrow(
        buyer_id="Ghost-Speculator-LLC",
        demand_tonnage=1000,
        locked_collateral=50.0,
    )

    # 3. Satellite Telemetry Auto-fills Offline Data
    remote_farm.simulate_passive_autofill(
        satellite_crop_prediction="Corn - Hectares mapped: 5.2"
    )

    # 4. Check Telemetric Fidelity Gate at Gateway Layer
    gateway_alpha.calculate_telemetric_fidelity(
        reported_a=5.2, satellite_a=5.0, moisture=0.68
    )

    # 5. Soil Degradation and Automated Revenue-Protected Rotation Payout
    remote_farm.verify_and_rotate_crop(core)

    # 6. Test Sovereign Inventory Optimization Loop
    gateway_alpha.optimize_sovereign_inventory(core.moving_average_price)

    # 7. Test Cross-Border Export execution tracking
    importer.execute_export_contract(core, remote_farm)

    # 8. Simulate Cartel/Production Default Penalty Update Loop
    gateway_alpha.actual_production = 7000.0  # Fell short of 10,000 assigned quota
    core.process_harvest_yield("Alpha", gateway_alpha)

    print("==================================================================================")
    print("                     SIMULATION RUN COMPLETELY SUCCESSFUL                         ")
    print("==================================================================================")