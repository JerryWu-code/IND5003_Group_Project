# IND5003_Group_Project

This is the IND5003 Group Project Repo. And this is the members' table of our team:

| 1         | 2              | 3           | 4         | 5          |
| --------- | -------------- | ----------- | --------- | ---------- |
| WU QILONG | XIANG XIAONENG | DONG XINYUE | QI SHUOLI | JIN YIXUAN |

We currently use the free server so that we only provide part of funtions in the website demo due to limited server performance, and if you want to explore the whole features, you could clone this repo and deploy this locally. Here are the guidance for installation and the descriptions for **dataset** and **[demo](https://ind5003groupproject-pg04-nyc-taxi.streamlit.app)**:



# Installation

### Clone this Repository

Enter the target directory you want to use, and use this command to clone and enter the folder:

```bash
git clone https://github.com/wu953855668/IND5003_Group_Project.git
cd IND5003_Group_Project
```

or this:

```bash
git clone git@github.com:wu953855668/IND5003_Group_Project.git
cd IND5003_Group_Project
```

And you should follow this folder structure (in `folder_structure.txt`):

```
.
├── Group_Project.ipynb
├── LICENSE
├── Main.py
├── README.md
├── data
│   ├── Location
│   ├── NYC_Shapefile
│   ├── Weather
│   └── green_raw
├── figs
├── folder_structure.txt
├── my_scripts
│   ├── Data_loader.py
│   ├── Regression.py
│   ├── Time_series_analysis.py
│   ├── Visualization.py
│   ├── __pycache__
│   └── ts.py
├── pages
│   ├── 1 Multivariable-Visualization.py
│   ├── 2 Geo-Visualization.py
│   ├── 3 Time-Series-Analysis.py
│   ├── 3 Time-Series-Prediction.py
│   └── 4 Regression Analysis.py
├── report
│   └── IND5003_PG04_Green_Taxi_NYC.pdf
└── requirements.txt
```



### Create virtual Environment

```bash
conda create -n env5003 python=3.11 -y
conda activate env5003
pip install --upgrade pip
pip install -r requirements.txt
```



### Run the Main.py

```bash
streamlit run Main.py
```



# Descriptions

## 1.Dataset

### Part1: Green Taxi Dataset in New York City

- We Collected data dating from **Jan 2022** to **Jul 2023** from this [website](https://www.nyc.gov/site/tlc/businesses/green-cab.page).
- Tracking **taxi service & accessibility** in the **boroughs in New City**.
- Respond to street hails but only in designated **green areas** (above W 110 St/E 96th St in Manhattan & in the boroughs)

**A fraction of pickups in the dataset originate far outside New York City's** **borders**. To streamline our analysis and accommodate limited computational resources, we **only considered taxi trips originating from locations within the** **defined area**.





### Part2: Daily weather data in New York City

- We Collected comprehensive daily weather data for New York City dating from **Jan 2022** to **Jul 2023** from this [website](https://www.ncei.noaa.gov/access/search/index).
- Integrating this weather data with the taxi dataset, we aim to delve into the interplay between weather conditions and taxi demand, potentially revealing significant correlations or causative factors. Our overarching objective is to arm taxi service providers with predictive insights, allowing them to anticipate demand shifts based on upcoming weather forecasts, ultimately enhancing service efficiency and customer satisfaction.
- The dataset provides in-depth weather metrics for each day, including:

|                NAME                |  Brief   |                         Desciptions                          |
| :--------------------------------: | :------: | :----------------------------------------------------------: |
|           **Dew Point**            | **ADPT** | Represents the temperature below which water droplets begin to condense from the air, indicating the moisture level of the atmosphere. |
| **Atmospheric Sea Level Pressure** | **ASLP** | This measures the atmospheric pressure at sea level, offering insights into weather conditions and patterns. |
|      **Wet Bulb Temperature**      | **AWBT** | Indicates the temperature a parcel of air would have if cooled to saturation by the evaporation of water into it. |
|       **Average Wind Speed**       | **AWND** | Provides the average speed of the wind, which can impact mobility patterns within the city. |





### Part3: Location zone data corresponding to ID

- We collected data **Taxi Zone Maps and Lookup Tables** from this [website](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and also get **Whole US ZIP Code Tabulation Areas**(shapefile: "~.shp") for geo-visualization from this [website](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2022&layergroup=ZIP+Code+Tabulation+Areas).
- Get the zone corresponding to each region ID.





## 2.[Demo](https://ind5003groupproject-pg04-nyc-taxi.streamlit.app)

### Feature1: Multifactors Exploring Data Visualization

**Dive into Multifactors Exploring Data Visualization, where journey lengths, temporal shifts, urban hotspots, and rider preferences intertwine to sculpt the taxi industry's ever-changing narrative.**

#### (1) Analysis of difference between short distance and long distance：

The difference between short and long trips is a key aspect of taxi services. "trip_distance" is the main metric that classifies a trip as short or long. The "PUtime" and "DOtime" variables are used to create time series data that provides insight into the temporal aspects of these journeys. In addition, "pick-up zones" and "pick-up zones" are used to identify popular locations associated with short and long distance trips. To better understand these differences, the analysis also considers the variables "passenger_count," "RatecodeID," and "payment_type." These aspects **help to assess potential differences in passenger behaviour, preferred rate codes and payment methods between short and long haul trips**.

This analysis is crucial for taxi service providers as it enables them to better understand their customers and effectively align their services with market needs. By recognizing these differences, taxi companies can **develop sound strategies**. These strategies may **include optimizing vehicle configurations, offering diversified service levels, and adjusting pricing strategies** to provide valuable insights into operational and marketing decisions, enabling the company to improve service levels and meet broader customer needs.



#### (2) Which areas have the most boarding and alighting:

Based on our analysis of the dataset, certain zones consistently show higher pickup and dropoff frequencies. Using the 'PUcount' and 'DOcount' metrics, we identified the top 3 zones for both pickups and dropoffs. The zones with the highest pickups might indicate popular residential areas or business hubs, while zones with the highest dropoffs could signify popular destinations, commercial areas, or tourist spots. Understanding these trends **helps taxi service providers optimize their fleet deployment to cater to the highest demand areas effectively**.



#### (3) Peak and Off-Peak Times

Analyzing peak and off-peak times for taxi services is crucial for **optimizing operations, improving customer satisfaction, and maximizing profits for a taxi company**. Consequently, we need to evaluate based on peak and off-peak times for taxi services. We may need to **deploy more taxis during high demand ensure efficient service and reduce the taxi count during off-peak**. 

The demand might be related to the timely, daily, weekly, and monthly basis, so we have a brief analysis of them using line charts and histograms. Additionally, the demand in different locations should be various, so we visualize the demand based on geographical information using the heated map. What's more, the weather could also be a factor in people choosing or not choosing a taxi to go out. Accordingly, we need the dataset: pickuptime, dropofftime, pickuparea, dropoffarea, and whether.



### Feature2: Geo-Visualization

**Unlock the city's taxi rhythms with Geo-Visualization—a strategic tool that empowers ride services to master demand hotspots and sculpt profit-maximizing pricing strategies.**

#### (1) Regional Counts

##### a.Borough Area

Provides an analysis of taxi demand based on different regional divisions.

- **Visualization**: Displays taxi demand data across boroughs.
- **Data Points**: Includes the number of pickups, drop-offs, and active taxis per borough.
- **Use Case**: Understand which boroughs have the highest demand to allocate resources effectively.



##### b. Zipcode Area

- **Visualization**: Shows taxi demand granularity at the zipcode level.
- **Data Points**: Captures detailed statistics including time-based demand fluctuations.
- **Use Case**: Pinpoint specific areas for targeted marketing and service deployment strategies.



#### (2) Regional Price

##### a. Borough Area

- **Dynamic Pricing**: Allows for adjustments in fare rates in response to demand intensity in each borough.
- **Analytics**: Provides historical data trends to forecast pricing adjustments.
- **Strategy**: Assist in developing borough-specific pricing strategies to optimize earnings.



##### b. Zipcode Area

- **Hyperlocal Pricing**: Enables even more granular pricing strategies within specific zip codes.
- **Market Analysis**: Offers insights into the economic profile of areas to tailor pricing effectively.
- **Growth Potential**: Identifies zip codes with emerging demand where growth-oriented pricing can be implemented.



### Feature3: Time Series Analysis

**This feature is designed to provide comprehensive insights into the fluctuating patterns of taxi demand and fare structures within different boroughs. Utilizing advanced analytical techniques, this feature helps taxi companies to predict, plan, and adjust their strategies in alignment with market trends and demand cycles.**

#### (1) Seasonal Time Series Analysis

The `Seasonal Time Series Analysis` module focuses on identifying and interpreting the cyclical fluctuations in taxi operations across various time frames, such as weekends or specific seasons. This analysis aids in recognizing high-demand periods, allowing for more efficient resource allocation, such as scaling fleet operations to match peak hour demand and enhance customer service.



#### (2) Decomposing Analysis

Our `Decomposing Analysis` segment employs a methodological approach to disentangle time series data into its core components: trend, seasonality, and residual. For taxi operations:

- **Trend Component**: Understand the long-term trajectory of order volumes, determining whether there is a gradual increase or decrease over time.
- **Seasonality Component**: Identify and predict cyclical patterns in order volumes throughout different periods, which is crucial for optimizing service availability.
- **Residual Component**: Analyze and interpret the data fluctuations not explained by the trend or seasonality, providing insights into anomalies or unexpected events that could impact service demand.

These decomposed insights are instrumental in formulating precise, data-driven strategies and decision-making processes that respond agilely to market shifts and business operational efficiency.



#### (3) Time Series Prediction

##### a.Seasonal Naive Prediction

The `Seasonal Naive Prediction` model sets a baseline forecast based on the assumption that the upcoming period will mirror the pattern observed in the past season. This straightforward method is grounded in historical data and is particularly effective for short-term projections with consistent weekly patterns, aiding in immediate operational decisions.



##### b.ARIMA

The `ARIMA` (Autoregressive Integrated Moving Average) model is a more complex forecasting tool that incorporates both non-seasonal and seasonal data components. It refines predictions by considering various parameters affecting the data, such as trends and seasonality factors. The ARIMA model's diagnostics suggest a good fit for the data, with the potential for further refinement, as indicated by the distribution and correlation of residuals.



### Feature4: Regression Analysis

**Discover the hidden dance of economics and elements: How do temperature shifts, passenger counts, rainfall patterns, the timing of rides, and journey lengths weave together to influence the cost of a trip? Dive into the mystery with our analysis.**

#### (1) Decision Tree

- **Insightful Breakdown**: Simplifies the complex relationship between fare and influencing factors into an easy-to-understand tree structure.
- **Variable Importance**: Reveals the relative significance of each factor affecting trip costs.
- **Strategic Pricing**: Informs fare-setting by highlighting key price determinants.



#### (2) XGBoost

- **Performance**: Delivers a robust predictive model with excellent accuracy through gradient boosting.

- **Scalability**: Efficiently handles a vast range of data with the ability to manage various types of regression analysis.
- **Outcome Refinement**: Refines fare estimates over time with continued learning capabilities.



#### (3) Gradient Boosting

- **Predictive Strength**: Uses a sequence of weak predictors to form a strong predictive model.
- **Error Reduction**: Focuses on minimizing errors from previous predictions for enhanced accuracy.
- **Fare Strategy**: Guides data-driven fare strategies, incorporating a multitude of external factors.
