#######################
# Imports
#######################

from pandas.tseries.offsets import DateOffset
import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
from pmdarima import auto_arima
import numpy as np
pio.renderers.default = 'browser'
import pandas as pd
pio.renderers.default = 'browser'
from sqlalchemy import create_engine


# make any grid with a function
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

# set size of streamlit page
st.set_page_config(layout="wide")


# set style of dataframe
styles = [

dict(selector="th", props=[("color", "#FFFFFF"),
("border", "1px solid #eee"),
("padding", "12px 35px"),
("border-collapse", "collapse"),
("background", "#002366"),
("text-transform", "uppercase"),
("font-size", "18px")
]),
dict(selector="td", props=[("color", "#FFFFFF"),
("border", "1px solid #eee"),
("padding", "12px 35px"),
("border-collapse", "collapse"),
("font-size", "18px"),
("background", "#002366")
]),
dict(selector="table", props=[
("font-family" , 'Arial'),
("margin" , "25px auto"),
("border-collapse" , "collapse"),
("border" , "1px solid #eee"),
("border-bottom" , "2px solid #00cccc"),
]),
dict(selector="caption", props=[("caption-side", "bottom")])
]




#######################
# Connection with DB
#######################

db_config = {
        'user': 'report',  # имя пользователя
        'pwd': 'DFSeew53dfgxz_dsffh6769675D',  # пароль
        'host': '51.250.69.136',
        'port': 5433,  # порт подключения
        'db': 'wb_dwh'  # название базы данных
        }

connection_string = 'postgresql://{}:{}@{}:{}/{}'.format(
        db_config['user'],
        db_config['pwd'],
        db_config['host'],
        db_config['port'],
        db_config['db'],
    )

engine = create_engine(connection_string)

#######################
# Loading orders
#######################

query = ''' SELECT * FROM stg.orders'''
orders = pd.read_sql_query(query, con=engine)
orders['last_change_date'] = orders['last_change_date'].dt.date
#######################
# Loading stocks
#######################

query = '''SELECT * FROM stg.stocks'''
stocks = pd.read_sql_query(query, con=engine)
stocks['lastchangedate'] = stocks['lastchangedate'].dt.date
#######################
# Creating the buttons
#######################

button_container = st.container()
with button_container:
    articles = orders.query('is_cancel == False')['nm_id'].unique()
    articles_selection = st.sidebar.multiselect('Choose a product article (nmid)',
                                        options=articles,
                                        max_selections=3,
                                        default=articles[0])

    for_string = [str(i) for i in articles_selection]
    string_articles = ' '.join(for_string)

    number = st.sidebar.number_input('Insert the critical value of a product in stock',
                                     min_value = 0,
                                     max_value = 1000,
                                     step = 1)




#######################
# Stock information
#######################
stock_container = st.container()
with stock_container:
    st.markdown('# Stocks info')
    st.markdown('#### General info')
    grid_1 = make_grid(1, (4, 2))

    # Getting up-to-date info about stock
    current_stock_date = stocks.sort_values(by=['lastchangedate'], ascending=False)['lastchangedate'].iloc[0]

    # General info about all stock
    current_stock = stocks.query('lastchangedate == @current_stock_date')
    stock_by_articles = current_stock.groupby('nmid')['quantity'].sum().reset_index().sort_values(by = 'quantity', ascending = False)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=stock_by_articles['nmid'], y=stock_by_articles['quantity']))
    fig.update_layout(barmode='overlay', width=900, height=400)
    fig.update_traces(opacity=0.75)
    fig.update_layout(xaxis_type='category')
    fig.update_layout(title=f'Remaining articles in stock {current_stock_date}')
    grid_1[0][0].plotly_chart(fig)

    # General info about warehouses

    warehouses = current_stock.groupby(['warehousename'])['quantity'].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=warehouses['warehousename'], values=warehouses['quantity']))
    fig.update_layout(barmode='overlay', height=200)
    fig.update_layout(title=f'Distribution of goods in warehouses {current_stock_date}')
    fig.update_traces(textposition='inside')
    fig.update_layout(
        height=400,
        width=430,
        uniformtext_minsize=10, uniformtext_mode='hide',
        legend=dict(font=dict(size=12)),
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50,
            pad=0
        ))
    grid_1[0][1].plotly_chart(fig)

    # Critical stock
    critical_in_stock = stock_by_articles.query('quantity <= @number').reset_index(drop=True).set_index('nmid')
    st.markdown(f'#### Running out of stock - quantity less than {number}')
    st.table(critical_in_stock.style.background_gradient(cmap="Reds_r"))



    # Detailed info about article
    st.markdown(f'#### Change inventory for chosen article(s) {string_articles} from  {stocks["lastchangedate"].min()} to {stocks["lastchangedate"].max()}')
    fig = go.Figure()
    for article in articles_selection:
        all_info = stocks.query('nmid == @article').groupby('lastchangedate')['quantity'].sum().reset_index()
        fig.add_trace(go.Scatter(x=all_info['lastchangedate'], y=all_info['quantity'], name = f'{article}'))
        fig.update_layout(barmode='overlay', width=1300, height=300)
        fig.update_traces(opacity=0.75)
    st.plotly_chart(fig)


#######################
# Orders information
#######################
orders_container = st.container()
with orders_container:
    st.markdown('# Orders info')
    st.write(f"#### Orders from {orders['last_change_date'].min()} to {orders['last_change_date'].max()}")

    # General info about all orders
    order_by_articles = orders.query('is_cancel == False').groupby('nm_id')['id'].count().sort_values(ascending=False).reset_index()
    order_by_articles.columns = ['nmid', 'orders']
    order_by_articles['nmid'] = order_by_articles['nmid'].astype('str')
    fig = go.Figure()
    fig.add_trace(go.Bar(x = order_by_articles['nmid'], y=order_by_articles['orders']))
    fig.update_layout(barmode='overlay', width=1300, height=300)
    fig.update_traces(opacity=0.75)
    fig.update_layout(xaxis_type='category')
    st.plotly_chart(fig)

    # Prediction
    st.write(f"#### Projected number of orders for the next 30 days for chosen article(s) {string_articles}")
    st.write(f"Prediction model - autoarima. Please wait, it may take a few seconds for the data to load")
    orders_ = orders.query('is_cancel == False').groupby(['nm_id', 'last_change_date'])['id'].count().reset_index()
    dict_arima = {}
    for article in articles_selection:
        article_sales = orders_.query('nm_id == @article').set_index('last_change_date')
        idx = pd.date_range(orders['last_change_date'].min(), orders['last_change_date'].max())
        article_sales = article_sales.reindex(idx)
        article_sales.loc[article_sales['nm_id'].isna(), 'nm_id'] = article
        article_sales = article_sales.fillna(0)
        article_sales.columns = ['article', 'sales']
        article_sales = article_sales[['sales']]
        future_dates = [article_sales.index[-1] + DateOffset(days=x) for x in range(0, 30)]

        model = auto_arima(article_sales,
                           trace=True,
                           test='adf',
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
        forecast = model.predict(n_periods=30)
        forecast = pd.DataFrame(forecast, index=future_dates[1:], columns=['Prediction'])
        dict_arima[article] = forecast['Prediction'].sum()
        article_sales['Prediction'] = np.nan
        forecast['sales'] = np.nan
        res = pd.concat([article_sales, forecast], axis=0).reset_index()
        res.columns = ['date', 'sales', 'prediction']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x= res['date'], y= res['sales'], name = 'orders'))
        fig.add_trace(go.Scatter(x=res['date'], y=res['prediction'], name = 'predicted orders'))
        fig.update_layout(barmode='overlay', width=1300, height=300)
        fig.update_traces(opacity=0.75)
        st.plotly_chart(fig)

    res_arima = pd.DataFrame(dict_arima.items(), columns=['nm_id', 'predicted_orders_arima_for_next_30_days']).set_index('nm_id').astype('int')


#######################
# Stock in days
#######################


stock_in_days_container = st.container()
with stock_in_days_container:
    st.markdown('# Remaining goods in days')
    for article in articles_selection:
        stocks_days = stock_by_articles.query('nmid == @article').merge(res_arima, right_on='nm_id', left_on='nmid')[['nmid', 'quantity', 'predicted_orders_arima_for_next_30_days']]
        if stocks_days['predicted_orders_arima_for_next_30_days'].sum() !=0:
            stocks_days['days'] = (stocks_days['quantity']/stocks_days['predicted_orders_arima_for_next_30_days']*30).astype('int')
            stocks_days.columns = ['nmid', 'in stock', 'predicted orders for the next 30 days', 'stock in days']
            stocks_days = stocks_days.set_index('nmid')
            stocks_days_style = stocks_days.style.set_table_styles(styles)
            st.table(stocks_days_style)

        else:
            st.markdown(f'#### The number of predicted orders for the product {article} is 0. There is no demand for this product')

