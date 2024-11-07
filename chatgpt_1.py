import json
import requests

import re
from unidecode import unidecode
from pdfminer.high_level import extract_text

pdf_path = r"C:\\Users\\mbandham\\Downloads\\_CEWIT Research Catalog 2019.pdf"
txt = extract_text(pdf_path)

def format_the_text(text):
    text = unidecode(text)
    text = text.replace('\n', ' ').replace('. (NSF)', '.')
    text = re.sub(r"@\s+", "@", text)
    text = re.sub(r"NETWORKS\s+\d+", "", text)
    text = re.sub(r"SECURITY\s+\d+", "", text)
    text = re.sub(r"IMAGING AND VISUALIZATION\s+\d+", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.split(r'ADVANCED COMPUTING SYSTEMS 69')[0]
    tt = re.split(r'(@stonybrook\.edu|@cs\.stonybrook\.edu)', text)
    text_splitted = [tt[i] + tt[i+1] if i+1 < len(tt) and tt[i+1] else tt[i] for i in range(0, len(tt), 2)]
    return text_splitted

def seperate_email_fname_last_name(input_text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    n_emails = re.findall(email_pattern, input_text)
    if len(n_emails) > 1:
        next_email = ';'.join(n_emails)
    else:
        next_email = n_emails[0]
    next_title = input_text.replace(next_email, '').strip()
    email_splitted = next_email.split('@')[0].split('.')
    if len(email_splitted) == 2 and len(n_emails) == 1:
        next_firstname = email_splitted[0].capitalize()
        next_lastname = email_splitted[1].capitalize()
    else:
        next_firstname = 'Professor'
        next_lastname = 'Professor'
    next_title = ''.join(next_title[: -2])
    return (next_email, next_firstname, next_lastname, next_title)

def get_data_prof_data(): 
    formatted_text = format_the_text(txt)
    next_title = formatted_text[0].split('Networks Secure Distributed ')[-1]
    next_title = 'Secure Distributed ' + next_title
    next_email, next_firstname, next_lastname, next_title = seperate_email_fname_last_name(next_title)
    very_last_content = formatted_text[-1]
    data = {}
    for x in range(1,len(formatted_text)-1):
        t_email, t_firstname, t_lastname, t_remaining_content = seperate_email_fname_last_name(formatted_text[x])
        t_title = t_remaining_content.split('.')[-1]
        current_content = t_remaining_content.replace(t_title, '')
        if next_email not in data:
            data[next_email] = (next_firstname, next_lastname, 'Project title: ' + next_title + ' : \n' + current_content)
        else:
            tt = data[next_email][2] + '\nProject title: ' + (next_title + ' : \n' + current_content)
            data[next_email] = (next_firstname, next_lastname, tt)
        next_email, next_firstname, next_lastname, next_title = (t_email, t_firstname, t_lastname, t_title)

    data[next_email] = (next_firstname, next_lastname, 'Project title: ' + next_title + ' : \n' + very_last_content)
    emails = []
    names = []
    project_titles = []
    for key, value in data.items():
        emails.append(key)
        names.append(value[0] + ' ' + value[1])
        project_titles.append(value[2])

    import pandas as pd
    df = pd.DataFrame({
        'Email': emails,
        "Name": names,
        "Project Title": project_titles
    })

    return df

# https://www.stonybrook.edu/commcms/cewit/work_with_us/index.php
# https://app.joinhandshake.com/stu/jobs/8306490?ref=preview-header-click&search_id=d286d605-0edf-4eea-83a1-e35cd333472b
# https://app.edenai.run/bricks/text/generation



def generate_email(prof_name, project_description):
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMDI1ODRjZTAtNTMyYy00N2IyLTkyZTYtYTMwODlmZWJjN2ZiIiwidHlwZSI6ImFwaV90b2tlbiJ9.tnUpIsQbRw8ojh4qeQscaP0nMYYbFepvGcj9lcA_xyk"}

    prompt = """"
        Write an email to professor inquiring any research assistant positions. 
        Please find the Professor's current project which is part of CEWIS below also attached my resume below.
        Please write email by showcasing my work experience and skillset according to the professor's project.
        Make sure to write a detailed email with my regards.
        Professor's research project: 
            professor name: {} \n
            {}.
        My resume:
            Manikanta Bandham
            Phone-Alt +1 (631)-730-0163 j Envelope manikanta.bandham@stonybrook.edu j LINKEDIN linkedin.com/in/bandhammanikanta
            EXPERIENCE
            Data Scientist Feb. 2021 – Jan 2024
            Ford Motor Company Chennai, India
             Designed and developed a use-case for large language models (LLMs) to validate the Compliance Demonstration
            Plan and Report (CDPR), thereby eliminating the need to manually review hundreds of pages of evidence files and
            reducing the risk of human errors. Utilized Google’s Text Bison model through Langchain.
             Ideated and Developed a model for forecasting the likelihood of employees leaving the company using Support Vector
            Machines. The model was packaged using Docker and deployed on the cloud using Kubernetes and Tekton.
             Implemented an Un-supervised NLP model for Topic identification and labeled 200k chat records, eliminated 900+
            hours of manual effort.
             Designed Analytical BI Dashboard to understand the Toxic Chemical usage trends in the manufacturing plants and
            developed & integrated a Machine learning model to forecast the Toxic Chemical usage for upcoming quarters and
            avoided $1.3M penalty annually to the company.
             Migrated an existing Alteryx Data wrangling Pipeline to BigQuery and reduced the processing time by 400%.
             Implemented Data pipelines using Dataflow with Python & Google BigQuery and processed 90M+ records.
            Software Engineer Jun. 2018 – Feb. 2021
            CenturyLink Bangalore, India
             Implemented an Angular-based Web Application as a Proof-of-Concept for an alternative to a Desktop-based
            Ticketing application and later released it to 50,000 users.
             Developed new ticketing creation flows into a Desktop-based ticketing application, which impacted 1.2M+ users.
             Designed Data Pipelines and ingested 50M+ records from multiple database systems into a Data lake using Alteryx.
            Software Engineer Dec 2015 – Jun. 2018
            UST Global Trivandrum, India
             Migrated existing Java-based Web services into GraphQL APIs and reduced the data query time by 120%
             Worked on an Angular Dashboard where users can log in and view their Credit reports, shipped it to 2M+ users.
             Built Rest endpoints using Java & Springboot to query the user PII information using Java and Spring boot.
            SKILLS
            Languages : Python, Java, Angular 4+ (typescript), SQL
            Databases : Google BigQuery, MYSQL
            Data Preprocessing : SQL, Google BigQuery-SQL, Alteryx
            Machine Learning : Large Language Models (LLM), Classification, Regression, & Clustering techniques
            Business Intelligence : QlikSense, Qlikview, Streamlit, Plotly, Dash
            Cloud/DevOps/MLops: Google Cloud Platform, Terraform, Kubernetes, Docker, Github, Tekton, VertexAI
            SKILLS
            Masters in Data Science - Stony Brook University, NY: Present
            Bachelor of Technology in Mechanical Engg. - Jawaharlal Nehru University, Ananthapuram: 77 %: 2011-2015
            ACHIEVEMENTS & EXTRACURRICULAR
             Ford-Google hackathon: 3rd winner for the use-case Battery Doctor and the solution is being validated and will be
            seen in upcoming cars.
             Hosted weekly Learning & Development sessions and coached teams on Python & Google Cloud tools at Ford.
             Awarded Asia Pacific Recognition for the success Employee Attrition Prediction project at Ford.
             Received the Execution Mindset award from the client at UST Global.
             I received a Gold medal for finishing in the top 1% in my undergraduate class of 60 students in 2015.
    """.format(prof_name, project_description)

    url = "https://api.edenai.run/v2/text/generation"
    payload = {
        "providers": "openai,cohere",
        "text": prompt,
        "temperature": 0.2,
        "max_tokens": 2048,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    print(result['openai']['generated_text'])
    
# generate_email()



df = get_data_prof_data()
