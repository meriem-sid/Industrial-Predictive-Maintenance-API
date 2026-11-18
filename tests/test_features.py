import pandas as pd
import numpy as np
import pandas.testing as pdt
from pdm.features import add_rolling_features
def test_future_cycles_do_not_affect_past_features():
#Build a tiny DataFrame for one engine
  data={
    'unit':[1,1,1,1,1],
    'cycle':[1,2,3,4,5],
    'sensor_1':[10,12,14,17,21],
    'sensor_2':[1,5,10,16,20]
  }

  df=pd.DataFrame(data)
  print(df)

  #Compute the features.
  features = ['sensor_1', 'sensor_2']

  df_features= add_rolling_features(df,features,window=2)
  print(df_features)

  #Change the sensor value at the last cycle and compute the features again.
  df_1=df.copy()

  df_1.loc[df_1.index[-1],'sensor_1'] = 100
  df_1.loc[df_1.index[-1], 'sensor_2'] = 200

  print(df_1['sensor_1'].iloc[-1])

  df_1_features= add_rolling_features(df_1,features,2)
  print(df_1_features)

  #Assert that the features for all earlier cycles are unchanged.
  earlier_before = df_features.iloc[:4]
  earlier_after = df_1_features.iloc[:4]

  pdt.assert_frame_equal(earlier_before, earlier_after)

# --- TEST 2: Features do not mix between different engines (units) ---
def test_features_do_not_mix_engines():
  data_multi = {
      'unit': [1, 1, 2, 2],
      'cycle': [1, 2, 1, 2],
      'sensor_1': [10, 20, 100, 200],
      'sensor_2': [5, 10, 50, 100]
  }
  df_multi = pd.DataFrame(data_multi)
  features = ['sensor_1', 'sensor_2']
  
  df_multi_features = add_rolling_features(df_multi, features, window=2)

  df_unit_2_isolated = df_multi[df_multi['unit'] == 2].copy()
  df_unit_2_isolated_features = add_rolling_features(df_unit_2_isolated, features, window=2)

  pdt.assert_frame_equal(
      df_multi_features[df_multi_features['unit'] == 2].reset_index(drop=True),
      df_unit_2_isolated_features.reset_index(drop=True)
  )