from serpapi import GoogleSearch
import pandas as pd
import pprint
import config



def download_data(q):

    file_name = q.replace(' ','_')+'.csv'
    # try to load the file if it exist
    try:
        df = pd.read_csv(file_name,index_col=[0])
    except:
        print('Creating new DataFrame.')
        df = pd.DataFrame()

    def call_serapi(df,page,q):
        params = {
            "engine": "google_jobs",
            "q": q,
            "hl": "en",
            "api_key": config.ApiKey,
            }
        if page !=0: #stat = 0 does not work?
            params["start"]=page



        search = GoogleSearch(params)
        # Api call
        results = search.get_dict()
        #pprint.pprint(results["jobs_results"])
        try:
            jobs_results = results["jobs_results"]
        except:
            print(results)
            return df
        else:
            #print(len(jobs_results))

            df = pd.concat([df,pd.DataFrame(jobs_results)],ignore_index=True)
            df.drop_duplicates(subset=['job_id'],inplace=True,ignore_index=True)

            return df

    last_len = df.shape[0]
    for i in range(100):
        df = call_serapi(df,i,q)
        if last_len == df.shape[0]:
            break
        else:
            last_len = df.shape[0]
        print(last_len)


    print(df.shape[0])
    df.to_csv(file_name,index=False)

download_data('data analyst toronto')
#download_data('data scientist toronto')
#download_data('software developer toronto')
#download_data('python developer toronto')
#download_data('python toronto')
download_data('blockchain toronto')
