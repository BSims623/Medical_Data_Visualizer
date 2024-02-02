import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('./medical_examination.csv')

# Add 'overweight' column
df['overweight'] = ((df.weight / ((df.height / 100)**2)) > 25).astype(int)
df.cholesterol = (df.cholesterol > 1).astype(int)
df.gluc = (df.gluc > 1).astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.


# Draw Categorical Plot
def draw_cat_plot():
  # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
  df_cat = df.melt(id_vars='cardio',
                   value_vars=[
                       'active', 'alco', 'cholesterol', 'gluc', 'overweight',
                       'smoke'
                   ])

  # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
  df_cat = pd.DataFrame(
      df_cat.groupby(['cardio', 'variable', 'value']).value_counts())

  # Draw the catplot with 'sns.catplot()'
  g = sns.catplot(data=df_cat,
                  kind='bar',
                  x='variable',
                  y='count',
                  col='cardio',
                  hue='value')
  g.set_axis_labels('variable', 'total')

  # Get the figure for the output
  fig = g.figure

  # Do not modify the next two lines
  fig.savefig('catplot.png')
  return fig


# Draw Heat Map
def draw_heat_map():
  # Clean the data
  df_heat = df[(df['ap_lo'] <= df['ap_hi'])
               & (df['height'] >= df['height'].quantile(0.025)) &
               (df['height'] <= df['height'].quantile(0.975)) &
               (df['weight'] >= df['weight'].quantile(0.025)) &
               (df['weight'] <= df['weight'].quantile(0.975))]
  # Calculate the correlation matrix
  corr = df_heat.corr()

  # Generate a mask for the upper triangle
  mask = np.triu(np.ones_like(corr))

  # Set up the matplotlib figure
  fig, ax = plt.subplots()

  # Draw the heatmap with 'sns.heatmap()'
  sns.heatmap(corr, annot=True, mask=mask, fmt=".1f", cmap='icefire')

  # Do not modify the next two lines
  fig.savefig('heatmap.png')
  return fig
