# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import hashlib
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    vuln_id = 'PHPWind_0006' # 平台漏洞编号，留空
    name = 'PHPWind flash xss' # 漏洞名称
    level = VulnLevel.MED # 漏洞危害级别
    type = VulnType.XSS # 漏洞类型
    disclosure_date = '2013-03-09'  # 漏洞公布时间
    desc = '''
        PHPWind flash xss漏洞。
    ''' # 漏洞描述
    ref = 'https://wooyun.shuimugan.com/bug/view?bug_no=017731' # 漏洞来源
    cnvd_id = '' # cnvd漏洞编号
    cve_id = '' #cve编号
    product = 'phpwind'  # 漏洞应用名称
    product_version = ''  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = 'c5a03ec6-7ad5-42d2-baef-d3a281e3bb67'
    author = '国光'  # POC编写者
    create_date = '2018-05-11' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            flash_md5 = "3a1c6cc728dddc258091a601f28a9c12"
            file_path = "/res/js/dev/util_libs/swfupload/Flash/swfupload.swf" 
            url = '{target}'.format(target=self.target)
            verify_url = url + file_path
            code, head,res, errcode, _ = hh.http( verify_url)
            if code == 200:           
                md5_value = hashlib.md5(res).hexdigest()
                if md5_value in flash_md5:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target,name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        super(Poc, self).exploit()


if __name__ == '__main__':
    Poc().run()