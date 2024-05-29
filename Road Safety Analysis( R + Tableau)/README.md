# Exploring road safety in New Zealand Police and NZTA CAS Data
## Introduction
Road safety is a critical concern for any society, affecting both individuals and the community as a whole. New Zealand, like many countries, faces the challenge of reducing road accidents and their associated impacts. This introduction provides an overview of the road safety situation in New Zealand and the significance of analysing the factors influencing road accidents. New Zealand's "Road to Zero" policy, spearheaded by the government, reflects a strong commitment to minimizing road fatalities and serious injuries (NZ Transport Agency, 2019). Road accidents not only result in personal tragedies but also have far-reaching consequences for families and society at large. Understanding the factors that contribute to road accidents is essential for devising effective prevention strategies.

This research aims to serve as a foundation for the development of effective strategies and policies to prevent accidents, thus making New Zealand's roadways safer for all its citizens.
## Research Question
1. Temporal Trends: Examining changes in car crash frequency over the past three years to identify any emerging trends or patterns.
2. Regional Comparison: Evaluating car crash rates and severity across different regions in New Zealand, with a focus on geographical patterns and hotspots.
3. Influence of Factors: Investigating how weather conditions, time of day, road infrastructure, etc. contribute to the severity of car crashes in New Zealand.
## Data Sources
1. The New Zealand Police Data’s Demand and Activity section provides counts of recorded vehicle collisions in the last three years at most (2020 - 2023). 
2. Crash Analysis System (CAS) from Waka Kotahi provides more field details of over 821,000 crashes.
## Methods
1. Data Visualisation in Tableau
- Crashes over time
- Crashes by region
- Crashes by time of day
2. Machine Learning(Random Forest) in R

Tree-based methods, which is regarded as generally more robust than linear regression models, especially when handling categorical data (Varghese,2018), non-linear relationships, and variable interactions. Therefore,random forest is used to deduce complex connections between multiple contributing elements and the level of severity.
- Predictors of severity
- Predictors of the number of casualties and damage
## Data Cleaning, Wrangling, and Pre-Processing
### Tableau
- Urban Context

Using the Police Data, we used Regular Expressions to create a column based on the Territorial Authority，enabling us to categorise it into two distinct groups: Urban and Non-Urban.
- Weekday Context
  
Using the Police Data, we used Regular Expressions to create a column based on the “Occurrence Day of Week”, enabling us to categorise it into two distinct groups: Weekday and Weekend.
### R Studio
- Coordinates
  
In accordance with the CAS data field descriptions, the CAS data originally provided coordinates in terms of "northing" and "easting." These are typically used in specific map projections or coordinate systems. However, for better compatibility and visual representation in Tableau, we converted these coordinates into the more commonly used "longitude" and "latitude" by using R.
- Model Variables
  
We sorted out which columns were viable predictor and response variables. We first removed metadata columns and derived variables. We then grouped together variables by the kind of casualty they were, such as vehicle damage, object damage, and property damage. We then segmented outcomes (count of casualties, severity type, count of injuries) as responses, and remaining indicators (ex. environmental factors, road infrastructure) as predictors. Our pipeline ensured the exclusion of response variables from other models onto the model in question, to avoid them from being used as a predictor.
- Null Values
  
We filled in null values for speedLimit based on the speed limits mandated by Waka Kotahi. Other null values were part of the data options as they were not applicable or were properly interpreted as nil or having no value. This process was to ensure the variables were usable in the random forest and regression modelling.
- Class balance for the Random Forest classifier
  
There are four main classes in Crash Severity: Fatal Crash, Serious Crash, Minor Injury, and Non-Injury. Most of the crashes in the CAS are in Minor and Non-Injury, which have lower stakes than Fatal and Serious Crashes, as the latter would require more action to prevent increased social cost. Additional pre-processing was done to account for this.

We declared initial class weights as the reciprocal of the count of each class. Using stratified random sampling, we preserved the original proportions for the test set to mimic the variations present in the original environment. Merging classes as Serious (Fatal and Serious Crashes) and Non-Serious (Minor and Non-Injury) in one of the experiments allowed us to re- frame the problem as binary instead of multi-class. De-duplicating from the majority (Non- Serious) class was done to reduce redundancies and reduce noise. Downsampling was also used in one of the experiments to better tune towards the prediction of Serious crashes.
## Results and Implementation
### Exploratory Analysis
- Regional Trend Comparison

During the car crash period, Auckland recorded the highest number of car accidents, followed by Waikato and Canterbury, which is expected given their larger populations. 

<img width="497" alt="Screenshot 2024-05-24 at 11 32 27" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/08bde71c-587a-4eff-92f9-1ce953bf0f4c">

It's evident that approximately 70% of car crashes in New Zealand occurred in areas with speed limits ranging from 50 to 99 km/h, which include urban and open roads. Additionally, more than a quarter of these accidents took place in areas such as motorways and expressways where the speed limit exceeds 100 km/h.

<img width="475" alt="Screenshot 2024-05-24 at 11 38 29" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/4fe564f8-86d0-4134-b293-b1ef3c03cde1">

The degree of reported crashes ranges from non-injury incidents to fatal accidents. Auckland, due to its popularity, large population, and high traffic volume, accounts for 30% of the reported crashes, while Waikato and Wellington contribute 12% and 10%, respectively. In regions where the "100 above" speed range category records higher crash counts, such as Auckland, Waikato, and Canterbury, there is a corresponding increase in the occurrence of severe crashes, including fatal and serious accidents.

<img width="817" alt="Screenshot 2024-05-24 at 11 42 13" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/0cf92f4f-a6c7-45b6-a448-93bed7f12393">

Overall, the New Zealand government's Road to Zero strategy has shown positive progress in reducing overall crash counts nationwide between 2020 and early 2023.

<img width="831" alt="Screenshot 2024-05-24 at 11 43 02" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/1bfba284-c773-4433-a357-a1429641af78">

- Car Crash records monthly Trend

There is a slight increase in accidents during the months of April to May and November to December annually. These specific time frames correspond to Easter and Christmas holidays, suggesting that holidays may play a significant role in contributing to the increased incidence of car accidents. 

<img width="793" alt="Screenshot 2024-05-24 at 11 43 50" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/c92939f9-fa7f-4e8d-a62c-bbf546bfa08b">

When considering different car crash severity, Christmas is the holiday with the highest car crash amount, followed by Easter.

<img width="595" alt="Screenshot 2024-05-24 at 11 45 12" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/1ec193fc-0856-4375-a5dc-7b88a255df91">

- Car Crash records hourly Trend

Crash records are highest in the time interval from 15:00 to 18:00 for almost all regions.

<img width="859" alt="Screenshot 2024-05-24 at 11 46 40" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/0eb22794-55ad-4a8d-bca3-3533c9008759">

Car crash rates are lower in Non-Urban areas compared to Urban areas. And both Urban and Non-Urban areas experience a significant increase in car crashes during the weekday hours of 6-9 AM and 3-5 PM.

<img width="792" alt="Screenshot 2024-05-24 at 11 48 56" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/e165bc81-32fc-402d-8740-13d38be02c3c">

### Using Random Forest to classify crashes as serious or non-serious

We trained several models of the classifier. We started with a multi-class classifier to directly label crashes with the original classes (Fatal, Serious, Minor, and Non-Injury); however, this model had poor accuracy and recall, which meant it could not predict much of the actual classes, and allows for a lot of serious crashes to be overlooked.

<img width="834" alt="Screenshot 2024-05-24 at 11 52 28" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/82d843c8-66d0-4e6c-b4e3-bde10e6cdd36">

We then went from multi-class to a binary classification problem after grouping Fatal with Serious as Serious and Non-Injury with Minor crashes as Non-Serious. This made sense as the first two groups are of stronger interest as they have higher social cost. The majority class (Non-Serious) was also de-duplicated to reduce the noise in an effort to balance theclasses. The accuracy and recall improved; however, there are still 40% of serious crashes being misclassified as non-serious.

The next model adds downsampling of the majority class up to 1.5x the minority class count. This greatly improved recall (i.e. reducing uncaught serious crashes), but suffered in overall accuracy, which means we are also predicting a lot of non-serious crashes as serious. This means the actual features of a serious crash are yet to be characterised.

One other method to improve the model was adjusting the class weight, as using the reciprocal of class counts may have had too large of an effect on weighting given the large gap between the two class counts. We tried using the reciprocal of the log of counts, which makes the gap smaller, but uses the reciprocal to favour the Serious crashes. This yielded the best model so far, as it had higher accuracy and a fair amount of recall.

To demonstrate the effects of class weights, we tried a version without it. The accuracy shot up; however, it was mostly from predicting the majority class correctly, and contains plenty of uncaught Serious crash cases.

The next iteration eases on the downsampling from 1.5x to 3x the minority class count. Compared to its 1.5x counterpart, it had a higher accuracy, but lower recall. However, this model still has less than 50% of predictions being correct. Another attempt is to use the reciprocal of log class weight. This improved the accuracy, exceeding the 50% mark; however, has a much lower recall than the 1.5x counterpart. At that point, nearly 50% of actual Serious cases are uncaught.

We settled on the binary model with a de-duplicated and downsampled majority to 1.5x the minority class, weighted by the reciprocal of the log of class counts.

The most important features to predicting Serious crashes consist of the road conditions and possible obstructions (both artificial and natural) such as speed limit, road configuration (roadLane), traffic control, number of lanes, weather, trees, ditch, region. The scale on the graph represents how much error is introduced when we do not consider these variables. To visualise how each variable affects the probability of a crash being serious, we used a partial dependence plot. While this oversimplifies the capabilities of the Random Forest, it gives a more interpretable view of the effects of each predictor in isolation. We can see some signsthat serious crashes involve less obstructions, 2-lane roads, and higher speed limits. It would then be good to provide extra precaution to those areas.

<img width="808" alt="Screenshot 2024-05-24 at 11 54 09" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/26cc915a-0ec1-4a09-9ec4-0fc04a8b7ad8">

### Using Random Forest to predict the number of casualties

We were able to run a random forest model on the dataset to predict the number of severe injuries. This allows us to run the algorithm to predict different response variables such as the other injuries as a regression task, or predicting the crash severity as a classification task.

Similar inputs were used in the regression models, but we are now predicting the number of casualties and damage as outcomes of crashes. Our regression models got fairly low test MSEs, which means our predictions were not far from the actual values, and means our models have some predictive power to them. We then take the important features for each model to create a final summary.

<img width="804" alt="Screenshot 2024-05-24 at 11 57 33" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/b18b1524-3c19-4250-878d-84c9a18cb040">

Fatal injuries are associated with the road conditions such as the lane configuration, number of lanes, lighting, and whether the street is a highway or not. In general, more obstructions, lanes, and higher speeds are associated with higher fatal injury counts.

<img width="741" alt="Screenshot 2024-05-24 at 11 58 09" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/965d35ec-25bf-4221-8540-4efb33127b66">

The features for serious injury count are associated with the road conditions such as the lane configuration, speed limit, and number of lanes. In general, more obstructions, lanes, and higher speeds are associated with higher serious injury counts.

<img width="723" alt="Screenshot 2024-05-24 at 11 58 36" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/3122268a-a5e6-4d0d-a967-fdef8b324588">

Minor injury counts are also associated with road conditions as important variables. Compared to serious injury counts, road works are less characteristic of being able to predict minor crashes.

<img width="712" alt="Screenshot 2024-05-24 at 11 59 03" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/a450ea38-eb84-4667-aee6-7a6eb423ffc4">

Vehicle Damage had mostly environmental factors as important features. The absence of certain objects like cliffs, ditches, roadworks, and trees increased the number of vehicle damage. However, the number of lanes and speed limit exhibited a different trend, as the casualties were higher at lower speed limits, and higher number of lanes.

<img width="724" alt="Screenshot 2024-05-24 at 11 59 23" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/4f9e7aa5-42f6-4a18-be30-a9e31a22f5b1">

For pedestrian casualties, road conditions were more prominent, such as street lighting, speed limits, light, lane configuration, and road surface. A higher number of pedestrian casualties are associated with more trees and bodies of water present in the crash. More casualties are associated with less lanes and lower speed limits. These may point to urban and suburban areas being important areas for pedestrian casualties.

<img width="800" alt="Screenshot 2024-05-24 at 11 59 44" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/00bfda0c-3b99-46e2-a823-375eacaca285">

The model for stray animals associates environmental factors like ditches, cliffs, trees, lighting, and banks as important features. Given the plot, it looks like areas with more lanes and higher speed limits are associated with more stray animals being involved in crashes.

<img width="770" alt="Screenshot 2024-05-24 at 12 00 12" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/3f50bf5c-8326-409c-9c96-26f58c95e119">

When it comes to property damage, road conditions and environmental factors are the most important features, such as speed limit, street lighting, cliffs, lighting, region, and whether the road was a street or highway. There is an association for road obstructions to have higher property damage. Higher speed limits, and a general uptrend in the number of lanes are also associated with more property damage.

<img width="735" alt="Screenshot 2024-05-24 at 12 00 51" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/a350b9e2-968b-4d0f-aa50-21632b9dccc1">

Object damage is associated with environmental factors and road conditions, with an association to more road obstructions contributing to more damage.

<img width="735" alt="Screenshot 2024-05-24 at 12 01 16" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/1e2a65ae-6eb6-4041-8073-192065418c6a">

From our random forest models, we found recurring variables of high importance across different crash outcomes. Street conditions, such as Street Light, Speed Limit, Number of Lanes, and Road Configuration are among the most frequently highly ranked variables in terms of importance. They are followed by environmental factors such as Region, Light, Cliffs/Banks.

<img width="798" alt="Screenshot 2024-05-24 at 12 02 30" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/c0c14d1e-e812-4955-b76f-b839684df611">

## Recommendations
### Addressing Declining Car Crash Trends
While New Zealand has witnessed a progressive decline in car accidents from 2021 to early 2023, this trend should be actively sustained and enhanced. To achieve this, it is strongly recommended that the action plans outlined in the Road to Zero program are expedited and rigorously executed. This program has already laid a solid foundation for reducing road accidents and improving safety. By fast-tracking its implementation, New Zealand can expect to see even better outcomes in terms of minimising road accidents and their associated impacts.

Four primary factors influencing crash severities are street lighting, the number of lanes, speed limits, and road configuration. Addressing these factors is crucial to enhance road safety. To reduce the severity of accidents, it is recommended to invest in improved street lighting, particularly on roads with inadequate lighting. Moreover, attention should be given to road configuration, ensuring it accommodates safe and efficient traffic flow. Roads with two or more lanes should have extra precautions and safety measures in place to ensure safe lane changes and effective congestion management. Areas with high-speed limits should undergo speed reduction considerations and heightened speed enforcement to minimise the impact of accidents. Implementing these recommendations will not only make the roads safer but also reduce the severity of accidents, making New Zealand's roads more secure and less prone to fatal crashes.
### Tailoring Safety Interventions to Regional Specifics
Recognizing that the number of crashes and their severities vary significantly from one region to another, it is imperative to tailor safety interventions to the specific characteristics of each area. This includes accounting for local factors such as road conditions, speed limits, and population density. For instance, regions like Waikato and Auckland, with high population density, should have focused safety initiatives due to their higher fatality rates. Additionally, regions with speed limits of 100 km/h and above, associated with severe crash rates, should undergo targeted safety improvements. In contrast, areas like Northland, which exhibit the highest likelihood of severe crashes, should receive specialised attention, with improved emergency response strategies to minimise the impacts of accidents. Such localised approaches are essential for making road safety more effective and efficient.
### Addressing Holiday Period Accidents
To address the issue of increased accidents during holiday periods, several key recommendations are proposed. Firstly, there should be a collaborative effort with law enforcement agencies to enhance police presence on the roads during holiday seasons. This can be achieved through visible police patrols and the implementation of sobriety checkpoints, which can act as deterrents to reckless and impaired driving.

Secondly, launching comprehensive public awareness campaigns is crucial. These campaigns should emphasise safe driving practices during holidays, with a specific focus on the dangers of drunk driving, distracted driving, and speeding. Utilising various media channels, including social media, billboards, and radio, will enable these messages to reach a wide audience effectively.

Additionally, traffic flow management strategies, such as the use of variable message signs and traffic signal coordination, should be implemented to optimise traffic movement and reduce congestion during peak holiday travel times. Ensuring the availability of safe and well- lit rest areas along major travel routes is another important measure to combat driver fatigue, a significant factor in accidents.

Lastly, enforcing strict penalties for driving under the influence (DUI) offences during the holidays is imperative. Conducting sobriety checkpoints and increasing penalties for DUI convictions will act as strong deterrents against impaired driving.
### Addressing Hourly Period Accidents
Addressing the elevated number of accidents occurring between 15:00 PM and 18:00 PM requires a multifaceted approach involving various stakeholders, including government authorities, transportation agencies, schools, and the public.

This comprehensive strategy encompasses initiatives such as launching public awareness campaigns to educate drivers about the unique risks during this time frame, encouraging employers to provide workplace flexibility to reduce rush-hour congestion, investing in infrastructure improvements like widening roads and enhancing signage, implementing advanced traffic management systems for real-time optimization, working with schools to improve student transportation safety, increasing law enforcement presence to enforce traffic laws, exploring technological solutions like intelligent traffic signals, promoting seasonal safety measures, conducting thorough data analysis to pinpoint trends and areas of concern, and engaging the community in reporting and addressing traffic-related issues.

The ultimate aim is to establish a collaborative effort that effectively reduces accidents during this critical time period.

## Reference
Drivers Licence Holder. NZ Transport Agency Open Data. (n.d.).
https://opendata-nzta.opendata.arcgis.com/documents/driver-licence-holders/about

2018 Census place summaries. Stat NZ.(n.d.). https://www.stats.govt.nz/tools/2018-census-place-summaries/ . Retrieved 7 October, 2023

Road-to-Zero-strategy_final. NZ Transport Agency. December 2019.(n.d.). https://www.transport.govt.nz/assets/Uploads/Report/Road-to-Zero-strategy_final.pdf

Speed Limit. NZ Transport Agency Road Code.(n.d.). https://www.nzta.govt.nz/roadcode/heavy-vehicle-road-code/road-code/about-limits/speed- limits/

Demand and Activity. . NZ police. (n.d.). https://www.police.govt.nz/about-us/statistics-and- publications/data-and-statistics/demand-and-activity

Cas Data field descriptions. Waka Kotahi open data. (n.d.). https://opendata- nzta.opendata.arcgis.com/pages/cas-data-field-descriptions

Guide to treatment of crash locations - definitions - Waka Kotahi NZ (n.d.). https://www.nzta.govt.nz/assets/resources/guide-to-treatment-of-crash- location/docs/definitions.pdf

Varghese, D. (2018). Comparative Study on Classic Machine learning Algorithms. Towards Data Science. https://towardsdatascience.com/comparative-study-on-classic-machine-learning algorithms- 24f9ff6ab222

