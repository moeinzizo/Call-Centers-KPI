#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[3]:


df = pd.read_csv("C:\\Users\\mzino\\OneDrive\\Desktop\\callStatusInfo.csv")


# In[25]:


def compute_thresholds(series, higher_is_better=False):
    avg = series.mean()
    std = series.std()
    if higher_is_better:
        return {
            "target": round(avg + std, 2),
            "threshold": round(avg, 2),
            "critical": round(avg - std, 2)
        }
    else:
        return {
            "target": round(avg - std, 2),
            "threshold": round(avg, 2),
            "critical": round(avg + std, 2)
        }


# In[32]:


#تبدیل زمان انتظار به ثانیه برای بدست آـوردن kpi

def time_to_seconds(time_str):
    try:
        if time_str.startswith('00:'):
            time_str = time_str[3:]       
        parts = time_str.split(':')
        
        if len(parts) == 2:
            minutes, seconds = map(float, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = map(float, parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            return float(time_str)
    except:
        return None

time_entries = df["میانگین زمان انتظار در صف"].str.split('00:').str[1:].explode()

df["time_seconds"] = time_entries.apply(time_to_seconds).dropna()

print(df["time_seconds"].head())


# In[33]:


kpi_results = {
    "تعداد تماس در صف": compute_thresholds(df["تعداد تماس در صف"], higher_is_better=False),
    
    "میانگین زمان انتظار در صف ": compute_thresholds(df["time_seconds"], higher_is_better=False),
    
    "نرخ موفقیت تماس (Success Rate)": compute_thresholds(df["موفق"] / df["کل تماس ها"], higher_is_better=True),
    
    "نرخ قطع تماس توسط مشتری": compute_thresholds(df["قطع توسط مشتری"] / df["کل تماس ها"], higher_is_better=False),
    
}


# In[34]:


print(kpi_results)

