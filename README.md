you can install this project through following command 

pip install -r requirements.txt

after installing you can run the scrapper using following command to get data in csv file

scrapy crawl trial -a job=any_job_type -a location=any_location_string -o filename.csv

example command to run this scrapper 

scrapy crawl trial -a job=Software%20Engineer -a location=america -o indeed_jobs_data.csv