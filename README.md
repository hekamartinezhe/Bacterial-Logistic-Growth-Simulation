# Bacterial Logistic Growth and Decay Simulation
Probably not very accurate logistic bacterial growth simulation using matplotlib and numpy.



## Main Purpose

This project aims to **simulate and visualize the logistic growth model** ($N(t)$) for a pathogenic bacterial population, such as *Pseudomonas aeruginosa*.

The primary objective is to **understand the full life cycle kinetics** of an infection (like SCUD). This includes the rapid growth phase and the subsequent decay phase. Understanding this entire process helps **substantiate and validate an effective treatment protocol (e.g., 22.5/1.5 dry-docking) when treating an animal with limited resources.**

By modeling the speed at which an infection reaches its carrying capacity ($K$) and how it behaves afterward, an intervention can be designed to collapse the growth rate ($\mu$) and permit recovery.



## The Models

### 1. The Logistic Growth Model: $N(t)$

This model describes the "S-curve" growth phase, where the population is limited by a carrying capacity.

$$N(t) = \frac{K}{1 + \left(\frac{K - N_0}{N_0}\right) e^{-\mu t}}$$

Where:
- **$N(t)$**: Population at time $t$.
- **$K$**: Carrying capacity (maximum sustainable population).
- **$N_0$**: Initial population.
- **$\mu$ (mu)**: Specific growth rate.
- **$t$**: Time.

### 2. The Decay (Death) Phase Model

This is the final phase in a closed system (batch culture). It occurs after the stationary phase, once nutrients are depleted and/or toxic waste products become lethal.

The model for this phase is typically **first-order decay kinetics**, which is the reverse of exponential growth. The rate of death is proportional to the current living population.

The differential model is:

$$\frac{dN}{dt} = -k_d \cdot N$$

Where **$k_d$** is the **specific death rate** (units of 1/time).

The solution $N(t)$ for the decay phase (starting after the stationary phase) is:

$$N(t) = K \cdot e^{-k_d (t - t_s)}$$

Where:
- **$N(t)$**: Population at time $t$ (during the death phase).
-
