import scrapy
import codecs
import csv
import datetime
from tutorial.items import Manual

class AllenSpider(scrapy.Spider):
    name = 'allen'
    filename = ''
    product_name=''
    produ_url=''
    product_type=''


    start_urls = ['https://www.allen-heath.com/products/']

    def parse(self, response):
        self.filename = 'product_' + str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) + '.csv'
        header = [
        'model','brand','product','product_parent', 'file_urls', 'type',"ean", 'url','thumb',"source"
        
        ]

        with open(self.filename, 'wb') as fp:
            fp.write(codecs.BOM_UTF8)

        with open(self.filename, 'a', newline='') as fp:
            csv.writer(fp).writerow(header)

        for quote in response.css('.seriesop'):

            # if(quote.css('ul') is not None): 
            #     yield {'subname':quote.css('a::attr(href)').get()}
            # else:
                # self.product=quote.css('a::text').get()

            product = response.css('.seriesop a img::attr("alt")').get()

            url=quote.css('a::attr(href)').get()
            if(url == "/dlive-home/" or url == "/avantis/" or url == "/sq-series/" or url == "/key-series/qu-series/" or url == "/ahm-64/" ):
                yield scrapy.Request('https://www.allen-heath.com'+url, self.parse_sub, cb_kwargs=dict(product=product))

            else:
                yield scrapy.Request(url, self.parse_sub, cb_kwargs=dict(product=product))

            yield {'url': url}
            # yield {'suburl':quote.css('a::attr(href)').get()}
            # yield {'suburl':url}
                
            

    def parse_sub(self, response, product):

        # def extract_with_css(query):
        #     return response.css(query).getall()
        for quote in response.css('.mega-menu-item-object-ahproducts'):

            # if(quote.css('ul') is not None): 
            #     yield {'subname':quote.css('a::attr(href)').get()}
            # else:
                # self.product=quote.css('a::text').get()
            sub_url=quote.css('a::attr(href)').get()
            product_name = quote.css('a::text').get()
            product = product
            # yield {'suburl':quote.css('a::attr(href)').get()}
            # yield {'suburl': sub_url}
                
            yield scrapy.Request(sub_url, self.parse_get_content,  cb_kwargs=dict(product_name=product_name, product=product)) 

    # def parse_author(self, response):

    #     def extract_with_css(query):
    #         return response.css(query).getall()
    #     for product_url in  extract_with_css('div.product-image p a::attr(href)'):
           
    #         yield scrapy.Request(product_url, self.parse_get_content) 
    def parse_get_content(self, response, product_name, product):

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
        # print(response.css('div.prodocs div.docdetails h5 a[href*="pdf"]::attr(href)').getall().text);
        # if(response.css('div.prodocs div.docdetails h5 a[href*="pdf"]::attr(href)').getall().toString().find('Guide') > 0):
        file_urls= response.css('div.prodocs div.docdetails h5 a[href*="pdf"]::attr(href)').getall()

        print(file_urls)
        image_url=response.css('div#productcontent:nth-child(1) div.row p img').attrib['src']
        yield{ "image_url":image_url}
        product_name = product_name
        product = product
        # for quote in response.css('.mega-menu-item-object-ahproducts'):

        #     if(quote.css('a::attr(href)').get() == response.url):
        #         product_name = quote.css('a::text').get()
                # print(product_name)
       

        # product_name=extract_with_css('h1:first-child::text')

        # categories=response.css('span.posted_in a::text').getall()
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
        # product=""
        # for product_item in product_array:
        #     product_item=upperfirst(product_item)
        #     product=product+product_item+" "
        
        product_parent_str=url_array[array_len-4]
        product_parent_array=product_parent_str.split('-')
        product_parent=""
        for product_parent_item in product_parent_array:
            product_parent_item=upperfirst(product_parent_item)
            product_parent=product_parent+product_parent_item+" "

        file_pdfs=response.css('h5 a[href*=".pdf"]')
        print(file_pdfs)
            # file_pdf_url=file_pdf.attrib['href']
            # file_type=file_pdf.css('::text').get()
            # yield{"file_pdf_url":file_pdf_url,"file_type":file_type,'array':url_array}

        
        # for item in response.css('li::text').getall():
        #     if item[:4]=="EAN:":
        #         ean_number=item[5:]  
        #     elif item[:3]=="EAN": 
        #         ean_array=item.split(':')
        #         ean_number=ean_array[1]
        # with open(self.filename, 'a', newline='', encoding='utf-8') as fp:
         
 # 'model','brand','product','product_parent', 'file_urls', 'type',"ean", 'url','thumb',"source"
       
        for file_pdf in file_pdfs:
            file_pdf_url=file_pdf.attrib['href']
            file_type=file_pdf.css('::text').get()
            yield{"file_pdf_url":file_pdf_url,"file_type":file_type,'array':url_array}      
            row = [
                product_name,
                "Allen & Heath",                   
                product,
                product_parent,
                file_pdf_url,      
                file_type,              
                ean_number ,
                product_url,
                image_url, 
                "allen-heath.com"               

            ]
            manual = Manual()
            
            manual['brand'] = 'Allen & Heath'
            manual['model'] = product_name
            manual['model_2'] = ''
            manual['product'] =product
            manual['product_parent']=product_parent
            manual['product_lang'] = 'en'

            manual['file_urls'] =  file_pdf_url 
            manual['type'] = file_type
            manual['files'] = []
            manual['eans']=ean_number

            manual['thumb'] = image_url
            manual['url'] = product_url
            manual['source'] = "allen-heath.com"
            with open(self.filename, 'a', newline='', encoding='utf-8') as fp:
                print(row)
                csv.writer(fp).writerow(row)
            yield manual
            
        
            
