#!/usr/bin/env python
# coding: utf-8

# **<h1> Mortality Predictions in ICU using ANN** 
#     
# Patients admitted to the ICU suffer from critical illness or injury and are at high risk of dying. ICU mortality rates differ widely depending on the underlying disease process, with death rates as low as 1 in 20 for patients admitted following elective surgery, and as high as 1 in 4 for patients with respiratory diseases. The risk of death can be approximated by evaluating the severity of a patient’s illness as determined by important physiologic, clinical, and demographic determinants.

# ![title](heart.png)

# In[1]:


# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

# Handle table-like data and matrices
import numpy as np
import pandas as pd
import math 
from sklearn.metrics import accuracy_score

from sklearn.model_selection import train_test_split
import keras

# Visualisation
import matplotlib.pyplot as plt
import seaborn as sns

# Configure visualisations
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style( 'white' )


# In[2]:


df = pd.read_csv('train.csv', encoding = 'utf-8')


# In[3]:


labels = pd.read_csv('labels.csv', encoding = 'utf-8')


# **<h2> Exploratory Data Analysis**
# 
# Henceforth, we will be doing the exploratory data analysis in order to identify the significant parameters contributing to the mortality rate and neglecting the rest.

# In[4]:


df.head()


# In[5]:


df.columns


# In[6]:


df.shape


# In[7]:


df.info()


# In[8]:


df.describe()


# In[9]:


labels.shape


# In[10]:


labels


# In[11]:


labels["In-hospital_death"].value_counts()


# In[12]:


#One Hot encoding
temp  =[]
for i in labels["In-hospital_death"]:
  if i == 0:
    temp.append([1,0])
  else:
    temp.append([0,1])
temp = np.array(temp)


# In[13]:


print(temp.shape)


# In[14]:


new = pd.concat([df , labels] , axis = 1)
print(new.shape)


# **<h3>Using Correlation heatmap to find important features and their relations with other features.**

# In[15]:


correlation_map = new[new.columns].corr()
obj = np.array(correlation_map)
obj[np.tril_indices_from(obj)] = False
fig,ax= plt.subplots()
fig.set_size_inches(25,18)
sns.heatmap(correlation_map, mask=obj,vmax=.7, square=True,annot=True)


# In[16]:


new_df = new.drop(['In-hospital_death'] , axis =1)
new_df.shape


# In[17]:


df = new_df


# In[18]:


df = df.drop(['Gender','Cholesterol','HCT','ICUType','Height'] , axis =1)


# **<h3> Scaling Data**

# In[19]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
df = scaler.fit_transform(df)


# **<H2> Deep Learning Model**
# 
# Dataframe df will be given as X parameter and Inhospitaldeath case will be given as Y.

# In[20]:


X = df
y = temp


# In[21]:


print(X.shape , y.shape)


# **<h3>Splitting Dataset**

# In[22]:


X_train , X_test , y_train , y_test  = train_test_split(X , y , test_size = 0.2)


# In[23]:


print(X_train.shape,X_test.shape,y_train.shape,y_test.shape)


# Importing necessary files.

# In[24]:


from keras.models import Sequential
from keras.layers import Dense, Dropout , BatchNormalization
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.optimizers import RMSprop, Adam


# **<h3> Building ANN Model**

# In[25]:


model = Sequential()

model.add(Dense(64, input_dim=X_train.shape[1] , activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(196, activation='relu'))
model.add(Dense(196, activation='relu'))

model.add(BatchNormalization())

model.add(Dense(256, activation='relu'))
model.add(Dense(2, activation='sigmoid'))

model.compile(optimizer = Adam(lr = 0.0005),loss='binary_crossentropy', metrics=['accuracy'])
print(model.summary())


# **<h3> Fitting the model**
# 

# In[38]:


history = model.fit(X_train, y_train , epochs=20 , batch_size = 128 , validation_data=(X_test, y_test))


# **<h3> Evaluating Performance using Accuracy ,Loss and Confusion Matrix**
# 
# 

# In[39]:


print(history.history.keys())


# In[40]:


plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


# In[41]:


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


# In[42]:


from sklearn.metrics import confusion_matrix
#prediction
pred = model.predict(X_test)
pred = np.argmax(pred,axis = 1) 
y_true = np.argmax(y_test,axis = 1)


# In[43]:


cnf_matrix = confusion_matrix(y_true, pred)
print(cnf_matrix)


# In[44]:


print(accuracy_score(y_true,pred))


# In[ ]:




