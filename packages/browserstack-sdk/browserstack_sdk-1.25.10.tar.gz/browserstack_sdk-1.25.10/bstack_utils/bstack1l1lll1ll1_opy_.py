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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll11l1l1_opy_ import bstack11lll11l11l_opy_
from bstack_utils.constants import *
import json
class bstack11ll1lll_opy_:
    def __init__(self, bstack1llll1llll_opy_, bstack11lll11lll1_opy_):
        self.bstack1llll1llll_opy_ = bstack1llll1llll_opy_
        self.bstack11lll11lll1_opy_ = bstack11lll11lll1_opy_
        self.bstack11lll11l1ll_opy_ = None
    def __call__(self):
        bstack11lll111lll_opy_ = {}
        while True:
            self.bstack11lll11l1ll_opy_ = bstack11lll111lll_opy_.get(
                bstack11111l_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡳࡱࡲ࡟ࡵ࡫ࡰࡩࠬᙛ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll11llll_opy_ = self.bstack11lll11l1ll_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll11llll_opy_ > 0:
                sleep(bstack11lll11llll_opy_ / 1000)
            params = {
                bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᙜ"): self.bstack1llll1llll_opy_,
                bstack11111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᙝ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll11ll1l_opy_ = bstack11111l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᙞ") + bstack11lll11l111_opy_ + bstack11111l_opy_ (u"ࠣ࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡦࡶࡩ࠰ࡸ࠴࠳ࠧᙟ")
            if self.bstack11lll11lll1_opy_.lower() == bstack11111l_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࡵࠥᙠ"):
                bstack11lll111lll_opy_ = bstack11lll11l11l_opy_.results(bstack11lll11ll1l_opy_, params)
            else:
                bstack11lll111lll_opy_ = bstack11lll11l11l_opy_.bstack11lll11ll11_opy_(bstack11lll11ll1l_opy_, params)
            if str(bstack11lll111lll_opy_.get(bstack11111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᙡ"), bstack11111l_opy_ (u"ࠫ࠷࠶࠰ࠨᙢ"))) != bstack11111l_opy_ (u"ࠬ࠺࠰࠵ࠩᙣ"):
                break
        return bstack11lll111lll_opy_.get(bstack11111l_opy_ (u"࠭ࡤࡢࡶࡤࠫᙤ"), bstack11lll111lll_opy_)