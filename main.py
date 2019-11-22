from indeed import get_last_page, extract_jobs
from save import save_to_file

last_page = get_last_page()
jobs = extract_jobs(last_page)
save_to_file(jobs)