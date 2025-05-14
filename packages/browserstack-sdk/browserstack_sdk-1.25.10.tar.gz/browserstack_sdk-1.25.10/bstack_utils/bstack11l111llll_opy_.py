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
from bstack_utils.helper import bstack11ll11l11_opy_
from bstack_utils.constants import bstack11ll1l1ll1l_opy_, EVENTS, STAGE
from bstack_utils.bstack11ll1ll1l1_opy_ import get_logger
logger = get_logger(__name__)
class bstack1l1ll11l1l_opy_:
    bstack111l11l1lll_opy_ = None
    @classmethod
    def bstack1lllll1l1l_opy_(cls):
        if cls.on() and os.getenv(bstack11111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨὐ")):
            logger.info(
                bstack11111l_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬὑ").format(os.getenv(bstack11111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣὒ"))))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨὓ"), None) is None or os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩὔ")] == bstack11111l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦὕ"):
            return False
        return True
    @classmethod
    def bstack1111l1l1l1l_opy_(cls, bs_config, framework=bstack11111l_opy_ (u"ࠢࠣὖ")):
        bstack11ll1llllll_opy_ = False
        for fw in bstack11ll1l1ll1l_opy_:
            if fw in framework:
                bstack11ll1llllll_opy_ = True
        return bstack11ll11l11_opy_(bs_config.get(bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬὗ"), bstack11ll1llllll_opy_))
    @classmethod
    def bstack1111l11ll11_opy_(cls, framework):
        return framework in bstack11ll1l1ll1l_opy_
    @classmethod
    def bstack1111lll1l11_opy_(cls, bs_config, framework):
        return cls.bstack1111l1l1l1l_opy_(bs_config, framework) is True and cls.bstack1111l11ll11_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭὘"), None)
    @staticmethod
    def bstack111llll1ll_opy_():
        if getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧὙ"), None):
            return {
                bstack11111l_opy_ (u"ࠫࡹࡿࡰࡦࠩ὚"): bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࠪὛ"),
                bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭὜"): getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫὝ"), None)
            }
        if getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ὞"), None):
            return {
                bstack11111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧὟ"): bstack11111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨὠ"),
                bstack11111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫὡ"): getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩὢ"), None)
            }
        return None
    @staticmethod
    def bstack1111l11l1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1ll11l1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack111ll1l1l1_opy_(test, hook_name=None):
        bstack1111l11ll1l_opy_ = test.parent
        if hook_name in [bstack11111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫὣ"), bstack11111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨὤ"), bstack11111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧὥ"), bstack11111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫὦ")]:
            bstack1111l11ll1l_opy_ = test
        scope = []
        while bstack1111l11ll1l_opy_ is not None:
            scope.append(bstack1111l11ll1l_opy_.name)
            bstack1111l11ll1l_opy_ = bstack1111l11ll1l_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1111l11l1l1_opy_(hook_type):
        if hook_type == bstack11111l_opy_ (u"ࠥࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠣὧ"):
            return bstack11111l_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣ࡬ࡴࡵ࡫ࠣὨ")
        elif hook_type == bstack11111l_opy_ (u"ࠧࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠤὩ"):
            return bstack11111l_opy_ (u"ࠨࡔࡦࡣࡵࡨࡴࡽ࡮ࠡࡪࡲࡳࡰࠨὪ")
    @staticmethod
    def bstack1111l11l11l_opy_(bstack11lll111l1_opy_):
        try:
            if not bstack1l1ll11l1l_opy_.on():
                return bstack11lll111l1_opy_
            if os.environ.get(bstack11111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠧὫ"), None) == bstack11111l_opy_ (u"ࠣࡶࡵࡹࡪࠨὬ"):
                tests = os.environ.get(bstack11111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔ࡟ࡕࡇࡖࡘࡘࠨὭ"), None)
                if tests is None or tests == bstack11111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣὮ"):
                    return bstack11lll111l1_opy_
                bstack11lll111l1_opy_ = tests.split(bstack11111l_opy_ (u"ࠫ࠱࠭Ὧ"))
                return bstack11lll111l1_opy_
        except Exception as exc:
            logger.debug(bstack11111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡷ࡫ࡲࡶࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡵ࠾ࠥࠨὰ") + str(str(exc)) + bstack11111l_opy_ (u"ࠨࠢά"))
        return bstack11lll111l1_opy_