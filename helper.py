import numpy as np

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------MEDAL TALLY SECTION FUNCTIONS------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------Function to get Country Year List---------------------------------------------
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['Region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


#-------------------------- Function to get medal tally depending on Year and Country-----------------------------------
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['Region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['Region'] == country)]

    if flag == 1:  # case when country is given and year is overall....then display data for every year of olympics
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['Total Medals'] = x['Gold'] + x['Silver'] + x['Bronze']
    #converting to integer value
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total Medals'] = x['Total Medals'].astype('int')
    return x


#-------------------------------Function to get Medal Tally (Not used)--------------------------------------------------

def medal_tally(df):
    # below code will basically remove data of players of same team (as they will have same medal collectively -> only 1 medal for the country) to display medals achieved by different countries.
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])
    # checking total medals : this line shows total medal count for each country (grouping by region will show contry name)
    medal_tally = medal_tally.groupby('Region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    # creating a column to display total medals
    medal_tally['Total Medals'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

#NOTE: THERE IS VARIATION IN DATA OF MEDALS FOR SOME COUNTRIES: Because of some exceptions as data is old and some changes were implemented regrading Obsolete nations, Name Change Notes, Participation Notes.
#Exception: Like Germany was earlier split in 3 regions.... so it's combined data of medals will be more now.
#Similarly russia had two regions in olympics at that tiime



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------OVERALL ANALYSIS SECTION FUNCTIONS--------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ----------Line Chart for Participating Nations Over Time + No. Of Events Over Time-------------------
def data_over_time(df, col):
    # removing duplicate rows for Year and col
    nations_over_time = df.drop_duplicates(['Year', col ])['Year'].value_counts().reset_index()
    #renaming columns
    nations_over_time.rename(columns={'count': 'Participating Nations', 'Year': 'Edition'} ,inplace= True) #inplace=True loads the chart in same place
    return nations_over_time

def events_over_time(df, col):
    # removing duplicate rows for Year and col
    event_over_time = df.drop_duplicates(['Year', col ])['Year'].value_counts().reset_index()
    #renaming columns
    event_over_time.rename(columns={'count': 'Total Events', 'Year': 'Edition'} ,inplace= True) #inplace=True loads the chart in same place
    return event_over_time

def athletes_over_time(df):
    athlete_over_time = df.drop_duplicates(['Year', 'Name' ])['Year'].value_counts().reset_index()
    athlete_over_time.rename(columns={'count': 'Participating Athletes', 'Year': 'Edition'} ,inplace= True) #inplace=True loads the chart in same place
    return athlete_over_time


#--------------------------Function: Most successful atheles in particular sport----------------------------------------
# --------------Function to filter top athletes based on selected sport
def get_top_athletes(selected_sport, df):
    if selected_sport == 'Overall':
        top_athletes = df.groupby('Name').agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
        top_athletes['Total Medals'] = top_athletes['Gold'] + top_athletes['Silver'] + top_athletes['Bronze']
    else:
        filtered_df = df[df['Sport'] == selected_sport]
        top_athletes = filtered_df.groupby('Name').agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
        top_athletes['Total Medals'] = top_athletes['Gold'] + top_athletes['Silver'] + top_athletes['Bronze']
    top_athletes = top_athletes.sort_values(by='Total Medals', ascending=False).head(15)
    return top_athletes


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------COUNTRY WISE ANALYSIS SECTION FUNCTIONS--------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------Function: Line Chart for Year Wise country medal tally----------------------------------------
def yearwise_medal_tally(df, country):
    # Remove those rows from dataframe where medal is nan
    temp_df = df.dropna(subset=['Medal'])
    # for team sports ..keep a single element
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['Region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

#--------------------------Function: telling in a particular sport  a particular country has won how many medals--------
def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['Region'] == country]

    # obtaining a pivot table of data then will present it through heatmap
    pt= new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

#--------------------------Function: Top 10 atheletes of the selected country country ------------------------------------
    
def top_athletes_countrywise(selected_country, df):
    filtered_df = df[df['Region'] == selected_country]
    top_athletes = filtered_df.groupby('Name').agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
    top_athletes['Total Medals'] = top_athletes['Gold'] + top_athletes['Silver'] + top_athletes['Bronze']
    top_athletes = top_athletes.sort_values(by='Total Medals', ascending=False).head(10)
    return top_athletes



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------ATHLETE WISE ANALYSIS SECTION FUNCTIONS--------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----Function: Height VS WEIGHT Graph for particular sport: 1. Height vs weight of all athlete   2. All medal holders  3. Gender of Athlete

def weight_vs_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'Region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport!= 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

#-----------------------Function ->Men VS Women Participation in Olympics over the years--------------------------------
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'Region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final



