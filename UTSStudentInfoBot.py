import requests
import math
import random
import rsa
import base64
import time

class UTSBot(object):
    def __init__(self):
        self.session = requests.Session()

    def success_code (self, code = 0) : 
        return code == 200 or code == 302

    def get_login_data(self) :

        data = {}

        # get viewstates and eventvalidation first
        response = self.session.get(self.login_url)
        
        if not self.success_code(response.status_code) :
            return None

        html                    = response.text
        viewstates              = self.get_viewstates(html)
        viewstatesgenerator     = self.get_viewstatesgenerator(html)
        eventvalidation         = self.get_eventvalidation(html)

        data["__EVENTTARGET"]           = "ctl00$Content$cmdLogin"
        data["__EVENTARGUMENT"]         = ""
        data["__VIEWSTATE"]             = viewstates
        data["__VIEWSTATEGENERATOR"]    = viewstatesgenerator
        data["__EVENTVALIDATION"]       = eventvalidation
        data["__SCROLLPOSITIONX"]       = "0"
        data["__SCROLLPOSITIONY"]       = "300"

        return data

    def get_viewstates(self, html = "") :
        return self.get_str_between(html, "<input type=\"hidden\" name=\"__VIEWSTATE\" id=\"__VIEWSTATE\" value=\"", "\" />")

    def get_viewstatesgenerator(self, html = "") :
        return self.get_str_between(html, "<input type=\"hidden\" name=\"__VIEWSTATEGENERATOR\" id=\"__VIEWSTATEGENERATOR\" value=\"", "\" />")

    def get_eventvalidation(self, html = "") :
        return self.get_str_between(html, "<input type=\"hidden\" name=\"__EVENTVALIDATION\" id=\"__EVENTVALIDATION\" value=\"", "\" />")

    def __get_familyname(self, html = "") :
        return self.get_str_between(html, "<input name=\"ctl00$Content$txtFamilyName$InputControl\" type=\"text\" value=\"", "\" maxlength")

    def __get_givenname(self, html = "") :
        return self.get_str_between(html, "<input name=\"ctl00$Content$txtGivenName$InputControl\" type=\"text\" value=\"", "\" maxlength")

    def __get_dateofbirth(self, html = "") :
        return self.get_str_between(html, "<input name=\"ctl00$Content$txtDateOfBirth$InputControl\" type=\"text\" value=\"", "\" maxlength=")

    def __get_gender(self, html = "") :
        return self.get_str_between(html, "<input name=\"ctl00$Content$txtGender$InputControl\" type=\"text\" value=\"", "\" maxlength=")

    def get_str_between(self, text, str_start, str_end) :

         start_index = text.find(str_start) + len(str_start)
         end_index = text.find(str_end, start_index)

         return text[start_index : end_index]

    def login(self, username, password):

        if not username or not password :
            return False

        self.login_url = "https://onestopadmin.uts.edu.au/estudent/login.aspx"

        self.username = username
        self.password = password

        postdata = self.get_login_data()

        if postdata == None:
            return False

        postdata["ctl00$Content$txtUserName$txtText"] = username
        postdata["ctl00$Content$txtPassword$txtText"] = password

        login_headers = {
            "Accept"            : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding"   : "gzip, deflate, br",
            "Accept-Language"   : "Accept-Language",
            "Cache-Control"     : "max-age=0",
            "Connection"        : "keep-alive",
            "Content-Type"      : "application/x-www-form-urlencoded",
            "Cookie"            : "BIGipServer~mdc2_cass_infrastructure~ci_pool_web_prod=1780533514.20480.0000; UTSName=" + username
            }

        response = self.session.post(self.login_url, data = postdata, headers = login_headers)

        return self.success_code(response.status_code)

    def get_personalinfo(self) :
        
        self.name_detail_url = "https://onestopadmin.uts.edu.au/eStudent/SM/PersDtls10.aspx?r=UTS.EST.WEB02&f=UTS.EST.PERSDTLS.WEB"

        html = self.session.get(self.name_detail_url).text

        return (self.__get_givenname(html) + " " + self.__get_familyname(html),
               self.__get_dateofbirth(html),
               self.__get_gender(html))

"""
if __name__ == '__main__':

    utsBot = UTSBot() 
    
    if not utsBot.login("Enter the student number here", "Enter the password here") :
        print("Login failed")
        exit

    print("Login success")

    (name, date_of_birth, gender) = utsBot.get_personalinfo()

    print("Name = " + name)
    print("Birthday = " + date_of_birth)
    print("Gender = " + gender)
   
"""
