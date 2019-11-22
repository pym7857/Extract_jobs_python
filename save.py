import csv

def save_to_file(jobs):
    file = open("jobs.csv", "w", -1, "utf-8") # refresh
    print(file)
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values())) # dict형태에서 values만 list형태로 가져온다.
    return