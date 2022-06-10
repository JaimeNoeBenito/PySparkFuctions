import pandas as pd
import nltk as nltk
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')


#Isolate and prepare the value (feature1) that will be use to predict the label 

if df.feature1.count()>0:

  df_tmp = df.feature1.drop_duplicates()
  df_tmp = pd.DataFrame(df_tmp)

  df_tmp['feature1BIS']=df_tmp.feature1.str.replace('-',' ')

  df_1_final=df_tmp.feature1BIS.drop_duplicates()
  df_labels_tmp=dfc['labelToPredict'].drop_duplicates()

  df_labels_tmp=pd.DataFrame(df_labels_tmp)

  df_labels_tmp['labelToPredictBIS']=df_labels_tmp.labelToPredict.str.replace('-',' ')
  df_label=df_labels_tmp.labelToPredictBIS.drop_duplicates()

  r=[]
  

  #Cosine algorithm 

  for i in df_1_final:
    X =str.upper(i)
    for y in df_label:
      Y =str.upper(y) 
      
      # tokenization 
      
      X_list = word_tokenize(X)  
      Y_list = word_tokenize(Y) 
      sw = stopwords.words('english') 
      l1 =[]
      l2 =[] 
      X_set = {w for w in X_list if not w in sw}  
      Y_set = {w for w in Y_list if not w in sw} 
      rvector = X_set.union(Y_set)  
      for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
      c = 0
      
      # cosine formula  
      
      for a in range(len(rvector)): 
        c+= l1[a]*l2[a] 
        cosine = c / float((sum(l1)*sum(l2))**0.5) 
        if cosine>0:
          r.append([i,y,cosine])
          
  #Generate new dataframe from the cosine algorithm

  if len(r)>0:

    x=pd.DataFrame(r)

    y=x.sort_values(by=[0,2])

    y=y.drop_duplicates(subset=[0],keep='last')

    y=y.rename(columns={0:'feature1BIS',1:'labelToPredictBIS',2:'RELATION'})

    y=y[y.RELATION>0.4]

    z=y.merge(df_tmp,how='inner',on='feature1BIS')

    z=z.drop(['feature1BIS'],1)

    z=z.merge(df_labels_tmp,how='inner',on='labelToPredictBIS')

    z=z.drop(['labelToPredictBIS'],1)

    #Add the LABEL ID value to the main dataframe

    df_final_labeId=df.merge(z,how='left',on='feature1')

    dfcm=dfc[['labelToPredict','LABELID']]

    dfcm=dfcm.drop_duplicates('LABELID')

    df_final_labeId=df_final_labeId.merge(dfcm,how='inner',on='labelToPredict')

    df_final_labeId=df_final_labeId.drop_duplicates(['list_of_fields_PK'])

    df_final_labeIdt=df_final_labeId[['list_of_fields_PK','feature1','labelToPredict']]

    df_final_labeId=df_final_labeId[['list_of_fields_PK','feature1','LABELID']]



# DBTITLE 1,Remove double quotes
df_final_labeId2 = df_final_labeId
for i, col in enumerate(df.columns):
    if(col == 'feature1'):
	df_final_labeId2.iloc[:, i] = df_final_labeId2.iloc[:, i].str.replace('"', '')
	df_final_labeId2.iloc[:, i] = df_final_labeId2.iloc[:, i].str.replace(',', '')


from datetime import datetime

timestamp = datetime.now().strftime("%Y_%m_%d")

filename="predictLabel_"+timestamp
    

#Generate the final csv file

df_final_labeId2.to_csv('your_path/{}.csv'.format(filenameid),header=True,index=False)