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
class bstack11111ll1l_opy_:
    def __init__(self, handler):
        self._11lllll1ll1_opy_ = None
        self.handler = handler
        self._11lllll1lll_opy_ = self.bstack11llllll111_opy_()
        self.patch()
    def patch(self):
        self._11lllll1ll1_opy_ = self._11lllll1lll_opy_.execute
        self._11lllll1lll_opy_.execute = self.bstack11lllll1l1l_opy_()
    def bstack11lllll1l1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࠤᕝ"), driver_command, None, this, args)
            response = self._11lllll1ll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11111l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࠤᕞ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11lllll1lll_opy_.execute = self._11lllll1ll1_opy_
    @staticmethod
    def bstack11llllll111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver