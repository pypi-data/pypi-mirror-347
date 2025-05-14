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
from collections import deque
from bstack_utils.constants import *
class bstack11l1lll11l_opy_:
    def __init__(self):
        self._111ll111ll1_opy_ = deque()
        self._111l1llll11_opy_ = {}
        self._111l1llllll_opy_ = False
    def bstack111ll111l1l_opy_(self, test_name, bstack111ll11111l_opy_):
        bstack111ll111l11_opy_ = self._111l1llll11_opy_.get(test_name, {})
        return bstack111ll111l11_opy_.get(bstack111ll11111l_opy_, 0)
    def bstack111l1lll1ll_opy_(self, test_name, bstack111ll11111l_opy_):
        bstack111l1llll1l_opy_ = self.bstack111ll111l1l_opy_(test_name, bstack111ll11111l_opy_)
        self.bstack111ll1111l1_opy_(test_name, bstack111ll11111l_opy_)
        return bstack111l1llll1l_opy_
    def bstack111ll1111l1_opy_(self, test_name, bstack111ll11111l_opy_):
        if test_name not in self._111l1llll11_opy_:
            self._111l1llll11_opy_[test_name] = {}
        bstack111ll111l11_opy_ = self._111l1llll11_opy_[test_name]
        bstack111l1llll1l_opy_ = bstack111ll111l11_opy_.get(bstack111ll11111l_opy_, 0)
        bstack111ll111l11_opy_[bstack111ll11111l_opy_] = bstack111l1llll1l_opy_ + 1
    def bstack1l1111ll1_opy_(self, bstack111l1lll1l1_opy_, bstack111ll111111_opy_):
        bstack111l1lllll1_opy_ = self.bstack111l1lll1ll_opy_(bstack111l1lll1l1_opy_, bstack111ll111111_opy_)
        event_name = bstack11ll11ll1ll_opy_[bstack111ll111111_opy_]
        bstack1l1ll1l111l_opy_ = bstack11111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤᴑ").format(bstack111l1lll1l1_opy_, event_name, bstack111l1lllll1_opy_)
        self._111ll111ll1_opy_.append(bstack1l1ll1l111l_opy_)
    def bstack1ll1111l1l_opy_(self):
        return len(self._111ll111ll1_opy_) == 0
    def bstack1ll1ll1l1l_opy_(self):
        bstack111ll1111ll_opy_ = self._111ll111ll1_opy_.popleft()
        return bstack111ll1111ll_opy_
    def capturing(self):
        return self._111l1llllll_opy_
    def bstack1l1llll111_opy_(self):
        self._111l1llllll_opy_ = True
    def bstack111ll11l_opy_(self):
        self._111l1llllll_opy_ = False