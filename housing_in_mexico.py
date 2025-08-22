# Import Matplotlib, pandas, and plotly
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

#reading the first csv file
df1 = pd.read_csv("data/brasil-real-estate-1.csv")
df2 = pd.read_csv("data/brasil-real-estate-2.csv")

#cleaning and wrangling
#df1
df1.dropna(inplace = True)
df1[["lat", "lon"]] = (
    df1["lat-lon"]
    .str.split(",", expand = True)
    .astype(float)
)
df1["state"] = (
    df1["place_with_parent_names"]
    .str.split("|", expand = True)[2]
)
df1["price_usd"] = (
    df1["price_usd"]
    .str.replace("$","",regex=False)
    .str.replace(",","",regex=False)
    .astype(float)
)
df1.drop(columns = ["place_with_parent_names", "lat-lon"], inplace = True)

#df2
df2["price_usd"] = (df2["price_brl"] / 3.19).round(2)
df2.dropna(inplace = True)
df2.drop(columns = ["price_brl"], inplace = True)

#concatenating the 2 dataframes
df = pd.concat([df1, df2])


#exploratory analysis

fig = px.scatter_mapbox(
    df,
    lat="lat", 
    lon="lon", 
    center={"lat": -14.2, "lon": -51.9},  # Map will be centered on Brazil
    width=600,
    height=600,
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)

fig.update_layout(mapbox_style="open-street-map")

fig.show()

#summary stats
summary_stats = df[["area_m2", "price_usd"]].describe()
summary_stats

#histogram of price
# Don't change the code below 👇
fig, ax = plt.subplots()

# Build histogram
ax.hist(df["price_usd"].head(20000))

# Label axes
ax.set_xlabel("Price [USD]")
ax.set_ylabel("Frequency")

# Add title
ax.set_title("Distribution of Home Prices");

#histogram of area
# Don't change the code below 👇
fig, ax = plt.subplots()

#Build box plot
ax.boxplot(df["area_m2"],vert = False)

# Label x-axis
ax.set_xlabel("Area [sq meters]")

# Add title
ax.set_title("Distribution of Home Sizes")

#median price by region
mean_price_by_region = df.groupby("region")["price_usd"].mean().sort_values()
mean_price_by_region

#bar plot of median price by region
# Don't change the code below 👇
fig, ax = plt.subplots()


# Build bar chart, label axes, add title
mean_price_by_region.plot(
    kind='bar',
    xlabel = "Region",
    ylabel = "Mean Price [USD]",
    title = "Mean Home Price by Region",
    ax=ax
)

#selecting southern region
df_south = df[df["region"] == "South"]

#properties in each state in south
homes_by_state = df_south["state"].value_counts()

#scatter plot of Price vs Area for the state with most houses in south
# Subset data
df_south_rgs = df_south[df_south["state"] == "Rio Grande do Sul"]

# Don't change the code below 👇
fig, ax = plt.subplots()


# Build scatter plot
ax.scatter(x=df_south_rgs["area_m2"], y=df_south_rgs["price_usd"])

# Label axes
ax.set_xlabel("Area [sq meters]")
ax.set_ylabel("Price [USD]")

# Add title
ax.set_title("Rio Grande do Sul: Price vs. Area")

# Dictionary of Area:Price correlation for each state in south
southern_states = df_south["state"].unique()
south_states_corr = {}

for s in southern_states:
    df_corr = df_south[df_south["state"] == s]
    p_coefficient = df_corr["area_m2"].corr(df_corr["price_usd"])
    south_states_corr[s] = p_coefficient 
south_states_corr
