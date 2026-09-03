# Safiri AI - Multi-Objective Shipment Route Optimizer

A decision-support system built to evaluate, score, and recommend optimal shipment routes across global supply chain networks under uncertainty.

## Overview

Selecting shipment routes in global logistics requires balancing trade-offs between cost, transit time, reliability, and risk. This project implements a weighted penalty optimization model to assist logistics operators by selecting optimal routes and providing human-interpretable trade-off explanations.

## Key Features

* **Multi-Objective Scoring Engine**: Evaluates candidate routes using a weighted penalty model balancing total cost, transit time, delay probability, and congestion indicators.
* **Feature Normalization**: Normalizes candidate route metrics per shipment to ensure fair cross-metric evaluation.
* **Pydantic Data Schemas**: Enforces robust validation and handles field alias mappings (e.g., `from` to `from_location`).
* **Operator Explainability**: Generates clear, plain-language summaries detailing why a specific route was selected over alternatives.
* **Synthetic Dataset Generator**: Simulates realistic multi-leg shipping scenarios with cost, time, and risk metrics.

## Scoring Methodology

The optimization engine calculates a composite penalty score ($S$) for each candidate route:

$$S = w_c \cdot C + w_t \cdot T + w_d \cdot D + w_g \cdot G$$

Where:
* **Cost Weight ($w_c$)**: 0.40
* **Time Weight ($w_t$)**: 0.30
* **Delay Risk Weight ($w_d$)**: 0.15
* **Congestion Weight ($w_g$)**: 0.15

Lower scores indicate preferable routes.

## Repository Structure

```text
shipment-router/
│
├── data/
│   └── shipment_dataset.json    # Synthetic shipment dataset
├── src/
│   ├── __init__.py
│   ├── cli.py                   # Command-line interface entry point
│   ├── engine.py                # Route evaluation and scoring logic
│   ├── generate_dataset.py     # Dataset generation utility
│   └── models.py                # Pydantic data schemas
└── tests/
    └── test_engine.py           # Pytest test suite

## Setup & Installation
Prerequisites
Python 3.10+

Virtual Environment Setup
PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
Install Dependencies
PowerShell
python -m pip install pydantic pytest
Usage
1. Generate Synthetic Dataset
To generate a fresh dataset of 26 shipments with multi-leg candidate routes:

PowerShell
$env:PYTHONPATH="."; python -m src.generate_dataset
2. Run Route Recommendation CLI
To execute the route optimization pipeline and view operator recommendations:

PowerShell
$env:PYTHONPATH="."; python -m src.cli --input data/shipment_dataset.json
3. Run Unit Tests
To verify schema parsing, metric aggregation, and scoring logic:

PowerShell
$env:PYTHONPATH="."; python -m pytest
