# Data

Datasets used in the solar power generation analysis project.

```text
data/
├── raw/
└── processed/
```

## `raw/`

Original datasets before cleaning or transformation.

* **Planta1_Generacion.csv**: inverter power generation data from Plant 1.
* **Planta2_Generacion.csv**: inverter power generation data from Plant 2.
* **Planta1_Sensores.csv**: meteorological and environmental data from Plant 1.
* **Planta2_Sensores.csv**: meteorological and environmental data from Plant 2.

## `processed/`

Processed analytical tables created from the raw data.

* **tablon_analitico_atmosferico.parquet**: meteorological and environmental data from Plant 1 and 2. It combines cleaned sensors data with new time variables at 15-minute intervals.
* **tablon_analitico_generacion.parquet**: inverter power generation data from Plant 1 and 2. It combines cleaned generation data with new time variables at 15-minute intervals.
* **tablon_analitico_diario.parquet**: Daily aggregated table combining both meteorological and generation datasets used to analyze broader patterns, ratios and performance trends over time.


## Note

Raw files are kept unchanged. Processed files are generated from the project notebooks.