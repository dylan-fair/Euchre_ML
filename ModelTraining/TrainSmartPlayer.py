import tensorflow as tf
import pandas as pd
import numpy as np
import ast
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, LSTM, Flatten, Dropout
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score



final_df = pd.read_csv('TrainingData/final_training_set.csv')

feature_list = ['card1_suit','card1_rank','card2_suit',
                'card2_rank','card3_suit','card3_rank',
                'card4_suit','card4_rank','card5_suit',
                'card5_rank','card_played_suit',
                'card_played_rank','position','trump',
                'leading_suit']

X_df = np.array(final_df[feature_list]).astype(np.float32)

#given the dealer card, the player's hand, and their action (hit or stay) was that the correct choice?
#for my model predition, i will default to my input being the dealer card, the player's hand, and they hit
#the question will be was it the correct decision.  if so, then cozmo should hit.  if not, then cozmo should stay.
#again, your reasoning might be different.  again, make sure that your data is in a form that can
#be converted to a tensor

# y_df = np.array(final_df['outcome']).astype(np.float32).reshape(-1,1)
y_df = final_df['label']

X_train, X_test, y_train, y_test = train_test_split(X_df, y_df, test_size = 0.2)


model = Sequential()
model.add(Dense(16, activation='relu'))
model.add(Dense(128))
model.add(Dense(32, activation='softmax'))
model.add(Dense(8))
model.add(Dense(1, activation='tanh'))
model.compile(loss='mean_squared_error', optimizer='sgd')

model.fit(X_train, y_train, epochs=6, batch_size=512, verbose=1)

pred_Y_test = model.predict(X_test)
#also get the actual results so we can compare
actuals = y_test

# Evaluate the model
mse = mean_squared_error(y_test, pred_Y_test)
mae = mean_absolute_error(y_test, pred_Y_test)
r2 = r2_score(y_test, pred_Y_test)

# Print the metrics
print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)
print("R-squared:", r2)


model.save('Models/card_choice_model.keras')




