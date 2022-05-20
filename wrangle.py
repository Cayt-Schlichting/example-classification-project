import pandas as pd
import numpy as np
import os
from env import host, username, password
from sklearn.model_selection import train_test_split

#### DATA ACQUISITION ####

#Function to create database url.  Requires local env.py with host, username and password. 
# No function help text provided as we don't want the user to access it and display their password on the screen
def get_db_url(db_name,user=username,password=password,host=host):
    url = f'mysql+pymysql://{user}:{password}@{host}/{db_name}'
    return url

#Create dataframe of accessible datasets.  
# DF contains filename, database name and SQL query.  
ind = ['titanic','iris','telco']
ds = pd.DataFrame(index=ind,columns=['filename','db_name','sql'])
ds.loc['titanic'] = ['titanic.csv','titanic_db',"""SELECT * FROM passengers;"""]
ds.loc['iris'] = ['iris.csv','iris_db',"""SELECT * FROM measurements JOIN species USING(species_id);"""]
telco_sql = """
SELECT * FROM customers
JOIN internet_service_types USING(internet_service_type_id)
JOIN contract_types USING(contract_type_id)
JOIN payment_types USING(payment_type_id)
JOIN customer_signups USING(customer_id);
"""
ds.loc['telco'] = ['telco.csv','telco_churn',telco_sql]

#Function to get new data from Codeup server
def getNewData(ds_name,ds=ds):
    """
    Retrieves dataset from Codeup DB and stores a local csv file

    Returns: Pandas dataframe
    Inputs:
      (R) - ds_name: The name of the dataset you want to access.
      (O) -      ds: A Pandas dataframe of the following format:
                    index: corresponds to the ds_name provided
                    columns: 
                    'filename': filename you want to store the data at and retrieve it from
                     'db_name': the name of the database in on the codeup server
                         'sql': contains SQL query to execute

    Supported datasets: 
      'titanic'
      'iris'
      'telco'
    """
    #pull out 
    db_name = ds.loc[ds_name,'db_name']
    sql = ds.loc[ds_name,'sql']
    filename = ds.loc[ds_name,'filename']
    
    df = pd.read_sql(sql,get_db_url(db_name))
    #write to disk - writes index as col 0:
    df.to_csv(filename)
    return 

#Function to get data from local file or Codeup server 
def getData(ds_name,ds=ds):
    """
    Retrieves dataset for working directory or Codeup DB. Stores a local copy if one did not exist

    Returns: Pandas dataframe
    Inputs:
      (R) - ds_name: The name of the dataset you want to access.
      (O) -      ds: A Pandas dataframe of the following format:
                    index: corresponds to the ds_name provided
                    columns: 
                    'filename': filename you want to store the data at and retrieve it from
                     'db_name': the name of the database in on the codeup server
                         'sql': contains SQL query to execute

    Supported datasets: 
      'titanic'
      'iris'
      'telco'
    """
    filename = ds.loc[ds_name,'filename']

    if os.path.isfile(filename): #check if file exists in WD
        #grab data, set first column as index
        return pd.read_csv(filename,index_col=[0])
    else: #Get data from SQL db
        df = getNewData(ds_name)
    return df
##########################
##########################


#### DATA PREPARATION ####

#### DATA SPLITTING ####
def splitData(df,target,**kwargs):
    """
    Splits data into three dataframes

    Returns: 3 dataframes in order of train, test, validate
    Inputs:
      (R) df: Pandas dataframe to be split
      (R) target: Column name of the target variable - used to stratifying
      (O -kw) val_ratio: Proportion of the whole dataset wanted for the validation subset (b/w 0 and 1). Default .2 (20%)
      (O -kw) test_ratio: Proportion of the whole dataset wanted for the test subset (b/w 0 and 1). Default .1 (10%)

    """
    #test and validation percentages of WHOLE dataset -
    val_per = kwargs.get('val_ratio',.2)
    test_per = kwargs.get('test_ratio',.1)

    #Calculate percentage we need of test/train subset
    tt_per = test_per/(1-val_per)

    #returns train then test, so test_size is the second set it returns
    tt, validate = train_test_split(df, test_size=val_per,random_state=88,stratify=df[target])
    #now split tt in train and test want 70/10 so test_size = 1/8 or .125
    train, test = train_test_split(tt, test_size=tt_per, random_state=88,stratify=tt[target])
    
    return train, test, validate

#### TELCO PREP ####
def prep_telco(df,**kwargs):
  """
  Cleans and prepares the telco data for analysis.  Assumes default SQL query was used.

  Returns: 3 dataframes in order of train, test, validate
  Inputs:
    (R) df: Pandas dataframe to be cleaned and split for analysis
    (O -kw) val_ratio: Proportion of the whole dataset wanted for the validation subset (b/w 0 and 1). Default .2 (20%)
    (O -kw) test_ratio: Proportion of the whole dataset wanted for the test subset (b/w 0 and 1). Default .1 (10%)

  """
  #HANDLE total_charge row: 
  #grab the indices with null values
  drp_ind = df[df.total_charges.str.strip() == ''].index
  #drop those indices
  df.drop(index=drp_ind,inplace=True)
  #Convert the column to float
  df.total_charges = df.total_charges.astype(float)

  #DROP unnecessary columns
  drp_col = ['payment_type_id','internet_service_type_id','contract_type_id','customer_id','signup_date']
  df.drop(columns = drp_col,inplace=True)
  #MAP subset of variables that are yes/no
  #phone_service, paperless_billing, partner, dependents, churn
  df['has_phone'] = df.phone_service.map({'Yes': 1, 'No': 0})
  df['is_paperless'] = df.paperless_billing.map({'Yes': 1, 'No': 0})
  df['has_dependents'] = df.partner.map({'Yes': 1, 'No': 0})
  df['has_partner'] = df.dependents.map({'Yes': 1, 'No': 0})
  df['has_churned'] = df.churn.map({'Yes': 1, 'No': 0})   

  #ENCODE the other categorical columns
  enc_col = ['gender', 'multiple_lines', 'online_security', 'online_backup', 'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies','payment_type','contract_type','internet_service_type']  
  d_df = pd.get_dummies(df[enc_col],drop_first=True)
  #concate encoded df to rest of df
  df = pd.concat([df,d_df],axis=1)

  #Now split the data:
  target='churn'
  train, test, validate = splitData(df,target,**kwargs)

  return train, test, validate


##########################
##########################