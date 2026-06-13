import os
import math

# Try importing matplotlib; provide an installation hint if missing
try:
    import matplotlib.pyplot as plt
except ImportError:
    import sys
    print("Error: matplotlib is required for visualization.")
    print("Please run: pip install matplotlib")
    sys.exit(1)

def run_visualized_simulation():
    months = list(range(1, 13))
    
    # Tracking arrays for our chart lines
    market_prices = []
    supply_quotas = []
    fidelity_scores = []
    
    # Baseline architectural metrics
    base_price = 250.0       # Standard price per metric ton
    base_quota = 1000.0      # Base global quota in metric tons
    
    print("Calculating 12-Month Macroeconomic Stress Run...")
    
    for month in months:
        # Simulate an adversarial economic shock event at Month 5 (Hyperinflation spike)
        if month == 5:
            price = base_price * 10.0  # Sudden 10x price shock
            fidelity = 0.55            # Telemetry mismatch due to sudden market panic
        elif month > 5:
            # Algorithmic recovery curve: formulas begin cooling the market back down
            decay_factor = month - 5
            price = (base_price * 10.0) / (1 + (decay_factor * 1.2))
            fidelity = min(1.0, 0.55 + (decay_factor * 0.09))
        else:
            # Steady baseline state (Months 1-4)
            price = base_price + (month * 2.5)
            fidelity = 0.98
            
        # The Elastic Supply Mesh Algorithm Core Equation:
        # High prices and lower telemetry fidelity compress the allowed export quota 
        # to prevent predatory market dumps.
        stabilization_modifier = fidelity / (price / base_price)
        adjusted_quota = base_quota * math.sqrt(stabilization_modifier)
        
        # Clip floor parameters to protect core baseline farmers from absolute zero
        final_quota = max(150.0, adjusted_quota)
        
        market_prices.append(price)
        supply_quotas.append(final_quota)
        fidelity_scores.append(fidelity * 100) # Scale to percentage for visual balance

    # Define the output directory inside the docs folder
    output_dir = os.path.join(os.getcwd(), 'docs')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'simulation_chart.png')

    # --- Matplotlib Plot Architecture Configuration ---
    fig, ax1 = plt.subplots(figsize=(10, 6))
    plt.title("DSAN Network: Adaptive Macroeconomic Equilibrium Under Stress", fontsize=14, fontweight='bold', pad=15)
    
    # Primary Axis: Price and Quota Strings
    ax1.set_xlabel("Simulation Timeline (Months)", fontsize=11, labelpad=10)
    line1 = ax1.plot(months, market_prices, color='#d9534f', linestyle='--', marker='o', linewidth=2, label='Market Price ($/Ton)')
    ax1.set_ylabel("Price Metrics ($ USD)", color='#d9534f', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='#d9534f')
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    # Secondary Axis: Shared view for Supply Quota
    ax2 = ax1.twinx()
    line2 = ax2.plot(months, supply_quotas, color='#5cb85c', linestyle='-', marker='s', linewidth=2, label='Elastic Supply Quota (Tons)')
    ax2.set_ylabel("Production Quota (Metric Tons)", color='#5cb85c', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='#5cb85c')
    
    # Tertiary Element: Overlay Fidelity Index Percentages
    line3 = ax1.plot(months, fidelity_scores, color='#0275d8', linestyle=':', marker='^', linewidth=1.5, label='Fidelity Score ($F_C$ %)')

    # Consolidate Legends across shared spatial planes
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#cccccc')

    plt.tight_layout()
    
    # Save chart asset to repository folder structure
    plt.savefig(output_path, dpi=300)
    print(f"Success! Analysis chart compiled and exported directly to: {output_path}")

if __name__ == '__main__':
    run_visualized_simulation()