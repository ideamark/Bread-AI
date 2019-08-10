import random
import re

from . import chat
from . import common
from . import memory
from breadbot.func import teach
from breadbot.func import web


def response(db, user, in_str):
    in_str = common.init_input(in_str)
    res = ''

    if re.match('^next|n$', in_str):
        res = memory.Memory(user).get_longstr_mem()
    elif re.match('^translate .*$', in_str):
        content = re.sub('^translate ', '', in_str)
        res = web.translate(content)
    elif re.match('^help$', in_str.lower()):
        res = common.show_help(user)
    elif re.match('^home$', in_str):
        res = web.show_homepage()
    elif re.search('[\u4e00-\u9fa5]', in_str):
        en_str = web.translate(in_str)
        res = chat.Chat(db).response(user, en_str)
        res = web.translate(res)

    if common.is_super(user):
        if re.match('^teach .*$', in_str):
            content = re.sub('^teach ', '', in_str)
            res = teach.Teach().do_teach(user, content)
        elif re.match('^corpus .*$', in_str):
            content = re.sub('^corpus ', '', in_str)
            res = web.corpus_search(content)

    if not res:
        res = chat.Chat(db).response(user, in_str)
    memory.Memory(user).save_dialog(in_str, res)
    res = memory.Memory(user).check_longstr(res)
    return res
