#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, Markup
# added code to avoid Tkinter errors
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import io, base64, os
import pandas as pd

#import logging

from datetime import datetime 
import yfinance as yf

# Default financial constants
DEFAULT_BUDGET = 10000
TRADING_DAYS_LOOP_BACK = 90
INDEX_SYMBOL = ['^DJI']
STOCK_SYMBOLS = ['BA','GS','UNH','MMM','HD','AAPL','MCD','IBM','CAT','TRV']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global variables
stock_data_df = None

app = Flask(__name__)

def prepare_pivot_market_data_frame():
    # prep data
    # loop through each stock and load csv
    stock_data_list = []

    return (stock_data)


@app.before_first_request
def startup():
    global stock_data_df

     # prepare pair trading data
    stock_data_df = prepare_pivot_market_data_frame()


@app.route("/", methods=['POST', 'GET'])
def get_pair_trade():
    if request.method == 'POST':
        selected_budget = request.form['selected_budget']
        # make sure the field isn't blank
        if selected_budget == '':
            selected_budget = 10000

        # calculate widest spread

        # budget trade size


        if request.form['submit'] == 'calculate_trade':
            return render_template('index.html',
                short_symbol = 'abc',
                long_symbol =  'abc',
                short_last_close = 5,
                short_size = 5,
                long_last_close = 5,
                long_size = round((float(8) * 0.5) / 8,2),
                selected_budget = 200)
        else:
            # build three charts
            stock = request.form['selected_security']
            initial_amount = request.form['initial_amount']
            quart_in  = request.form['quart_in']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            
            starting_amount = float(initial_amount)
            quart_contrib= float(quart_in)
            stocks_ratio = 1
            bonds_ratio = 0
            xpercent = 3

            #stock_symbol= "SSO"
            stock_symbol= stock
            Bond_fund_symbol="BND" 

            #start_date = "2010-1-1"
            #end_date = "2020-1-20"
            
            #stocks_df = get_pricing(stock_symbol, start_date=start_date, end_date=end_date)
            
            

            #define the ticker symbol
            #tickerSymbol = 'MSFT'

            #get data on this ticker
            tickerData = yf.Ticker(stock_symbol)
            #get the historical prices for this ticker
            stocks_df = tickerData.history(period='1d', start=start_date, end=end_date)
            
            
            
            stocks_cl_df=stocks_df['Close']
            f_dt= pd.to_datetime(stocks_cl_df.index)# convert index to datetime index
            stocks_cl_df = stocks_cl_df.reindex(f_dt)
            st_rs= stocks_cl_df.resample('Q')
            stocks_cl_q_last= st_rs.last()
            stocks_cl_q_first= st_rs.first()
            current_stock_price = stocks_cl_q_last[0]           
            starting_shares=int(float(starting_amount*stocks_ratio)/float(current_stock_price))
            stock_balance_df = starting_shares*stocks_cl_df# stock balance over all times
            shares_df = pd.Series
            current_shares = starting_shares
            stock_balance = stock_balance_df[0]

            sb_qs_rs = stock_balance_df.resample('Q')
            stock_balance_qs_df= sb_qs_rs.first()
            total_balance_qs_df = stock_balance_qs_df.copy()#just initializing the total balnce
            
            # calculations of ijr
            ijr_shares_df  = pd.DataFrame([starting_shares for x in range (len(stocks_cl_df))], index=stocks_cl_df.index)

            ijr_q_rs = ijr_shares_df.resample('Q').interpolate()
            #ijr_q_df= ijr_q_rs.first(1)
            #ijr_q_df.head()
            #stock_balance_qs_df.head()
            nbr_shares_df = stocks_cl_q_last.rdiv(float(quart_contrib))
            rsum = 0
            nbr_shares_df[0]= starting_shares + nbr_shares_df[0]
            #import pdb ; pdb.set_trace()
            #ijr_q_rs.to_frame()
            contrib_amount_q = pd.DataFrame([(ix)*quart_contrib for ix,x in enumerate(range(len(ijr_q_rs)))], index=ijr_q_rs.index)
            #contrib_amount_q = pd.Series([(ix)*quart_contrib for ix,x in enumerate(range(len(ijr_q_rs)))])

            for i in range(len(nbr_shares_df)-1):
                #rsum+=nbr_shares_df[i]
                ind = i+1
                nbr_shares_df[ind] = nbr_shares_df[ind] + nbr_shares_df[i]
    
            ijr_with_cash_df =stocks_cl_df*nbr_shares_df
            ijr_with_cash_df= ijr_with_cash_df.fillna(method='bfill').fillna(method ='bfill').fillna(method='ffill')            
            full_index= stocks_cl_df.index
            nbr_shares_df = nbr_shares_df.reindex(index = full_index, method='bfill')
            contrib_amount = contrib_amount_q.reindex(index = full_index, method = 'bfill')
            contrib_series = pd.DataFrame(contrib_amount, index = ijr_with_cash_df.index)
            #contrib_amount = contrib_amount_q.fillna(method='bfill').fillna(method ='bfill').fillna(method='ffill') 
            ijr_with_cash_df = nbr_shares_df* stocks_cl_df
            
            
            
            #import pdb ; pdb.set_trace()
            #ijr_with_cash_df = ijr_with_cash_df[:-20]
            plt.figure 
            frame = {
                    stock_symbol:stocks_cl_df*starting_shares,
                    stock_symbol+'_with_cash_injections':ijr_with_cash_df,
                    #'Contributions' : contrib_series
                    } 
            portfolio_nocash_df= pd.DataFrame(frame)
            
            portfolio_nocash_df.plot(title='With quarterly cash Injections', markevery =100)
            plt.grid()
            
            # WEAK SYMBOL - GO LONG
            #fig, ax = plt.subplots()
            #ax.plot(temp_series1.index, long_market_data)
            #plt.suptitle('Overly Bearish - Buy: ' + weakest_symbol[0])

            # rotate dates
            #myLocator = mticker.MultipleLocator(2)
            #ax.xaxis.set_major_locator(myLocator)
            #fig.autofmt_xdate()

            # fix label to only show first and last date
            #labels = ['' for item in ax.get_xticklabels()]
            #labels[1] = temp_series1.index[0]

            #labels[-2] = temp_series1.index[-1]
            #ax.set_xticklabels(labels)

            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            chart1_plot = Markup('<img style="padding:1px; border:1px solid #021a40; width: 90%; height: 500px" src="data:image/png;base64,{}">'.format(plot_url))

            chart2_plot = Markup('<img style="padding:1px; border:1px solid #021a40; width: 80%; height: 300px" src="data:image/png;base64,{}">'.format(plot_url))

            chart_diff_plot = Markup('<img style="padding:1px; border:1px solid #021a40; width: 80%; height: 300px" src="data:image/png;base64,{}">'.format(plot_url))

            #import pdb ; pdb.set_trace()
            final_value_port = round(ijr_with_cash_df[-1])
            final_value_index = round(stocks_cl_df[-1]*starting_shares)
            contributed_amount = quart_contrib*len(ijr_q_rs)
            
            index_inc = round((stocks_cl_df[-1]-stocks_cl_df[1])*100/stocks_cl_df[1])
            time_frame = int(end_date.split('-')[0]) - int(start_date.split('-')[0])
            in_amount  = float((starting_amount+contributed_amount))
            out_amount  = float(final_value_port)
            roe = round(((out_amount)*100)/in_amount)
            
            #import pdb ; pdb.set_trace()
            
            
            return render_template('charts.html',
                chart1_plot = chart1_plot,
                chart2_plot = chart2_plot,
                chart_diff_plot = chart_diff_plot,
                short_symbol = stock,
                long_symbol = stock,
                short_last_close = 5,
                short_size = 2,
                long_last_close = 3,
                long_size = 1,
                selected_budget = 1000,
                initial_amount = initial_amount,
                security = stock,
                final_value_port = final_value_port,
                final_value_index = final_value_index,
                contrib_amount = contributed_amount,
                index_inc = index_inc,
                time_frame = time_frame,
                roe = roe
                )

    else:
        # First time visit - return default settings
        return render_template('index.html',
            short_symbol = "None",
            long_symbol = "None",
            short_last_close = 0,
            short_size = 0,
            long_last_close = 0,
            long_size = 0,
            selected_budget = DEFAULT_BUDGET)

if __name__=='__main__':
    app.run(debug=True)


