import numpy as np
import pandas as pd
import yfinance as yf


class Asset:
    def __init__(self, ticker, sector, asset_class, quantity, purchase_price):
        self.ticker = ticker
        self.sector = sector
        self.asset_class = asset_class
        self.quantity = quantity
        self.purchase_price = purchase_price

    def transaction_value(self):
        return self.quantity * self.purchase_price

    def obtain_prices(self, start, end):
        prices = yf.download(self.ticker, start=start, end=end, auto_adjust=True)["Close"].dropna()
        return prices

    def current_price(self):
        prices = self.obtain_prices(start="2024-01-01", end="2026-04-20")
        return prices.iloc[-1]

    def current_value(self):
        return self.quantity * self.current_price()


class Portfolio:
    def __init__(self):
        # Initialize as empty list, so you are free to construct any portfolio you like
        self.assets = []

    def add_asset(self, asset):
        self.assets.append(asset)

    def get_df(self, start="2024-01-01", end="2026-04-20"):
        tickers = [asset.ticker for asset in self.assets]
        prices = yf.download(tickers,start=start,end=end,auto_adjust=True)["Close"]
        return prices.dropna()

    def total_transaction_value(self):
        return sum(asset.transaction_value() for asset in self.assets)
    

    def total_current_value(self):
        return sum(asset.current_value() for asset in self.assets)

    def portfolio_table(self):
        rows = []

        for asset in self.assets:
            current_price = float(asset.current_price())
            current_value = asset.quantity * current_price
            transaction_value = asset.transaction_value()

            rows.append({
                "Ticker": asset.ticker,
                "Sector": asset.sector,
                "Asset Class": asset.asset_class,
                "Quantity": asset.quantity,
                "Purchase Price": asset.purchase_price,
                "Current Price": current_price,
                "Transaction Value": transaction_value,
                "Current Value": current_value,
                "P/L": current_value - transaction_value})

        df = pd.DataFrame(rows)
        df["Weight"] = df["Current Value"] / df["Current Value"].sum()

        return df

    def groupby_table(self, group_col):
        '''
        group_col = 'Sector' or 'Asset Class' 
        '''
        df = self.portfolio_table()

        grouped = (df.groupby(group_col).agg(
                {
                    "Transaction Value": "sum",
                    "Current Value": "sum",
                    "P/L": "sum"
                }).reset_index())
            
        grouped["Weight"] = grouped["Current Value"] / grouped["Current Value"].sum()

        return grouped

   
    
    def simulate(self, start='2024-01-01', end = '2026-04-20',method="MVN",paths = 100_000, len_simulations = 252*15, seed_value = 10, block_size=20): 

        # Obtain price series of all assets in the portfolio and compute returns
        prices = self.get_df(start = start, end = end) 
        returns = prices.pct_change().dropna() 

        # Obtain weight per asset in the portfolio 
        table = self.portfolio_table() 
        portfolio_value = table['Current Value'].sum() 
        weight = table['Weight']
        returns_array = returns.values
        n_obs, n_assets = returns_array.shape

        
        np.random.seed(seed_value)
        # Simulate paths x len_simulations x assets from the multivariate_normal distribution
        if method== "MVN":
            # Obtain mean and covariance matrices
            mu = returns.mean().values # len(assets)
            cov = returns.cov().values # len(assets) x len(assets)  

            simulated_assets_returns = np.random.multivariate_normal(
            mu, 
            cov, 
            size = (paths, len_simulations)
            )
        # Alternatively, use bootstrapping for a better preservation of the empirical distribution
        elif method == "Bootstrap":
            # sample individual days
            idx = np.random.randint(0, n_obs, size=(paths, len_simulations))
            simulated_assets_returns = returns_array[idx]

        # Another alternative is the block bootstrap, preserving autocorrelation, a commonly known trait of financial assets.
        elif method == "BlockBootstrap":
            simulated_assets_returns = np.zeros((paths, len_simulations, n_assets))

            n_blocks = int(np.ceil(len_simulations / block_size))

            for i in range(paths):
                path = []

                for _ in range(n_blocks):
                    start_idx = np.random.randint(0, n_obs - block_size + 1)
                    block = returns_array[start_idx:start_idx + block_size]
                    path.append(block)

                path = np.vstack(path)[:len_simulations]
                simulated_assets_returns[i] = path

        else:
            raise ValueError("method must be 'MVN', 'Bootstrap', or 'BlockBootstrap'")

        # Multiply the asset returns by the portfolio weights to obtain one vector in each len_simulations
        simulated_portfolio_returns = simulated_assets_returns @ weight.values # dimensions paths x len_simulations

        cumulative_returns = np.cumprod(1 + simulated_portfolio_returns, axis=1)
        # Prepend a column of ones (representing starting point = 1)
        cumulative_returns = np.column_stack([np.ones(paths), cumulative_returns])
        # Scale by portfolio value to get simulated value paths
        simulated_value_paths = portfolio_value * cumulative_returns

        return simulated_portfolio_returns, simulated_value_paths
    
    
    def simulation_metrics(self, simulated_portfolio_returns,simulated_value_paths, rf=0.0, alpha=0.05):
        '''Analyzes the key statistics of the simulated return paths'''
        years = simulated_portfolio_returns.shape[1] / 252
        table = self.portfolio_table() 
        portfolio_value = table['Current Value'].sum()
        initial_value = simulated_value_paths[:, 0]
        final_value = simulated_value_paths[:, -1]
        cumulative_return = (final_value - initial_value)/ initial_value
        annualized_return = (final_value/initial_value)**(1 / years) - 1
        annualized_vol = simulated_portfolio_returns.std(ddof=1, axis=1) * np.sqrt(252)
        sharpe_ratio = (annualized_return - rf) / annualized_vol
        # Compute the Value at Risk, and Expected Shortfall at quantile alpha (set at 5%)
        var_threshold = np.percentile(simulated_portfolio_returns, 100 * alpha)
        VaR_return = var_threshold
        ES_return = simulated_portfolio_returns[simulated_portfolio_returns <= var_threshold].mean()

        report = {
        "Mean Final Value": final_value.mean(),
        "Median Final Value": np.median(final_value),
        "Mean Cumulative Return": cumulative_return.mean(),
        "Median Cumulative Return": np.median(cumulative_return),
        "Mean Annual Return": annualized_return.mean(),
        "Mean Annual Volatility": annualized_vol.mean(),
        "Mean Sharpe Ratio": np.nanmean(sharpe_ratio),
        f"{int(alpha*100)}% VaR Return": VaR_return,
        f"{int(alpha*100)}% Expected Shortfall Return": ES_return,
        "Probability of Loss": np.mean(final_value < initial_value),
        "Worst Final Value": final_value.min(),
        "Best Final Value": final_value.max()
        }

        return pd.DataFrame(report, index=["Value"]).T
    
