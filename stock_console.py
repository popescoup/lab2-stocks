# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortDailyData
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Add Stock ---")
        symbol = input("Enter Ticker Symbol: ")
        name = input("Enter Company Name: ")
        shares = float(input("Enter Number of Shares: "))
        new_stock = Stock(symbol, name, shares)
        stock_list.append(new_stock)
        option = input("Stock Added - Enter to Add Another Stock or 0 to Stop: ")
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol + "  ", end="")
    print("]")
    symbol = input("Which stock do you want to buy?: ")
    shares = float(input("How many shares do you want to buy?: "))
    for stock in stock_list:
        if stock.symbol == symbol:
            stock.buy(shares)
    input("Press Enter to Continue")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol + "  ", end="")
    print("]")
    symbol = input("Which stock do you want to sell?: ")
    shares = float(input("How many shares do you want to sell?: "))
    for stock in stock_list:
        if stock.symbol == symbol:
            stock.sell(shares)
    input("Press Enter to Continue")

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol + "  ", end="")
    print("]")
    symbol = input("Which stock do you want to delete?: ")
    for stock in stock_list:
        if stock.symbol == symbol:
            stock_list.remove(stock)
            break
    input("Press Enter to Continue")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("Stock List ----")
    print(f"{'SYMBOL':<12}{'NAME':<20}{'SHARES'}")
    print("=" * 38)
    for stock in stock_list:
        print(f"{stock.symbol:<12}{stock.name:<20}{stock.shares}")
    input("\nPress Enter to Continue")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ----")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol + "  ", end="")
    print("]")
    symbol = input("Which stock do you want to use?: ")
    for stock in stock_list:
        if stock.symbol == symbol:
            print("Ready to add data for: ", symbol)
            print("Enter Data Separated by Commas - Do Not use Spaces")
            print("Enter a Blank Line to Quit")
            print("Enter Date,Price,Volume")
            print("Example: 8/28/20,47.85,10550")
            entry = input("Enter Date,Price,Volume: ")
            while entry != "":
                data = entry.split(",")
                daily_data = DailyData(datetime.strptime(data[0], "%m/%d/%y"), float(data[1]), float(data[2]))
                stock.add_data(daily_data)
                entry = input("Enter Date,Price,Volume: ")

# Display Report for All Stocks
def display_report(stock_list):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_list:
        print(f"\nReport for: {stock.symbol} {stock.name}")
        print(f"Shares: {stock.shares}")
        if len(stock.DataList) == 0:
            print("No daily history.")
        else:
            for daily_data in stock.DataList:
                print(f"{daily_data.date.strftime('%m/%d/%y')}   ${daily_data.close:,.2f}   {daily_data.volume}")
    print("\n--- Report Complete ---")
    input("Press Enter to Continue")


# Display Chart
def display_chart(stock_list):
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol + "  ", end="")
    print("]")
    symbol = input("Which stock do you want to use?: ")
    display_stock_chart(stock_list, symbol)

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("--- Data Saved to Database ---")
            input("Press Enter to Continue")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("--- Data Loaded from Database ---")
            input("Press Enter to Continue")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieving Stock Data from Yahoo! Finance ---")
    print("This will retrieve data from all stocks in your stock list.")
    dateFrom = input("Enter starting date: (MM/DD/YY): ")
    dateTo = input("Enter ending date: (MM/DD/YY): ")
    recordCount = stock_data.retrieve_stock_web(dateFrom, dateTo, stock_list)
    sortDailyData(stock_list)
    print("Records Retrieved: ", recordCount)
    input("Press Enter to Continue")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV file from Yahoo! Finance---")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol + "  ", end="")
    print("]")
    symbol = input("Which stock do you want to use?: ")
    filename = input("Enter filename: ")
    stock_data.import_stock_web_csv(stock_list, symbol, filename)
    sortDailyData(stock_list)
    print("CSV File Imported")
    input("Press Enter to Continue")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()