#!/bin/python3

from bs4 import BeautifulSoup as bs
import requests, random, time

loginURL = "https://vnl.falcooonline.com/VNLOnline/FrmInloggen.aspx"
user = "YOUR USERNAME HERE"
password = "YOUR PASSWORD HERE"

#Login. Parameter 1: session object, parameter 2: soup of last GET
def login(session, s):
	print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	print("@@@@@@@@@ logging in @@@@@@@@@@@@@")
	print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
	time.sleep(5 + random.random() * 10)
	lastfocus = "" #s.find("__LASTFOCUS").attrs["value"]
	viewstate = s.find(id="__VIEWSTATE").attrs["value"]
	viewstategenerator = s.find(id="__VIEWSTATEGENERATOR").attrs["value"]
	eventtarget = "" #s.find("__EVENTTARGET").attrs["value"]
	eventargument = "" #s.find("__EVENTARGUMENT").attrs["value"]
	eventvalidation = s.find(id="__EVENTVALIDATION").attrs["value"]
	session.post(loginURL, data= {"LabUser":user, "LabPwd":password, "ButLogin":"Inloggen", "__LASTFOCUS":lastfocus, "__VIEWSTATE":viewstate, "__VIEWSTATEGENERATOR":viewstategenerator, "__EVENTTARGET":eventtarget, "__EVENTARGUMENT":eventargument, "__EVENTVALIDATION":eventvalidation} )
	time.sleep(5 + random.random() * 10)


