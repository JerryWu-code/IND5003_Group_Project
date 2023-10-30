# IND5003_Group_Project

This is the IND5003 Group Project Repo. And this is the members' table of our team:

| 1         | 2              | 3           | 4         | 5          |
| --------- | -------------- | ----------- | --------- | ---------- |
| WU QILONG | XIANG XIAONENG | DONG XINYUE | QI SHUOLI | JIN YIXUAN |

Here are the descriptions for **dataset** and **demo**:



## 1.Dataset

### Part1: Green Taxi Dataset in New York City

- We Collected data dating from **Jan 2022** to **Jul 2023** from this [website](https://www.nyc.gov/site/tlc/businesses/green-cab.page).
- Tracking **taxi service & accessibility** in the **boroughs in New City**.
- Respond to street hails but only in designated **green areas** (above W 110 St/E 96th St in Manhattan & in the boroughs)

**A fraction of pickups in the dataset originate far outside New York City's** **borders**. To streamline our analysis and accommodate limited computational resources, we **only considered taxi trips originating from locations within the** **defined area**.

### Part2: Daily weather data in New York City

### Part3: Location zone data corresponding to ID
- We Collected data **Taxi Zone Maps and Lookup Tables** from this [website](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
- Get the zone corresponding to each region ID

## 2.Demo

### Feature1: DashBoard

#### (1)Analysis of difference between short distance and long distance：
The difference between short and long trips is a key aspect of taxi services. "trip_distance" is the main metric that classifies a trip as short or long. The "PUtime" and "DOtime" variables are used to create time series data that provides insight into the temporal aspects of these journeys. In addition, "pick-up zones" and "pick-up zones" are used to identify popular locations associated with short and long distance trips. To better understand these differences, the analysis also considers the variables "passenger_count," "RatecodeID," and "payment_type." These aspects help to assess potential differences in passenger behaviour, preferred rate codes and payment methods between short and long haul trips.

This analysis is crucial for taxi service providers as it enables them to better understand their customers and effectively align their services with market needs. By recognizing these differences, taxi companies can develop sound strategies. These strategies may include optimizing vehicle configurations, offering diversified service levels, and adjusting pricing strategies to provide valuable insights into operational and marketing decisions, enabling the company to improve service levels and meet broader customer needs.

#### (2)哪些地区上车下车最多: 
'PUcount', 'DOcount'
the top 3 pickup zones are...
the top 3 drop-off zones are...
Zones with most pickups; Zones with most drop-offs; 

#### (3)打车高峰期和非高峰是什么时候: Peak and Off-Peak Times
Analyzing peak and off-peak times for taxi services is crucial for optimizing operations, improving customer satisfaction, and maximizing profits for a taxi company. Consequently, we need to evaluate based on peak and off-peak times for taxi services. We may need to deploy more taxis during high demand ensure efficient service and reduce the taxi count during off-peak. 

The demand might be related to the timely, daily, weekly, and monthly basis, so we have a brief analysis of them using line charts and histograms. Additionally, the demand in different locations should be various, so we visualize the demand based on geographical information using the heated map. What's more, the weather could also be a factor in people choosing or not choosing a taxi to go out. Accordingly, we need the dataset: pickuptime, dropofftime, pickuparea, dropoffarea, and whether.

### Feature2: Prediction--Regional Counts/Price

#### (1)区域PU上车频数按时间 & 预测

Utilizing the dataset, predictive models can be created, such as SVM, XgBoost, RandomForest. These models can forecast future pick-up frequencies within certain time periods and certain areas, aiding companies in deploying taxis strategically. Real-time predictions allow companies to dynamically adjust their fleet, ensuring taxis are where they are needed most and maximizing the profit. The precision of the prediction is analyzed after the prediction to ensure the preciseness.

#### (2)区域PU上车打车价格按时间 & 预测



### Feature3: Vehicle Scheduling
Vehicle scheduling involves the strategic allocation of vehicles based on a combination of factors,  primarily focusing on density and proximity. These two critical factors contribute to the computation of a score that  guides the dispatch of vehicles to various regions.

Density, as a key determinant, highlights the concentration of service demand in specific areas. The higher the density of the drop-off location, That means the more traffic there is in this area, the more traffic can be diverted. Simultaneously, proximity considers the geographical closeness of these areas to the available vehicle fleet.

By assessing both density and proximity, a score is generated for each area, allowing for the prioritization of vehicle dispatch. Areas with high scores—indicating a combination of high service demand and proximity to the vehicle pool—are given precedence in scheduling. This approach optimizes the utilization  of resources and enhances the efficiency of transportation services, ensuring that vehicles are dispatched to areas where they are most needed. Consequently, vehicle scheduling based on density and proximity plays a pivotal role in meeting customer demands effectively and  improving the overall performance of the transportation system.
