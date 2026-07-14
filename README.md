# Solar Power Plant data quality and fault exploratory analysis

## Project overview
This project explores the operational data of two utility-scale solar power plants with the objective of reviewing data quality and identifying potential measurement anomalies.

The analysis follows a structured workflow, starting with data validation and exploratory analysis before progressively investigating sensor faults, inverter measurement issues and potential mismatches.

Although the dataset is publicly available, the complete analysis methodology, feature engineering, anomaly detection criteria and business conclusions were developed independently as part of this portfolio project.


## Business Context
Reliable operational data is essential for monitoring the performance of photovoltaic plants. Missing records, sensor failures or incorrect measurements can lead to inaccurate production estimates, delayed maintenance actions and unaccurate forecasting models.

For this reason, validating data quality is often the first step before a performance analysis, predictive maintenance or energy forecasting.


## Project Objectives
The main objectives of this analysis are:

- Review the overall quality of the available datasets.
- Identify missing records and temporal inconsistencies.
- Detect potential irradiation sensor failures.
- Detect inverter measurement anomalies.
- Prioritize the most critical inverter fault days that would require further inspection.
- Produce a technical report summarizing the main findings.

## Dataset description

### Analyzed Datasets
- Planta1_Generacion.csv: Inverter power generation data.
- Planta2_Generacion.csv: Inverter power generation data.
- Planta1_Sensores.csv: Meteorological and environmental data.
- Planta2_Sensores.csv: Meteorological and environmental data.

### Coverage Period
- Plants: P1, P2.
- Inverters per plant: 22.
- Start date: 15/05/2020.
- End date: 17/06/2020.
- Total duration: 34 days.
- Expected frequency: Measurements every 15 minutes (96 records/day).

## Repository Structure
```text
data/
├── raw/
├── processed/
notebooks/
reports/
├── graphics/
README.md
requirements.txt
```

## Methodology
The analysis followed a progressive investigation approach, where each finding guided the next stage of the analysis.
The workflow consisted of:

1. Data quality.
2. Time series validation.
3. Creation of the final datasets for the EDA Phase.
4. Exploratory Data Analysis (EDA).
    - Atmospherical sensors validation.
    - Irradiation vs Energy.
    - Irradiation vs Inverter DC Power.
    - Inverter AC Power vs DC Power correlation.
    - Inverter AC Power vs Energy.
    - Inverter measurement fault detection on critical days.
5. Inverter fault type analysis.
6. Inverter fault severity ranking.
8. Business interpretation of the detected anomalies.


## Analytical Techniques

The project combines several common data analysis techniques, including:

- Exploratory Data Analysis (EDA)
- Time-series analysis
- Feature engineering
- Correlation analysis (Pearson & Spearman)
- Robust statistical metrics (median and IQR)
- Anomaly detection
- Data quality assessment
- Fault severity ranking


## Assumptions & Limitations
Several assumptions were made during the analysis due to the limited contextual information available with the datasets.

- No maintenance logs were available to validate whether anomalies corresponded to actual equipment failures or scheduled shutdowns.
- The installed capacity of each plant was unknown.
- External meteorological data was not available for validation.
- Detected anomalies should therefore be interpreted as potential measurement issues rather than confirmed hardware failures.

## Dataset Validation
Before starting the exploratory analysis, the raw datasets were reviewed to identify inconsistencies that could affect the results.

### Confirmed Data Issues
#### Plant 1 DC Power Scale Mismatch
Plant 1 DC power values in `Planta1_Generacion.csv` were consistently **10× higher than expected** under equivalent operating conditions. Cross-validation against AC power and Plant 2 confirmed a decimal scale error. All Plant 1 DC power values were divided by 10 before the analysis.

#### Irregular Time Series Intervals
Both the generation and weather sensor datasets contain missing 15-minute timestamp records throughout the observation period. These gaps include missing inverter measurements, **particularly affecting four inverters in Plant 2**. To preserve the integrity of the original data, no interpolation was applied; instead, the missing intervals were retained and explicitly considered during the analysis. The impact of these gaps on individual inverters is examined later in the EDA phase.

### Assumptions Adopted
#### Irradiation Variable
The variable `irradiacion_wh_m2` from `Planta1_Sensores.csv` and `Planta2_Sensores.csv`shows values that are inconsistent with typical solar irradiation expressed in KWh/m². As no documentation about the sensor units was available, the variable was kept unchanged and treated as a relative irradiation indicator throughout the analysis. Consequently, irradiation analyses focus on temporal consistency and anomaly detection rather than absolute physical values.

## Exploratory Data Analysis Findings
Each insight presented below builds upon the previous one, following the same investigation process that would typically be carried out during a real exploratory data analysis project.

### Insight 1.1 - Missing Irradiation Records During Solar Hours in Plant 1

Missing irradiation records were detected during the main solar capture period (06:00–20:00) in Plant 1.

![15-Minute Irradiation Records on Critical Days](reports/graphics/irradiation_critical_days_15min.png)
*15-minute irradiation records during selected critical days. Missing daytime intervals can be clearly observed in Plant 1.*

The main gaps identified were:

1. **2020-05-19:** Missing records at 11:45, 12:00 and 12:45 during a high-irradiation period.
2. **2020-05-20:** Missing records from 13:30 to 17:15 (16 consecutive intervals).
3. **2020-05-21:** Missing records from 06:00 to 07:30, mainly during low-irradiation hours.
4. **2020-05-23:** Missing records from 06:00 to 06:30 at the beginning of the solar capture period.

These gaps affect the daily accumulated irradiation and any metric that depends on it.

---

### Insight 1.2 - Relationship Between High Performance Ratio and Irradiation Data Gaps

A visible relationship was found between unusually high Performance Ratio values and days with missing irradiation records during solar hours.

![Daily Performance Ratio by Plant](reports/graphics/daily_performance_ratio.png)
*Daily Performance Ratio by plant. Several of the highest PR values coincide with days affected by missing irradiation records.*

The clearest cases were observed on **May 18 and May 20**.

Since the Performance Ratio uses irradiation as part of its calculation, missing irradiation records can artificially increase its value.

This suggests that missing irradiation records are one of the main causes behind the abnormal PR values.

---

### Insight 1.3 - Severe Irradiation and DC Power Mismatch in Plant 2

The comparison between irradiation and DC Power revealed a clear mismatch in Plant 2. Plant 1 also shows some mismatches, although they are much more localized and mainly occur during periods of high irradiation.

![Irradiation vs DC Power by Plant](reports/graphics/dc_power_vs_irradiation.png)  
*Irradiation compared with DC Power in both plants. Plant 2 shows a severe mismatch, while Plant 1 presents only localized deviations.*

In Plant 2, similar irradiation levels often correspond to very different DC Power values, suggesting that the recorded power does not always follow the expected production pattern.

To determine whether the problem was related to inverter conversion, DC and AC Power were compared during these anomalous periods.

---

### Insight 2 - DC/AC Power Conversion Faults Discarded

DC and AC Power remain almost perfectly correlated, even during the anomalous periods detected previously.

The analysis was filtered using:

- **Irradiation threshold:** >16 Wh/m2
- **DC Power threshold:** <180 kW

Results:

- **Pearson correlation:** 1.000
- **Spearman correlation:** 1.000

This rules out faults in the DC-to-AC conversion process. The anomalies therefore originate before or during the measurement stage rather than during power transformation.

The next step was to analyze inverter behaviour at hourly resolution.

---

### Insight 3 - Different Inverter Anomalies detected at Hourly Level in Critical Days

A detailed review of representative critical days revealed different types of inverter anomalies.

![Hourly AC Power by Inverter - Plant 1](reports/graphics/ac_power_by_inverter_hourly_critical_days_plant_1.png)
*Hourly AC Power recorded by inverter during representative critical days in Plant 1.*

![Hourly AC Power by Inverter - Plant 2](reports/graphics/ac_power_by_inverter_hourly_critical_days_plant_2.png)
*Hourly AC Power recorded by inverter during representative critical days in Plant 2.*

Some representative examples are:

- **Plant 1 (2020-05-20):** All inverters are missing records during the same daytime interval.
- **Plant 2 (2020-05-15):** Several inverters show abnormal power measurements.
- **Plant 2 (2020-05-20):** Some inverters present missing records during specific hourly intervals.

These patterns suggest that not all anomalies share the same origin.

---

### Insight 3.1 - Measurement System Failures Confirmed

Some missing power records were identified as measurement failures rather than real production losses.
Although power measurements disappear temporarily, daily accumulated energy continues increasing, confirming that electricity was still being generated.

**Plant 1 (2020-05-20):**
| Hour  |   DC |   AC | Energy  |
| ----- | ---: | ---: | ------: |
| 13:00 | 1154 | 1126 |    5092 |
| 13:15 | 1133 | 1107 |    5333 |
| 17:30 |  171 |  168 |    8180 |
| 17:45 |  143 |  140 |    8204 |


This also explains why the daily average power becomes artificially lower:
- Daily power is calculated using the average of the available interval records.
- Daily energy is obtained from the maximum accumulated energy value recorded during the day.

Because of this, missing power records reduce the daily average while daily energy remains correct.

---

### Insight 3.2 - Inverter Shutdowns or Operational Faults Identified
A second type of anomaly was also detected.

**Plant 2 (2020-05-15):**
| Hour  |  DC |  AC | Energy  |
| ----- | --: | --: | ------: |
| 09:15 | 861 | 843 |    1378 |
| 09:30 | 262 | 256 |    1534 |
| 09:45 |   0 |   0 |    1541 |
| 10:00 |   0 |   0 |    1541 |

In these cases:
- DC Power equals zero.
- AC Power equals zero.
- Daily accumulated energy does not increase during the affected interval.

This indicates that the inverter stopped producing energy rather than simply failing to report measurements. The available information suggests either a planned shutdown or an operational fault. Since maintenance records are not available, the exact cause cannot be confirmed.

---

## Inverter Maintenance Priority Ranking

Two fault types were scored independently:

- **Missing records:** inverter with less than 50% of the median daily records during solar hours (06:00–20:00). Each affected day was weighted ×5.
- **Zero-power anomalies:** inverter power below 5% of the hourly median while the plant median exceeded 100 kW.

`Score = anomalous_hours + (absence_days × 5)`

![Inverter Fault Ranking](reports/graphics/inverter-fault-ranking_priority_review.png)
*Priority ranking of inverter faults based on missing records and anomalous zero-power events.*

Key findings:

- **Plant 1** shows mostly isolated and low-severity faults. Only two inverters require urgent review.
- **Plant 2** presents a much more critical situation, with **17 out of 22 inverters** showing persistent anomalies.
- The three most affected inverters (`Et9kgGMDl729KT4`, `LYwnQax7tkwH5Cb` and `Quc1TzYxW2pYoWX`) recorded anomalies on approximately **24–28 of the 34 analyzed days**.
- The number of affected inverters and the persistence of the faults suggest a broader measurement or operational issue rather than isolated inverter failures.


## Recommendations
Based on the findings, the following actions are recommended:

- Inspect the irradiation sensors, particularly in Plant 2.
- Investigate the root cause of repeated inverter shutdowns detected in Plant 2.
- Review the calibration and data acquisition systems.
- Validate the reported DC power measurements for the most affected inverters.
- Implement automatic monitoring rules to detect future measurement anomalies.
- Verify the detected events against maintenance logs before taking operational decisions.

## Future Work
Possible extensions of this project include:

- Integration with maintenance logs and weather information.
- Automated anomaly detection.
- Predictive maintenance models.
- Energy production forecasting.
- Long-term inverter reliability analysis.


## Conclusion
This project shows how exploratory data analysis can identify hidden data quality issues before building predictive models.

The investigation revealed widespread irradiation sensor failures, multiple inverter measurement anomalies and repeated inverter shutdowns, all of which could seriously affect any downstream analysis if left undetected.

Overall, Plant 2 presents significantly poorer data quality than Plant 1 and should be prioritised for technical inspection. More importantly, the project demonstrates the value of combining data validation, exploratory analysis and domain knowledge to distinguish between measurement problems and real operational faults.