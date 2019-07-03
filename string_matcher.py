#-*-coding:utf8;-*-
from collections import OrderedDict



class string_match(object):
    def __init__(self,data_source=None):
        self.dictx,self.dicty,self.lists = dict(),dict(),data_source
        self.boolean = False
        
    
    def match_string(self,x,y,prints=False):
        " returns the match of x to y as a percentage "
        
        a = set(x.split())
        b = set(y.split())
        c = float(len(a&b))
        d = float(len(a|b))
        try:similarity_ratio = round(((c/d)*100/1),2)
        except:similarity_ratio = 0
        if similarity_ratio >= 1:self.dictx[y] = similarity_ratio
        else:pass
        if prints:
            print(x,y,similarity_ratio)
        else:pass
        return(similarity_ratio)
    
    def find_match(self,args,func,data_source,prints=False):
        for id,string in enumerate(data_source):
            func(args,string)
        dictz = list(OrderedDict(sorted(self.dictx.items(), key=lambda t: t[1], reverse=True)))
        dicts = list(OrderedDict(sorted(self.dicty.items(), key=lambda t: t[1], reverse=True)))
        try:
            test = dictz[0]
            for id,string in enumerate(data_source):
                if func(test,string,prints) >=100:
                    self.dictx = dict()
                    return((id,string))
                else:pass
        except IndexError as e:
            self.dictx = dict()
            return None
        self.dictx = dict()
