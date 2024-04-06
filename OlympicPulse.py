# OlympicPulse | Harnessing Olympics Insights

#NOTE: Focused on Summer Olympics Only

import streamlit as st  #used for web application
import pandas as pd
import preprocessor, helper   #added our files
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

#----------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------wide page view for default-------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------------
def wide_space_default():
    st.set_page_config(layout="wide")

wide_space_default()

#----------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------User Menu-------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------
st.sidebar.image('olympic_logo.png')

st.sidebar.title('Summer Olympics Analysis')
user_menu = st.sidebar.radio(
    'Select an Option : ',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis' )
)

#This data will show all the record of players of olympics along with their medals: Preprocessed data
df = preprocessor.preprocess(df , region_df)
# st.dataframe(df)

#----------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------Medal Tally Section--------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------

#if Medal Tally is clicked then we display the medals_tally of every country
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally Options ")

    # -------------------------------------------Year and COuntry Dropdowns
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year: ", years)
    selected_country = st.sidebar.selectbox("Select Country: ", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal Tally ")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s Performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)


#----------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------Overall Analysis Section--------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['Region'].unique().shape[0]

    st.title("Top Statistics : Summer Olympics")
    col1, col2, col3 =  st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 =  st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

#--------------------------Line Chart-> Participating Nations Over Time-------------------------------------------------
    st.title("Overall Athlete Data")
    st.dataframe(df)

    st.title("Participating nations over the years")
    nations_over_time = helper.data_over_time(df, 'Region')
    #st.dataframe(nations_over_time)
    nations_over_time = nations_over_time.sort_values('Region')  # here region will show year and count will show no. of regions
 
    fig = px.line(nations_over_time, x="Region", y="count")
    
    st.plotly_chart(fig)

#--------------------------Line Chart-> No. of Events Over the Years----------------------------------------------------
    st.title("Events over the years")
    
    events_over_time = helper.data_over_time(df, 'Event')
    #st.dataframe(events_over_time)
    
    events_over_time = events_over_time.sort_values('Event')  #here event is for year
    fig = px.line(events_over_time, x="Event", y="count")
    st.plotly_chart(fig)

#--------------------------Line Chart-> No. of Athletes Over the Years--------------------------------------------------
    st.title("Number of athletes over the years")
    
    athlete_over_time = helper.athlete_over_time(df)
    
    st.dataframe(athlete_over_time)
    athlete_over_time = athlete_over_time.sort_values('')  #here event is for year
    
    
    fig = px.line(athlete_over_time, x="Edition", y="Participating Athletes")
    st.plotly_chart(fig)
#--------------------------HeatMap-> No. of Events of one sport---------------------------------------------------------
    st.title("Number of events in all sports over time")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax= sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

#--------------------------Table: Most successful atheles in particular sport-------------------------------------------
    st.title("Most successful athletes ")
    #sport list for select box
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport= st.selectbox("Select a Sport", sport_list)
    x= helper.most_successful(df, selected_sport)
    st.table(x)

#----------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------Country-wise Analysis Section---------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------

if user_menu == 'Country-wise Analysis':

#------------------------Line Chart -> Country-wise yearly medal tally--------------------------------------------------

    #user input for country
    st.sidebar.title('Country-wise Analysis')
    #creating a list for options in dropdown
    country_list = df['Region'].dropna().unique().tolist()   #dropna() used because we have nan values for Region also
    country_list.sort()

    selected_country= st.sidebar.selectbox('Select the country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    #code to give line chart
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + "'s Medal tally over the years")
    st.plotly_chart(fig)

#--------------------HeatMap -> telling in a particular sport  a particular country has won how many medals-------------

    pt = helper.country_event_heatmap(df, selected_country)
    st.title(selected_country + " excels in the following sports")

    # Check if the pivot table is empty
    if pt.empty:
        st.write("No data available for ", selected_country)
    else:
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)


#--------------------Top 10 atheletes of country based on sports--------------------------------------------------------
    st.title(selected_country + "'s top 10 atheletes")
    best10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(best10_df)


#----------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------Athlete-wise Analysis Section---------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------

if user_menu == 'Athlete-wise Analysis':

#----------------PDF(probability Distrubtion of athletes' age who have participate in Olympic)--------------------------

    athlete_df = df.drop_duplicates(subset=['Name', 'Region'])

    #PDF(probability Distrubtion  of age
    x1= athlete_df['Age'].dropna()
    #PDF for age distribution of gold medalists
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    #PDF for age distribution of silver medalists
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    #PDF for age distribution of bronze medalists
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4], ['Overall Age', 'Gold Medalish', 'Silver Medalist', 'Bronze Medalist'], show_hist= False, show_rug= False)

    fig.update_layout(autosize = False, width= 1100, height = 800)  #code to make width and height of graph bigger
    st.title('Distribution of Age')
    st.plotly_chart(fig)

#---------------- GRAPH Plot: Age distribution with resepct to every sport-----------------------------------------------------

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions',
                     'Handball', 'Weightlifting', 'Wrestling', 'Shooting', 'Boxing', 'Taekwondo',
                     'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball',
                     'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
#INTERPRETING THE GRAPH:
# NOTE: IN GRAPH, SHARP OR HIGH CURVES WILL SHOW THE AGE RANGE IN WHICH THAT PARTICULAR MEDAL WINNING RATE IS HIGH FOR A PARTICULAR SPORT
#MORE FLAT CURVE MEANS-> THAT SPORT CAN BE PLAYED AT ANY AGE...for example ART COMPETITIONS

    #Gold medalists-------------------------------------------------
    x1 = []
    name1 = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_medalists_age = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if not gold_medalists_age.empty:
            x1.append(gold_medalists_age)
            name1.append(sport)

    fig = ff.create_distplot(x1, name1, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1100, height=800)  # code to make width and height of graph bigger
    st.title('Distribution of Age w.r.t. Sports(Gold Medalists)')
    st.plotly_chart(fig)

    #Silver medalists--------------------------------------------------
    x2 = []
    name2 = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_medalists_age = temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna()
        if not gold_medalists_age.empty:
            x2.append(gold_medalists_age)
            name2.append(sport)

    fig = ff.create_distplot(x2, name2, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1100, height=800)  # code to make width and height of graph bigger
    st.title('Distribution of Age w.r.t. Sports(Silver Medalists)')
    st.plotly_chart(fig)

    #Bronze medalists---------------------------------------------------
    x3 = []
    name3 = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_medalists_age = temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna()
        if not gold_medalists_age.empty:
            x3.append(gold_medalists_age)
            name3.append(sport)

    fig = ff.create_distplot(x3, name3, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1100, height=800)  # code to make width and height of graph bigger
    st.title('Distribution of Age w.r.t. Sports(Bronze Medalists)')
    st.plotly_chart(fig)




#---------------- GRAPH Plot: For a particular sport: Height vs Weight--------------------------------------------------

#Height VS WEIGHT plot for particular sport: 1. Height vs weight of all athlete   2. All medal holder 3. Gender of Athlete

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height vs Weight')
    #selecting sport
    selected_sport = st.selectbox("Select a Sport", sport_list)

    temp_df = helper.weight_vs_height(df, selected_sport ) #function call
    fig, ax = plt.subplots()

    sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=100)

    st.pyplot(fig)


#-------------------------Men VS Women Participation in Olympics over the years-----------------------------------------

    final = helper.men_vs_women(df)

    st.title('Men VS Women participation over the years')

    fig= px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1100, height=800)  # code to make width and height of graph bigger
    st.plotly_chart(fig)


