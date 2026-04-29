from model import Asset, Portfolio
from view import Viewer


class PortfolioController:
    def __init__(self):
        self.portfolio = Portfolio()
        self.viewer = Viewer()

    def run(self):
        while True:
            print("\n--- Portfolio Tracker ---")
            print("1. Add asset")
            print("2. View portfolio")
            print("3. View sector table")
            print("4. View asset class table")
            print("5. Plot prices")
            print("6. Run simulation")
            print("q. Quit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_asset()

            elif choice == "2":
                table = self.portfolio.portfolio_table()
                print(table.to_string(index=False))

            elif choice == "3":
                table = self.portfolio.groupby_table("Sector")
                print(table.to_string(index=False))

            elif choice == "4":
                table = self.portfolio.groupby_table("Asset Class")
                print(table.to_string(index=False))

            elif choice =="5":
                self.plot_prices_menu()

            elif choice == "6":
                self.run_simulation()

            elif choice == "q":
                print("Goodbye.")
                break

            else:
                print("Invalid choice. Try again.")

    def add_asset(self):
        ticker = input("Ticker: ")
        sector = input("Sector: ")
        asset_class = input("Asset class: ")

        quantity = float(input("Quantity: "))
        purchase_price = float(input("Purchase price: "))

        asset = Asset(
            ticker=ticker,
            sector=sector,
            asset_class=asset_class,
            quantity=quantity,
            purchase_price=purchase_price
        )

        self.portfolio.add_asset(asset)

        print(f"\nAdded {ticker} to the portfolio.")
    
    def plot_prices_menu(self):
        print("\nPlot options: ")
        print("1. Raw prices")
        print("2. Normalized prices (base=1), recommended for more than 1 stock.")

        choice = input("Choose an option: (input 1 or 2)")
        if choice == "1": 
            self.viewer.plot_prices(self.portfolio, normalized = False)
        elif choice == "2": 
            self.viewer.plot_prices(self.portfolio, normalized = True)
        else: 
            print("Invalid Choice. Choose '1' or '2'.")

    def run_simulation(self):
        method = input("Simulation method (MVN / Bootstrap / BlockBootstrap): ")

        sim_returns, sim_values = self.portfolio.simulate(
            method=method,
            paths=10_000,
            len_simulations=252 * 15
        )

        metrics = self.portfolio.simulation_metrics(
            sim_returns,
            sim_values,
            rf=0.0,
            alpha=0.05
        )

        print("\n--- Simulation Metrics ---")
        print(metrics.to_string())

        self.viewer.plot_simulation_fan_chart(sim_values)
