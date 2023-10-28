# IND5003_Group_Project

This is the IND5003 Group Project Repo. And this is the members' table of our team:

| 1         | 2              | 3           | 4         | 5          |
| --------- | -------------- | ----------- | --------- | ---------- |
| WU QILONG | XIANG XIAONENG | DONG XINYUE | QI SHUOLI | JIN YIXUAN |

Here are the descriptions for **dataset** and **demo**:



## 1.Dataset--Green Taxi in NY City

### Green Taxi Dataset in New York City

- We Collected data dating from **Jan 2022** to **Jul 2023** from this [website](https://www.nyc.gov/site/tlc/businesses/green-cab.page).
- Tracking **taxi service & accessibility** in the **boroughs in New City**.
- Respond to street hails but only in designated **green areas** (above W 110 St/E 96th St in Manhattan & in the boroughs)

**A fraction of pickups in the dataset originate far outside New York City's** **borders**. To streamline our analysis and accommodate limited computational resources, we **only considered taxi trips originating from locations within the** **defined area**.



## 2.Demo

### Feature1: DashBoard

#### (1)短途和长途的区别分析：

trip_distance判段长短途，"PUtime", "DOtime"做时钟图，’'pickup zone', 'dropoff zone'用来计算长短途的热门地点，最后"passenger_count", "RatecodeID", "payment_type"看看长短途在这个三个方面有没有差异。这个问题可以帮助出租车公司更好地了解他们的客户和市场需求。他们可以根据这些差异来制定更精细的策略，例如优化车辆分配，提供不同的服务水平，或者调整价格策略，为公司提供运营和市场营销决策提供有力的依据。

#### (2)哪些地区上车下车最多: 
'PUcount', 'DOcount'
the top 3 pickup zones are...
the top 3 drop-off zones are...
Zones with most pickups; Zones with most drop-offs; 

#### (3)打车高峰期和非高峰是什么时候: 
需要数据：
1/ pickuptime
2/ dropofftime
3/ pickuparea
4/ dropoffarea
5/ whether
可视化：
折线图：时间（日/周/年）-count—pickup/dropoff 
直方图：weather
heat map: 最繁忙的时间和地点用深色表示



### Feature2: Prediction--Regional Counts/Price

#### (1)区域PU上车U频数按时间 & 预测

#### (2)区域PU上车打车价格按时间 & 预测



### Feature3: Vehicle Scheduling

#### 车辆按照 density高 & 距离近 两个因素计算的分数，对不同区域进行调度
