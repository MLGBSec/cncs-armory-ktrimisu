# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'info_hg' # 平台漏洞编号，留空
    name = '.hg 源码泄露' # 漏洞名称
    level = VulnLevel.MED # 漏洞危害级别
    type = VulnType.INFO_LEAK # 漏洞类型
    disclosure_date = ''  # 漏洞公布时间
    desc = '''
    在运行hg init的时候会生成.hg文件夹,如果暴露在外网上面会早操源码泄露,攻击者可以直接根据泄露的文件夹恢复网站源码.
        ''' # 漏洞描述
    ref = '' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = ''  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '25c9594d-2f28-4601-878f-3e6851f80eae'
    author = 'cscan'  # POC编写者
    create_date = '2018-04-26' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            request = requests.get('{target}/.hg/'.format(target=self.target))
            if request.status_code == 200:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常{}'.format(e))


    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
