from scrapy import Spider
from scrapy import Request
from ..items import NasdaqscrapeItem
import re




class NasdaqSpider(Spider):
    name = "nasdaq"

    start_urls = [
        "https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&pagesize=200&region=North+America&sortname=marketcap&sorttype=1&page=1"
    ]


    def parse(self, response):

        result_urls = [
            'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&pagesize=200&region=North+America&sortname=marketcap&sorttype=1&page={}'.format(x) for x in range(1, 4)]

        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)

    def parse_result_page(self, response):
        info_page_urls = response.xpath('//h3/a/@href').extract()

        for url in info_page_urls:
            yield Request(url=url, callback=self.parse_info_page)

    def parse_info_page(self, response):

        numeric_const_pattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
        rx = re.compile(numeric_const_pattern, re.VERBOSE)

        symbol = response.xpath('//*[@id="quotes-left-content"]/div[1]/span/b//text()').extract_first()
        price = rx.findall(response.xpath('//*[@id="qwidget_lastsale"]//text()').extract_first())
        industry = response.xpath('//*[@id="qbar_sectorLabel"]/a//text()').extract_first()

        bestBidAsk = str(rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[1]/div[2]//text()').extract_first())).split(",")
        if len(bestBidAsk) > 1:
            bestBid = rx.findall(bestBidAsk[0])
            bestAsk = rx.findall(bestBidAsk[1])
        else:
            bestBid = rx.findall(bestBidAsk[0])
            bestAsk = rx.findall(bestBidAsk[0])
        oneyeartarget = rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[2]/div[2]//text()').extract_first())

        todaysHighLow = str(rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[3]/div[2]//text()').extract_first())).split(",")
        if len(todaysHighLow) > 1:
            todaysHigh = rx.findall(todaysHighLow[0])
            todaysLow = rx.findall(todaysHighLow[1])
        else:
            todaysHigh = rx.findall(todaysHighLow[0])
            todaysLow = rx.findall(todaysHighLow[0])

        shareVolume = re.sub('[^0-9,]', "", response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[4]/div[2]//text()').extract_first())
        fiftyDayAvgVol = re.sub('[^0-9,]', "", response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[5]/div[2]//text()').extract_first())
        previousClose = re.sub('[^0-9,]', "", response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[6]/div[2]//text()').extract_first())

        fiftytwoHighLow = str(rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[7]/div[2]//text()').extract_first())).split(",")
        if len(fiftytwoHighLow) > 1:
            fiftytwoHigh = rx.findall(fiftytwoHighLow[0])
            fiftytwoLow = rx.findall(fiftytwoHighLow[1])
        else:
            fiftytwoHigh = rx.findall(fiftytwoHighLow[0])
            fiftytwoLow = rx.findall(fiftytwoHighLow[0])

        marketCapExtract = re.sub('[^0-9,]', "", response.xpath('//*[@id="left-column-div"]/div[1]/div[1]/div/div[8]/div[2]//text()').extract_first())
        marketCap = re.sub(r'[,\.]', '', marketCapExtract)

        pe_ratio = rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[2]/div/div[1]/div[2]//text()').extract_first())
        forward_pe_one_year = rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[2]/div/div[2]/div[2]//text()').extract_first())
        earnings_per_share = rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[2]/div/div[3]/div[2]//text()').extract_first())
        annualizedDiv = rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[2]/div/div[4]/div[2]//text()').extract_first())
        exDivDate = response.xpath('//*[@id="left-column-div"]/div[1]/div[2]/div/div[5]/div[2]//text()').extract_first()
        divPayDate = response.xpath('//*[@id="left-column-div"]/div[1]/div[2]/div/div[6]/div[2]//text()').extract_first()
        currentYield = rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[2]/div/div[7]/div[2]//text()').extract_first())
        beta = rx.findall(response.xpath('//*[@id="left-column-div"]/div[1]/div[2]/div/div[8]/div[2]//text()').extract_first())

        items = NasdaqscrapeItem()
        items['symbol'] = symbol
        items['price'] = price
        items['industry'] = industry
        items['bestBid'] = bestBid
        items['bestAsk'] = bestAsk
        items['oneyeartarget'] = oneyeartarget
        items['todaysHigh'] = todaysHigh
        items['todaysLow'] = todaysLow
        items['shareVolume'] = shareVolume
        items['fiftyDayAvgVol'] = fiftyDayAvgVol
        items['previousClose'] = previousClose
        items['fiftytwoHigh'] = fiftytwoHigh
        items['fiftytwoLow'] = fiftytwoLow
        items['marketCap'] = marketCap
        items['pe_ratio'] = pe_ratio
        items['forward_pe_one_year'] = forward_pe_one_year
        items['earnings_per_share'] = earnings_per_share
        items['annualizedDiv'] = annualizedDiv
        items['exDivDate'] = exDivDate
        items['divPayDate'] = divPayDate
        items['currentYield'] = currentYield
        items['beta'] = beta
        yield items