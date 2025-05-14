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
class RobotHandler():
    def __init__(self, args, logger, bstack1111ll1l11_opy_, bstack1111llll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1l11_opy_ = bstack1111ll1l11_opy_
        self.bstack1111llll11_opy_ = bstack1111llll11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111ll1l1l1_opy_(bstack1111l1lll1_opy_):
        bstack1111ll1111_opy_ = []
        if bstack1111l1lll1_opy_:
            tokens = str(os.path.basename(bstack1111l1lll1_opy_)).split(bstack11111l_opy_ (u"ࠧࡥࠢဒ"))
            camelcase_name = bstack11111l_opy_ (u"ࠨࠠࠣဓ").join(t.title() for t in tokens)
            suite_name, bstack1111l1llll_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll1111_opy_.append(suite_name)
        return bstack1111ll1111_opy_
    @staticmethod
    def bstack1111ll111l_opy_(typename):
        if bstack11111l_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥန") in typename:
            return bstack11111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤပ")
        return bstack11111l_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥဖ")