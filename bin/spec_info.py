import os
import sys
import json
import re

#商品情報にhtmltagをつけるClass
class Productdetail:

    def __init__(self):
        global fixedphrase, headline
        constant = json.load(open(".\\etc\\constant.json", "r"))
        fixedphrase = constant["fixedphrase"]
        headline = constant["headline"]

    def create_tagging(self, item, incidental):

        HEAD = PTag.step_in(str(incidental["SALES_POINT"]))

        AGE = DtTag.step_in(headline["AGE"]) +\
              DdTag.step_in(str(item["AGE"]))

        MATERIAL = DtTag.step_in(headline["MATERIAL"]) +\
                   DdTag.step_in(str(item["MATERIAL"]))

        ORIGIN = DtTag.step_in(headline["ORIGIN"]) +\
                 DdTag.step_in(str(item["ORIGIN"]))

        SIZE = DtTag.step_in(headline["SIZE"]) +\
               DdTag.step_in(str(incidental["ITEM_SIZE"]))

        WEIGHT = DtTag.step_in(headline["WEIGHT"]) +\
                 DdTag.step_in(str(incidental["WEIGHT"]))

        text_list = [AGE, MATERIAL, ORIGIN, SIZE, WEIGHT]
        text_list2 = Item_Exclusion.check(text_list)
        text = ''.join(text_list2)

        PRODUCT_SPEC = DlTag.step_in(text)

        DISCRIPTION_LIST = [item["CATALOG_COPY"], item["CATCHCOPY_SUB1"], item["CATCHCOPY_SUB2"], item["CATCHCOPY_SUB3"]]
        DISCRIPTION = DivTag.step_in(
            H4Tag.step_in(headline["DISCRIPTION"]) +
            OlTag.step_in(
                LiTag.step_in(
                DISCRIPTION_LIST
                )
            )
        )
        

        CARE = DivTag.step_in(
            H4Tag.step_in(headline["CARE"]) +
            OlTag.step_in(
                LiTag.step_in(
                str(incidental["CARE"])
                )
            )
        )

        CAUTION = DivTag.step_in(
            H4Tag.step_in(headline["CAUTION"]) + 
            OlTag.step_in(
                LiTag.step_in(
                str(incidental["CAUTION"])
                )
            )
        ) 
        
        BABY = PTag.step_in(fixedphrase["baby"])

        text_list1 = [HEAD, PRODUCT_SPEC, DISCRIPTION, CARE, CAUTION, BABY]
        text = ''.join(text_list1)

        return text

#各種TagClassのSuperClass                
class HtmlTag(object):

    #センテンスが入る場合は、「。」区切りでsplitする。デフォルトはsplitせずに値をそのまま返却する。
    @classmethod
    def split(self, value):
        return value
    
    #タグで挟むメソッド
    @classmethod
    def sandwitched_by_tags(self, tag, value):
        if value == "":
            return ""
        return '<' + tag + '>' + value + '</' + tag + '>'
    
    #htmlを形成する
    @classmethod
    def step_in(self, value):
        r = self.split(value)
        tag_name = self.__name__.lower().replace("tag", "")

        v = ""
        if type(r) == filter or type(r) == list:
            for a in r:
                a = Delete.newline(a)
                a = Delete.chara(a)
                v += self.sandwitched_by_tags(tag_name, a)
        else:
            v = Delete.newline(r)
            v = Delete.chara(v)
            v = self.sandwitched_by_tags(tag_name, v)

        return v
#各種TagClass  
class DtTag(HtmlTag): pass          

class DdTag(HtmlTag): pass

class H4Tag(HtmlTag): pass

class DlTag(HtmlTag):
    @classmethod
    def sandwitched_by_tags(self, tag, value):
        return '<' + tag + ' id="productDetail">' + value + '</' + tag + '>'

class LiTag(HtmlTag):
    @classmethod
    def split(self, value):
        if type(value) != list:
            s = filter(lambda str:str != '', value.split('。'))
            return s
        return value

    @classmethod
    def step_in(self, value):
        r = self.split(value)
        tag_name = self.__name__.lower().replace("tag", "")

        v = ""
        if type(r) == filter or type(r) == list:
            for a in r:
                a = Delete.newline(a)
                a = Delete.chara(a)
                v += self.sandwitched_by_tags(tag_name, a)
        else:
            v = Delete.newline(r)
            v = Delete.chara(v)
            v = self.sandwitched_by_tags(tag_name, v)

        if type(r) != list:
            v = LiTag.lireplace(tag_name, v)

        return v

    @classmethod
    def lireplace(self, tag, value):
        value = value.replace("</%s>" % tag, "。</%s>" % tag)
        return value

class DivTag(HtmlTag): 
    @classmethod
    def sandwitched_by_tags(self, tag, value):
        return '<' + tag + ' class="productExp">' + value + '</' + tag + '>'

    @classmethod
    def step_in(self, value):
        r = self.split(value)
        tag_name = self.__name__.lower().replace("tag", "")

        return self.sandwitched_by_tags(tag_name, r)

class OlTag(HtmlTag):
    @classmethod
    def sandwitched_by_tags(self, tag, value):
        return '<' + tag + ' id="styleCircle">' + value + '</' + tag + '>'

    @classmethod
    def step_in(self, value):
        r = self.split(value)
        tag_name = self.__name__.lower().replace("tag", "")

        return self.sandwitched_by_tags(tag_name, r)

class PTag(HtmlTag):
    @classmethod
    def sandwitched_by_tags(self, tag, value):
        if value == fixedphrase["baby"]:
            return '<' + tag + ' class=\"recommendCategory\">' + value + '</' + tag + '>'
        return '<' + tag + ' style="font-size:16px;  font-weight:bold; text-align:left; margin-bottom:10px; line-height:120%;">' + value + '</' + tag + '>' + '<br />'

    @classmethod
    def step_in(self, value):
        r = self.split(value)
        tag_name = self.__name__.lower().replace("tag", "")

        v = ""
        if type(r) == filter or type(r) == list:
            for a in r:
                a = Delete.newline(a)
                a = Delete.chara(a)
                v += self.sandwitched_by_tags(tag_name, a)
        else:
            v = Delete.newline(r)
            if value != fixedphrase["baby"]:
                v = Delete.chara(v)
            v = self.sandwitched_by_tags(tag_name, v)
        
        return v

class Delete:
    @classmethod
    def openjson(self):
        deletecharacter = json.load(open(".\\etc\\deletecharacter.json", "r"))
        #character = deletecharacter["character"]
        return deletecharacter
        
    @classmethod
    def chara(self, value):
        deletecharacter = self.openjson()
        sentencelist = list(deletecharacter["sentence"].values())
        symbollist = list(deletecharacter["symbol"].values())
        valuelist = sentencelist + symbollist
        for a in valuelist:
            if re.search("。", a) :
                a = a.replace("。", "")
            value = value.replace(a, "")
        return value

    @classmethod
    def newline(self, value):
        value = value.replace('\r\n', "")
        value = value.replace('\r', "")
        value = value.replace('\n', "")
        return value

class Item_Exclusion:
    @classmethod
    def check(self, text_list1):
        text_list2 = []
        for a in text_list1:
            if a.find("<dd>") != -1:
                text_list2.append(a)
        return text_list2