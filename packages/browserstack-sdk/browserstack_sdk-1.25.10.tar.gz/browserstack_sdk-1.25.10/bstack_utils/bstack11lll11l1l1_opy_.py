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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll11l11l_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l111ll11_opy_ = urljoin(builder, bstack11111l_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳࠨᶉ"))
        if params:
            bstack111l111ll11_opy_ += bstack11111l_opy_ (u"ࠤࡂࡿࢂࠨᶊ").format(urlencode({bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᶋ"): params.get(bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᶌ"))}))
        return bstack11lll11l11l_opy_.bstack111l111lll1_opy_(bstack111l111ll11_opy_)
    @staticmethod
    def bstack11lll11ll11_opy_(builder,params=None):
        bstack111l111ll11_opy_ = urljoin(builder, bstack11111l_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭ᶍ"))
        if params:
            bstack111l111ll11_opy_ += bstack11111l_opy_ (u"ࠨ࠿ࡼࡿࠥᶎ").format(urlencode({bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᶏ"): params.get(bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᶐ"))}))
        return bstack11lll11l11l_opy_.bstack111l111lll1_opy_(bstack111l111ll11_opy_)
    @staticmethod
    def bstack111l111lll1_opy_(bstack111l111ll1l_opy_):
        bstack111l111l1ll_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᶑ"), os.environ.get(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᶒ"), bstack11111l_opy_ (u"ࠫࠬᶓ")))
        headers = {bstack11111l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᶔ"): bstack11111l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᶕ").format(bstack111l111l1ll_opy_)}
        response = requests.get(bstack111l111ll1l_opy_, headers=headers)
        bstack111l111llll_opy_ = {}
        try:
            bstack111l111llll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack11111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨᶖ").format(e))
            pass
        if bstack111l111llll_opy_ is not None:
            bstack111l111llll_opy_[bstack11111l_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᶗ")] = response.headers.get(bstack11111l_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᶘ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l111llll_opy_[bstack11111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᶙ")] = response.status_code
        return bstack111l111llll_opy_