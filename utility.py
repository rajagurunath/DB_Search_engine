from faker import Faker
import pandas as pd

def fake_data_generator(n_rows=100):
    fake = Faker()
    list_of_tuples=[]
    for _ in range(n_rows):
        list_of_tuples.append((fake.name(),fake.phone_number(),fake.address(),fake.email(),
                               ))
    return pd.DataFrame(list_of_tuples,columns=['name','PH','address','email'])
    


if __name__=='__main__':
     sample_df=fake_data_generator()   
     sample_df.to_csv('sample_data.csv',index=False)     