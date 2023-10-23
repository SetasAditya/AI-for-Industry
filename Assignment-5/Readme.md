- Our dataset features consists of three datatypes
     1. float
     2. integer
     3. object
- All are numerical features.

- Checking missing values by below methods:

     1. df.isnull().sum()
        - It returns null values for each column
          
     2. isnull().any()
        - It returns True if column have NULL Values
        - It returns False if column don't have NULL Values
          
     3. Percentage of Missing values

split  data into training and testing sets of 70:30 ratio
30% of test size selected
random_state is random seed

Initially Random Forest Regressor is used. We got a test score of 0.72.


Then XGBoost is used which led to better result of 0.78