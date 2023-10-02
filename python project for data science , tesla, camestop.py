#!/usr/bin/env python
# coding: utf-8

# #### Question 1 - Extracting Tesla Stock Data Using yfinance
# 
# 

# In[1]:


get_ipython().system('pip install yfinance==0.1.67')
get_ipython().system('mamba install bs4==4.10.0 -y')
get_ipython().system('pip install nbformat==4.2.0')
get_ipython().system('pip install -U yfinance pandas')
get_ipython().system('pip install pandas==1.3.5')

get_ipython().system('pip install requests==2.26.0')
get_ipython().system('pip install plotly==5.3.1')
get_ipython().system('pip install html5lib')
get_ipython().system('pip install --upgrade nbformat')

get_ipython().system('pip install ipykernel')


# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[3]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[4]:


tesla = yf.Ticker('TSLA')


# In[5]:


tesla_data = tesla.history(period="max")


# In[6]:


tesla_data.reset_index(inplace=True)
tesla_data.head(5)


# #### Question 2 - Extracting Tesla Revenue Data Using Webscraping - 1 Points
# 

# In[7]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text


# In[8]:


soup = BeautifulSoup(html_data, "html")
print(soup.prettify())


# In[9]:


tesla_revenue = pd.DataFrame(columns = ["Date","Revenue"])

for table in soup.find_all('table'):
    if table.find('th').getText().startswith("Tesla Quarterly Revenue"):
        for row in table.find("tbody").find_all("tr"):
            col = row.find_all("td")
            if len(col) != 2: continue
            Date = col[0].text
            Revenue = col[1].text.replace("$","").replace(",","")
               
            tesla_revenue = tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[10]:


tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[11]:


tesla_revenue.tail(5)


# #### Question 3 - Extracting GameStop Stock Data Using yfinance
# 

# In[12]:


gme = yf.Ticker('GME')


# In[13]:


gme_data = gme.history(period = "max")


# In[14]:


gme_data.reset_index(inplace=True)
gme_data.head(5)


# #### Question 4 - Extracting GameStop Revenue Data Using Webscraping

# In[15]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

html_data  = requests.get(url).text


# In[16]:


soup = BeautifulSoup(html_data,"html5lib")


# In[17]:


tables = soup.find_all('table')
for index,table in enumerate(tables):
    if ("GameStop Quarterly Revenue" in str(table)):
        table_index = index
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        gme_revenue = gme_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)


# In[18]:


gme_revenue.tail()


# #### Question 5 - Tesla Stock and Revenue Dashboard - 2 Points
# 

# In[21]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# #### Question 6 - GameStop Stock and Revenue Dashboard
# 

# In[22]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




