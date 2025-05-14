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
import builtins
import logging
class bstack11l111l111_opy_:
    def __init__(self, handler):
        self._11lll11111l_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._11lll1111ll_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11111l_opy_ (u"ࠩ࡬ࡲ࡫ࡵࠧ᙮"), bstack11111l_opy_ (u"ࠪࡨࡪࡨࡵࡨࠩᙯ"), bstack11111l_opy_ (u"ࠫࡼࡧࡲ࡯࡫ࡱ࡫ࠬᙰ"), bstack11111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᙱ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._11lll111l1l_opy_
        self._11lll1111l1_opy_()
    def _11lll111l1l_opy_(self, *args, **kwargs):
        self._11lll11111l_opy_(*args, **kwargs)
        message = bstack11111l_opy_ (u"࠭ࠠࠨᙲ").join(map(str, args)) + bstack11111l_opy_ (u"ࠧ࡝ࡰࠪᙳ")
        self._log_message(bstack11111l_opy_ (u"ࠨࡋࡑࡊࡔ࠭ᙴ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᙵ"): level, bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙶ"): msg})
    def _11lll1111l1_opy_(self):
        for level, bstack11lll111ll1_opy_ in self._11lll1111ll_opy_.items():
            setattr(logging, level, self._11lll111l11_opy_(level, bstack11lll111ll1_opy_))
    def _11lll111l11_opy_(self, level, bstack11lll111ll1_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack11lll111ll1_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._11lll11111l_opy_
        for level, bstack11lll111ll1_opy_ in self._11lll1111ll_opy_.items():
            setattr(logging, level, bstack11lll111ll1_opy_)