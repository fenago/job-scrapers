[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fenago/job-scrapers/HEAD)
<br />
You can install this project through following command: 

pip install -r requirements.txt

After installing you can run the scrapper using following command to get data in CSV file:

scrapy crawl trial -a job=any_job_type -a location=any_location_string -o filename.csv

example command to run this scrapper 


Just replace your spaces in string with %20 and add -a before location like below command:

scrapy crawl trial -a job="data%20analyst" -a location="fort%20lauderdale" -o indeed_jobs_data.csv



