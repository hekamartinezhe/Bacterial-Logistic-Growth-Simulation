import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# --- 1. Definition of the Mathematical Models ---


def logistic_model(t, K, N0, mu):
    """
    Calculates the population N(t) using the logistic growth model.
    t: current time.
    K: maximum carrying capacity.
    N0: initial population.
    mu: growth rate for Pseudomonas aeruginosa
    """
    A = (K - N0) / N0
    population = K / (1 + A * np.exp(-mu * t))
    return population


def decay_model(t_in_bath, N_start_of_bath, D_value):
    """
    Calculates the population N(t) using the D-value decay model.
    t_in_bath: time elapsed INSIDE the current bath.
    N_start_of_bath: population at the START of that bath.
    D_value: time to kill 90% of the population.
    """
    # N(t) = N_start * 10^(-t / D)
    population = N_start_of_bath * (10**(-t_in_bath / D_value))
    return population

# --- 2. Unified Simulation Method ---


def simulate_full_protocol(
    # Growth parameters
    N0, K, g,
    # Problem parameters
    t_growth_period,
    # Treatment parameters
    t_total_treatment, t_wet, t_dry, D_value,
    # Simulation parameters
    steps_per_hour=10
):
    """
    Unifies the simulation: first logistic growth, then the 
    treatment protocol (wet/dry).
    """

    # --- A. Initial Setup ---
    t_sim_total = t_growth_period + t_total_treatment
    t_cycle = t_wet + t_dry
    mu = np.log(2) / g

    # Create time and population vectors
    t_vector = np.linspace(0, t_sim_total, t_sim_total * steps_per_hour)
    N_vector = np.zeros_like(t_vector)

    N_vector[0] = N0
    N_start_of_bath = 0.0  # Variable to track the population at the start of a bath

    # --- B. Simulation Loop (step-by-step) ---
    for i in range(1, len(t_vector)):
        t_current = t_vector[i]
        t_prev = t_vector[i-1]

        # --- PHASE 1: LOGISTIC GROWTH (The Problem) ---
        if t_current <= t_growth_period:
            N_vector[i] = logistic_model(t_current, K, N0, mu)

        # --- PHASE 2: TREATMENT PROTOCOL (The Solution) ---
        else:
            # Calculate times relative to the treatment
            t_in_treatment = t_current - t_growth_period
            t_pos_in_cycle = t_in_treatment % t_cycle

            t_in_treatment_prev = t_prev - t_growth_period
            t_pos_in_cycle_prev = t_in_treatment_prev % t_cycle

            # --- WET Sub-phase (Medicated Bath/Decay) ---
            if t_pos_in_cycle <= t_wet:
                # Detect if we just entered the WET phase
                # (The cycle time is less than the previous, or it's the first step)
                if (t_pos_in_cycle < t_pos_in_cycle_prev) or (t_in_treatment_prev < 0):
                    # Save population at the start of the bath
                    N_start_of_bath = N_vector[i-1]

                t_in_bath = t_pos_in_cycle
                N_vector[i] = decay_model(
                    t_in_bath, N_start_of_bath, D_value)

            # --- DRY Sub-phase (Dry-dock/Static) ---
            else:
                # Population remains constant (we assume mu_dry = 0)
                N_vector[i] = N_vector[i-1]

    return t_vector, N_vector

# --- 3. Running the Simulation ---


# --- INPUT Parameters ---
# Growth
N0_param = 100               # Initial Population
K_param = 2_000_000_000      # Carrying Capacity (2 billion)
g_param = 0.5                # Generation Time (30 min)

# Problem
t_growth_param = 18          # Hours we let the infection grow (up to K)

# Treatment (Protocol 22.5 / 1.5)
t_wet_param = 1.5            # 1.5 hours in medicated bath
t_dry_param = 22.5           # 22.5 hours in dry-dock
D_value_param = 0.5          # D-value of 30 min for Povidone-Iodine
t_treatment_days = 4         # Days of treatment
t_total_treatment_param = t_treatment_days * 24  # Total hours of treatment

# Run the method
t, N = simulate_full_protocol(
    N0=N0_param, K=K_param, g=g_param,
    t_growth_period=t_growth_param,
    t_total_treatment=t_total_treatment_param,
    t_wet=t_wet_param, t_dry=t_dry_param,
    D_value=D_value_param,
    steps_per_hour=10  # This was 'pasos_por_hora'
)

# --- 4. Visualization (Matplotlib) ---

plt.figure(figsize=(15, 8))
plt.plot(t, N, color='red', linewidth=2, label='Bacterial Population N(t)')

# Logarithmic scale
plt.yscale('log')

# --- Plot Formatting ---
plt.title(
    f'Full Simulation: Logistic Growth vs. {t_dry_param}/{t_wet_param} Protocol', fontsize=16)
plt.xlabel('Time (hours)', fontsize=12)
plt.ylabel('Bacterial Population (Logarithmic Scale)', fontsize=14)
plt.grid(True, which='both', linestyle='--', alpha=0.6)

# Add "Treatment Start" line
plt.axvline(x=t_growth_param, color='green', linestyle='--', linewidth=2,
            label=f'Treatment Start (t={t_growth_param}h)')

# Mark the treatment cycles
t_cycle = t_wet_param + t_dry_param
for i in range(t_treatment_days):
    t_bath = t_growth_param + (i * t_cycle)
    plt.axvline(x=t_bath, color='blue', linestyle=':', alpha=0.5,
                label=f'Bath Day {i+1}' if i < 2 else None)

# Format Y-axis to not use 10^x notation
formatter = FuncFormatter(lambda y, _: '{:,.0f}'.format(y))
plt.gca().yaxis.set_major_formatter(formatter)

plt.legend()
plt.tight_layout()
plt.show()
