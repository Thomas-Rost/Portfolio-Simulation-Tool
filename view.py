import numpy as np 
import pandas as pd 
import yfinance as yf 
import matplotlib.pyplot as plt 
from model import Asset, Portfolio



class Viewer: 

    def plot_prices(self, obj, start="2024-01-01",end="2026-04-20", normalized = False):
        
        if isinstance(obj, Asset): 
            prices = obj.obtain_prices(start, end) 
            plt.plot(prices.index, prices, label = f'Price Series {obj.ticker} ')
            plt.xlabel('Date') 
            plt.ylabel('Price') 
            plt.legend() 
            plt.tight_layout() 
            plt.show()
        
        elif isinstance(obj, Portfolio): 

            df_prices = obj.get_df(start, end)
            if normalized ==False: 
                plt.plot(df_prices)
                plt.xlabel('Date') 
                plt.ylabel('Price') 
                plt.legend(df_prices.columns)
                plt.tight_layout() 
                plt.show()
            else: 
                df_prices_normalized = df_prices / df_prices.iloc[0,:]
                plt.plot(df_prices_normalized)
                plt.xlabel('Date') 
                plt.ylabel('Price') 
                plt.legend(df_prices_normalized.columns)
                plt.tight_layout() 
                plt.show() 

    def plot_simulation_paths(self, simulated_value_paths, n_paths=100):
        plt.figure(figsize=(10, 6))

        n_paths = min(n_paths, simulated_value_paths.shape[0])

        for i in range(n_paths):
            plt.plot(simulated_value_paths[i, :], alpha=0.15)

        plt.title("Simulated Portfolio Value Paths")
        plt.xlabel("Simulation Step")
        plt.ylabel("Portfolio Value")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_simulation_fan_chart(self, simulated_value_paths):
        median_path = np.percentile(simulated_value_paths, 50, axis=0)
        p5 = np.percentile(simulated_value_paths, 5, axis=0)
        p25 = np.percentile(simulated_value_paths, 25, axis=0)
        p75 = np.percentile(simulated_value_paths, 75, axis=0)
        p95 = np.percentile(simulated_value_paths, 95, axis=0)

        x = np.arange(simulated_value_paths.shape[1])

        plt.figure(figsize=(10, 6))

        plt.fill_between(x, p5, p95, alpha=0.25, label="5%-95% range")
        plt.fill_between(x, p25, p75, alpha=0.35, label="25%-75% range")
        plt.plot(x, median_path, linewidth=2, label="Median path")

        plt.title("Portfolio Simulation Fan Chart")
        plt.xlabel("Simulation Step")
        plt.ylabel("Portfolio Value")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def plot_final_value_distribution(self, simulated_value_paths):
        final_values = simulated_value_paths[:, -1]

        plt.figure(figsize=(10, 6))
        plt.hist(final_values, bins=50)

        plt.title("Distribution of Final Portfolio Values")
        plt.xlabel("Final Portfolio Value")
        plt.ylabel("Frequency")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()