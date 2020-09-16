# Binance-Altcoin-Asset-Cost-Calculator
Altcoin asset cost calculator for Binance, auto read the trading history and convert it to excel report.

## Usage
### 1. install environment
```
conda create -n alt -f freeze.yml
source activate alt
```
### 2. Get your API key from Binance
https://binance.zendesk.com/hc/zh-cn/articles/360002502072-%E5%A6%82%E4%BD%95%E5%88%9B%E5%BB%BAAPI
### 3. Replace your source/key_example with your KEY and PRIVATE_KEY
Remember to protect your PRIVATE_KEY.
### 4. change the query_list in main.py 
```
query_list = ['BTS', 'BTC', 'ETH', 'ALGO', 'SRM', 'XRP', 'IOTA', \
              'NULS', 'SXP', 'SOL', 'XTZ', 'SUSHI', 'TRX', 'DOT','LINK','BNB', \
              'BCH', 'EOS', 'XLM', 'ATOM']
```
### 5. python main.py

### EXAMPLE OUTPUT
![image](https://github.com/jasonyl13579/Binance-Altcoin-Asset-Cost-Calculator/blob/master/source/example.PNG)
THAT'S ALL!!
