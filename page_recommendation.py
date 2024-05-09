import time
import streamlit as st
import pdf2doi
import os
import tempfile
from paper import Paper
import requests
def recommendation_api(paper_doi):
    paper = '10.1021/acs.jmedchem.0c00013'
    url = f'https://api.semanticscholar.org/recommendations/v1/papers/forpaper/doi:{paper_doi}'
    query_params = {'fields': 'title,url,year,authors,isOpenAccess', 'limit': '5'}
    api_key = ''  # Replace with the actual API key
    headers = {'x-api-key': api_key}
    papers = []
    # Send the API request
    response = requests.get(url, params=query_params, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        # Process and print the response data as needed
        for paper in  response_data['recommendedPapers']:
            paper = Paper(**paper)
            papers.append(paper)
        return papers
    else: 
        None


pdf2doi.config.set('verbose',False)
# pdf2doi.config.print()

# File uploader
uploaded_files = st.file_uploader(
    "Upload PDF files", type="pdf", accept_multiple_files=True
)
# with st.container():

l_btn = []
def write_table_recommendations(papers:list[Paper], org_title):
    global l_btn

    papers = [Paper('1', 'url', 'year', [{'name':'dddd'}], True,'id',{'url':'https://pubs.acs.org/doi/pdf/10.1021/acs.jmedchem.4c00168'}),
              Paper('2 3dddddd', 'url', 'year', [{'name':'dddd'}], True,'id',{'url':'https://pubs.acs.org/doi/pdf/10.1021/acs.jmedchem.4c00168'}),
              Paper('titlewo dddddd', 'url', 'year', [{'name':'dddd'}], True,'id',{'url':'https://pubs.acs.org/doi/pdf/10.1021/acs.jmedchem.4c00168'})]
    #   self.paperId = paperId
    #   self.title = title
    #   self.url = url 
    #   self.year = year 
    #   self.authors = [name['name'] for name in authors]
    #   self.isOpenAcess = isOpenAccess

    # colms = st.columns((1))
    container = st.container(border=True)


    colms = st.columns((4, 1, 1, 1, 1))
    fields = ["Title", 'URL', 'year', 'authors', "Download"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)
    
    print(len(papers))
    for i, paper in enumerate(papers):
        if (not paper.isOpenAcess):
            continue
        col1, col2, col3, col4, col5  = colms
        col1.write(paper.title)
        col2.write(paper.url)
        col3.write(paper.year)
        col4.write(', '.join(paper.authors))
        url_pdf = paper.openAccessPdf
        if url_pdf:
            button_phold = col5.checkbox('',key=len(l_btn))  # create a placeholder
            l_btn.append({'pdf_url':url_pdf,'btn_ref':button_phold, 'title':paper.title, 'org_title': org_title})
        # button_type = "⬇️"
        # do_action = button_phold.button(button_type, key=i)
        # if do_action:
        #      button_phold.empty()  #  remove button


for uploaded_file in uploaded_files:
    st.write("filename:", uploaded_file.name)
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
            f.write(uploaded_file.getvalue())

    # results = pdf2doi.pdf2doi(os.path.join(path))
    results = {'identifier': 'lol'}
    if results:
        st.write("DOI", results['identifier'])
        with st.spinner('Wait for it...'):
            # recommended_papers = recommendation_api(results['identifier'])
            recommended_papers = 'dd'
        if recommended_papers:
            st.success('Recomendations found')
            write_table_recommendations(recommended_papers, uploaded_file.name)
        else:
            st.error('No recommendations found')


if (l_btn):
    if st.button('Download'):
        # check_if_any_enable = bne
        # if l_btn.any():
            with st.spinner('Wait for it...'):
                for btn_pack in l_btn:
                    if btn_pack['btn_ref']:
                        headers = {
                            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0"
                        }
                        r = requests.get(btn_pack['pdf_url'], headers=headers)
                        print(btn_pack['pdf_url'])
                        new_folder = f'RecommendedPdf/{btn_pack['org_title'].replace('.pdf','')}'
                        os.makedirs(new_folder, exist_ok=True)
                        with open(f'{new_folder}/{btn_pack['title']}.pdf', 'wb') as fd:
                            fd.write(r.content)
            st.success('Files downloaded')
