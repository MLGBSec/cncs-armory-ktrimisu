# encoding: utf-8
import os
from CScanPoc.lib.core.log import CSCAN_LOGGER as logger
from CScanPoc.lib.core.utils import iter_modules
from CScanPoc.lib.api.utils import load_poc_mod
from CScanPoc.lib.api.component import Component
from .progress import progress


def _clean_up_poc_dirs(path):
    '''移除所有无用目录（空或者只有 .pyc 的目录）'''
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files) != 0:
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                _clean_up_poc_dirs(fullpath)
            elif fullpath.endswith('.pyc'):
                os.remove(fullpath)
    # if folder empty, delete it
    if len(os.listdir(path)) == 0:
        logger.info('Remove empty dir: {}'.format(path))
        os.rmdir(path)


def sort_pocs(poc_base_dir, ignore_dirs=['common']):
    '''将 POC 放置到其检查的 产品类型/产品名 目录下'''

    mod_count = 0
    if '.venv' not in ignore_dirs:
        ignore_dirs.append('.venv')
    for (mod, d, file_name) in iter_modules(poc_base_dir, ignore_dirs):
        mod_count += 1
        progress(mod_count, mod_count, '处理模块', os.path.join(d, file_name))
        (vuln, _) = load_poc_mod(mod)
        if vuln is None:
            continue
        prd = vuln.product
        component = Component.get_component(prd)
        typ = component.type
        should_be_in = os.path.join(
            poc_base_dir, typ.name, prd.replace(' ', '_'))

        if should_be_in != d:
            if not os.path.exists(should_be_in):
                os.makedirs(should_be_in)
            src_file = os.path.join(d, file_name)
            dst_file = os.path.join(should_be_in, file_name)
            logger.info('move from {} to {}'.format(src_file, dst_file))
            os.rename(src_file, dst_file)

    logger.info(
        '********* Clean up poc dir: {} ************'.format(poc_base_dir))
    _clean_up_poc_dirs(poc_base_dir)
