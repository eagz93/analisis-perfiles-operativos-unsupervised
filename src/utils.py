"""
Funciones auxiliares para el análisis de datos eléctricos
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple


def load_electrical_data(filepath: str) -> pd.DataFrame:
    """
    Carga el dataset de datos eléctricos y realiza conversión básica de tipos.
    
    Parameters:
    -----------
    filepath : str
        Ruta al archivo CSV
        
    Returns:
    --------
    pd.DataFrame
        DataFrame con los datos cargados
    """
    df = pd.read_csv(filepath)
    
    # Convertir FECHA a datetime
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    
    return df


def remove_constant_columns(df: pd.DataFrame, threshold: float = 0.0) -> Tuple[pd.DataFrame, List[str]]:
    """
    Elimina columnas con varianza cero o constantes.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame original
    threshold : float
        Umbral de varianza mínima (default 0.0)
        
    Returns:
    --------
    Tuple[pd.DataFrame, List[str]]
        DataFrame limpio y lista de columnas eliminadas
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    removed_cols = []
    
    for col in numeric_cols:
        if df[col].std() <= threshold:
            removed_cols.append(col)
    
    df_clean = df.drop(columns=removed_cols)
    
    return df_clean, removed_cols


def engineer_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea features temporales derivadas.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con columna 'FECHA' y 'HORA'
        
    Returns:
    --------
    pd.DataFrame
        DataFrame con nuevas columnas temporales
    """
    df = df.copy()
    
    # Features cíclicas para hora
    df['HORA_SIN'] = np.sin(2 * np.pi * df['HORA'] / 24)
    df['HORA_COS'] = np.cos(2 * np.pi * df['HORA'] / 24)
    
    # Día de la semana (0=lunes, 6=domingo)
    df['DIA_SEMANA'] = df['FECHA'].dt.dayofweek
    
    # Es fin de semana
    df['ES_FIN_SEMANA'] = (df['DIA_SEMANA'] >= 5).astype(int)
    
    # Franja horaria
    df['FRANJA'] = pd.cut(df['HORA'], 
                          bins=[0, 6, 12, 18, 24],
                          labels=['Madrugada', 'Mañana', 'Tarde', 'Noche'],
                          include_lowest=True)
    
    # Es hora pico (considerando horario industrial típico)
    df['ES_HORA_PICO'] = ((df['HORA'] >= 8) & (df['HORA'] <= 18)).astype(int)
    
    return df


def engineer_electrical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea features derivadas de variables eléctricas.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con variables eléctricas
        
    Returns:
    --------
    pd.DataFrame
        DataFrame con nuevas columnas eléctricas
    """
    df = df.copy()
    
    # Factor de potencia (si KVAHD > 0)
    df['FACTOR_POTENCIA'] = np.where(df['KVAHD'] > 0, 
                                      df['KWHD'] / df['KVAHD'], 
                                      0)
    
    # Desbalance de corriente (coeficiente de variación)
    corrientes = df[['IA', 'IB', 'IC']]
    df['CORRIENTE_MEDIA'] = corrientes.mean(axis=1)
    df['CORRIENTE_STD'] = corrientes.std(axis=1)
    df['DESBALANCE_CORRIENTE'] = np.where(df['CORRIENTE_MEDIA'] > 0,
                                          df['CORRIENTE_STD'] / df['CORRIENTE_MEDIA'],
                                          0)
    
    # Desbalance de voltaje (coeficiente de variación)
    voltajes = df[['VA', 'VB', 'VC']]
    df['VOLTAJE_MEDIO'] = voltajes.mean(axis=1)
    df['VOLTAJE_STD'] = voltajes.std(axis=1)
    df['DESBALANCE_VOLTAJE'] = np.where(df['VOLTAJE_MEDIO'] > 0,
                                        df['VOLTAJE_STD'] / df['VOLTAJE_MEDIO'],
                                        0)
    
    # THD promedio por fase
    thd_corriente = df[['THD_CORRIENTE_FASE_A', 'THD_CORRIENTE_FASE_B', 'THD_CORRIENTE_FASE_C']]
    df['THD_CORRIENTE_PROMEDIO'] = thd_corriente.mean(axis=1)
    
    thd_voltaje = df[['THD_VOLT_FASE_A', 'THD_VOLT_FASE_B', 'THD_VOLT_FASE_C']]
    df['THD_VOLTAJE_PROMEDIO'] = thd_voltaje.mean(axis=1)
    
    # Potencia reactiva aparente (aproximación)
    df['KVAR_APARENTE'] = np.sqrt(np.maximum(0, df['KVAHD']**2 - df['KWHD']**2))
    
    return df


def prepare_features_for_ml(df: pd.DataFrame, 
                            exclude_cols: List[str] = None,
                            scale: bool = True) -> Tuple[pd.DataFrame, StandardScaler]:
    """
    Prepara features numéricas para machine learning.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame original
    exclude_cols : List[str]
        Columnas a excluir (ej: identificadores, fechas)
    scale : bool
        Si se debe escalar con StandardScaler
        
    Returns:
    --------
    Tuple[pd.DataFrame, StandardScaler]
        DataFrame con features preparadas y scaler usado (o None)
    """
    if exclude_cols is None:
        exclude_cols = ['FECHA', 'INTERVALO', 'CATEGORIA', 'DENSIDADCARGA', 
                       'TIPO_INSTALACION', 'PT', 'CT', 'FRANJA']
    
    # Seleccionar solo columnas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    feature_cols = [col for col in numeric_cols if col not in exclude_cols]
    
    X = df[feature_cols].copy()
    
    # Manejar NaN e infinitos
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())
    
    scaler = None
    if scale:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    
    return X, scaler


def calculate_phase_imbalance(df: pd.DataFrame, 
                              phase_cols: List[str],
                              method: str = 'max_deviation') -> pd.Series:
    """
    Calcula el desbalance entre fases.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con columnas de fases
    phase_cols : List[str]
        Nombres de las columnas de fases
    method : str
        Método de cálculo: 'max_deviation' o 'coefficient_variation'
        
    Returns:
    --------
    pd.Series
        Serie con el desbalance calculado
    """
    phases = df[phase_cols]
    mean_val = phases.mean(axis=1)
    
    if method == 'max_deviation':
        max_dev = phases.max(axis=1) - phases.min(axis=1)
        imbalance = np.where(mean_val > 0, max_dev / mean_val, 0)
    else:  # coefficient_variation
        std_val = phases.std(axis=1)
        imbalance = np.where(mean_val > 0, std_val / mean_val, 0)
    
    return pd.Series(imbalance, index=df.index)


def get_cluster_statistics(df: pd.DataFrame, 
                          cluster_col: str,
                          feature_cols: List[str] = None) -> pd.DataFrame:
    """
    Calcula estadísticas descriptivas por cluster.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame con columna de clusters
    cluster_col : str
        Nombre de la columna de clusters
    feature_cols : List[str]
        Columnas para calcular estadísticas (None = todas numéricas)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame con estadísticas por cluster
    """
    if feature_cols is None:
        feature_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if cluster_col in feature_cols:
            feature_cols.remove(cluster_col)
    
    stats = df.groupby(cluster_col)[feature_cols].agg(['mean', 'std', 'min', 'max'])
    
    return stats


def detect_outliers_iqr(df: pd.DataFrame, 
                        columns: List[str] = None,
                        threshold: float = 1.5) -> pd.DataFrame:
    """
    Detecta outliers usando el método IQR.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame original
    columns : List[str]
        Columnas a analizar (None = todas numéricas)
    threshold : float
        Multiplicador del IQR (típicamente 1.5)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame booleano indicando outliers por columna
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    outliers = pd.DataFrame(index=df.index)
    
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        outliers[col] = (df[col] < lower_bound) | (df[col] > upper_bound)
    
    return outliers
