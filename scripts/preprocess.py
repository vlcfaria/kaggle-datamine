import pandas as pd
import argparse

question_mapping = {
    'Q1': 'duration-seconds',
    'Q2': 'age-years',
    'Q3': 'gender',
    'Q4': 'country-residence',
    'Q5': 'student-status',
    'Q6': 'data-science-course-platforms',
    'Q7': 'helpful-first-data-science-products',
    'Q8': 'highest-formal-education',
    'Q9': 'published-academic-research',
    'Q10': 'research-used-machine-learning',
    'Q11': 'years-writing-code',
    'Q12': 'regular-programming-languages',
    'Q13': 'regular-ides',
    'Q14': 'hosted-notebook-products',
    'Q15': 'regular-data-visualization-libraries',
    'Q16': 'years-using-ml-methods',
    'Q17': 'regular-ml-frameworks',
    'Q18': 'regular-ml-algorithms',
    'Q19': 'regular-computer-vision-methods',
    'Q20': 'regular-nlp-methods',
    'Q21': 'pre-trained-model-download-services',
    'Q22': 'most-used-ml-model-hubs',
    'Q23': 'current-role-title',
    'Q24': 'current-employer-industry',
    'Q25': 'company-size',
    'Q26': 'individuals-responsible-for-data-science',
    'Q27': 'employer-incorporates-ml',
    'Q28': 'important-role-activities',
    'Q29': 'current-yearly-compensation-usd',
    'Q30': 'money-spent-on-ml-cloud-services-past-5-years-usd',
    'Q31': 'used-cloud-computing-platforms',
    'Q32': 'best-cloud-developer-experience',
    'Q33': 'used-cloud-computing-products',
    'Q34': 'used-data-storage-products',
    'Q35': 'used-data-products',
    'Q36': 'used-business-intelligence-tools',
    'Q37': 'regular-managed-ml-products',
    'Q38': 'used-automated-ml-tools',
    'Q39': 'used-ml-model-serving-products',
    'Q40': 'used-ml-model-experiment-monitoring-tools',
    'Q41': 'used-responsible-ethical-ai-products',
    'Q42': 'used-specialized-hardware-for-ml-training',
    'Q43': 'tpu-usage-count',
    'Q44': 'favorite-data-science-media-sources'
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help='input .csv', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.i)
    labels = df.iloc[0]
    df = df[1:]
    
    cols = [*df] #Assume cols are sorted
    top = int(cols[-1].split('_')[0][1:])

    for i in range(2, top+1):
        #Check if multiple answers
        if f'Q{i}' not in cols:
            #Find all choices
            multi = [col for col in df.columns if col.startswith(f'Q{i}_')]
            for c in multi:
                #Apply encoding
                df[c] = df[c].notnull().astype(int)
                
                #Rename
                value = labels[c].split('- ')[-1].lstrip()

                #Remove 'Other' values
                if value == 'Other' or value.startswith('None'):
                    df.drop(columns=[c], inplace=True)
                else:
                    df.rename(columns={c: c.split('_')[0]+ '_' + value}, inplace=True)
                

    df.to_csv('processed.csv', index=False)