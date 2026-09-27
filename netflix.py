#!/usr/bin/env python
# coding: utf-8
# lec 16 - 19Sep2026 remain 
# please complete it
# this notes are revision of lec 16
# read xlex
# fillna
# remove duplicate

# lec 17 - analysis data using pandas and matplotlibshape is used for count how many rows and duplicate columns in dataset

# describe is use to find all statistical information in 

# isnull.sum is use to find all null values in dataset

# duplicate is use to find duplicate records in dataset

# value count is use to count total repeated values

# dataframe is use to make tables in pandas using dictionary and list

# pip install streamlit 
# or 
# python -m pip install streamlitpython :- 
# --> data science :- to find pattern in data , understand data , to predict future
# --> data analytics :- to analysis the data

# data analytics and data science is related
# if data is not analysised how data sciencist can perform operation on data ?

# data analysis :- 
# --> pandas is used to collect and clean data
# 1. collect :- sql , excel , csv
# 2. clean
#    -->  null
#    --> duplicate
#    --> error
#    --> information
#    --> statistical information
# 3. problem statement
# 4. charts and graphs
# 5. analysis 
#6. comparison
# In[ ]:





# In[ ]:


# 1.


# In[3]:

import streamlit
import pandas as pd
import matplotlib.pyplot as plt


# In[4]:


# to create tabular structure in python

sales = pd.DataFrame({"quantity" : [1,2,3,4,5,6,],
                      "price" : [100,200,300,400,500,600],
                     })      


# In[5]:


sales 


# In[6]:


# additional step

sales["price"].value_counts().plot(kind = "bar")


# In[7]:


netflix = pd.read_csv("Netflix.csv")


# In[8]:


netflix


# In[9]:


netflix.shape


# In[10]:


netflix.info()


# In[11]:


# from this above information we unstand that Watch_Date datatype is str it should be date


# In[12]:


netflix.isnull()


# In[13]:


netflix.isnull().sum()


# In[14]:


# for statiscal information

netflix.describe()


# In[15]:


netflix.duplicated()


# In[16]:


netflix.duplicated().sum()


# In[17]:


netflix.drop_duplicates()


# In[18]:


netflix.drop_duplicates(inplace = True)


# In[19]:


netflix


# In[20]:


netflix["Watch_Date"] = pd.to_datetime(netflix["Watch_Date"])


# In[21]:


netflix.info()


# In[22]:


netflix["month"] = netflix["Watch_Date"].dt.month_name()


# In[23]:


netflix


# In[24]:


netflix.groupby("month")["Monthly_Revenue"].sum().plot(kind = "bar" , ylabel = "Monthly_Revenue", xlabel = "month")


# In[25]:


netflix.groupby("month")["Monthly_Revenue"].sum().plot(kind = "line" , ylabel = "Monthly_Revenue", xlabel = "month")


# In[26]:


netflix.groupby("month")["Monthly_Revenue"].sum().plot(kind = "pie" , ylabel = "Monthly_Revenue", xlabel = "month")


# In[27]:


netflix.groupby("month")["Monthly_Revenue"].sum().plot(kind = "bar" , ylabel = "Monthly_Revenue", xlabel = "month" , title = "Month-wise Revenue")


# In[28]:


netflix.groupby("Region")["Rating"].sum().plot(kind = "bar" , ylabel = "Rating", xlabel = "Region")


# In[29]:


netflix.groupby("Region")["Rating"].sum().plot(kind = "pie" , ylabel = "Rating", xlabel = "Region")


# In[84]:


netflix.groupby("Region")["Rating"].sum().plot(kind = "line" , ylabel = "Rating", xlabel = "Region")


# In[30]:


netflix.groupby("Region")["Rating"].sum().plot(kind = "pie" , ylabel = "rating", xlabel = "region" , title = "Region-wise Rating" , autopct = '%1.1f%%')


# In[31]:


netflix.groupby("Device")["Monthly_Revenue"].sum().plot(kind = "line" , ylabel = "Monthly_Revenue", xlabel = "Device" , title = "Device-wise Revenue")


# In[34]:


netflix["Rating"].value_counts().plot(kind  = "bar" , title = "Total Ratings")


# In[35]:


netflix.groupby("Region")["Monthly_Revenue"].sum().plot(kind = "bar" , ylabel = "Montly_Revenue" , xlabel = "Region" , title = "Region-wise Revenue")


# In[37]:


netflix.groupby("Subscription_Plan")["Watch_Count"].sum().plot(kind = "pie" , title = "Subscription Plan wise Watch Count" , autopct = "%1.1f%%")


# In[ ]:




