import pandas as pd 
import streamlit as st 
import altair as alt

@st.cache_data
def load_data():
    df = pd.read_csv("Nigerian_Road_Traffic_Crashes_2020_2024.csv")

    


    st.title("Nigerian Road Traffic Crash Analysis (2020-2024)")
    st.write(df)
    return df

try:
    df = load_data()

    #Section 2 filter section

    # filter 1 State filter
    selected_state = st.sidebar.selectbox("Select State", df["State"].unique())

    # filter 2 Quarter filter
    selected_quarter = st.sidebar.selectbox("Selected Quarter", df["Quarter"].unique())

    # filter 3 Accident severity filter
    min_injured = st.sidebar.slider("Minimum Number Injured", min_value=0, max_value=df["Num_Injured"].max())
    max_injured = st.sidebar.slider("Maximum Number Injured", min_value=0, max_value=df["Num_Injured"].max())

    # filter 4 Number killed filter
    min_killed = st.sidebar.slider("Minimum Number Killed", min_value=0, max_value=df["Num_Killed"].max())
    max_killed = st.sidebar.slider("Maximum Number Killed", min_value=0, max_value=df["Num_Killed"].max())

    # filter 5 Cause of Crashes
    selected_cause = st.sidebar.multiselect("Select Accident Cause", ["Speed violation", "Driving under alcohol/drug influence", "Poor weather", "Fatigue"])

    # filter 6 Total crashes filter
    min_crashes = st.sidebar.slider("Minimum Total Crashes", min_value=0, max_value=df["Total_Crashes"].max())
    max_crashes = st.sidebar.slider("Maximum Total Crashes", min_value=0, max_value=df["Total_Crashes"].max())


    # filter 7 # Vehicle involved filter
    min_vehicles = st.sidebar.slider("Minimum Vehicles Involved", min_value=0, max_value=df["Total_Vehicles_Involved"].max())
    max_vehicles = st.sidebar.slider("Maximum Vehicles Involved", min_value=0, max_value=df["Total_Vehicles_Involved"].max())

    # Filter data
    filtered_df = df[(df["State"] == selected_state) & 
                 (df["Quarter"] == selected_quarter) & 
                 (df["Num_Injured"] >= min_injured) & 
                 (df["Num_Injured"] <= max_injured) & 
                 (df["Num_Killed"] >= min_killed) & 
                 (df["Num_Killed"] <= max_killed) & 
                 (df["Total_Crashes"] >= min_crashes) & 
                 (df["Total_Crashes"] <= max_crashes) & 
                 (df["Total_Vehicles_Involved"] >= min_vehicles) & 
                 (df["Total_Vehicles_Involved"] <= max_vehicles)]

    # Apply cause filter
    if selected_cause:
        cause_filter = df[selected_cause].any(axis=1)
        filtered_df = filtered_df[cause_filter]

    # Section 3 Kpis overview
    #total_crashes_rate = df.groupby("Quarter")["Total_Crashes"].sum().reset_index()
    injury_rate = df["Num_Injured"].sum() / df["Total_Crashes"].sum()
    fatality_rate = df["Num_Killed"].sum() / df["Total_Crashes"].sum()
    speed_violation_rate = (df["SPV"].sum() / df["Total_Crashes"].sum()) * 100
    driving_under_influence_rate = (df["DAD"].sum() / df["Total_Crashes"].sum()) * 100
    total_deaths = df["Num_Killed"].sum()

    # Display KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Crashes", df["Total_Crashes"].sum())
    col2.metric("Injury Rate", f"{injury_rate:.2f}")
    col3.metric("Fatality Rate", f"{fatality_rate:.2f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Speed Violation Rate", f"{speed_violation_rate:.2f}%")
    col5.metric("Driving Under Influence Rate", f"{driving_under_influence_rate:.2f}%")
    col6.metric("Total Deaths", total_deaths)

    #st.write("Total Crashes Rate by Quarter:")
    #st.write(total_crashes_rate)

    # Section 4 (Analysis Finding)
    st.header("1. State with the highest number of fatalities in a single quarter")
    fatalities = df.groupby(["State", "Quarter"])["Num_Killed"].sum().reset_index()
    top_10_fatalities = fatalities.nlargest(10, 'Num_Killed')[['State', 'Quarter', 'Num_Killed']]
    # Find the state with the highest number of fatalities in a single quarter
    st.write("Top 10 States with Highest Fatalities:")
    st.table(top_10_fatalities)

    chart_1 = alt.Chart(top_10_fatalities).mark_bar().encode(
        x=alt.X('State:N', sort='-y'),
        y='Num_Killed:Q',
        color=alt.Color('Num_Killed:Q', scale=alt.Scale(scheme='plasma')),
        tooltip=['State:N', 'Quarter:N', 'Num_Killed:Q']
    ).properties(
        title='Top 10 States with Highest Fatalities',
        width=800,
        height=600
    )

    # Display the chart
    st.write(chart_1, use_container_width=True)

    st.header("2. State with the Highest Death")
    state_deaths = df.groupby("State")["Num_Killed"].sum().reset_index()

    top_10_deaths = state_deaths.nlargest(10, 'Num_Killed')[['State', 'Num_Killed']]


    st.write("Top 10 States with Highest Number of Deaths:")
    st.table(top_10_deaths)

    #Create a bar chart
    chart_2 = alt.Chart(top_10_deaths).mark_bar().encode(
        x=alt.X('State:N', sort='-y'),
        y='Num_Killed:Q',
        color=alt.Color('Num_Killed:Q', scale=alt.Scale(scheme='reds')),
        tooltip=['State:N', 'Num_Killed:Q']
    ).properties(
        title='Top 10 States with Highest Number of Deaths',
        width=800,
        height=600
    )
    st.write(chart_2, use_container_width=True)

    st.header("3. Which state recorded the highest number of crashes during the entire period?")
    state_crashes = df.groupby('State')['Total_Crashes'].sum().reset_index()

    # Sort the results in descending order and get the top 15 states
    top_15_states = state_crashes.sort_values(by='Total_Crashes', ascending=False).head(15)

    st.write("Top 15 States with Highest Number of Crashes:")
    st.table(top_15_states)

    # Create the Altair bar chart
    chart_3 = alt.Chart(top_15_states).mark_bar().encode(
        x=alt.X('State', sort='-y', axis=alt.Axis(title='State')),
        y=alt.Y('Total_Crashes', axis=alt.Axis(title='Total Crashes (2020-2024)')),
        tooltip=['State', 'Total_Crashes']
    ).properties(
        title='Top 15 States by Total Road Traffic Crashes (2020-2024)'
    )
    st.write(chart_3, use_container_width=True)


    st.header("4. What is the main reason for crashes? Is it speeding, dangerous driving, or something else? This information can guide efforts to prevent future accidents.")
    crash_factors = df[['SPV', 'DAD', 'PWR', 'FTQ', 'Other_Factors']].sum()

    # Convert the Series to a DataFrame for Altair plotting
    factors_df = crash_factors.reset_index()
    factors_df.columns = ['Reason', 'Count']
    main_reason = factors_df.sort_values(by='Count', ascending=False).iloc[0]

    # --- Display the results using Streamlit ---
    st.header("Main Reason for Crashes")

    # Get the top reasons for crashes
    top_reasons = factors_df.sort_values(by='Count', ascending=False).head(5)

    # Display the top reasons in a table
    st.write(top_reasons)

    # Create the Altair bar chart
    chart_4 = alt.Chart(factors_df).mark_bar().encode(
        x=alt.X('Reason', sort='-y', axis=alt.Axis(title='Reason for Crash')),
        y=alt.Y('Count', axis=alt.Axis(title='Number of Crashes')),
        tooltip=['Reason', 'Count']
    ).properties(
        title='Contribution of Various Factors to Road Crashes'
    )

    st.write(chart_4, use_container_width=True)


    st.header("5.Which quarter has the highest number of crashes?")

    quarterly_crashes = df.groupby('Quarter')['Total_Crashes'].sum().reset_index()
    st.write(quarterly_crashes)

    # Create the Altair bar chart
    chart_5 = alt.Chart(quarterly_crashes).mark_bar().encode(
        x=alt.X('Quarter', sort=None, axis=alt.Axis(title='Quarter')),
        y=alt.Y('Total_Crashes', axis=alt.Axis(title='Total Crashes')),
        tooltip=['Quarter', 'Total_Crashes']
    ).properties(
    title='Total Crashes by Quarter (2020-2024)'
    )
    st.write(chart_5, use_container_width=True)

    ftq_crashes = df['FTQ'].sum()

    total_crashes = df['Total_Crashes'].sum()

    percentage_ftq = (ftq_crashes / total_crashes) * 100

    st.header("6. How safe are vehicles on the road?")

    # Create a dataframe for the data
    vehicle_safety_data = pd.DataFrame({
        'Category': ['Faulty Vehicles', 'All Other Crashes'],
        'Count': [ftq_crashes, total_crashes - ftq_crashes],
        'Percentage': [percentage_ftq, 100 - percentage_ftq]
    })

    # Display the data in a table
    st.write(vehicle_safety_data)

    # Create and display the Altair bar chart
    chart_6 = alt.Chart(vehicle_safety_data).mark_bar().encode(
        x=alt.X('Category', sort=None, axis=alt.Axis(title='Cause')),
        y=alt.Y('Count', axis=alt.Axis(title='Number of Crashes')),
        tooltip=['Category', 'Count', 'Percentage']
    ).properties(
        title='Comparison of Crashes Caused by Faulty Vehicles'
    )

    st.write(chart_6, use_container_width=True)
























except FileNotFoundError:
    st.error("The file was not found. Please check the file path.")
except pd.errors.EmptyDataError:
    st.error("The file is empty. Please check the file contents.")
except Exception as e:
    st.error(f"An error occurred: {e}")


