# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        if path.exists("stocks.db") == False:
            stock_data.create_database()

        # Create Window
        self.root = Tk()
        self.root.title("Stock Manager")
        self.root.configure(bg="#f0f0f0")

        # Add Menubar
        self.menubar = Menu(self.root)

        # Add File Menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_command(label="Load", command=self.load)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Add Web Menu
        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(label="Scrape Data from Yahoo! Finance...", command=self.scrape_web_data)
        self.webmenu.add_command(label="Import CSV from Yahoo! Finance...", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web", menu=self.webmenu)

        # Add Chart Menu
        self.chartmenu = Menu(self.menubar, tearoff=0)
        self.chartmenu.add_command(label="Display Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=self.chartmenu)

        # Add menus to window
        self.root.config(menu=self.menubar)

        # Add heading information
        self.headingLabel = Label(self.root, text="No Stock Selected", bg="#f0f0f0", font=("Helvetica", 14))
        self.headingLabel.pack(pady=5)

        # Add stock list
        self.stockList = Listbox(self.root, width=20, exportselection=False)
        self.stockList.pack(side=LEFT, fill=Y, padx=5, pady=5)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)

        # Add Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        # Set Up Main Tab
        self.mainTab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.mainTab, text="Main")

        Label(self.mainTab, text="Add Stock", bg="#f0f0f0", font=("Helvetica", 11)).grid(row=0, column=0, columnspan=2, pady=5)
        Label(self.mainTab, text="Symbol:", bg="#f0f0f0").grid(row=1, column=0, sticky=W, padx=5)
        self.addSymbolEntry = Entry(self.mainTab)
        self.addSymbolEntry.grid(row=1, column=1, padx=5)
        Label(self.mainTab, text="Name:", bg="#f0f0f0").grid(row=2, column=0, sticky=W, padx=5)
        self.addNameEntry = Entry(self.mainTab)
        self.addNameEntry.grid(row=2, column=1, padx=5)
        Label(self.mainTab, text="Shares:", bg="#f0f0f0").grid(row=3, column=0, sticky=W, padx=5)
        self.addSharesEntry = Entry(self.mainTab)
        self.addSharesEntry.grid(row=3, column=1, padx=5)
        Button(self.mainTab, text="Add Stock", command=self.add_stock).grid(row=4, column=0, columnspan=2, pady=5)
        Button(self.mainTab, text="Delete Stock", command=self.delete_stock).grid(row=5, column=0, columnspan=2, pady=5)

        Label(self.mainTab, text="Update Shares", bg="#f0f0f0", font=("Helvetica", 11)).grid(row=6, column=0, columnspan=2, pady=5)
        Label(self.mainTab, text="Shares:", bg="#f0f0f0").grid(row=7, column=0, sticky=W, padx=5)
        self.updateSharesEntry = Entry(self.mainTab)
        self.updateSharesEntry.grid(row=7, column=1, padx=5)
        Button(self.mainTab, text="Buy", command=self.buy_shares).grid(row=8, column=0, pady=5)
        Button(self.mainTab, text="Sell", command=self.sell_shares).grid(row=8, column=1, pady=5)

        # Setup History Tab
        self.historyTab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.historyTab, text="History")
        self.dailyDataList = Text(self.historyTab, width=50, height=20)
        self.dailyDataList.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Setup Report Tab
        self.reportTab = Frame(self.notebook, bg="#f0f0f0")
        self.notebook.add(self.reportTab, text="Report")
        self.stockReport = Text(self.reportTab, width=50, height=20)
        self.stockReport.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Call MainLoop
        self.root.mainloop()

    # This section provides the functionality
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        if not self.stockList.curselection():
            return
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END,row)
                self.stockReport.insert(END, f"Report for: {stock.symbol} {stock.name}\n")
                self.stockReport.insert(END, f"Shares: {stock.shares}\n")
                if len(stock.DataList) == 0:
                    self.stockReport.insert(END, "*** No daily history.\n")
                else:
                    for daily_data in stock.DataList:
                        row = daily_data.date.strftime("%m/%d/%y") + "   " + '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                        self.stockReport.insert(END, row)
                self.stockReport.insert(END, "\n--- Report Complete ---\n")


                    

    
    # Add new stock to track.
    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(),self.addNameEntry.get(),float(str(self.addSharesEntry.get())))
        self.stock_list.append(new_stock)
        self.stockList.insert(END,self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)

    # Buy shares of stock.
    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # Sell shares of stock.
    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.remove(stock)
                break
        self.stockList.delete(self.stockList.curselection())
        self.headingLabel['text'] = "No Stock Selected"

    # Get data from web scraping.
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy")
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except:
            messagebox.showerror("Cannot Get Data from Web","Check Path for Chrome Driver")
            return
        sortDailyData(self.stock_list)
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
            sortDailyData(self.stock_list)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + "Import Complete")
    
    # Display stock price chart.
    def display_chart(self):
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list,symbol)


def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()