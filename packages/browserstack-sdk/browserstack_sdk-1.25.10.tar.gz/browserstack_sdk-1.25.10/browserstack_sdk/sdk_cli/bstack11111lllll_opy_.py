# coding: UTF-8
import sys
bstack111l1_opy_ = sys.version_info [0] == 2
bstack11l11ll_opy_ = 2048
bstack1l1l1_opy_ = 7
def bstack11111l_opy_ (bstack11l11_opy_):
    global bstack11l1111_opy_
    bstack1l1lll_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111_opy_ = bstack11l11_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1lll_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l1llll_opy_] + bstack1l111_opy_ [bstack1l1llll_opy_:]
    if bstack111l1_opy_:
        bstack1l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11ll_opy_ - (bstack11ll111_opy_ + bstack1l1lll_opy_) % bstack1l1l1_opy_) for bstack11ll111_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1l1ll1_opy_ = str () .join ([chr (ord (char) - bstack11l11ll_opy_ - (bstack11ll111_opy_ + bstack1l1lll_opy_) % bstack1l1l1_opy_) for bstack11ll111_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1l1ll1_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack11111l11l1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack111111lll1_opy_:
    bstack1l1111l1l1l_opy_ = bstack11111l_opy_ (u"ࠥࡦࡪࡴࡣࡩ࡯ࡤࡶࡰࠨᔦ")
    context: bstack11111l11l1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack11111l11l1_opy_):
        self.context = context
        self.data = dict({bstack111111lll1_opy_.bstack1l1111l1l1l_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᔧ"), bstack11111l_opy_ (u"ࠬ࠶ࠧᔨ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack11111l1ll1_opy_(self, target: object):
        return bstack111111lll1_opy_.create_context(target) == self.context
    def bstack1ll11l1111l_opy_(self, context: bstack11111l11l1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll1ll1l11_opy_(self, key: str, value: timedelta):
        self.data[bstack111111lll1_opy_.bstack1l1111l1l1l_opy_][key] += value
    def bstack1lll1111l1l_opy_(self) -> dict:
        return self.data[bstack111111lll1_opy_.bstack1l1111l1l1l_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack11111l11l1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )