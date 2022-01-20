#!/usr/bin/env python
# coding: utf-8

# # Importing necessary dataset

# In[103]:


import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# ## Importing all 15 csv files

# In[104]:


file_path = r'C:\Users\vanes\OneDrive\Desktop\RTRA_csv'
all_csv_files = glob.glob(file_path + '/*.csv')

csv_list = []

for csv_file in all_csv_files:
    combined_dataframe = pd.read_csv(csv_file, index_col = None, header = 0)
    csv_list.append(combined_dataframe)
    
data = pd.concat(csv_list, axis = 0, ignore_index = True)
data


# In[105]:


data.NAICS.value_counts()


# In[5]:


#data[['SYEAR', 'SMTH']] = data[['SYEAR', 'SMTH']].astype(object) 
#print(data.dtypes) 


# ## Getting *Postal service, couriers and messengers* from Postal service[491] & Couriers and messengers[492]

# In[106]:


Couriers_and_messengers = data.loc[data['NAICS'].str.contains('492', na = False)]
Couriers_and_messengers


# In[107]:


Postal_service = data.loc[data['NAICS'].str.contains('491', na = False)]
Postal_service


# In[108]:


Postal_service_couriers_and_messengers = pd.concat([Postal_service, Couriers_and_messengers])
Postal_service_couriers_and_messengers


# ### Changing all names of the NACIS column to *Postal service, couriers and messengers*
# 
# After changing all column names to *Postal service, couriers and messengers*, the dataframe was sorted by the **SYEAR and SMTH** columns. Then, the *Employment* column was segregated to add up consecutives even rows to get the sum of empoyments from both [491] and [492].
# 
# After that, the dataframe was merged back and the columns names were changed to reflect *Data Output Template*.

# In[109]:


Postal_service_couriers_and_messengers = Postal_service_couriers_and_messengers.replace(
    'Postal service[491]', 'Postal service, couriers and messengers')
Postal_service_couriers_and_messengers = Postal_service_couriers_and_messengers.replace(
    'Couriers and messengers[492]', 'Postal service, couriers and messengers')
Postal_service_couriers_and_messengers


# In[110]:


df1 = Postal_service_couriers_and_messengers.sort_values(['SYEAR', 'SMTH'])
df1.head(50)


# In[111]:


df = df1.drop(['SYEAR', 'SMTH', 'NAICS'], axis = 1)
df


# In[112]:


df.index = np.arange(1,len(df)+1)
df = df.reset_index()
df


# In[113]:


df = df.set_index('index')
df_odd = df.loc[df.index.values % 2 == 1]
df_even = df.loc[df.index.values % 2 == 0]
df_even = df_even.set_index(df_even.index.values - 1)
new = df_odd.add(df_even, fill_value = 0)
new = new.reset_index().reset_index()
new


# In[114]:


df2 = df1[np.arange(len(df)) % 2 == 0]
df2 = df2.reset_index().reset_index()
df2


# In[115]:


df3 = pd.merge(df2, new, how = 'inner', on = 'level_0')
df3 = df3.drop(['level_0', 'index_x', '_EMPLOYMENT__x', 'index_y'], axis = 1)
df3.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Postal_service_couriers_and_messengers   = df3

Postal_service_couriers_and_messengers = Postal_service_couriers_and_messengers[
    (Postal_service_couriers_and_messengers.SYEAR != 2019)]

Postal_service_couriers_and_messengers   


# ## Getting *Farms* from Crop production[111] & Animal production and aquaculture[112]

# In[116]:


Crop_Production = data.loc[data['NAICS'].str.contains('111', na = False)]
Crop_Production


# In[117]:


Animal_production_and_aquaculture = data.loc[data['NAICS'].str.contains('112', na = False)]
Animal_production_and_aquaculture


# In[118]:


Farms = pd.concat([Crop_Production, Animal_production_and_aquaculture])
Farms


# ### Changing all names of the NACIS column to *Farms*
# 
# After changing all column names to *Farms*, the dataframe was sorted by the **SYEAR and SMTH** columns. Then, the *Employment* column was segregated to add up consecutives even rows to get the sum of empoyments from both [111] and [112].
# 
# After that, the dataframe was merged back and the columns names were changed to reflect *Data Output Template*.

# In[119]:


Farms = Farms.replace('Crop production[111]', 'Farms')
Farms = Farms.replace('Animal production and aquaculture[112]', 'Farms')
Farms


# In[120]:


df1 = Farms.sort_values(['SYEAR', 'SMTH'])
df1.head(50)


# ### Executing all aforementioned steps in one cell 

# In[121]:


df = df1.drop(['SYEAR', 'SMTH', 'NAICS'], axis = 1)
df

df.index = np.arange(1,len(df)+1)
df = df.reset_index()
df

df = df.set_index('index')
df_odd = df.loc[df.index.values % 2 == 1]
df_even = df.loc[df.index.values % 2 == 0]
df_even = df_even.set_index(df_even.index.values - 1)
new = df_odd.add(df_even, fill_value = 0)
new = new.reset_index().reset_index()
new

df2 = df1[np.arange(len(df)) % 2 == 0]
df2 = df2.reset_index().reset_index()
df2

df3 = pd.merge(df2, new, how = 'inner', on = 'level_0')
df3 = df3.drop(['level_0', 'index_x', '_EMPLOYMENT__x', 'index_y'], axis = 1)
df3.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Farms = df3

Farms = Farms[(Farms.SYEAR != 2019)]

Farms


# ## Getting *Food, beverage and tobacco manufacturing* from Food manufacturing[311] & Beverage and tobacco product manufacturing[312]

# In[122]:


Food_manufacturing = data.loc[data['NAICS'].str.contains('311', na = False)]
Food_manufacturing


# In[123]:


Beverage_and_tobacco_product_manufacturing = data.loc[data['NAICS'].str.contains('312', na = False)]
Beverage_and_tobacco_product_manufacturing


# In[124]:


Food_beverage_and_tobacco_manufacturing = pd.concat([Food_manufacturing, Beverage_and_tobacco_product_manufacturing])
Food_beverage_and_tobacco_manufacturing


# ### Changing all names of the NACIS column to *Food, beverage and tobacco manufacturing*
# 
# After changing all column names to *Food, beverage and tobacco manufacturing*, the dataframe was sorted by the **SYEAR and SMTH** columns. Then, the *Employment* column was segregated to add up consecutives even rows to get the sum of empoyments from both [311] and [312].
# 
# After that, the dataframe was merged back and the columns names were changed to reflect *Data Output Template*.

# In[126]:


Food_beverage_and_tobacco_manufacturing = Food_beverage_and_tobacco_manufacturing.replace(
    'Food manufacturing[311]', 'Food, beverage and tobacco manufacturing')
Food_beverage_and_tobacco_manufacturing = Food_beverage_and_tobacco_manufacturing.replace(
    'Beverage and tobacco product manufacturing[312]', 'Food, beverage and tobacco manufacturing')
Food_beverage_and_tobacco_manufacturing


# In[127]:


df1 = Food_beverage_and_tobacco_manufacturing.sort_values(['SYEAR', 'SMTH'])
df1.tail(50)


# ### Executing all aforementioned steps in one cell 

# In[128]:


df = df1.drop(['SYEAR', 'SMTH', 'NAICS'], axis = 1)
df

df.index = np.arange(1,len(df)+1)
df = df.reset_index()
df

df = df.set_index('index')
df_odd = df.loc[df.index.values % 2 == 1]
df_even = df.loc[df.index.values % 2 == 0]
df_even = df_even.set_index(df_even.index.values - 1)
new = df_odd.add(df_even, fill_value = 0)
new = new.reset_index().reset_index()
new

df2 = df1[np.arange(len(df)) % 2 == 0]
df2 = df2.reset_index().reset_index()
df2

df3 = pd.merge(df2, new, how = 'inner', on = 'level_0')
df3 = df3.drop(['level_0', 'index_x', '_EMPLOYMENT__x', 'index_y'], axis = 1)
df3.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Food_beverage_and_tobacco_manufacturing = df3

Food_beverage_and_tobacco_manufacturing =Food_beverage_and_tobacco_manufacturing[
    (Food_beverage_and_tobacco_manufacturing.SYEAR != 2019)]

Food_beverage_and_tobacco_manufacturing


# ## Getting  *Business, building and other support services*  from Management of companies and enterprises[55] & Administrative and support, waste management and remediation services[56]
# 
# The whole process was repeated to obatin the *Business, building and other support services*. After changing all column names to *Business, building and other support services*, the dataframe was sorted by the **SYEAR and SMTH** columns. Then, the *Employment* column was segregated to add up consecutives even rows to get the sum of empoyments from both [55] and [56].
# 
# After that, the dataframe was merged back and the columns names were changed to reflect *Data Output Template*.

# In[129]:


MCE = data[data['NAICS'] == 'Management of companies and enterprises [55]']
MCE


# In[130]:


MCE.SYEAR.value_counts().sort_values()


# As we can see, **Management of companies and enterprises** collected data till 2015, as such the *2016-2019* data has to be removed from **Administrative and support, waste management and remediation services** before algorithm can correctly add consecutive even rows to get the required sum. After getting the correct sum, the *2016-2019* will be added.

# In[131]:


AWR = data[data['NAICS'] == 'Administrative and support, waste management and remediation services [56]']
AWR


# In[132]:


AWR_reduced = AWR[(data['SYEAR'] != 2016) & (data['SYEAR'] != 2017) & (data['SYEAR'] != 2018) & (data['SYEAR'] != 2019)]
AWR_reduced


# In[133]:


AWR_removed_data = AWR[(data['SYEAR'] == 2016) | (data['SYEAR'] == 2017) | (data['SYEAR'] == 2018) | (data['SYEAR'] == 2019)]
AWR_removed_data


# In[134]:


Business_building_and_other_support_services = pd.concat([MCE, AWR_reduced])
Business_building_and_other_support_services


# In[135]:


Business_building_and_other_support_services = Business_building_and_other_support_services.replace(
    'Management of companies and enterprises [55]', 'Business, building and other support services')
Business_building_and_other_support_services = Business_building_and_other_support_services.replace(
    'Administrative and support, waste management and remediation services [56]', 'Business, building and other support services')
Business_building_and_other_support_services


# In[136]:


df1 = Business_building_and_other_support_services.sort_values(['SYEAR', 'SMTH'])
df1.head(50)


# ### Executing all aforementioned steps in one cell 

# In[138]:


df = df1.drop(['SYEAR', 'SMTH', 'NAICS'], axis = 1)
df

df.index = np.arange(1,len(df)+1)
df = df.reset_index()
df

df = df.set_index('index')
df_odd = df.loc[df.index.values % 2 == 1]
df_even = df.loc[df.index.values % 2 == 0]
df_even = df_even.set_index(df_even.index.values - 1)
new = df_odd.add(df_even, fill_value = 0)
new = new.reset_index().reset_index()
new

df2 = df1[np.arange(len(df)) % 2 == 0]
df2 = df2.reset_index().reset_index()
df2

df3 = pd.merge(df2, new, how = 'inner', on = 'level_0')
df3 = df3.drop(['level_0', 'index_x', '_EMPLOYMENT__x', 'index_y'], axis = 1)
df3.columns = ['SYEAR', 'SMTH', 'NAICS', '_EMPLOYMENT_']
Business_building_and_other_support_services = df3

Business_building_and_other_support_services


# Adding removed data and renaming the coulmns now

# In[139]:


Business_building_and_other_support_services = pd.concat([Business_building_and_other_support_services, AWR_removed_data])
Business_building_and_other_support_services.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']

Business_building_and_other_support_services


# In[140]:


Business_building_and_other_support_services = Business_building_and_other_support_services[
    (Business_building_and_other_support_services.SYEAR != 2019)]
Business_building_and_other_support_services


# ## Getting  *Local and Indigenous public administration*  from Local, municipal and regional public administration[913], Aboriginal public administration[914] & International and other extra-territorial public administration[919]
# 
# The whole process was repeated to obatin the *Local and Indigenous public administration*. After changing all column names to *Business, building and other support services*, the dataframe was sorted by the **SYEAR and SMTH** columns. Then, the *Employment* column was segregated to add up three consecutives rows to get the sum of empoyments from [913], [914] and [919].
# 
# After that, the dataframe was merged back and the columns names were changed to reflect *Data Output Template*.

# In[141]:


LMRPA = data.loc[data['NAICS'].str.contains('913', na = False)]
LMRPA


# In[142]:


Aboriginal_public_administration = data.loc[data['NAICS'].str.contains('914', na = False)]
Aboriginal_public_administration


# In[143]:


IETPA = data.loc[data['NAICS'].str.contains('919', na = False)]
IETPA


# In[145]:


Local_and_Indigenous_public_administration = pd.concat([LMRPA, Aboriginal_public_administration, IETPA])
Local_and_Indigenous_public_administration


# In[43]:


Local_and_Indigenous_public_administration = Local_and_Indigenous_public_administration.replace(
    'Local, municipal and regional public administration[913]', 'Local and Indigenous public administration')
Local_and_Indigenous_public_administration = Local_and_Indigenous_public_administration.replace(
    'Aboriginal public administration[914]','Local and Indigenous public administration')
Local_and_Indigenous_public_administration = Local_and_Indigenous_public_administration.replace(
    'International and other extra-territorial public administration[919]', 'Local and Indigenous public administration')
Local_and_Indigenous_public_administration


# In[146]:


df1 = Local_and_Indigenous_public_administration.sort_values(['SYEAR', 'SMTH'])
df1


# ### Executing the rest of the aforementioned steps in the subsequent cells

# In[147]:


df = df1.drop(['SYEAR', 'SMTH', 'NAICS'], axis = 1)
df

df.index = np.arange(1,len(df)+1)
df = df.reset_index()

df = df.set_index('index')
df_first = df.loc[df.index.values % 3 == 1].reset_index()
df_second = df.loc[df.index.values % 3 == 2].reset_index()
df_third = df.loc[df.index.values % 3 == 0].reset_index()


# In[148]:


new  = pd.merge(df_first, df_second, left_index=True, right_index=True)
new  = pd.merge(new, df_third, left_index=True, right_index=True)
new['EMPLOYMENT'] = new['_EMPLOYMENT__x'] + new['_EMPLOYMENT__y'] + new['_EMPLOYMENT_']
new = new['EMPLOYMENT']
new.to_frame()


# In[149]:


df2 = df1[np.arange(len(df)) % 3 == 0]
df2 = df2.reset_index().reset_index()
df2


# In[151]:


df3 = pd.merge(df2, new, left_index=True, right_index=True)
df3 = df3.drop(['level_0', 'index', '_EMPLOYMENT_'], axis = 1)
df3.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Local_and_Indigenous_public_administration = df3

Local_and_Indigenous_public_administration = Local_and_Indigenous_public_administration[
    (Local_and_Indigenous_public_administration.SYEAR != 2019)]

Local_and_Indigenous_public_administration


# ## Getting  *Broadcasting, data processing, and information*  from 	Broadcasting (except Internet)[515], Data processing, hosting, and related services[518] & International and other Other information services[519]
# 
# A new method was applied to obatin the *Broadcasting, data processing, and information*. The three extracted dataframes were merged on their indexes. Then, all the *Employment* columns were added to get the sum of empoyments from [515], [518] and [519]. 
# 
# After that, the other columns were removed, the NAICS column name was cahnged to *Broadcasting, data processing, and information* and the columns names were changed to reflect *Data Output Template*.

# In[152]:


Broadcasting_exceptInternet = data.loc[data['NAICS'].str.contains('515', na = False)].reset_index()
Broadcasting_exceptInternet


# In[153]:


Data_processing_hosting = data.loc[data['NAICS'].str.contains('518', na = False)].reset_index()
Data_processing_hosting


# In[154]:


other_information_services = data.loc[data['NAICS'].str.contains('519', na = False)].reset_index()
other_information_services


# In[155]:


Broadcasting_data_processing_and_information = pd.merge(
    Broadcasting_exceptInternet, Data_processing_hosting, left_index=True, right_index=True)
Broadcasting_data_processing_and_information = pd.merge(
    Broadcasting_data_processing_and_information, other_information_services, left_index=True, right_index=True)
Broadcasting_data_processing_and_information


# In[156]:


Broadcasting_data_processing_and_information = Broadcasting_data_processing_and_information.drop([
    'index_x', 'SYEAR_x', 'SMTH_x', 'NAICS_x', 'index_y', 'SYEAR_y', 'SMTH_y', 'NAICS_y', 'index'], axis =1)
Broadcasting_data_processing_and_information


# In[157]:


Broadcasting_data_processing_and_information['EMPLOYMENT'] =(Broadcasting_data_processing_and_information['_EMPLOYMENT__x'] + 
Broadcasting_data_processing_and_information['_EMPLOYMENT__y'] + Broadcasting_data_processing_and_information['_EMPLOYMENT_'])
Broadcasting_data_processing_and_information = Broadcasting_data_processing_and_information.drop(
    ['_EMPLOYMENT__x', '_EMPLOYMENT__y', '_EMPLOYMENT_'], axis = 1)
Broadcasting_data_processing_and_information = Broadcasting_data_processing_and_information.replace(
    'Other information services[519]', 'Broadcasting data processing and information')
Broadcasting_data_processing_and_information.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']


# In[158]:


Broadcasting_data_processing_and_information = Broadcasting_data_processing_and_information[
    (Broadcasting_data_processing_and_information.SYEAR != 2019)]

Broadcasting_data_processing_and_information


# ## Getting  *Transit, sightseeing, and pipeline transportation*  from Transit and ground passenger transportation[485], Pipeline transportation[486] & Scenic and sightseeing transportation[487]	
# 
# The new method was applied to obatin the *Transit, sightseeing, and pipeline transportation*. The three extracted dataframes were merged on their indexes. Then, all the *Employment* columns were added to get the sum of empoyments from [485], [486] and [487]. 
# 
# After that, the other columns were removed, the NAICS column name was cahnged to *Transit, sightseeing, and pipeline transportation* and the columns names were changed to reflect *Data Output Template*.

# In[159]:


Transit_and_ground_passenger_transportation = data.loc[data['NAICS'].str.contains('485', na = False)].reset_index()
Transit_and_ground_passenger_transportation


# In[160]:


Pipeline_transportation = data.loc[data['NAICS'].str.contains('486', na = False)].reset_index()
Pipeline_transportation


# In[161]:


Scenic_and_sightseeing_transportation = data.loc[data['NAICS'].str.contains('487', na = False)].reset_index()
Scenic_and_sightseeing_transportation


# In[162]:


Transit_sightseeing_and_pipeline_transportation = pd.merge(
    Transit_and_ground_passenger_transportation, Pipeline_transportation, left_index=True, right_index=True)
Transit_sightseeing_and_pipeline_transportation = pd.merge(
    Transit_sightseeing_and_pipeline_transportation, Scenic_and_sightseeing_transportation, left_index=True, right_index=True)
Transit_sightseeing_and_pipeline_transportation


# In[163]:


Transit_sightseeing_and_pipeline_transportation = Transit_sightseeing_and_pipeline_transportation.drop([
    'index_x', 'SYEAR_x', 'SMTH_x', 'NAICS_x', 'index_y', 'SYEAR_y', 'SMTH_y', 'NAICS_y', 'index'], axis =1)
Transit_sightseeing_and_pipeline_transportation


# In[164]:


Transit_sightseeing_and_pipeline_transportation['EMPLOYMENT'] =(Transit_sightseeing_and_pipeline_transportation['_EMPLOYMENT__x'] + 
Transit_sightseeing_and_pipeline_transportation['_EMPLOYMENT__y'] + Transit_sightseeing_and_pipeline_transportation['_EMPLOYMENT_'])
Transit_sightseeing_and_pipeline_transportation = Transit_sightseeing_and_pipeline_transportation.drop(
    ['_EMPLOYMENT__x', '_EMPLOYMENT__y', '_EMPLOYMENT_'], axis = 1)
Transit_sightseeing_and_pipeline_transportation = Transit_sightseeing_and_pipeline_transportation.replace(
    'Scenic and sightseeing transportation[487]', 'Transit, sightseeing, and pipeline transportation')
Transit_sightseeing_and_pipeline_transportation.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Transit_sightseeing_and_pipeline_transportation


# In[165]:


Transit_sightseeing_and_pipeline_transportation = Transit_sightseeing_and_pipeline_transportation[
    (Transit_sightseeing_and_pipeline_transportation.SYEAR != 2019)]

Transit_sightseeing_and_pipeline_transportation


# ## Getting  *Finance*  from Monetary authorities - central bank[521], Credit intermediation and related activities[522]	, International and Blank[523] & Funds and other financial vehicles[526]	
# 
# The new method was applied to obatin the *Finance*. The four extracted dataframes were merged on their indexes. Then, all the *Employment* columns were added to get the sum of empoyments from [521], [522], [523], and [526]. **This time around [523] had no rows as proven below. Also, [521] contains data for only 1997-1999, as such a little data manipulation was done to obtain the right results.**
# 
# After that, the other columns were removed, the NAICS column name was cahnged to *Finance* and the columns names were changed to reflect *Data Output Template*.

# In[166]:


Monetary_authorities_central_bank = data.loc[data['NAICS'].str.contains('521', na = False)].reset_index()
Monetary_authorities_central_bank


# In[167]:


Credit_intermediation_and_related_activities = data.loc[data['NAICS'].str.contains('522', na = False)].reset_index()
Credit_intermediation_and_related_activities


# In[168]:


blank_for_523 = data.loc[data['NAICS'].str.contains('523', na = False)].reset_index()
blank_for_523


# In[169]:


Funds_and_other_financial_vehicles = data.loc[data['NAICS'].str.contains('526', na = False)].reset_index()
Funds_and_other_financial_vehicles.columns = ['index', 'SYEAR', 'SMTH', 'NAICS', '_EMPLOYMENT_']
Funds_and_other_financial_vehicles


# In[170]:


add_on = Funds_and_other_financial_vehicles.loc[(Funds_and_other_financial_vehicles['SYEAR'] != 1997) & (Funds_and_other_financial_vehicles['SYEAR'] != 1998) & (Funds_and_other_financial_vehicles['SYEAR'] != 1999)]
add_on = add_on.drop('_EMPLOYMENT_', axis =1)
add_on['_EMPLOYMENT_'] = 0
Monetary_authorities_central_bank = pd.concat([Monetary_authorities_central_bank, add_on])
Monetary_authorities_central_bank


# In[212]:


Finance = pd.merge(
   Monetary_authorities_central_bank,Credit_intermediation_and_related_activities, left_index=True, right_index=True)
Finance = pd.merge(
    Finance, Funds_and_other_financial_vehicles, left_index=True, right_index=True)
Finance


# In[213]:


Finance = Finance.drop([
    'index_x', 'SYEAR_x', 'SMTH_x', 'NAICS_x', 'index_y', 'SYEAR_y', 'SMTH_y', 'NAICS_y', 'index'], axis =1)
Finance


# In[214]:


Finance['EMPLOYMENT'] =(Finance['_EMPLOYMENT__x'] + 
Finance['_EMPLOYMENT__y'] + Finance['_EMPLOYMENT_'])
Finance = Finance.drop(
    ['_EMPLOYMENT__x', '_EMPLOYMENT__y', '_EMPLOYMENT_'], axis = 1)
Finance = Finance.replace(
    'Funds and other financial vehicles[526]', 'Finance')
Finance.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Finance


# In[215]:


Finance = Finance[(Finance.SYEAR != 2019)]
Finance


# ## Getting  *Private and trades education*  from Business and secretarial schools[6114], Technical and trade schools[6115]	,  Other schools and instruction[6116] & Educational support services[6117]	
# 
# A new method was applied to obatin the *Private and trades education*. **The four extracted dataframes' __EMPLOYMENT__ were added to get the accurate results without merge methods.

# In[216]:


BSS = data.loc[data['NAICS'] == 6114].reset_index()
BSS


# In[217]:


TTS = data.loc[data['NAICS'] == 6115].reset_index()
TTS


# In[218]:


OSI = data.loc[data['NAICS'] == 6116].reset_index()
OSI


# In[219]:


ESS = data.loc[data['NAICS'] == 6117].reset_index()
ESS


# In[220]:


ESS['EMPLOYMENT'] = BSS['_EMPLOYMENT_'] + OSI['_EMPLOYMENT_'] + TTS['_EMPLOYMENT_'] + ESS['_EMPLOYMENT_']
Private_and_trades_education = ESS


# In[221]:


Private_and_trades_education = Private_and_trades_education.replace(6117, 'Private and trades education')
Private_and_trades_education = Private_and_trades_education.drop('_EMPLOYMENT_', axis= 1)
Private_and_trades_education = Private_and_trades_education.drop('index', 1)
Private_and_trades_education


# In[222]:


Private_and_trades_education = Private_and_trades_education[(Private_and_trades_education.SYEAR != 2019)]
Private_and_trades_education.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Private_and_trades_education


# ## Getting  *Transportation equipment manufacturing (excluding shipbuilding)*  from Motor vehicle manufacturing[3361], Motor vehicle body and trailer manufacturing[3362],  Motor vehicle parts manufacturing[3363],  Aerospace product and parts manufacturing[3364], Railroad rolling stock manufacturing[3365] & Other transportation equipment manufacturing[3369]	
# 
# The new method was applied to obatin the **Transportation equipment manufacturing (excluding shipbuilding)**. **The six extracted dataframes' __EMPLOYMENT__ were added to get the accurate results without merge methods.**

# In[223]:


Motor_vehicle_manufacturing = data.loc[data['NAICS'] == 3361].reset_index()
Motor_vehicle_manufacturing


# In[224]:


Motor_vehicle_body_and_trailer_manufacturing = data.loc[data['NAICS'] == 3362].reset_index()
Motor_vehicle_body_and_trailer_manufacturing


# In[225]:


Motor_vehicle_parts_manufacturing = data.loc[data['NAICS'] == 3363].reset_index()
Motor_vehicle_parts_manufacturing 


# In[226]:


Aerospace_product_and_parts_manufacturing = data.loc[data['NAICS'] == 3364].reset_index()
Aerospace_product_and_parts_manufacturing


# In[227]:


Railroad_rolling_stock_manufacturing = data.loc[data['NAICS'] == 3365].reset_index()
Railroad_rolling_stock_manufacturing


# In[228]:


Other_transportation_equipment_manufacturing = data.loc[data['NAICS'] == 3369].reset_index()
Other_transportation_equipment_manufacturing


# In[229]:


Other_transportation_equipment_manufacturing['EMPLOYMENT'] = Other_transportation_equipment_manufacturing['_EMPLOYMENT_'] + Railroad_rolling_stock_manufacturing['_EMPLOYMENT_'] + Aerospace_product_and_parts_manufacturing['_EMPLOYMENT_'] + Motor_vehicle_parts_manufacturing['_EMPLOYMENT_'] + Motor_vehicle_body_and_trailer_manufacturing['_EMPLOYMENT_'] + Motor_vehicle_manufacturing['_EMPLOYMENT_']
Transportation_equipment_manufacturing_excluding_shipbuilding = Other_transportation_equipment_manufacturing


# In[230]:


Transportation_equipment_manufacturing_excluding_shipbuilding = Transportation_equipment_manufacturing_excluding_shipbuilding.replace(3369, 
                                                    'Transportation equipment manufacturing - excluding shipbuilding')
Transportation_equipment_manufacturing_excluding_shipbuilding = Transportation_equipment_manufacturing_excluding_shipbuilding.drop(
    '_EMPLOYMENT_', axis= 1)
Transportation_equipment_manufacturing_excluding_shipbuilding = Transportation_equipment_manufacturing_excluding_shipbuilding.drop(
'index', 1)
Transportation_equipment_manufacturing_excluding_shipbuilding


# In[231]:


Transportation_equipment_manufacturing_excluding_shipbuilding = Transportation_equipment_manufacturing_excluding_shipbuilding[
    (Transportation_equipment_manufacturing_excluding_shipbuilding.SYEAR != 2019)]
Transportation_equipment_manufacturing_excluding_shipbuilding.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Transportation_equipment_manufacturing_excluding_shipbuilding


# ## Getting  *Legal, accounting, design, research, and advertising services*  from  Legal services[5411], Accounting, tax preparation, bookkeeping and payroll services[5412],  Specialized design services[5414],   Scientific research and development services[5417], Advertising, public relations, and related services[5418] & Other professional, scientific and technical services[5419]	
# 
# The new method was applied to obatin the **Transportation equipment manufacturing (excluding shipbuilding)**. **The six extracted dataframes' __EMPLOYMENT__ were added to get the accurate results without merge methods.**

# In[232]:


LS = data.loc[data['NAICS'] == 5411].reset_index()
LS


# In[233]:


ATPBP = data.loc[data['NAICS'] == 5412].reset_index()
ATPBP


# In[234]:


SDS = data.loc[data['NAICS'] == 5414].reset_index()
SDS


# In[235]:


SRDS = data.loc[data['NAICS'] == 5417].reset_index()
SRDS


# In[236]:


APRRS = data.loc[data['NAICS'] == 5418].reset_index()
APRRS


# In[237]:


OPSTS = data.loc[data['NAICS'] == 5419].reset_index()
OPSTS


# In[238]:


OPSTS['EMPLOYMENT'] = LS['_EMPLOYMENT_'] + ATPBP['_EMPLOYMENT_'] + SDS['_EMPLOYMENT_'] + SRDS['_EMPLOYMENT_'] + APRRS['_EMPLOYMENT_'] + OPSTS['_EMPLOYMENT_']
Legal_accounting_design_research_and_advertising_services = OPSTS


# In[239]:


Legal_accounting_design_research_and_advertising_services = Legal_accounting_design_research_and_advertising_services.replace(5419, 
                                                    'Legal, accounting, design research and advertising services')
Legal_accounting_design_research_and_advertising_services = Legal_accounting_design_research_and_advertising_services.drop(
    '_EMPLOYMENT_', axis= 1)
Legal_accounting_design_research_and_advertising_services = Legal_accounting_design_research_and_advertising_services.drop(
'index', 1)
Legal_accounting_design_research_and_advertising_services


# In[240]:


Legal_accounting_design_research_and_advertising_services = Legal_accounting_design_research_and_advertising_services[
    (Legal_accounting_design_research_and_advertising_services.SYEAR != 2019)]
Legal_accounting_design_research_and_advertising_services.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Legal_accounting_design_research_and_advertising_services


# ## Getting  *Other retail trade(excluding cars and personal care)*  from  [442], [443],  [444],  [445], [446], [447], [448],  [451],   [452], [453] & [454]	
# 
# The new method was applied to obatin the **Other retail trade(excluding cars and personal care)**. **The eleven extracted dataframes' __EMPLOYMENT__ were added to get the accurate results without merge methods.**

# In[241]:


Furniture_and_home_furnishings_stores = data.loc[data['NAICS'].str.contains('442', na = False)].reset_index()
Furniture_and_home_furnishings_stores


# In[242]:


Electronics_and_appliance_stores = data.loc[data['NAICS'].str.contains('443', na = False)].reset_index()
Electronics_and_appliance_stores


# In[243]:


BMGESD = data.loc[data['NAICS'].str.contains('444', na = False)].reset_index()
BMGESD


# In[244]:


Food_and_beverage_stores = data.loc[data['NAICS'].str.contains('445', na = False)].reset_index()
Food_and_beverage_stores


# In[245]:


Health_and_personal_care_stores = data.loc[data['NAICS'].str.contains('446', na = False)].reset_index()
Health_and_personal_care_stores


# In[246]:


Gasoline_stations = data.loc[data['NAICS'].str.contains('447', na = False)].reset_index()
Gasoline_stations


# In[247]:


Clothing_and_clothing_accessories_stores = data.loc[data['NAICS'].str.contains('448', na = False)].reset_index()
Clothing_and_clothing_accessories_stores


# In[248]:


SGHBMS = data.loc[data['NAICS'].str.contains('451', na = False)].reset_index()
SGHBMS


# In[249]:


General_merchandise_stores = data.loc[data['NAICS'].str.contains('452', na = False)].reset_index()
General_merchandise_stores


# In[250]:


Miscellaneous_store_retailers = data.loc[data['NAICS'].str.contains('453', na = False)].reset_index()
Miscellaneous_store_retailers


# In[251]:


Non_store_retailers = data.loc[data['NAICS'].str.contains('454', na = False)].reset_index()
Non_store_retailers


# In[252]:


SGHBMS['EMPLOYMENT'] = Non_store_retailers['_EMPLOYMENT_'] + Miscellaneous_store_retailers['_EMPLOYMENT_'] + General_merchandise_stores['_EMPLOYMENT_'] + SGHBMS['_EMPLOYMENT_'] + Clothing_and_clothing_accessories_stores['_EMPLOYMENT_'] + Gasoline_stations['_EMPLOYMENT_'] + Health_and_personal_care_stores['_EMPLOYMENT_'] + Food_and_beverage_stores['_EMPLOYMENT_'] + BMGESD['_EMPLOYMENT_'] + Electronics_and_appliance_stores['_EMPLOYMENT_'] + Furniture_and_home_furnishings_stores['_EMPLOYMENT_']
Other_retail_trade = SGHBMS
Other_retail_trade


# In[253]:


Other_retail_trade = Other_retail_trade.replace('Sporting goods, hobby, book and music stores[451]', 
                                                    'Other retail trade(excluding cars and personal care)')
Other_retail_trade = Other_retail_trade.drop(['_EMPLOYMENT_', 'index'], axis= 1)
Other_retail_trade


# In[254]:


Other_retail_trade = Other_retail_trade[(Other_retail_trade.SYEAR != 2019)]
Other_retail_trade.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Other_retail_trade


# ## Getting  *Other manufacturing*  from [313], [314], [315], [316], [323], [324], [325], [326], [327], [334], [335], [337] & [339]

# In[255]:


Textile_mills = data.loc[data['NAICS'].str.contains('313', na = False)].reset_index()
Textile_mills


# In[256]:


Textile_product_mills = data.loc[data['NAICS'].str.contains('314', na = False)].reset_index()
Textile_product_mills


# In[257]:


Clothing_manufacturing = data.loc[data['NAICS'].str.contains('315', na = False)].reset_index()
Clothing_manufacturing


# In[258]:


Leather_and_allied_product_manufacturing = data.loc[data['NAICS'].str.contains('316', na = False)].reset_index()
Leather_and_allied_product_manufacturing


# In[259]:


Printing_and_related_support_activities = data.loc[data['NAICS'].str.contains('323', na = False)].reset_index()
Printing_and_related_support_activities


# In[260]:


Petroleum_and_coal_product_manufacturing = data.loc[data['NAICS'].str.contains('324', na = False)].reset_index()
Petroleum_and_coal_product_manufacturing


# In[261]:


Chemical_manufacturing = data.loc[data['NAICS'].str.contains('325', na = False)].reset_index()
Chemical_manufacturing


# In[262]:


Plastics_and_rubber_products_manufacturing = data.loc[data['NAICS'].str.contains('326', na = False)].reset_index()
Plastics_and_rubber_products_manufacturing


# In[263]:


Non_metallic_mineral_product_manufacturing = data.loc[data['NAICS'].str.contains('327', na = False)].reset_index()
Non_metallic_mineral_product_manufacturing


# In[264]:


Computer_and_electronic_product_manufacturing = data.loc[data['NAICS'].str.contains('334', na = False)].reset_index()
Computer_and_electronic_product_manufacturing


# In[265]:


EAC = data.loc[data['NAICS'].str.contains('335', na = False)].reset_index()
EAC


# In[266]:


Furniture_and_related_product_manufacturing = data.loc[data['NAICS'].str.contains('337', na = False)].reset_index()
Furniture_and_related_product_manufacturing


# In[267]:


Miscellaneous_manufacturing = data.loc[data['NAICS'].str.contains('339', na = False)].reset_index()
Miscellaneous_manufacturing


# In[268]:


EAC['EMPLOYMENT'] = Miscellaneous_manufacturing['_EMPLOYMENT_'] + Furniture_and_related_product_manufacturing['_EMPLOYMENT_'] + EAC['_EMPLOYMENT_'] + Computer_and_electronic_product_manufacturing['_EMPLOYMENT_'] + Non_metallic_mineral_product_manufacturing['_EMPLOYMENT_'] + Plastics_and_rubber_products_manufacturing['_EMPLOYMENT_'] + Textile_product_mills['_EMPLOYMENT_'] + Chemical_manufacturing['_EMPLOYMENT_'] + Petroleum_and_coal_product_manufacturing['_EMPLOYMENT_'] + Clothing_manufacturing['_EMPLOYMENT_'] + Printing_and_related_support_activities['_EMPLOYMENT_'] + Leather_and_allied_product_manufacturing['_EMPLOYMENT_'] + Textile_mills['_EMPLOYMENT_']
Other_manufacturing = EAC
Other_manufacturing


# In[269]:


Other_manufacturing = Other_manufacturing.replace('Electrical equipment, appliance and component manufacturing[335]', 
                                                    'Other manufacturing')
Other_manufacturing = Other_manufacturing.drop(['_EMPLOYMENT_', 'index'], axis= 1)
Other_manufacturing


# In[270]:


Other_manufacturing = Other_manufacturing[(Other_manufacturing.SYEAR != 2019)]
Other_manufacturing.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Other_manufacturing


# ## Extracting the single NAICS number industries

# In[271]:


Fishing_hunting_and_trapping = data.loc[data['NAICS'].str.contains('114', na = False)]
Fishing_hunting_and_trapping = Fishing_hunting_and_trapping[(Fishing_hunting_and_trapping.SYEAR != 2019)]
Fishing_hunting_and_trapping.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Fishing_hunting_and_trapping


# In[272]:


Forestry_and_logging = data.loc[data['NAICS'].str.contains('113', na = False)]
Forestry_and_logging = Forestry_and_logging[(Forestry_and_logging.SYEAR != 2019)]
Forestry_and_logging.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Forestry_and_logging


# In[273]:


SPAF = data.loc[data['NAICS'].str.contains('115', na = False)]
SPAF = SPAF[(SPAF.SYEAR != 2019)]
SPAF.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
SPAF


# In[274]:


Oil_and_gas_extraction = data.loc[data['NAICS'].str.contains('211', na = False)]
Oil_and_gas_extraction = Oil_and_gas_extraction[(Oil_and_gas_extraction.SYEAR != 2019)]
Oil_and_gas_extraction.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Oil_and_gas_extraction


# In[275]:


SAMOG = data.loc[data['NAICS'].str.contains('213', na = False)]
SAMOG = SAMOG[(SAMOG.SYEAR != 2019)]
SAMOG.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
SAMOG


# In[276]:


Mining_and_quarrying  = data.loc[data['NAICS'].str.contains('212', na = False)]
Mining_and_quarrying = Mining_and_quarrying[(Mining_and_quarrying.SYEAR != 2019)]
Mining_and_quarrying.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Mining_and_quarrying


# In[277]:


Wood_product_manufacturing = data.loc[data['NAICS'].str.contains('321', na = False)]
Wood_product_manufacturing = Wood_product_manufacturing[(Wood_product_manufacturing.SYEAR != 2019)]
Wood_product_manufacturing.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Wood_product_manufacturing


# In[278]:


Paper_manufacturing = data.loc[data['NAICS'].str.contains('322', na = False)]
Paper_manufacturing = Paper_manufacturing[(Paper_manufacturing.SYEAR != 2019)]
Paper_manufacturing.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Paper_manufacturing


# In[279]:


Primary_metal_manufacturing = data.loc[data['NAICS'].str.contains('331', na = False)]
Primary_metal_manufacturing = Primary_metal_manufacturing[(Primary_metal_manufacturing.SYEAR != 2019)]
Primary_metal_manufacturing.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Primary_metal_manufacturing


# In[280]:


Fabricated_metal_product_manufacturing = data.loc[data['NAICS'].str.contains('332', na = False)]
Fabricated_metal_product_manufacturing = Fabricated_metal_product_manufacturing[(Fabricated_metal_product_manufacturing.SYEAR != 2019)]
Fabricated_metal_product_manufacturing.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Fabricated_metal_product_manufacturing


# In[281]:


Machinery_manufacturing = data.loc[data['NAICS'].str.contains('333', na = False)]
Machinery_manufacturing = Machinery_manufacturing[(Machinery_manufacturing.SYEAR != 2019)]
Machinery_manufacturing.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Machinery_manufacturing


# In[282]:


Motor_vehicle_and_parts_dealers = data.loc[data['NAICS'].str.contains('441', na = False)]
Motor_vehicle_and_parts_dealers = Motor_vehicle_and_parts_dealers[(Motor_vehicle_and_parts_dealers.SYEAR != 2019)]
Motor_vehicle_and_parts_dealers.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Motor_vehicle_and_parts_dealers


# In[283]:


Health_and_personal_care_stores = data.loc[data['NAICS'].str.contains('446', na = False)]
Health_and_personal_care_stores = Health_and_personal_care_stores[(Health_and_personal_care_stores.SYEAR != 2019)]
Health_and_personal_care_stores.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Health_and_personal_care_stores


# In[284]:


Air_transportation = data.loc[data['NAICS'].str.contains('481', na = False)]
Air_transportation = Air_transportation[(Air_transportation.SYEAR != 2019)]
Air_transportation.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Air_transportation


# In[285]:


Rail_transportation = data.loc[data['NAICS'].str.contains('482', na = False)]
Rail_transportation = Rail_transportation[(Rail_transportation.SYEAR != 2019)]
Rail_transportation.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Rail_transportation


# In[286]:


Water_transportation = data.loc[data['NAICS'].str.contains('483', na = False)]
Water_transportation = Water_transportation[(Water_transportation.SYEAR != 2019)]
Water_transportation.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Water_transportation


# In[287]:


Truck_transportation = data.loc[data['NAICS'].str.contains('484', na = False)]
Truck_transportation = Truck_transportation[(Truck_transportation.SYEAR != 2019)]
Truck_transportation.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Truck_transportation


# In[288]:


Support_activities_for_transportation = data.loc[data['NAICS'].str.contains('488', na = False)]
Support_activities_for_transportation = Support_activities_for_transportation[(Support_activities_for_transportation.SYEAR != 2019)]
Support_activities_for_transportation.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Support_activities_for_transportation


# In[289]:


Warehousing_and_storage = data.loc[data['NAICS'].str.contains('493', na = False)]
Warehousing_and_storage = Warehousing_and_storage[(Warehousing_and_storage.SYEAR != 2019)]
Warehousing_and_storage.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Warehousing_and_storage


# In[290]:


Insurance_carriers_and_related_activities = data.loc[data['NAICS'].str.contains('524', na = False)]
Insurance_carriers_and_related_activities = Insurance_carriers_and_related_activities[(Insurance_carriers_and_related_activities.SYEAR != 2019)]
Insurance_carriers_and_related_activities.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Insurance_carriers_and_related_activities


# In[291]:


Ambulatory_health_care_services = data.loc[data['NAICS'].str.contains('621', na = False)]
Ambulatory_health_care_services = Ambulatory_health_care_services[(Ambulatory_health_care_services.SYEAR != 2019)]
Ambulatory_health_care_services.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Ambulatory_health_care_services


# In[292]:


Hospitals = data.loc[data['NAICS'].str.contains('622', na = False)]
Hospitals = Hospitals[(Hospitals.SYEAR != 2019)]
Hospitals.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Hospitals


# In[293]:


Truck_transportation = data.loc[data['NAICS'].str.contains('623', na = False)]
Truck_transportation = Truck_transportation[(Truck_transportation.SYEAR != 2019)]
Truck_transportation.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Truck_transportation


# In[294]:


Social_assistance = data.loc[data['NAICS'].str.contains('624', na = False)]
Social_assistance = Social_assistance[(Social_assistance.SYEAR != 2019)]
Social_assistance.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Social_assistance


# In[295]:


Publishing_industries = data.loc[data['NAICS'].str.contains('511', na = False)]
Publishing_industries = Publishing_industries[(Publishing_industries.SYEAR != 2019)]
Publishing_industries.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Publishing_industries


# In[296]:


MPSRI = data.loc[data['NAICS'].str.contains('512', na = False)]
MPSRI = MPSRI[(MPSRI.SYEAR != 2019)]
MPSRI.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
MPSRI


# In[297]:


Telecommunications = data.loc[data['NAICS'].str.contains('517', na = False)]
Telecommunications = Telecommunications[(Telecommunications.SYEAR != 2019)]
Telecommunications.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Telecommunications


# In[298]:


PSSR = data.loc[data['NAICS'].str.contains('711', na = False)]
PSSR = PSSR[(PSSR.SYEAR != 2019)]
PSSR.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
PSSR


# In[299]:


AGRI = data.loc[data['NAICS'].str.contains('713', na = False)]
AGRI = AGRI[(AGRI.SYEAR != 2019)]
AGRI.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
AGRI


# In[300]:


Heritage_institutions = data.loc[data['NAICS'].str.contains('712', na = False)]
Heritage_institutions = Heritage_institutions[(Heritage_institutions.SYEAR != 2019)]
Heritage_institutions.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Heritage_institutions


# In[301]:


Food_services_and_drinking_places = data.loc[data['NAICS'].str.contains('722', na = False)]
Food_services_and_drinking_places = Food_services_and_drinking_places[(Food_services_and_drinking_places.SYEAR != 2019)]
Food_services_and_drinking_places.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Food_services_and_drinking_places


# In[302]:


Accommodation_services = data.loc[data['NAICS'].str.contains('721', na = False)]
Accommodation_services = Accommodation_services[(Accommodation_services.SYEAR != 2019)]
Accommodation_services.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Accommodation_services


# In[303]:


Federal_government_public_administration = data.loc[data['NAICS'].str.contains('911', na = False)]
Federal_government_public_administration = Federal_government_public_administration[(Federal_government_public_administration.SYEAR != 2019)]
Federal_government_public_administration.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Federal_government_public_administration


# In[304]:


PTPA = data.loc[data['NAICS'].str.contains('912', na = False)]
PTPA = PTPA[(PTPA.SYEAR != 2019)]
PTPA.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
PTPA


# In[305]:


Utilities_22 = data.loc[data['NAICS'].str.contains('Utilities', na = False)]
Utilities_22 = Utilities_22[:276]
Utilities_22 = Utilities_22[(Utilities_22.SYEAR != 2019)]
Utilities_22.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Utilities_22


# In[306]:


Construction = data.loc[data['NAICS'].str.contains('23', na = False)]
Construction = Construction[:276]
Construction = Construction[(Construction.SYEAR != 2019)]
Construction.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Construction


# In[307]:


Wholesale_trade = data.loc[data['NAICS'].str.contains('41', na = False)]
Wholesale_trade = Wholesale_trade[:276]
Wholesale_trade = Wholesale_trade[(Wholesale_trade.SYEAR != 2019)]
Wholesale_trade.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Wholesale_trade


# In[308]:


Real_estate_rental_and_leasing = data.loc[data['NAICS'].str.contains('53', na = False)]
Real_estate_rental_and_leasing = Real_estate_rental_and_leasing[:276]
Real_estate_rental_and_leasing = Real_estate_rental_and_leasing[(Real_estate_rental_and_leasing.SYEAR != 2019)]
Real_estate_rental_and_leasing.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Real_estate_rental_and_leasing


# In[309]:


Other_services = data.loc[data['NAICS'].str.contains('81', na = False)]
Other_services = Other_services[:276]
Other_services = Other_services[(Other_services.SYEAR != 2019)]
Other_services.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Other_services


# In[310]:


Ship_and_boat_building = data.loc[data['NAICS'] == 3366]
Ship_and_boat_building = Ship_and_boat_building.replace(3366, 'Ship and boat building')
Ship_and_boat_building = Ship_and_boat_building[(Ship_and_boat_building.SYEAR != 2019)]
Ship_and_boat_building.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Ship_and_boat_building


# In[311]:


AERS = data.loc[data['NAICS'] == 5413]
AERS = AERS.replace(5413, 'Architectural, engineering and related services')
AERS = AERS[(AERS.SYEAR != 2019)]
AERS.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
AERS


# In[312]:


CSDRS = data.loc[data['NAICS'] == 5415]
CSDRS = CSDRS.replace(5415, 'Computer systems design and related services')
CSDRS = CSDRS[(CSDRS.SYEAR != 2019)]
CSDRS.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
CSDRS


# In[313]:


MSTCS = data.loc[data['NAICS'] == 5416]
MSTCS = MSTCS.replace(5416, 'Management, scientific and technical consulting services')
MSTCS = MSTCS[(MSTCS.SYEAR != 2019)]
MSTCS.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
MSTCS


# In[314]:


Elementary_and_secondary_schools = data.loc[data['NAICS'] == 6111]
Elementary_and_secondary_schools = Elementary_and_secondary_schools.replace(6111, 'Elementary and secondary schools')
Elementary_and_secondary_schools = Elementary_and_secondary_schools[(Elementary_and_secondary_schools.SYEAR != 2019)]
Elementary_and_secondary_schools.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Elementary_and_secondary_schools


# In[315]:


CCC = data.loc[data['NAICS'] == 6112]
CCC = CCC.replace(6112, 'Community colleges and C.E.G.E.P.s')
CCC = CCC[(CCC.SYEAR != 2019)]
CCC.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
CCC


# In[316]:


Universities = data.loc[data['NAICS'] == 6113]
Universities = Universities.replace(6113, 'Universities')
Universities = Universities[(Universities.SYEAR != 2019)]
Universities.columns = ['SYEAR', 'SMTH', 'LMO_Detailed_Industry', 'Employment']
Universities


# In[317]:


data_output_mixed = pd.concat([Other_manufacturing, Other_retail_trade, Legal_accounting_design_research_and_advertising_services, 
Transportation_equipment_manufacturing_excluding_shipbuilding, Private_and_trades_education, Finance,
Transit_sightseeing_and_pipeline_transportation, Broadcasting_data_processing_and_information,
Local_and_Indigenous_public_administration, Business_building_and_other_support_services, 
Food_beverage_and_tobacco_manufacturing, Farms, Postal_service_couriers_and_messengers])


data_output_single = pd.concat([Federal_government_public_administration, Food_services_and_drinking_places, Heritage_institutions,
                               AGRI, PSSR, Telecommunications, MPSRI, Publishing_industries, Social_assistance, 
                               Truck_transportation, Hospitals, Ambulatory_health_care_services,
                               Insurance_carriers_and_related_activities, Warehousing_and_storage,  
                               Support_activities_for_transportation, Truck_transportation, Water_transportation, 
                               Rail_transportation, Air_transportation, Health_and_personal_care_stores, 
                               Motor_vehicle_and_parts_dealers, Machinery_manufacturing, Fabricated_metal_product_manufacturing,
                               Primary_metal_manufacturing, Paper_manufacturing, Wood_product_manufacturing, 
                               Mining_and_quarrying, SAMOG, Oil_and_gas_extraction, SPAF, Forestry_and_logging, 
                               Fishing_hunting_and_trapping, Universities, CCC,  Elementary_and_secondary_schools, MSTCS, CSDRS,
                               AERS, Ship_and_boat_building, Other_services, Real_estate_rental_and_leasing, Wholesale_trade, 
                               Construction, Utilities_22, PTPA, Accommodation_services])

data_output = pd.concat([data_output_mixed, data_output_single])
data_output = data_output.sort_values(['SYEAR', 'SMTH', 'LMO_Detailed_Industry'])
data_output


# # EDA

# ## 1. How employment in Construction evolved overtime?

# In[318]:


plt.figure(figsize=(18,10))
plt.plot(Construction['SYEAR'], Construction['Employment'], color = 'r',marker='o', linewidth=1)

plt.xlabel('Year', fontsize=18)
plt.xticks(rotation=40, fontsize = 14)
plt.ylabel('Construction', fontsize=18)
plt.yticks(fontsize = 14)
plt.title('Evolvement of employment in Construction overtime', fontsize=22)
red = patches.Patch(color='red', label='Construction')
plt.legend(handles=[red], prop = {'size':15})


# In[319]:


plt.figure(figsize=(18,10))
plt.bar(Construction['SYEAR'], Construction['Employment'], color = 'r')

plt.xlabel('Year', fontsize=18)
plt.xticks(rotation=40, fontsize = 14)
plt.ylabel('Construction', fontsize=18)
plt.yticks(fontsize = 14)
plt.title('Evolvement of employment in Construction overtime', fontsize=22)
red = patches.Patch(color='red', label='Construction')
plt.legend(handles=[red], prop = {'size':15})


# ## 2. How employment in Construction evolved over time, compared to the total employment across all industries?

# In[320]:


data_output.loc[data_output['LMO_Detailed_Industry'] == 'Construction [23]'].groupby('SYEAR').sum()['Employment']
data_output.loc[data_output['LMO_Detailed_Industry'] != 'Construction [23]'].groupby('SYEAR').sum()['Employment']


# In[321]:


plt.figure(figsize=(14,10))
x_industries = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', 
                '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
x_indexes = np.arange(len(x_industries))
width = 0.20


y_construction = [1489750, 1424750, 1363500, 1345750, 1347250, 1401500, 1412000, 1705000, 1989000, 2097000, 2301000, 2616750, 
                 2444750, 2380750, 2365750, 2383250, 2453000, 2406500, 2417750, 2536000, 2743250, 2860750]
plt.bar(x_indexes, y_construction, width = width, label = 'Construction')


y_other = [20344750, 20454250, 20863000, 22305750, 22218750, 22602000, 22585750, 22602000, 23088750, 23592500, 24161500, 
           24339750, 23966000, 24443500, 24485750, 24895000, 24865750, 25087750, 25415500, 26156250, 27012500, 27220250]
plt.bar(x_indexes - width, y_other, width = width ,label = 'All other companies')


plt.legend()
plt.xlabel('Years of Construction evolvement', fontsize=18)
plt.xticks(ticks = x_indexes, labels = x_industries, fontsize = 12, rotation = 60)
plt.ylabel('Evolvement of Construction employment over time', fontsize=18)
plt.yticks(fontsize = 14)
plt.title('Evolvement of Construction compared to All other industries', fontsize=22)


# ## 3. How employment in Other manufacturing evolved over time, compared to the employment across Other retail trade in terms of month and years?

# In[322]:


manufacturing_series = data_output_mixed.loc[data_output_mixed['LMO_Detailed_Industry'] == 'Other manufacturing'].groupby('SYEAR').sum()['Employment'].to_frame()
retail_series = data_output_mixed.loc[data_output_mixed['LMO_Detailed_Industry'] == 'Other retail trade(excluding cars and personal care)'].groupby('SYEAR').sum()['Employment'].to_frame()
years = pd.Series(x_industries).to_frame()


# In[323]:


plt.figure(figsize=(18,10))
plt.plot(years[0], manufacturing_series['Employment'], color = 'r',marker='o', linewidth=1)
plt.plot(years[0], retail_series['Employment'], color = 'b',marker='o', linewidth=1)

plt.xlabel('Year', fontsize=22)
plt.xticks(rotation=40, fontsize = 14)
plt.ylabel('Other manufacturing  VS  Other retail', fontsize=22)
plt.yticks(fontsize = 14)
plt.title('Annual evolvement of Other manufacturing  VS  Other retail', fontsize=22)
red = patches.Patch(color='red', label='Other manufacturing')
blue = patches.Patch(color='blue', label='Other retail trade(excluding cars and personal care)')
plt.legend(handles=[red, blue], prop = {'size':15})


# In[324]:


manufacturing_list = data_output_mixed.loc[data_output_mixed['LMO_Detailed_Industry'] == 'Other manufacturing'].groupby('SMTH').sum()['Employment'].to_list()
retail_list = data_output_mixed.loc[data_output_mixed['LMO_Detailed_Industry'] == 'Other retail trade(excluding cars and personal care)'].groupby('SMTH').sum()['Employment'].to_list()


# In[325]:


plt.figure(figsize=(14,10))
x_industries = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
x_indexes = np.arange(len(x_industries))
width = 0.20

plt.bar(x_indexes, manufacturing_list, width = width, label = 'Other manufacturing')
plt.bar(x_indexes - width, retail_list, width = width ,label = 'Other retail')

plt.legend()
plt.xlabel('Month', fontsize=20)
plt.xticks(ticks = x_indexes, labels = x_industries, fontsize = 12, rotation = 60)
plt.ylabel('Other manufacturing  VS  Other retail', fontsize=18)
plt.yticks(fontsize = 14)
plt.title('Monthly evolvement of Other manufacturing  VS  Other retail', fontsize=22)


# ## 4. What is the monthly distribution of employment across all industries?

# In[326]:


plt.figure(figsize=(16,8))
plt.hist(data_output['Employment'], bins =40)
#plt.plot(years[0], retail_series['Employment'], color = 'b',marker='o', linewidth=1)

plt.xlabel('Employment number', fontsize=22)
plt.xticks(rotation=40, fontsize = 14)
#plt.ylabel('Other manufacturing  VS  Other retail', fontsize=22)
plt.yticks(fontsize = 0.1)
plt.title('Monthly distribution of employment across all industries', fontsize=22)
#red = patches.Patch(color='blue', label='Other manufacturing')
blue = patches.Patch(color='blue', label='Employment distribution across all industries')
plt.legend(handles=[blue], prop = {'size':15})


# ## 5. What is the monthly distribution of employment of mulitple NAICS numbers industries VS single NAICS number industries?

# ### mulitple NAICS numbers industries

# In[327]:


plt.figure(figsize=(16,8))
plt.hist(data_output_mixed['Employment'], bins = 25, color = 'r')
#plt.plot(years[0], retail_series['Employment'], color = 'b',marker='o', linewidth=1)

plt.xlabel('Employment number', fontsize=22)
plt.xticks(rotation=40, fontsize = 14)
#plt.ylabel('Other manufacturing  VS  Other retail', fontsize=22)
plt.yticks(fontsize = 0.1)
plt.title('Monthly distribution of employment across mulitple NAICS numbers industries', fontsize=22)
#red = patches.Patch(color='blue', label='Other manufacturing')
blue = patches.Patch(color='red', label='Employment distribution across mulitple NAICS numbers industries')
plt.legend(handles=[blue], prop = {'size':15})


# ### single NAICS number industries

# In[328]:


plt.figure(figsize=(16,8))
plt.hist(data_output_single['Employment'], bins = 25, color = 'k')
#plt.plot(years[0], retail_series['Employment'], color = 'b',marker='o', linewidth=1)

plt.xlabel('Employment number', fontsize=22)
plt.xticks(rotation=40, fontsize = 14)
#plt.ylabel('Other manufacturing  VS  Other retail', fontsize=22)
plt.yticks(fontsize = 0.1)
plt.title('Monthly distribution of employment across mulitple NAICS numbers industries', fontsize=22)
#red = patches.Patch(color='blue', label='Other manufacturing')
blue = patches.Patch(color='black', label='Employment distribution across mulitple NAICS numbers industries')
plt.legend(handles=[blue], prop = {'size':15})


# In[ ]:




