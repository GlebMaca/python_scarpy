import scrapy
import codecs
import csv
import datetime


class AuthorSpider(scrapy.Spider):
    name = 'author'
    filename = ''
  
    produ_url=''
    product_type=''

    


    start_urls = ['https://nevir.es/']

    def parse(self, response):
        self.filename = 'product_' + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '.csv'
        header = [
        'model','brand','product','product_parent', 'file_urls', 'type',"ean", 'url','thumb',"source"
        
        ]

        with open(self.filename, 'wb') as fp:
            fp.write(codecs.BOM_UTF8)

        with open(self.filename, 'a', newline='') as fp:
            csv.writer(fp).writerow(header)

        for quote in response.css('.menu-item-object-product_cat '):

            if(quote.css('ul')): 
                yield {'subname':quote.css('a::attr(href)').get()}
            else:
                self.product=quote.css('a::text').get()
                url=quote.css('a::attr(href)').get()
                yield {'suburl':quote.css('a::attr(href)').get()}
                yield scrapy.Request(url, self.parse_author) 
    
        # yield from response.follow_all(author_page_links, self.parse_author)
       
        # # pagination_links = response.css('li.next a')
        # # yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).getall()
        for product_url in  extract_with_css('h6.edgtf-product-list-title a::attr(href)'):
           
            yield scrapy.Request(product_url, self.parse_get_content) 
    def parse_get_content(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        def sliceindex(x):
            i = 0
            for c in x:
                if c.isalpha():
                    i = i + 1
                    return i
                i = i + 1

        def upperfirst(x):
            i = sliceindex(x)
            return x[:i].upper() + x[i:]
        manual_url=''
        file_url=''
        fontname=''
        file_urls= response.css('a[href*="pdf"]::attr(href)').getall()
    
        image_url=response.css('div.woocommerce-product-gallery__image a img').attrib['src']
        product_name=extract_with_css('h2.edgtf-single-product-title::text')

        categories=response.css('span.posted_in a::text').getall()
        # self.product=categories[0]
        # self.product_parent= categories[1]
        # if(self.product=="TELEVISORES"):
        #     self.product=categories[1]
        #     self.product_parent= categories[0]

        ean_number=''

     
        product_url=response.url
        url_array=product_url.split('/')
        array_len=len(url_array)
        product_str=url_array[array_len-3]
        product_array=product_str.split('-')
        product=""
        for product_item in product_array:
            product_item=upperfirst(product_item)
            product=product+product_item+" "
        yield{'product':product}
        product_parent_str=url_array[array_len-4]
        product_parent_array=product_parent_str.split('-')
        product_parent=""
        for product_parent_item in product_parent_array:
            product_parent_item=upperfirst(product_parent_item)
            product_parent=product_parent+product_parent_item+" "

        file_pdfs=response.css('a[href*=".pdf"]')
            # file_pdf_url=file_pdf.attrib['href']
            # file_type=file_pdf.css('::text').get()
            # yield{"file_pdf_url":file_pdf_url,"file_type":file_type,'array':url_array}

        
        for item in response.css('li::text').getall():
            if item[:4]=="EAN:":
                ean_number=item[5:]  
            elif item[:3]=="EAN": 
                ean_array=item.split(':')
                ean_number=ean_array[1]
        with open(self.filename, 'a', newline='', encoding='utf-8') as fp:
         

            for file_pdf in file_pdfs:
                file_pdf_url=file_pdf.attrib['href']
                file_type=file_pdf.css('::text').get()
                # yield{"file_pdf_url":file_pdf_url,"file_type":file_type,'array':url_array}      
                row = [
                    product_name,
                    "Nevir",                   
                    product,
                    product_parent,
                    file_pdf_url,      
                    file_type,              
                    ean_number ,
                    product_url,
                    image_url, 
                    "nevir.es"               

                ]
                
               
                print(row)
                csv.writer(fp).writerow(row)
