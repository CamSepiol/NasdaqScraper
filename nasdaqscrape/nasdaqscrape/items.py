# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NasdaqscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    symbol = scrapy.Field()
    marketCap = scrapy.Field()
    bestBid = scrapy.Field()
    bestAsk = scrapy.Field()
    todaysHigh = scrapy.Field()
    todaysLow = scrapy.Field()
    shareVolume = scrapy.Field()
    fiftyDayAvgVol = scrapy.Field()
    previousClose = scrapy.Field()
    fiftytwoHigh = scrapy.Field()
    fiftytwoLow = scrapy.Field()
    annualizedDiv = scrapy.Field()
    exDivDate = scrapy.Field()
    divPayDate = scrapy.Field()
    currentYield = scrapy.Field()
    price = scrapy.Field()
    industry = scrapy.Field()
    oneyeartarget = scrapy.Field()
    pe_ratio = scrapy.Field()
    forward_pe_one_year = scrapy.Field()
    earnings_per_share = scrapy.Field()
    beta = scrapy.Field()

