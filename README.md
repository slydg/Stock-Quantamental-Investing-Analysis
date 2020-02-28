# Stock Quantamental Investing Analysis Report

## Contributors
- slydg: AntiRomance@outlook.com
- peihan-tian-simon: peihantian@brandeis.edu

## How to use
- ts_date: The folder of time series data for backtest 
- basic_data: The folder of stocks` basic financial information
- All files ended with '_data' are used to download data from tushare
- basic_features: Using Lasso to select featurs
- basic_model: A randomforest clasifier to decide which stock will possibly perform well in the next 3 months
- back_test: Used to build strategies and calculate the return rate   

## Results presentation and data sources
- Back testing results: During the 90-day backtest period, the actual yield of 14% was much higher than the market's performance over the same period.

![avatar](back_test_result.png)
- Data sources: Tushare
- Data type: The financial statements of companies listed on the Shanghai Stock Exchange for the first to third quarters of 2019 include three major tables (balance sheet, cash flow statement, income statement) and basic financial ratios.
- Data pre-processing: Financial data with missing values exceeding 30% of the total number of all companies will be deleted, and the remaining missing values will be filled according to the average value of the industry of the company.

## Preliminary analysis: selection and interpretation of financial characteristics
### Preparation for analysis
Considering that there are differences in the specific influence of indicators in different industries, the original data should not be used for feature selection. We calculated the relative rankings (in percentage) of the indicators  within the industry. These values are used instead of the original values. After determining the financial indicators, we consider the average monthly return of each stock within three months after its financial statements are issued as a market response. Similarly, considering that the average returns of different industries are different, we use the relative rankings of the monthly average returns instead. 
### Feature selection with Lasso
After the above analysis is completed, we use the LASSO method for feature selection, and determine the appropriate hyperparameters by cross-validation. We use the stock market response within three months after the company releases its financial statements, that is, the relative ranking of monthly average returns, as the dependent variable to determine whether each indicator has an impact.

![avatar](seasonal_factors.png)
### Variable interpretation
As can be seen from the figure, financial indicators including ROE, net profit and other indicators of corporate profitability, corporate liquidity indicators including asset turnover and inventory turnover, and several indicators of corporate cash flow have relatively obvious influences. At the same time, the companies with rapid equity growth in the past may have a relatively negetive market performance. We think that the current mean regression phenomenon may be a relatively reasonable explanation.

## Stock screening model using random forest
### Data preprocessing
According to the above LASSO screening results, the selected financial indicators were introduced into the model as independent variables. Considering the different market performance in different industries, we may need to put the infuence of the industry in to the model. However, due to the large number of industries (110 different industries), One-Hot coding of industries will cause a too sparse variable matrix. We choose to use the random forest stock selection model within the industry. Therefore, consistent with LASSO, each of the above indicators has been processed in the relative ranking in the industry. The purpose of random forest stock selection is to select stocks with relatively good market performance within the industry. Therefore, we divide each stock into two categories based on the relative ranking in the industry in terms of average earnings in the three months after the quarterly financial statement is released. The first 50% are recorded as category 1, and the remaining stocks are recoeded as category 0.
### Model fitting and testing
After the above processing, the data is transferred into the random forest model. The experiments show that the so-called "random forest does not cause overfitting" is untenable. To avoid overfitting, we set the maximum depth and maximum leaf nodes of each subtree. Considering that a total of 54 variables enter the model, we set the maximum number of child nodes to 54 and correspondingly the maximum depth is set to 5 layers. After cross-validation, we obtained a model with a training set accuracy of 0.7 and a test set accuracy of 0.6.

## Stock selection model backtesting
After completing the above work, we have obtained a relatively reliable preliminary stock selection model. Next, we will use this model to further build a stock selection strategy and conduct backtests to verify the reliability of the strategy. We will build a rough stock selection strategy model for backtesting, and then adopt the portfolio adjustment based on it, calculate the backtested return of the stock selection strategy with portfolio adjustment and compare it with the market rate of return.
### Preliminary stock selection strategy
The problem that needs to be paid attention to when conducting backtesting is that “time backwards” and “predicting the future” should not occur, that is, the judgment of the date is very important. We chose October 31, 2019 as the starting point for backtesting. At this point, most companies have published the third quarter financial statements, and those that have not been announced are not considered in the candidate stock. Taking into account the so-called momentum effect of the stock market, it is highly likely that industries that have performed will continue to perform well in the future. Therefore, before determining the investment portfolio, we calculated the average return of each industry in the three months before October 31, 2019, and selected the top 20 industries as candidate industries. Next, the trained random forest model is introduced to determine whether the stocks in the candidate industries will perform well in the future. After the above processing, all the stocks whose output is "1" are regarded as all the selected stocks. Ranking the selected stocks based on the returns of the past 3 months. The top one-third of these stocks are used as investment portfolios. We give each of these 100,000 yuan as the assets invested at the beginning of the backtest period. During the next three months of the backtest period, no adjustments are made to the portfolio. Based on backtesting calculations, the final yield was 12.1%.
### Adjusting the portfolio using market information
Considering the limited accuracy of the random forest used in stock selection and the possibility of misselection, we believe that market data should be used rationally to make dynamic adjustments to the current portfolio. The adjustment is still based on the momentum effect on the stock market, and stocks that have performed well in the past are likely to perform well in the future.
Therefore, every day we rank the stocks of the stocks selected (not the portfolio) before based on the returns from the begining of the backtest period to this days and select the top n stocks (the 'n' equals to the current number of stocks in the portfolio) as the new portfolio. Then, the current assets are evenly distributed to the new portfolio. In order to be more realistic, we assume that each adjustment will require payment of five-tenths of the amount of the adjustment as a handling fee. If the adjustment is too frequent, this fee will result in a large loss, so the accuracy of the preliminary model will also greatly affect the final return.
After developing the above investment strategy, we have written the code to constantly adjust the portfolio during the backtesting. This strategy has been confirmed to be effective in increasing investment returns, resulting in a 15% benefit. After the backtesting, we compare the earnings of the above strategies with those of the Shanghai Composite Index, and plot the returns in the same line chart, as shown in the following figure. The comparison shows that the stock selection strategy has a good performance.

![avatar](back_test_result.png)

