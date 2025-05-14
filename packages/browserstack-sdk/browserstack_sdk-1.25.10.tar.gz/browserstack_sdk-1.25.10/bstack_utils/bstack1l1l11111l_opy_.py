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
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11llll111ll_opy_, bstack1lll11l1l1_opy_, get_host_info, bstack11ll11l1ll1_opy_, \
 bstack11l1l1l11l_opy_, bstack11l11llll1_opy_, bstack111l1lllll_opy_, bstack11l1l1111ll_opy_, bstack1l11l1lll_opy_
import bstack_utils.accessibility as bstack11l1ll1l1_opy_
from bstack_utils.bstack11l111llll_opy_ import bstack1l1ll11l1l_opy_
from bstack_utils.percy import bstack1l1111111l_opy_
from bstack_utils.config import Config
bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1111111l_opy_()
@bstack111l1lllll_opy_(class_method=False)
def bstack1111ll11ll1_opy_(bs_config, bstack1lll111l1l_opy_):
  try:
    data = {
        bstack11111l_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧἉ"): bstack11111l_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭Ἂ"),
        bstack11111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨἋ"): bs_config.get(bstack11111l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨἌ"), bstack11111l_opy_ (u"ࠫࠬἍ")),
        bstack11111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪἎ"): bs_config.get(bstack11111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩἏ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪἐ"): bs_config.get(bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪἑ")),
        bstack11111l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧἒ"): bs_config.get(bstack11111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ἓ"), bstack11111l_opy_ (u"ࠫࠬἔ")),
        bstack11111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩἕ"): bstack1l11l1lll_opy_(),
        bstack11111l_opy_ (u"࠭ࡴࡢࡩࡶࠫ἖"): bstack11ll11l1ll1_opy_(bs_config),
        bstack11111l_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪ἗"): get_host_info(),
        bstack11111l_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩἘ"): bstack1lll11l1l1_opy_(),
        bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩἙ"): os.environ.get(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩἚ")),
        bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩἛ"): os.environ.get(bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪἜ"), False),
        bstack11111l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨἝ"): bstack11llll111ll_opy_(),
        bstack11111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ἞"): bstack1111l1ll111_opy_(),
        bstack11111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬ἟"): bstack1111l1l111l_opy_(bstack1lll111l1l_opy_),
        bstack11111l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧἠ"): bstack1111l1l1l11_opy_(bs_config, bstack1lll111l1l_opy_.get(bstack11111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫἡ"), bstack11111l_opy_ (u"ࠫࠬἢ"))),
        bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧἣ"): bstack11l1l1l11l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢἤ").format(str(error)))
    return None
def bstack1111l1l111l_opy_(framework):
  return {
    bstack11111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧἥ"): framework.get(bstack11111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩἦ"), bstack11111l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩἧ")),
    bstack11111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ἠ"): framework.get(bstack11111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨἩ")),
    bstack11111l_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩἪ"): framework.get(bstack11111l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫἫ")),
    bstack11111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩἬ"): bstack11111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨἭ"),
    bstack11111l_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩἮ"): framework.get(bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪἯ"))
  }
def bstack1l1llll1l_opy_(bs_config, framework):
  bstack1111111ll_opy_ = False
  bstack1111l1lll_opy_ = False
  bstack1111l1l11l1_opy_ = False
  if bstack11111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨἰ") in bs_config:
    bstack1111l1l11l1_opy_ = True
  elif bstack11111l_opy_ (u"ࠬࡧࡰࡱࠩἱ") in bs_config:
    bstack1111111ll_opy_ = True
  else:
    bstack1111l1lll_opy_ = True
  bstack1llll111l_opy_ = {
    bstack11111l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ἲ"): bstack1l1ll11l1l_opy_.bstack1111l1l1l1l_opy_(bs_config, framework),
    bstack11111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧἳ"): bstack11l1ll1l1_opy_.bstack1l1l11111_opy_(bs_config),
    bstack11111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧἴ"): bs_config.get(bstack11111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨἵ"), False),
    bstack11111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬἶ"): bstack1111l1lll_opy_,
    bstack11111l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪἷ"): bstack1111111ll_opy_,
    bstack11111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩἸ"): bstack1111l1l11l1_opy_
  }
  return bstack1llll111l_opy_
@bstack111l1lllll_opy_(class_method=False)
def bstack1111l1ll111_opy_():
  try:
    bstack1111l1l11ll_opy_ = json.loads(os.getenv(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧἹ"), bstack11111l_opy_ (u"ࠧࡼࡿࠪἺ")))
    return {
        bstack11111l_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪἻ"): bstack1111l1l11ll_opy_
    }
  except Exception as error:
    logger.error(bstack11111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡷࡪࡺࡴࡪࡰࡪࡷࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣἼ").format(str(error)))
    return {}
def bstack1111lll11ll_opy_(array, bstack1111l1ll11l_opy_, bstack1111l11llll_opy_):
  result = {}
  for o in array:
    key = o[bstack1111l1ll11l_opy_]
    result[key] = o[bstack1111l11llll_opy_]
  return result
def bstack1111ll1l1l1_opy_(bstack1111111l_opy_=bstack11111l_opy_ (u"ࠪࠫἽ")):
  bstack1111l11lll1_opy_ = bstack11l1ll1l1_opy_.on()
  bstack1111l1l1ll1_opy_ = bstack1l1ll11l1l_opy_.on()
  bstack1111l1l1lll_opy_ = percy.bstack111l1ll1l_opy_()
  if bstack1111l1l1lll_opy_ and not bstack1111l1l1ll1_opy_ and not bstack1111l11lll1_opy_:
    return bstack1111111l_opy_ not in [bstack11111l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨἾ"), bstack11111l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩἿ")]
  elif bstack1111l11lll1_opy_ and not bstack1111l1l1ll1_opy_:
    return bstack1111111l_opy_ not in [bstack11111l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧὀ"), bstack11111l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩὁ"), bstack11111l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬὂ")]
  return bstack1111l11lll1_opy_ or bstack1111l1l1ll1_opy_ or bstack1111l1l1lll_opy_
@bstack111l1lllll_opy_(class_method=False)
def bstack1111ll1lll1_opy_(bstack1111111l_opy_, test=None):
  bstack1111l1l1111_opy_ = bstack11l1ll1l1_opy_.on()
  if not bstack1111l1l1111_opy_ or bstack1111111l_opy_ not in [bstack11111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫὃ")] or test == None:
    return None
  return {
    bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪὄ"): bstack1111l1l1111_opy_ and bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪὅ"), None) == True and bstack11l1ll1l1_opy_.bstack11l111ll_opy_(test[bstack11111l_opy_ (u"ࠬࡺࡡࡨࡵࠪ὆")])
  }
def bstack1111l1l1l11_opy_(bs_config, framework):
  bstack1111111ll_opy_ = False
  bstack1111l1lll_opy_ = False
  bstack1111l1l11l1_opy_ = False
  if bstack11111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ὇") in bs_config:
    bstack1111l1l11l1_opy_ = True
  elif bstack11111l_opy_ (u"ࠧࡢࡲࡳࠫὈ") in bs_config:
    bstack1111111ll_opy_ = True
  else:
    bstack1111l1lll_opy_ = True
  bstack1llll111l_opy_ = {
    bstack11111l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨὉ"): bstack1l1ll11l1l_opy_.bstack1111l1l1l1l_opy_(bs_config, framework),
    bstack11111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩὊ"): bstack11l1ll1l1_opy_.bstack1l1l1l1111_opy_(bs_config),
    bstack11111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩὋ"): bs_config.get(bstack11111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪὌ"), False),
    bstack11111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧὍ"): bstack1111l1lll_opy_,
    bstack11111l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ὎"): bstack1111111ll_opy_,
    bstack11111l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ὏"): bstack1111l1l11l1_opy_
  }
  return bstack1llll111l_opy_