# Binance-Altcoin-Asset-Cost-Calculator
Altcoin asset cost calculator for Binance/FTX, auto read the trading history and convert it to excel report.

## Website (GUI helper)

https://corn-fat.medium.com/%E6%8A%95%E8%B3%87%E5%B9%A3%E5%9C%88%E5%BF%85%E5%82%99-%E5%85%8D%E8%B2%BB%E8%87%AA%E8%A3%BD%E8%B3%87%E7%94%A2%E7%B5%B1%E8%A8%88%E5%B7%A5%E5%85%B7-4c5a1c114552
## Usage
### 1. install environment
```
conda create -n alt -f freeze.yml
source activate alt
```
### 2. Get your API key from Binance
https://binance.zendesk.com/hc/zh-cn/articles/360002502072-%E5%A6%82%E4%BD%95%E5%88%9B%E5%BB%BAAPI
### 3. Replace your exe/key_example with your KEY and PRIVATE_KEY
Remember to protect your PRIVATE_KEY.
### 4. change the query_list in main.py 
```
query_list = ['BTS', 'BTC', 'ETH', 'ALGO', 'SRM', 'XRP', 'IOTA', \
              'NULS', 'SXP', 'SOL', 'XTZ', 'SUSHI', 'TRX', 'DOT','LINK','BNB', \
              'BCH', 'EOS', 'XLM', 'ATOM']
```
### 5. python main.py

### EXAMPLE OUTPUT
![image](https://github.com/jasonyl13579/Binance-Altcoin-Asset-Cost-Calculator/blob/master/result/example2.PNG)
![image](https://github.com/jasonyl13579/Binance-Altcoin-Asset-Cost-Calculator/blob/master/result/everyday.png)
THAT'S ALL!!
