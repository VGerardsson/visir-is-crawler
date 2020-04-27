class ArticleLinks:
    url = None
    title = None
    htmltag = None
    datevalue = None
    ArticleExtract = None
    ImageLink = None
    newspaper = None
    difficultylevel = None
    articleBody = []

    def __init__(self, url=None, title=None, htmltag=None, datevalue=None, ArticleExtract=None, ImageLink=None, newspaper=None, difficultylevel=None, articleBody=[]):
        self.url = url
        self.title = title
        self.htmltag = htmltag
        self.datevalue = datevalue
        self.ArticleExtract = ArticleExtract
        self.ImageLink = ImageLink
        self.newspaper = newspaper
        self.difficultylevel = difficultylevel
        self.articleBody = articleBody
