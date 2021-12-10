# -*- coding: utf-8 -*-
import scrapy
from artworks.items import ArtworksItem
import datetime
import re


# Any additional imports (items, libraries,..)


class TrialSpider(scrapy.Spider):
    name = 'dice_jobs'

    def __init__(self, job=None, location=None, *args, **kwargs):
        super(TrialSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.dice.com/jobs?q={job}&location={location}']

    base_url = 'https://www.dice.com'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url)

    def parse(self, response):
        job_details = response.xpath(
            "//a[@class='card-title-link bold']")
        print(len(job_details))
        for detail in job_details:
            job_id = detail.xpath('@id').extract_first()
            browse_url = detail.xpath('@href').extract_first()
            yield scrapy.Request(url=browse_url, callback=self.parse_art_work, meta= {'job_id': job_id})
        # next_page_tab = response.xpath("//a[contains(text(),'»')]/@href").extract_first()
        # if next_page_tab:
        #     next_page_url = self.base_url + next_page_tab
        #     yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_art_work(self, response):
        position = response.xpath(
            "//h1[@class='jobTitle']/text()").extract_first()
        company = response.xpath(
            "//li[@class='employer hiringOrganization']/span/text()").extract_first()
        location = response.xpath(
            "//li[@class='location']//text()").extract()
        location = ' '.join([x for x in location if x])
        salary = response.xpath(
            "//div[@class='iconsiblings']/span[@class='mL20']/text()").extract_first()
        description = response.xpath(
            "//p[strong[contains(text(),'Job Description')]]//following-sibling::p[1]/text()").extract_first()
        description2 = response.xpath(
            "//p[strong[contains(text(),'Job Description')]]//following-sibling::p[2]/text()").extract_first()
        description = description + ' ' + description2
        job_type = response.xpath(
            "//div[@class='iconsiblings']/span[not(@class)]/text()").extract_first()
        posted_date = response.xpath("//li[@class='posted ']//span/text()").extract_first()
        if posted_date and 'days' in posted_date:
            posted_date = re.search('[0-9]+', str(posted_date)).group()
            posted_date = (datetime.datetime.now() - datetime.timedelta(days=int(posted_date))).strftime('%Y-%m-%d')
        elif posted_date and 'hour' in posted_date:
            posted_date = re.search('[0-9]+', str(posted_date)).group()
            posted_date = (datetime.datetime.now() - datetime.timedelta(hours=int(posted_date))).strftime('%Y-%m-%d')
        skills = response.xpath("(//ul[preceding::*[contains(text(),'& Skills')]])[1]//li/text()").extract()
        if not skills:
            skills = response.xpath("(//text()[contains(.,'skills:')])[2]//following-sibling::ul/li/text()").extract()
        if skills:
            skills = ','.join([x for x in skills if x])
        else:
            skills = None
        if company:
            art_work_item = {
                'company': company,
                'description': description,
                'id': response.meta['job_id'],
                'job_type': job_type,
                'location': location,
                'posted_date':posted_date,
                'salary': salary,
                'position': position,
                'skills': skills
            }
            yield ArtworksItem(art_work_item)
