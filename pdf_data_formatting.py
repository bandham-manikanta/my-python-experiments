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
