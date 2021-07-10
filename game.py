from os import name


class game:
    name = ""
    gURL = ""
    companies = []
    languages = []
    genres = []
    originalSize = ""
    repackSize = ""

    def __init__(self,Fname,Flink,oriSize,ReSize,Compa,Genra,Lang):
        self.name = Fname
        self.gURL = Flink
        self.companies = Compa
        self.originalSize = oriSize
        self.repackSize = ReSize
        self.genres = Genra
        self.languages = Lang

    def getName(self):
        return self.name
        
    def getURL(self):
        return self.gURL

    def getComp(self):
        return self.companies

    def getOri(self):
        return self.originalSize

    def getRe(self):
        return self.repackSize
    def getlang(self):
        return self.languages
    def getgenra(self):
        return self.genres


    
