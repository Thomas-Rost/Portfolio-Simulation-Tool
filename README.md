# Portfolio Simulation Tool

A Python command-line portfolio tracker and simulator built with a Model-View-Controller architecture.

## How to run the project: 
1. make a virtual environment:  python -m venv venv
2. Activate the environment
For macOS/Linux: source venv/bin/activate
For Windows: venv\Scripts\activate
3. Install dependencies pip install -r requirements.txt
4. start the program on the terminal:  python main.py



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
