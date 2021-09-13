import yfinance as yf

msft = yf.Ticker("MSFT")
print(msft.info)

#get historical market data
hist = msft.history(period='max')
print(hist)