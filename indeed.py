import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

# 최대 페이지 개수 뽑아내기
def get_last_page():
    indeed_result = requests.get(URL)
    indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')
    pagination = indeed_soup.find('div', {"class":"pagination"})
    pages = pagination.find_all('a') # list

    spans = []
    for page in pages:
        spans.append(page.find('span').string) # string extract
    spans = spans[:-1]  # 맨 끝에 Next 제거
    spans = list(map(int, spans)) # list원소를 int형으로 변환
    max_page = max(spans)
    return max_page

def extract_job(html):
    title = html.find("div", {"class": "title"}).find("a")["title"] # attribute
    company = html.find("span", {"class": "company"})
    if company is None:
        print('에러 title:', title)
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip() # 공백 제거
    location = html.find("div", {"class": "recJobLoc"})['data-rc-loc'] # attribute
    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://www.indeed.com/viewjob?jk={job_id}"
    }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}..")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"}) # list
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
