# Formula 1 Race Strategy Simulator

## Project Overview

This project uses real Formula 1 race data obtained through the FastF1 API to analyse tyre degradation and simulate race strategies. The objective is to identify the fastest strategy by balancing tyre performance, fuel load effects, and pit stop time losses.

The project combines data collection, data cleaning, modelling, optimisation, and visualisation into a complete end-to-end workflow. Rather than relying on theoretical assumptions alone, the simulator incorporates real race information to explore how strategic decisions can influence race outcomes.

## Step 1: Data Collection

The first stage uses the FastF1 package to access official Formula 1 timing data from a selected Grand Prix.

For each lap, the dataset contains:

• Driver  
• Lap Number  
• Lap Time  
• Tyre Compound  
• Tyre Life (Tyre Age)  
• Pit Stop Information

Example:

laps = load_race_laps(2023, "Bahrain", "R")

This creates a dataframe containing race information that can be analysed and used in the simulator.

## Step 2: Data Cleaning

Raw Formula 1 data contains many laps that do not accurately represent tyre performance. Pit-stop laps, safety car periods, and irregular laps can distort analysis.

To improve data quality:

• Pit-in laps are removed  
• Pit-out laps are removed  
• Inaccurate laps are excluded  
• Missing values are filtered out  
• Lap times are converted into seconds

The result is a cleaner dataset that better reflects genuine race pace and tyre behaviour.

## Step 3: Tyre Degradation Modelling

As tyres age, their performance gradually deteriorates, resulting in slower lap times.

A degradation model is fitted for each tyre compound:

• Soft  
• Medium  
• Hard

The model estimates a relationship of the form:

Lap Time = Base Pace + (Tyre Age × Degradation Rate)

where:

• Base Pace represents the expected pace on fresh tyres  
• Degradation Rate represents the performance loss per lap

This allows tyre performance to be quantified and compared across compounds.

Because Formula 1 race data is highly variable due to fuel loads, traffic, and driver pace differences, tyre models provide an approximation of overall tyre behaviour rather than an exact representation of reality.

## Step 4: Race Simulation

The race is divided into stints. A stint is a continuous period on a single tyre compound between pit stops.

Each stint is defined by:

• Tyre Compound  
• Stint Length

Every lap of the race is simulated individually.

For each lap, the simulator calculates:

Lap Time = Base Pace + (Tyre Age × Degradation Rate) + Fuel Effect

This captures two key aspects of race performance:

1. Tyres become slower as they wear.
2. Cars become faster as fuel is burned throughout the race.

The simulator therefore reflects the trade-off between tyre degradation and fuel reduction.

## Step 5: Pit Stops

Pit stops improve tyre performance by providing fresh tyres, but they come at the cost of lost time.

For this project, a pit-stop time loss of approximately 22 seconds is assumed.

Every time a strategy requires a tyre change, the pit-stop penalty is added to the total race time.

This creates the central strategic challenge:

• Stop early and benefit from fresher tyres.
• Stay out longer and avoid losing time in the pit lane.

The optimal strategy depends on the balance between these competing effects.

## Step 6: Strategy Optimisation

The simulator evaluates multiple strategy options automatically.

For a one-stop strategy, a range of possible pit-stop laps is tested.

For each candidate pit-stop lap:

1. A complete race is simulated.
2. The total race time is calculated.
3. The result is recorded.
4. The fastest strategy is identified.

The simulator can also compare entirely different approaches, such as:

• One-stop strategies
• Two-stop strategies

Example result:

Best one-stop: Pit lap 24
Race time: 5278.03 s

Best two-stop: Pit laps 18 and 38
Race time: 5277.29 s

Two-stop strategy wins

This allows different race plans to be compared objectively.

## Step 7: Visualisation

To better understand optimisation results, a graph is generated showing:

• Pit Stop Lap (x-axis)
• Total Race Time (y-axis)

The plot shows how race time changes as the pit-stop window changes.

The lowest point on the curve represents the optimal pit window.

Visualisation provides an intuitive way to verify the simulator's behaviour and understand how strategy decisions influence overall performance.

## Results

Using real Bahrain Grand Prix race data:

• FastF1 data was successfully loaded and processed.
• Tyre degradation estimates were generated from historical race laps.
• One-stop and two-stop race strategies were simulated.
• Optimal pit-stop windows were identified.
• Results were visualised using Matplotlib.

The project demonstrates how Formula 1 strategy can be explored through simulation and data analysis.

## Challenges Encountered

Several challenges were faced during development:

• Cleaning race data to remove non-representative laps.
• Handling limited data for certain tyre compounds.
• Separating tyre degradation from fuel-load effects.
• Ensuring the simulation produced realistic strategy outcomes.
• Debugging Python errors related to data processing and plotting.

Addressing these problems provided valuable experience in working with real-world datasets and imperfect information.

## Future Improvements

Several additions could make the simulator more realistic:

• Safety Car modelling
• Virtual Safety Car periods
• Weather changes
• Driver-specific pace models
• Overtaking and traffic effects
• DRS impacts
• Tyre warm-up effects
• Monte Carlo race simulations
• Machine-learning-based strategy prediction
• Multi-race calibration using an entire season of data

These enhancements would increase the realism and predictive capability of the simulator.

## Technical Skills Demonstrated

This project demonstrates practical experience in:

• Python Programming
• Data Cleaning and Preprocessing
• Data Visualisation
• Linear Regression
• Optimisation Techniques
• Simulation Modelling
• Motorsport Analytics
• Working with APIs
• Handling Real-World Datasets
• Problem Solving and Debugging

## Personal Reflection

This project allowed me to combine my interest in engineering, quantitative modelling, and Formula 1. Beginning with raw race timing data, I developed a complete workflow that transforms real-world information into an analytical decision-making tool.

Through building the simulator, I gained experience in data collection, cleaning, modelling, optimisation, and visualisation while developing a deeper understanding of how Formula 1 teams manage tyre degradation, fuel effects, and pit-stop timing when making race strategy decisions.

More broadly, the project demonstrated how relatively simple mathematical models and programming techniques can be used to investigate complex real-world systems and support data-driven decision-making.
