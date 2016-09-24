# -*- coding: utf-8 -*-
"""
    @
    @Description:   This script counts tweet w key word per day and prints the count 
    @               distribution of tweets by date
    @               
    @               
    @Author:        rima
    @Last modified: 07/09/2015 
"""

import time
import ujson as json
import sys
morepath = ['/Users/zc/Documents/twitter_research/TurkishElection/src/RESTApi', '/Library/Python/2.7/site-packages/mmseg-1.3.0-py2.7-macosx-10.9-intel.egg', '/Library/Python/2.7/site-packages/PyInstaller-2.1-py2.7.egg', '/Library/Python/2.7/site-packages/distribute-0.7.3-py2.7.egg', '/Library/Python/2.7/site-packages/py2app-0.9-py2.7.egg', '/Library/Python/2.7/site-packages/modulegraph-0.12-py2.7.egg', '/Library/Python/2.7/site-packages/altgraph-0.12-py2.7.egg', '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python', '/Library/Python/2.7/site-packages/mechanize-0.2.5-py2.7.egg', '/Library/Python/2.7/site-packages/oauth2-1.5.211-py2.7.egg', '/Library/Python/2.7/site-packages/httplib2-0.9-py2.7.egg', '/usr/local/lib/wxPython-3.0.2.0/lib/python2.7/site-packages', '/usr/local/lib/wxPython-3.0.2.0/lib/python2.7/site-packages/wx-3.0-osx_cocoa', '/Library/Frameworks/Python.framework/Versions/2.7/lib/python27.zip', '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7', '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-darwin', '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac', '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/plat-mac/lib-scriptpackages', '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-tk', '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-old', '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload', '/Users/zc/Library/Python/2.7/lib/python/site-packages', '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages', '/usr/local/lib/wxPython-3.0.2.0/lib/python2.7', '/Library/Python/2.7/site-packages']
sys.path += morepath
import pickle 
import pymongo
import datetime 
import itertools

import numpy as np
from matplotlib import pyplot as plt
from sets import Set


import pickle
''' use this dictionary for 10/15/14 - 1/15/15 prtotests
key_dic={3:{"terms":[u"validebağ",u"çamlıca konakları",u"cami inşaatı",u"koruluğu"],"counter":0,"protest":"Protest against mosque construction","start":datetime.datetime(2014,10,18,00,00,000000),"end":datetime.datetime(2014,10,19,23,59,000000), "tweets":[]},
         4:{"terms":[u"Adaletin kara günü",u"17 Aralık",u"rüşvet",u"yolsuzluk",u"17-25"],"counter":0,"protest":"anti-corruption protest","start":datetime.datetime(2014,10,20,00,00,000000),"end":datetime.datetime(2014,10,21,23,59,000000),"tweets":[]},
         5:{"terms":[u"Cumartesi anneleri"],"counter":0,"protest":"Saturday Mothers Protest","start":datetime.datetime(2014,10,25,00,00,000000),"end":datetime.datetime(2014,10,26,23,59,000000),"tweets":[]},
         6:{"terms":[u"validebağ",u"çamlıca konakları",u"cami inşaatı",u"koruluğu"],"counter":0,"protest":"Protest against mosque construction","start":datetime.datetime(2014,10,27,00,00,000000),"end":datetime.datetime(2014,10,28,23,59,000000),"tweets":[]},
         7:{"terms":[u"madenci",u"maden faciası",u"maden",u"soma",u"ermenek",u"maden işçisi",u"maden kazası"],"counter":0,"protest":"Miners protest","start":datetime.datetime(2014,10,29,00,00,000000),"end":datetime.datetime(2014,10,30,23,59,000000),"tweets":[]},
         8:{"terms":[u"IŞİD zulmü",u"kobane",u"suruç"],"counter":0,"protest":"Protest for solidarity with Kobane","start":datetime.datetime(2014,11,01,00,00,000000),"end":datetime.datetime(2014,11,02,23,59,000000),"tweets":[]},
         9:{"terms":[u"validebağ",u"çamlıca konakları",u"cami inşaatı",u"koruluğu"],"counter":0,"protest":"Protest against mosque construction","start":datetime.datetime(2014,11,02,00,00,000000),"end":datetime.datetime(2014,11,03,23,59,000000),"tweets":[]},
         10:{"terms":[u"yök protestosu",u"yök'ü protesto",u"ankara üniversitesi"],"counter":0,"protest":"student protest","start":datetime.datetime(2014,11,8,00,00,000000),"end":datetime.datetime(2014,11,9,23,59,000000),"tweets":[]},
         11:{"terms":[u"HES",u"termik santral",u"çimento",u"siyanür",u"Trabzon",u"derelerin kardeşliği"],"counter":0,"protest":"Environment protest","start":datetime.datetime(2014,11,9,00,00,000000),"end":datetime.datetime(2014,11,10,23,59,000000),"tweets":[]},
         12:{"terms":[u"validebağ",u"çamlıca konakları",u"cami inşaatı",u"koruluğu"],"counter":0,"protest":"Protest against mosque construction","start":datetime.datetime(2014,11,13,00,00,000000),"end":datetime.datetime(2014,11,14,23,59,000000),"tweets":[]},
         13:{"terms":[u"sağlık bütçesi",u"saglık bakanlığı",u"sağlık bakanı",u"bütçe tasarısı",u"plan ve bütçe komisyonu",u"sağlık emekçileri"],"counter":0,"protest":"Doctors protest","start":datetime.datetime(2014,11,20,00,00,000000),"end":datetime.datetime(2014,11,21,23,59,000000),"tweets":[]},
         14:{"terms":[u"birleşik metal-iş",u"mess",u"metal işçileri"],"counter":0,"protest":"Workers protest","start":datetime.datetime(2014,11,21,00,00,000000),"end":datetime.datetime(2014,11,22,23,59,000000),"tweets":[]},
         15:{"terms":[u"25 kasım",u"kadına şiddet",u"kadın erkek eşit"],"counter":0,"protest":"Women protest","start":datetime.datetime(2014,11,23,00,00,000000),"end":datetime.datetime(2014,11,24,23,59,000000),"tweets":[]},
         16:{"terms":[u"taşeron işçi",u"yol-iş",u"iznerji",u"tcdd",u"kesk"],"counter":0,"protest":"Workers protest","start":datetime.datetime(2014,11,24,00,00,000000),"end":datetime.datetime(2014,11,25,23,59,000000),"tweets":[]},
         17:{"terms":[u"madenci",u"özelleştirme",u"yatağan",u"termik santral",u"maden-iş",u"tes-iş",u"sattırmayacağız"],"counter":0,"protest":"Miners protest","start":datetime.datetime(2014,12,01,00,00,000000),"end":datetime.datetime(2014,12,05,23,59,000000),"tweets":[]},
         18:{"terms":[u"maltepe üniversitesi",u"hastahanesi",u"dev sağlık iş",u"sendika",u"işçi"],"counter":0,"protest":"Hospital workers protest","start":datetime.datetime(2014,12,8,00,00,000000),"end":datetime.datetime(2014,12,9,23,59,000000),"tweets":[]},
         19:{"terms":[u"memurlar",u"emekliler",u"bütçe görüşmeleri",u"meclis önü"],"counter":0,"protest":"Government employees protest","start":datetime.datetime(2014,12,10,00,00,000000),"end":datetime.datetime(2014,12,11,23,59,000000),"tweets":[]},
         20:{"terms":[u"halk için bütçe",u"emekçi",u"iç güvenlik paketi",u"aile hekimleri grev",u"acil hastaları"],"counter":0,"protest":"Doctors protest","start":datetime.datetime(2014,12,12,00,00,000000),"end":datetime.datetime(2014,12,14,23,59,000000),"tweets":[]},
         21:{"terms":[u"taraftar grubu çarşı",u"çarşı darbe",u"çarşı dava"],"counter":0,"protest":"Soccer Fun Clup solidarity protest, Gezi Park related","start":datetime.datetime(2014,12,16,00,00,000000),"end":datetime.datetime(2014,12,16,23,59,000000),"tweets":[]},
         22:{"terms":[u"hırsız var",u"17 Aralık",u"rüşvet",u"yolsuzluk",u"17-25"],"counter":0,"protest":"anti-corruption protest","start":datetime.datetime(2014,12,17,00,00,000000),"end":datetime.datetime(2014,12,18,23,59,000000),"tweets":[]},
         23:{"terms":[u"hattat holding",u"işten atma",u"işten çıkarma",u"hema maden",u"gmis",u"ttk"],"counter":0,"protest":"Miners protest","start":datetime.datetime(2014,12,19,00,00,000000),"end":datetime.datetime(2014,12,20,23,59,000000),"tweets":[]},
         24:{"terms":[u"eğitim-iş",u"laik eğitim",u"emeğe saygı yürüyüşü"],"counter":0,"protest":"Teachers protest","start":datetime.datetime(2014,12,20,00,00,000000),"end":datetime.datetime(2014,12,21,23,59,000000),"tweets":[]},
         25:{"terms":[u"disk",u"asgari ücret",u"net 1800 lira",u"birleşik metal-iş",u"mess", u"metal işçileri"],"counter":0,"protest":"worker protest","start":datetime.datetime(2014,12,22,00,00,000000),"end":datetime.datetime(2014,12,24,23,59,000000),"tweets":[]},
         26:{"terms":[u"faşist saldırı",u"öğrencilere saldırı"],"counter":0,"protest":"Students protest","start":datetime.datetime(2014,12,25,00,00,000000),"end":datetime.datetime(2014,12,26,23,59,000000),"tweets":[]},
         27:{"terms":[u"Kent savunması",u"Haziran Hareketi",u"Gezi",u"Birleşik Haziran",u"gerici eğitim"],"counter":0,"protest":"Gezi Park Solidarity Protest","start":datetime.datetime(2014,12,28,00,00,000000),"end":datetime.datetime(2014,12,29,23,59,000000),"tweets":[]},
         28:{"terms":[u"Ülker işçileri",u"70. günü",u"hastahanesi işçileri",u"demokratik kitle"],"counter":0,"protest":"Workers protest","start":datetime.datetime(2015,01,03,00,00,000000),"end":datetime.datetime(2015,01,04,23,59,000000),"tweets":[]},
         29:{"terms":[u"iztuzu plajı",u"caretta",u"yaşam alanı"],"counter":0,"protest":"Environment protest","start":datetime.datetime(2015,01,04,00,00,000000),"end":datetime.datetime(2015,01,05,23,59,000000),"tweets":[]},
         30:{"terms":[u"Je suis Charlie",u"Charlie Hebdo"],"counter":0,"protest":"Charlie Hebdo Solidarity Protest","start":datetime.datetime(2015,1,9,00,00,000000),"end":datetime.datetime(2015,01,10,23,59,000000),"tweets":[]},
         31:{"terms":[u"haziran hareketi", u"laik eğitim",u"gerici eğitim"],"counter":0,"protest":"Protest against religious education","start":datetime.datetime(2015,01,11,00,00,000000),"end":datetime.datetime(2015,01,12,23,59,000000),"tweets":[]}
         }
'''
key_dic={"workers protest":{"terms":[u"Renault",u"işçi",u"direniş",u"metal",u"ego",u"patron",u"talep",u"işten atma",u"Türk metal",u"sendika",u"protesto"],"counter":0,"protest":"Protest against mosque construction","start":datetime.datetime(2015,6,12,00,00,000000),"end":datetime.datetime(2015,6,13,23,59,000000), "tweets":[]},
         "workers protest women's protest":{"terms":[u"Özgecan Aslan",u"isyan",u"protesto",u"cinayet",u"dava",u"katil",u"ceza",u"tecavüz"],"counter":0,"protest":"anti-corruption protest","start":datetime.datetime(2015,6,13,00,00,000000),"end":datetime.datetime(2015,6,14,23,59,000000),"tweets":[]},
         "miners protested":{"terms":[u"soma",u"ermenek",u"katliam",u"facia",u"maden",u"kazası",u"madenci",u"kömür",u"madenci"],"counter":0,"protest":"Protest against mosque construction","start":datetime.datetime(2015,6,16,00,00,000000),"end":datetime.datetime(2015,6,17,23,59,000000), "tweets":[]},
         "June movement (gezi park protests)":{"terms":[u"haziran hareketi",u"protesto",u"gezi",u"park",u"gezi parkı",u"görülmemiş hesap kalmayacak",u"birleşik haziran",u"görülmemiş",u"taksim",u"protesto",u"direniş"],"counter":0,"protest":"anti-corruption protest","start":datetime.datetime(2015,6,22,00,00,000000),"end":datetime.datetime(2015,6,23,23,59,000000),"tweets":[]},
         }


def extract_dates (tweets):
    '''this function returns an empty dictionary of dates keys extracted from the created at date of  all tweets'''
    dates_dic={}
    for tweet in tweets:
        day=datetime.datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y').date()
        dates_dic[day]={}
        for k, ptotest in key_dic.iteritems():
            dates_dic[day][k]=0
        #dic={date:{"protest_name":0, protest2:0},date2...
    
    return dates_dic
    
def keywordsInDay(days,tweets):
    ''' this function adds count of tweets with keywords per create_at in the dictionary'''
    #days={date:{}
    for tweet in tweets:
        created_at=datetime.datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y').date()
        text=tweet["text"]
        for protest in key_dic:
            keywords=key_dic[protest]["terms"]#list of words per protest
            for keyword in keywords:
                if keyword in text:
                    days[created_at][protest] +=1
                    break
    return days
    
def print_nestedDic(protest_count_per_day,s):
    '''this function is just to dispaly results'''
    #print label
    for k,v in protest_count_per_day.iteritems():
        for ke,i in v.iteritems():
            s+= str(ke)+"\t " #+ str(i)+" " use this to prin the title
    
        print s
        s=''
        break
    #print values
    for k,v in protest_count_per_day.iteritems():
         
        s+= str(k)+"\t "
        for ke,i in v.iteritems():
            #s+= str(ke)+"\t " #+ str(i)+" " use this to prin the title
            
            s+= str(i)+"\t "#if isinstance(v, dict): #use this
            
            #print_nestedDic(v,s)
        #else:
            #s += str(v)
            #print "{0} : {1}".format(k, v)
            #print s
            
        print s
        s='' 
        
            
if __name__ == "__main__":
    #change file name: UNcensored_tweets_with_protest_keywords_June3_June26.p, UNcensored_tweets_with_protest_keywords_June3_June26.p
    tweets = pickle.load( open( "UNcensored_tweets_with_protest_keywords_June3_June26.p", "rb" ) )
    days=extract_dates(tweets)# make an empty dictionary of dates
    protest_count_per_day=keywordsInDay(days,tweets)
    print protest_count_per_day 
    print_nestedDic(protest_count_per_day, s='')
    