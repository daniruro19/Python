import scrapy


class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&ref_=adv_prv']
    base_url  = "https://www.imdb.com"
    cont=0

    #funcion generadora

    def parse(self, response):
        movies=response.css("div.lister-item > div.lister-item-content")
        next_page=response.css(".nav a.next-page::attr(href)").get()

        for movie in movies:
            title=movie.css("h3.lister-item-header > a::text").get()
            number=movie.css("h3.lister-item-header > span.lister-item-index::text").get()
            actores=movie.css("p > a::text").getall()

            href=movie.css("h3.lister-item-header > a::attr(href)").get()
            title_link=self.base_url + href

            yield response.follow(url= title_link, callback=self.parse_reviews, meta = {'number': number, 'titulo':title, 'cast':actores})

        if self.cont < 5 :
            self.cont+=1
            yield response.follow(url = next_page, callback=self.parse)
                
    def parse_reviews(self, response):
        reviews= response.css("ul.sc-3ff39621-0 .score::text").getall()
        

        print("MOVIE:",response.meta.get("number"),response.meta.get("titulo"),response.meta.get("cast"),reviews)
