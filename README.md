# Portfolio Simulation Tool

A Python command-line portfolio tracker and simulator built with a Model-View-Controller architecture.

This project was created for the a.s.r. Vermogensbeheer Portfolio Tracker assignment. It lets users add assets, view portfolio tables, analyze sector and asset-class weights, plot historical prices, and simulate future portfolio values under uncertainty.

## Features

- Add assets with ticker, sector, asset class, quantity, and purchase price
- Download historical price data using `yfinance`
- View current portfolio value, transaction value, profit/loss, and asset weights
- Group portfolio exposure by:
  - Sector
  - Asset class
- Plot raw or normalized historical price series
- Simulate 15 years of portfolio outcomes using:
  - Multivariate normal simulation
  - Bootstrap simulation
  - Block bootstrap simulation
- Display simulation risk metrics such as:
  - Mean final value
  - Median final value
  - Annualized return
  - Annualized volatility
  - Sharpe ratio
  - Value at Risk
  - Expected Shortfall
  - Probability of loss

## Project Structure

```text
Portfolio-Simulation-Tool/
│
├── main.py              # Entry point of the application
├── controller.py        # Controller: handles user input and application flow
├── model.py             # Model: stores assets, portfolio calculations, simulations
├── view.py              # View: creates plots and visual output
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
