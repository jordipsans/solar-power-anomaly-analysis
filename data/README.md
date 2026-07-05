# Data

Datasets used in the solar power generation analysis project.

```text
data/
├── raw/
└── processed/
```

## `raw/`

Original datasets before cleaning or transformation.

* **Planta1_Generacion.csv**: Inverter power generation data from Plant 1.
* **Planta2_Generacion.csv**: Inverter power generation data from Plant 2.
* **Planta1_Sensores.csv**: Meteorological and environmental data from Plant 1.
* **Planta2_Sensores.csv**: Meteorological and environmental data from Plant 2.

## `processed/`

Processed analytical tables created from the raw data.

* **tablon_analitico_preparado.pkl**: Main analytical table. It combines cleaned generation and sensor data at 15-minute intervals.
* **tablon_analitico_diario.pkl**: Daily aggregated table used to analyze broader patterns and performance trends over time.

## Note

Raw files are kept unchanged. Processed files are generated from the project notebooks.