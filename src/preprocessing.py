import pandas as pd
import numpy as np

# Add time features from a datetime column
def add_time_features(df, datetime_col="fecha_hora"):
    df = df.copy()
    fecha_hora = pd.to_datetime(df[datetime_col], errors="coerce")

    return df.assign(
        **{
            datetime_col: fecha_hora,
            "fecha": fecha_hora.dt.normalize(),
            "mes": fecha_hora.dt.month,
            "dia": fecha_hora.dt.day,
            "hora": fecha_hora.dt.hour,
            "minuto": fecha_hora.dt.minute,
            "time": fecha_hora.dt.time,
        }
    )

# Análisis de regularidad de series temporales para detección de anomalías
def summarize_dataset(df, name):
    s = df['fecha_hora']
    if not np.issubdtype(s.dtype, np.datetime64):
        s = pd.to_datetime(s.astype(str).str.strip(), dayfirst=True, errors='coerce')

    s = s.dropna().sort_values().drop_duplicates()
    diffs = s.diff().dropna()
    expected = pd.Timedelta(minutes=15)

    return {
        'dataset': name,
        'rows': len(df),
        'unique_timestamps': len(s),
        'start': s.iloc[0] if len(s) else pd.NaT,
        'end': s.iloc[-1] if len(s) else pd.NaT,
        'constant_interval': diffs.nunique() == 1 if len(diffs) else False,
        'min_step': diffs.min() if len(diffs) else None,
        'max_step': diffs.max() if len(diffs) else None,
        'expected_step_15min': expected,
        'interval_counts': diffs.value_counts().sort_index().to_dict(),
        'parse_failures': df['fecha_hora'].isna().sum() if np.issubdtype(df['fecha_hora'].dtype, np.datetime64) else pd.to_datetime(df['fecha_hora'].astype(str).str.strip(), dayfirst=True, errors='coerce').isna().sum(),
    }

# Comprovacion de regularidad de registros a nivel diario
def daily_timestamp_quality(
    df,
    group_cols,
    datetime_col="fecha_hora",
    freq="15min"
):
    df = df.copy()
    df[datetime_col] = pd.to_datetime(df[datetime_col], errors="coerce")
    df["fecha"] = df[datetime_col].dt.normalize()

    observed = (
        df.groupby(group_cols + ["fecha"], as_index=False)
        .agg(
            registros_observados=(datetime_col, "nunique"),
            primer_timestamp=(datetime_col, "min"),
            ultimo_timestamp=(datetime_col, "max"),
        )
    )

    expected_per_day = int(pd.Timedelta(days=1) / pd.Timedelta(freq))

    observed["registros_esperados"] = expected_per_day
    observed["missing_timestamps"] = (
        observed["registros_esperados"] - observed["registros_observados"]
    )
    observed["pct_missing"] = (
        observed["missing_timestamps"] / observed["registros_esperados"]
    )

    return observed