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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l11ll1l1l_opy_, bstack11111lll_opy_, bstack11l11llll1_opy_, bstack11ll1ll1_opy_, \
    bstack11l1l11111l_opy_
from bstack_utils.measure import measure
def bstack1l11l1111l_opy_(bstack111l111l111_opy_):
    for driver in bstack111l111l111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack1l1llll11_opy_)
def bstack111ll11l1_opy_(driver, status, reason=bstack11111l_opy_ (u"ࠫࠬᶚ")):
    bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
    if bstack1l11l11ll1_opy_.bstack1111lll111_opy_():
        return
    bstack111ll1l1l_opy_ = bstack11l1llll_opy_(bstack11111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᶛ"), bstack11111l_opy_ (u"࠭ࠧᶜ"), status, reason, bstack11111l_opy_ (u"ࠧࠨᶝ"), bstack11111l_opy_ (u"ࠨࠩᶞ"))
    driver.execute_script(bstack111ll1l1l_opy_)
@measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack1l1llll11_opy_)
def bstack1l1l1l111_opy_(page, status, reason=bstack11111l_opy_ (u"ࠩࠪᶟ")):
    try:
        if page is None:
            return
        bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
        if bstack1l11l11ll1_opy_.bstack1111lll111_opy_():
            return
        bstack111ll1l1l_opy_ = bstack11l1llll_opy_(bstack11111l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᶠ"), bstack11111l_opy_ (u"ࠫࠬᶡ"), status, reason, bstack11111l_opy_ (u"ࠬ࠭ᶢ"), bstack11111l_opy_ (u"࠭ࠧᶣ"))
        page.evaluate(bstack11111l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᶤ"), bstack111ll1l1l_opy_)
    except Exception as e:
        print(bstack11111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡿࢂࠨᶥ"), e)
def bstack11l1llll_opy_(type, name, status, reason, bstack1ll11ll111_opy_, bstack1l1ll11ll1_opy_):
    bstack1ll1l11l11_opy_ = {
        bstack11111l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩᶦ"): type,
        bstack11111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶧ"): {}
    }
    if type == bstack11111l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ᶨ"):
        bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᶩ")][bstack11111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᶪ")] = bstack1ll11ll111_opy_
        bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᶫ")][bstack11111l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᶬ")] = json.dumps(str(bstack1l1ll11ll1_opy_))
    if type == bstack11111l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᶭ"):
        bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶮ")][bstack11111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᶯ")] = name
    if type == bstack11111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨᶰ"):
        bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶱ")][bstack11111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᶲ")] = status
        if status == bstack11111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᶳ") and str(reason) != bstack11111l_opy_ (u"ࠤࠥᶴ"):
            bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶵ")][bstack11111l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫᶶ")] = json.dumps(str(reason))
    bstack11l1ll1lll_opy_ = bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪᶷ").format(json.dumps(bstack1ll1l11l11_opy_))
    return bstack11l1ll1lll_opy_
def bstack1llll1111_opy_(url, config, logger, bstack1llllll1l_opy_=False):
    hostname = bstack11111lll_opy_(url)
    is_private = bstack11ll1ll1_opy_(hostname)
    try:
        if is_private or bstack1llllll1l_opy_:
            file_path = bstack11l11ll1l1l_opy_(bstack11111l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᶸ"), bstack11111l_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ᶹ"), logger)
            if os.environ.get(bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᶺ")) and eval(
                    os.environ.get(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᶻ"))):
                return
            if (bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᶼ") in config and not config[bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᶽ")]):
                os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᶾ")] = str(True)
                bstack111l111l11l_opy_ = {bstack11111l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨᶿ"): hostname}
                bstack11l1l11111l_opy_(bstack11111l_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭᷀"), bstack11111l_opy_ (u"ࠨࡰࡸࡨ࡬࡫࡟࡭ࡱࡦࡥࡱ࠭᷁"), bstack111l111l11l_opy_, logger)
    except Exception as e:
        pass
def bstack1lll1ll11l_opy_(caps, bstack111l111l1l1_opy_):
    if bstack11111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵ᷂ࠪ") in caps:
        caps[bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᷃")][bstack11111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪ᷄")] = True
        if bstack111l111l1l1_opy_:
            caps[bstack11111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᷅")][bstack11111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ᷆")] = bstack111l111l1l1_opy_
    else:
        caps[bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ᷇")] = True
        if bstack111l111l1l1_opy_:
            caps[bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᷈")] = bstack111l111l1l1_opy_
def bstack111l1l1111l_opy_(bstack111l11ll1l_opy_):
    bstack111l1111lll_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭᷉"), bstack11111l_opy_ (u"᷊ࠪࠫ"))
    if bstack111l1111lll_opy_ == bstack11111l_opy_ (u"ࠫࠬ᷋") or bstack111l1111lll_opy_ == bstack11111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭᷌"):
        threading.current_thread().testStatus = bstack111l11ll1l_opy_
    else:
        if bstack111l11ll1l_opy_ == bstack11111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᷍"):
            threading.current_thread().testStatus = bstack111l11ll1l_opy_