import os
import pandas as pd
import glob
import numpy as np

# use your path
path = '/Users/your file data location/'                     
all_files = glob.glob(os.path.join(path, "*.csv"))     

df_single = []
for f in all_files:
    df = pd.read_csv(f)
    #Open field test is 5 minutes and every second is made by 30 frames which lead to 9000 (30 f per sec * 60 sec * 5 min), 
    # In here we added this limitation of 9000 in row index to eliminate the 
    #rest of the open field test vedio in that mostly are more than 5 minutes_ we tried to correct it. 
    df2= df.drop(df.index[np.where(df.index > 9000)])
    acceleration = np.zeros(len(df2))
    # the following multiplied number 3/10 is representing the coefficient of 1 second equal with 30 frame and 1cm=1/100 meter.  
    df2['Velocity'] = df2['Distance_cm']*(3/10)
    #in the range we drop the frame zero which is rational and should be included.
    for i in range(1, 9000):
        acceleration[i] = (df2.loc[i+1, 'Velocity'] - df2.loc[i, 'Velocity'])*30
    df2['Acceleration'] = acceleration
    df2 = df2[['Frame','ROI_location','ROI_transition','Distance_cm', 'Velocity', 'Acceleration']]
    df_single.append(df2)

# Concatenate the individual DataFrames into a single DataFrame
concatenated_df = pd.concat(df_single, axis=0)

# Drop the rows with an index greater than 8999

concatenated_df.to_csv('/Users/yourfilelocation for save /output.csv', index=False)

#Print the value counts of the ROI_location column to check for rows with multiple values
#print(concatenated_df['ROI_location'].value_counts())
