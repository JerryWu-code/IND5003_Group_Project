# IND5003_Group_Project

This is the IND5003 Group Project Repo. And this is the members' table of our team:

| 1         | 2              | 3           | 4         | 5          |
| --------- | -------------- | ----------- | --------- | ---------- |
| WU QILONG | XIANG XIAONENG | DONG XINYUE | QI SHUOLI | JIN YIXUAN |

We currently use the free server so that we only provide part of funtions in the website demo due to limited server performance, and if you want to explore the whole features, you could clone this repo and deploy this locally. Here are the guidance for installation and the descriptions for **dataset** and **[demo](https://ind5003groupproject-pg04-greentaxi-nyc.streamlit.app/)**:



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





## 2.[Demo](https://ind5003groupproject-pg04-greentaxi-nyc.streamlit.app/)

### Feature1: Multifactors Exploring Data Visualization

#### (1)Analysis of difference between short distance and long distance：
The difference between short and long trips is a key aspect of taxi services. "trip_distance" is the main metric that classifies a trip as short or long. The "PUtime" and "DOtime" variables are used to create time series data that provides insight into the temporal aspects of these journeys. In addition, "pick-up zones" and "pick-up zones" are used to identify popular locations associated with short and long distance trips. To better understand these differences, the analysis also considers the variables "passenger_count," "RatecodeID," and "payment_type." These aspects **help to assess potential differences in passenger behaviour, preferred rate codes and payment methods between short and long haul trips**.

This analysis is crucial for taxi service providers as it enables them to better understand their customers and effectively align their services with market needs. By recognizing these differences, taxi companies can **develop sound strategies**. These strategies may **include optimizing vehicle configurations, offering diversified service levels, and adjusting pricing strategies** to provide valuable insights into operational and marketing decisions, enabling the company to improve service levels and meet broader customer needs.

#### (2)Which areas have the most boarding and alighting:

Based on our analysis of the dataset, certain zones consistently show higher pickup and dropoff frequencies. Using the 'PUcount' and 'DOcount' metrics, we identified the top 3 zones for both pickups and dropoffs. The zones with the highest pickups might indicate popular residential areas or business hubs, while zones with the highest dropoffs could signify popular destinations, commercial areas, or tourist spots. Understanding these trends **helps taxi service providers optimize their fleet deployment to cater to the highest demand areas effectively**.

#### (3)Peak and Off-Peak Times
Analyzing peak and off-peak times for taxi services is crucial for **optimizing operations, improving customer satisfaction, and maximizing profits for a taxi company**. Consequently, we need to evaluate based on peak and off-peak times for taxi services. We may need to **deploy more taxis during high demand ensure efficient service and reduce the taxi count during off-peak**. 

The demand might be related to the timely, daily, weekly, and monthly basis, so we have a brief analysis of them using line charts and histograms. Additionally, the demand in different locations should be various, so we visualize the demand based on geographical information using the heated map. What's more, the weather could also be a factor in people choosing or not choosing a taxi to go out. Accordingly, we need the dataset: pickuptime, dropofftime, pickuparea, dropoffarea, and whether.



### Feature2: Geo-Visualization

#### (1)Regional Counts

##### a.Borough Area



##### b.Zipcode Area



#### (2)Regional Price

##### a.Borough Area



##### b.Zipcode Area



### Feature3: Time Series Analysis

#### (1)Regional PU Boarding Frequency by Time & Predictions

Utilizing the dataset, predictive models can be created, such as SVM, XgBoost, RandomForest. These models can forecast future pick-up frequencies within certain time periods and certain areas, **aiding companies in deploying taxis strategically**. Real-time predictions allow companies to dynamically adjust their fleet, ensuring taxis are where they are needed most and maximizing the profit. The precision of the prediction is analyzed after the prediction to ensure the preciseness.

#### (2)Regional PU Boarding Taxi Prices by Time & Predictions

Using our dataset, we can develop predictive models to forecast the average taxi fare for pickups in different regions over time. This can be achieved using regression models, neural networks, or time series forecasting methods. By predicting taxi fare trends, service providers can **develop dynamic pricing strategies**, **offering discounts during low-demand periods and surge pricing during high-demand times**. These strategies can increase revenue and ensure that the taxi fleet is effectively utilized. Moreover, by providing fare predictions to customers in advance, taxi services can enhance transparency and improve customer trust.



#### Feature4: Regression Analysis



