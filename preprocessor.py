import pandas as pd

#this function is just doing pre processing in data:
# 0. Removing Winter Olympic Data
# 1. Adding region column to athelete file
# 2. Removing duplicates from file
# 3. Adding medals columns
def preprocess( df, region_df):
    #filtering the data only for Summer Olympics
    df = df[df['Season']== 'Summer']
    #merge with region_df for region column in main file
    df = df.merge(region_df, on='NOC', how='left')
    #removing duplicates
    df.drop_duplicates(inplace=True)
    #one hot encoding medals -> basically adding rows of gold silver and bronze medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df