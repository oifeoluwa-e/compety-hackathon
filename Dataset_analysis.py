#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing packages needed for the analysis

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


# In[2]:


#read dataset

df = pd.read_csv('DATASET.CSV')


# In[3]:


#understanding the data contained within the dateset 

df.describe(include='all')


# In[4]:


#checking for null values
df.isnull().sum()


# In[5]:


df.head(10)


# In[6]:


df.info()


# In[7]:


#Unique session count by platform and variation
session_count = df.groupby(['platform', 'variation'])['session_id'].nunique().reset_index()

session_count.columns = ['platform', 'variation', 'unique_session_count']

print(session_count)


# In[8]:


#Users count by platform and variation
user_count = df.groupby(['platform', 'variation'])['user_id'].count() #nunique().reset_index()

user_count.columns = ['platform', 'variation', 'unique_user_count']

print(user_count)


# In[9]:


#Unique Users count by platform and variation
unique_user_count = df.groupby(['platform', 'variation'])['user_id'].nunique().reset_index()

unique_user_count.columns = ['platform', 'variation', 'unique_user_count']

print(unique_user_count)


# In[10]:


# Plot using Seaborn
plt.figure(figsize=(8, 6))
sns.barplot(
    x='platform', 
    y='unique_user_count', 
    hue='variation', 
    data=unique_user_count, 
    palette='viridis'
)

# Add labels and title
plt.xlabel('Platform')
plt.ylabel('Unique User Count')
plt.title('User Count by Platform and Variation')
plt.legend(title='Variation')

# Show plot
plt.show()


# In[11]:


df['datetime_event'] = pd.to_datetime(df['datetime_event'])
# Extract the date (without time) from the datetime
df['date'] = df['datetime_event'].dt.date

# Group by date and variation, then count unique user_id per day
daily_users = df.groupby(['date', 'variation'])['user_id'].nunique().reset_index()

# Plot the line chart
plt.figure(figsize=(12, 6))

for variation in daily_users['variation'].unique():
    subset = daily_users[daily_users['variation'] == variation]
    plt.plot(subset['date'], subset['user_id'], label=f'Variation {variation}')

# Chart settings
plt.title('Trend of Number of Users by Day (Split by Variation)')
plt.xlabel('Date')
plt.ylabel('Number of Unique Users')
plt.xticks(rotation=45)
plt.legend(title='Variation')
plt.grid(True)

# Show the plot
plt.show()


# In[12]:


# Extract the hour from the datetime
df['hour'] = df['datetime_event'].dt.hour

# Group by hour and variation, then count unique user_id per hour
hourly_users = df.groupby(['hour', 'variation'])['user_id'].nunique().reset_index()

# Plot the line chart
plt.figure(figsize=(12, 6))

for variation in hourly_users['variation'].unique():
    subset = hourly_users[hourly_users['variation'] == variation]
    plt.plot(subset['hour'], subset['user_id'], label=f'Variation {variation}')

# Chart settings
plt.title('Trend of Number of Users by Hour (Split by Variation)')
plt.xlabel('Hour of the Day')
plt.ylabel('Number of Unique Users')
plt.xticks(range(0, 24))
plt.legend(title='Variation')
plt.grid(True)

# Show the plot
plt.show()


# In[13]:


#User count by platform and variation

filtered_df = df[(df['event_type'] == 'order_finished')]

user_count = filtered_df.groupby(['platform', 'variation'])['user_id'].count().reset_index()

user_count.columns = ['platform', 'variation', 'user_count']

print(user_count)


# In[14]:


# Count of User by platform, variation with Successful order
filtered_df = df[(df['event_type'] == 'order_finished') & (df['final_order_status'] == 'successful')]

# Group by platform, variation, and final_order_status, then count distinct user_id
user_count_successful = filtered_df.groupby(['platform', 'variation', 'final_order_status'])['user_id'].count().reset_index()

user_count_successful.columns = ['platform', 'variation', 'final_order_status', 'user_count']

print(user_count_successful)


# In[15]:


# Count of User by platform, variation with Cancelled order
filtered_df = df[(df['event_type'] == 'order_finished') & (df['final_order_status'] == 'cancelled')]

# Group by platform, variation, and final_order_status, then count distinct user_id
user_count_cancelled = filtered_df.groupby(['platform', 'variation', 'final_order_status'])['user_id'].count().reset_index()

user_count_cancelled.columns = ['platform', 'variation', 'final_order_status', 'user_count']

print(user_count_cancelled)


# In[16]:


# Count of User by platform, variation with Cancelled order
filtered_df = df[(df['event_type'] == 'order_finished') & (df['final_order_status'] == 'refunded_after_delivery')]

# Group by platform, variation, and final_order_status, then count distinct user_id
user_count_returned = filtered_df.groupby(['platform', 'variation', 'final_order_status'])['user_id'].count().reset_index()

user_count_returned.columns = ['platform', 'variation', 'final_order_status', 'user_count']

print(user_count_returned)


# In[ ]:





# In[17]:


df['datetime_event'] = pd.to_datetime(df['datetime_event'])

# Calculate time spent per session in minutes
session_time = df.groupby('session_id')['datetime_event'].agg(['min', 'max']).reset_index()
session_time['time_spent_seconds'] = (session_time['max'] - session_time['min']).dt.total_seconds()

# Merge the time spent back to the original DataFrame
df = df.merge(session_time[['session_id', 'time_spent_seconds']], on='session_id', how='left')

df.head(10)


# In[18]:


# drop duplicates to avoid repeated time spent per session
unique_sessions = df.drop_duplicates(subset='session_id')

# Calculate the average time spent per variation
avg_time_per_variation = unique_sessions.groupby(['platform','variation'])[['time_spent_seconds']].mean().reset_index()

avg_time_per_variation


# In[19]:


# Extract the day from datetime_event
df['event_day'] = df['datetime_event'].dt.day

# Group by platform, variation, and event_day, then count distinct user_id
user_count = (
    df.groupby(['platform', 'variation', 'event_day'])['user_id']
    .nunique()
    .reset_index()
    .rename(columns={'user_id': 'user_count'})
)

# Sort by platform, variation, and user_count descending
user_count = user_count.sort_values(by=['platform', 'variation', 'user_count'], ascending=[True, True, False])

print(user_count)


# In[20]:


#Hyphotesis testing

#focusing on conversion rate using instances where event_type = 'order_finshed'

# Filter the data where event_type is 'order_finished'
df_filtered = df[df['event_type'] == 'order_finished']

# Group by event_type and variation, then count the final_order_status
result_1 = df_filtered.groupby(['event_type', 'variation'])['final_order_status'].count().reset_index(name='count_order')

result_1 = result_1.sort_values(by='variation')


print(result_1)


# In[21]:


# Group by event_type, final_order_status, and variation, then count final_order_status
result_2 = df_filtered.groupby(['event_type', 'final_order_status', 'variation'])['final_order_status'].count().reset_index(name='count_order')

result_2 = result_2.sort_values(by='variation')


print(result_2)


# In[22]:


#Counting user by unique session

# Group by variation, platform, user_id, session_id and count distinct user_id per session
grouped = df.groupby(['variation', 'platform', 'session_id'])['user_id'].nunique().reset_index(name='countUser')

# Sum the countUser values for each variation and platform
result = grouped.groupby(['variation'])['countUser'].sum().reset_index()

print(result)


# In[23]:


#From the data above, we prepare the hyphothesis table

from statsmodels.stats.proportion import proportions_ztest

hypothesis_table = {
'variation':[1,2],
'total_users_by_session':[116589,62705],
'success':[28661,16197]
}

hypothesis_table = pd.DataFrame(hypothesis_table).set_index('variation')

hypothesis_table


# In[24]:


hypothesis_table['conversion_rate'] = hypothesis_table['success']/hypothesis_table['total_users_by_session']

hypothesis_table


# In[25]:


#Using Hyphothesis testing

'''
Ho: Increasing the size of food images on restaurant menu cards will not improve conversion to orders.

H1: Increasing the size of food images on restaurant menu cards will improve conversion to orders.
'''
# Conversion counts
success_1 = hypothesis_table.loc[1, 'success']
success_2 = hypothesis_table.loc[2, 'success']

# total users
tot_a = hypothesis_table.loc[1, 'total_users_by_session']
tot_b = hypothesis_table.loc[2, 'total_users_by_session']

# Perform the Z-test
stat, pval = proportions_ztest([success_1, success_2], [tot_a, tot_b])

print(f'Z-statistic: {stat:.2f}')
print(f'p-value: {pval:.8f}')


# In[26]:


#Conclusion

#since p-value is less than 0.001, we reject Ho and accept H1

# Therefore, we can conclude that result is highly statistically significant: Increasing the size of food images on restaurant menu cards will improve conversion to orders.

