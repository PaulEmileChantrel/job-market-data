import pandas as pd
import json


# Methode to process a df given the csv file_name
# This will return mutiple df 
def process_data(file_name='data_analyst_toronto.csv'):
    # Loading the dataframe file
    df = pd.read_csv(file_name)
    print(df.shape[0])

    # We drop the job duplicates
    df = df.drop_duplicates(subset=['description','title','company_name','via']).reset_index(drop=True)
    print(df.shape[0])

    # Group by a columns name and get the number of item for each category
    # Order in descending order to get the top results first
    def get_top_n_from_col(df,col_name,n):
        new_df = df.groupby([col_name]).size().reset_index(name='counts').sort_values(by='counts',ascending=False).reset_index(drop=True)
        new_df = new_df[:n]
        print(new_df.head())
        return new_df

    # Get the top companies
    companies = get_top_n_from_col(df,'company_name',8)

    # Get the top job listing places
    via = get_top_n_from_col(df,'via',8)

    # Get the top job titles
    job_title = get_top_n_from_col(df,'title',8)

    # Next, we will look for key words in the job desriptions
    key_words = ['SQL','mySQL','Tableau','Python','Power BI', 'Azur','AWS','Hive','Excel','Visual Basic','R','Google Analytics','Omniture','Datorama','ETL','Tririga', 'Ariba', 'Coupa','BigQuery','Snowflake','Redshit','DAX','Java','JavaScript','HTML','CSS','API']
    key_word_dict = {}

    # Creating a dictionary to count the keywords
    for key in key_words:
        key_word_dict[key]=0

    # We also look for keywords regarding the type of work
    work = {'Hybrid':0,'Remote':0,'Office':0}

    # Looking for keywodrs in the df
    for i in range(df.shape[0]):
        description = df['description'][i]
        for k in key_words:
            if k in description:
                #We increase the count for the key word k by one when we have a match
                key_word_dict[k]+=1

        # We look for hybrid first, since hybrid job descriptions also often use the word remote
        if 'hybrid' in description.lower():
            work['Hybrid']+=1
        elif 'remote' in description.lower():
            work['Remote']+=1
        else:
            work['Office']+=1

    key_df = pd.DataFrame.from_dict(key_word_dict, orient='index',columns=['counts']).sort_values(by='counts',ascending=False)
    print(key_df[:8])

    work_df = pd.DataFrame.from_dict(work, orient='index',columns=['counts']).sort_values(by='counts',ascending=False)
    print(work_df.head())

    # Finnaly, we look for the different types of scheduals
    schedule_type = {}
    for i in range(df.shape[0]):
        extensions = df['detected_extensions'][i].replace("\'", "\"").replace('True','\"True\"').replace('–','-')

        #print(extensions)
        extensions = json.loads(extensions)

        if extensions.get('schedule_type'):
            job_schedual_type = extensions['schedule_type']
            if schedule_type.get(job_schedual_type) or schedule_type.get(job_schedual_type)==0:

                schedule_type[job_schedual_type] += 1
            else:
                schedule_type[job_schedual_type] = 0

    schedule_type_df = pd.DataFrame.from_dict(schedule_type, orient='index',columns=['counts']).sort_values(by='counts',ascending=False)
    print(schedule_type_df.head())

    # We return the different df
    return companies,via,job_title,key_df,work_df,schedule_type_df
