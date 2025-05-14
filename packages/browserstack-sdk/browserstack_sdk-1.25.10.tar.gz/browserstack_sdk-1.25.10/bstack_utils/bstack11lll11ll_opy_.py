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
import threading
import logging
import bstack_utils.accessibility as bstack11l1ll1l1_opy_
from bstack_utils.helper import bstack11l11llll1_opy_
logger = logging.getLogger(__name__)
def bstack1lllllll11_opy_(bstack1l11lll1l_opy_):
  return True if bstack1l11lll1l_opy_ in threading.current_thread().__dict__.keys() else False
def bstack1l11111111_opy_(context, *args):
    tags = getattr(args[0], bstack11111l_opy_ (u"ࠧࡵࡣࡪࡷࠬᙥ"), [])
    bstack1111l111_opy_ = bstack11l1ll1l1_opy_.bstack11l111ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1111l111_opy_
    try:
      bstack1l11l1l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllllll11_opy_(bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᙦ")) else context.browser
      if bstack1l11l1l111_opy_ and bstack1l11l1l111_opy_.session_id and bstack1111l111_opy_ and bstack11l11llll1_opy_(
              threading.current_thread(), bstack11111l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᙧ"), None):
          threading.current_thread().isA11yTest = bstack11l1ll1l1_opy_.bstack1lll1l11_opy_(bstack1l11l1l111_opy_, bstack1111l111_opy_)
    except Exception as e:
       logger.debug(bstack11111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡧ࠱࠲ࡻࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪᙨ").format(str(e)))
def bstack11l11lll11_opy_(bstack1l11l1l111_opy_):
    if bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᙩ"), None) and bstack11l11llll1_opy_(
      threading.current_thread(), bstack11111l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᙪ"), None) and not bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡣࡸࡺ࡯ࡱࠩᙫ"), False):
      threading.current_thread().a11y_stop = True
      bstack11l1ll1l1_opy_.bstack11ll11l1ll_opy_(bstack1l11l1l111_opy_, name=bstack11111l_opy_ (u"ࠢࠣᙬ"), path=bstack11111l_opy_ (u"ࠣࠤ᙭"))