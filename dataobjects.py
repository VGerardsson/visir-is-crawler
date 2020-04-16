class ArticleLinks:
    url = None
    title = None
    htmltag = None
    datevalue = None
    ArticleExtract = None
    ImageLink = None

    def __init__(self, url=None, title=None, htmltag=None, datevalue=None, ArticleExtract=None, ImageLink=None):
        self.url = url
        self.title = title
        self.htmltag = htmltag
        self.datevalue = datevalue
        self.ArticleExtract = ArticleExtract
        self.ImageLink = ImageLink
