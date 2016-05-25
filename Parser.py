# ************************************************
#
# Student 1	: 150120059 - Cemal Fatih Kuyucu
# Student 2	: 150120014 - Meriç Turan
# Student 3	: 150110006 - Alperen Babagil
# 
# Course	: BLG 440E
# Term		: 2015-2016 Spring
# File		: Parser.py
# 
# *********************************************** #

#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
import re
from dateutil import parser
import json

DATA = {}

class chromium_crawler(scrapy.Spider):


	name = 'chromium_googlesource_com'
	start_urls = ['https://chromium.googlesource.com/chromium/src/']


	DOWNLOAD_DELAY = 0.00


	def parse(self, response):

		#unicode(response.body.decode(response.encoding)).encode('utf-8')
		
		next_link = response.css("a.LogNav-next::attr('href')").extract()
		commit_links = response.css(u"ol.CommitLog > li > a.u-sha1::attr('href')").extract()

		if len(next_link) == 1:
			yield scrapy.Request(response.urljoin(next_link[0]), self.parse)

		for commit_url in commit_links:
			yield scrapy.Request(response.urljoin(commit_url), self.parse_comitter)



	def parse_comitter(self, response):
		meta_data = response.css(u"div.u-monospace.Metadata > table > tr")
		author_meta_data = meta_data[1].css("td::text")
		committer_meta_data = meta_data[2].css("td::text")

		author = author_meta_data[0].extract()
		time_stamp = committer_meta_data[1].extract()
		time_stamp = parser.parse(time_stamp)
		diff_tree = response.css(u"ul.DiffTree > li > a::text").extract()

		for file in diff_tree:
			if not file in DATA:
				DATA[file] = []

			DATA[file].append({"Author" : author, "Time_Stamp" : str(time_stamp)})

				
	def closed(self, reason):
	
		Data_File = open("/home/CemalOdev/DATA.json", "w")
	
		Data_File.write(json.dumps(DATA))

