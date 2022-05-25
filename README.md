### Project Summary

**Project Goal:** The goal of this project is to identify key drivers of customer churn in order to make recommendations on how to minimize future churn.  We aim to create a model to identify customers at a higher risk of churn and use this to take preventative action.
- Identify key drivers of churn
- Develop and test classification models for identifying customers at risk of churn

**Initial Hypothesis:**
- I expect churn to be primarily affected by:
  - **Cost:** Higher cost customers will be more likely to leave.
  - **Contract:** Customers are less likely to leave if they have a 1 or 2 year contract.
  - **Alternatives:** Internet customers without alternatives will be less likely to leave.  
    - NOTE: This dataset does not have the information to test this hypothesis, however the availability of alternatives is an important unknown to keep in mind.

**Initial Questions:**
- What features are the key drivers of churn?
- Which of these features can be used to predict churn?


**Project Plan:**
- Acquire data from servers
- Prepare Data:
  - Identify any duplicate or unusable columns
  - Identify any missing data
  - Identify any needed transformation
  - Takes steps to clean data 
- Combine all data acquisition and preparation steps into modules
- Explore data
  - subset non-encoded data for visualizations
  - create visual representations of all features in relation to target variable
  - perform hypothesis testing on subset of features that visually appear to be drivers of churn
  - conduct some multivariate analysis, primarily using features identified as drivers of churn
- Model
  - subset encoded data for modeling
  - Create baseline
  - Determine model methods to use and hyperparameters for each.  Minimum of 10 models.
  - Generate and fit these models on the train dataset
  - Run model statistics to identify top performing models (3-5)
  - Run this subset of modoels against the validate subset
  - Evaluate which model performed the best based off preferred model statistics and performance across subsets
- Generate Final Report
  - Include subset of details across project steps
  - run model over test dataset

Deliverables:
- wrangle.py module with preparation and acquisition functions
  - wrangle_notebook.ipynb contains steps and notes on data acquisition and preparation decisions
- eda.ipynb
  - Contains exploratory analysis of the data including visualizations and hypothesis testing
- modeling.ipynb
  - Contains full modeling work, with notes on parameter choices and model evaluation
- Final_Report.ipynb
  - Contains curtailed version of project in presentable format.  
- predictions.csv
  - Contains best model's predictions and probability on test subset

**Reproducing the project:**
- User will need an env.py file with the the following variables: 'host', 'user' (username), and 'password'
- Data preparation assumes explicit list of columns and database tables. Changes to the underlying database may require updated data cleaning
- The additional files contain

**Data Dictionary:**

*This does not contain a list of the categorical columns after encoding*


|Column                    |Non-Null Count  |Dtype  |Description and Values|
|------                    |--------------  |-----  |:-----|
|gender                    |7043 non-null   |object |gender: ['Female' 'Male']|
|senior_citizen            |7043 non-null   |int64  |[0 1]|
|partner                   |7043 non-null   |object |['Yes' 'No']|
|dependents                |7043 non-null   |object |['Yes' 'No']|
|tenure                    |7043 non-null   |int64  |Months customer has been with Telco|
|phone_service             |7043 non-null   |object |['Yes' 'No']|
|multiple_lines            |7043 non-null   |object |If the customer has multiple phone lines: ['No' 'Yes' 'No phone service']|
|online_security           |7043 non-null   |object |['Yes' 'No' 'No internet service']|
|online_backup             |7043 non-null   |object |['Yes' 'No' 'No internet service']|
|device_protection         |7043 non-null   |object |['Yes' 'No' 'No internet service']|
|tech_support              |7043 non-null   |object |['Yes' 'No' 'No internet service']|
|streaming_tv              |7043 non-null   |object |['Yes' 'No' 'No internet service']|
|streaming_movies          |7043 non-null   |object |['Yes' 'No' 'No internet service']|
|paperless_billing         |7043 non-null   |object |Whether the customer uses paperless billing: ['Yes' 'No']|
|monthly_charges           |7043 non-null   |float64|Monthly charge of customer (dollars)|
|total_charges             |7043 non-null   |object |Total charges in customer lifetime (dollars)|
|churn                     |7043 non-null   |object |Whether the customer churned last month: ['Yes' 'No']|
|internet_service_type     |7043 non-null   |object |Internet service customer uses: ['DSL' 'Fiber optic' 'None']|
|contract_type             |7043 non-null   |object |Contract of customer: ['One year' 'Month-to-month' 'Two year']|
|payment_type              |7043 non-null   |object |Payment method customer uses: ['Mailed check' 'Electronic check' 'Credit card (automatic)' 'Bank transfer (automatic)']|
