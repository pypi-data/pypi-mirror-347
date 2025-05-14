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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11lll1ll1l1_opy_ as bstack11llll11l1l_opy_, EVENTS
from bstack_utils.bstack1l1l1ll111_opy_ import bstack1l1l1ll111_opy_
from bstack_utils.helper import bstack1l11l1lll_opy_, bstack111l11llll_opy_, bstack11l1l1l11l_opy_, bstack11lllll1111_opy_, \
  bstack11lllll1l11_opy_, bstack1lll11l1l1_opy_, get_host_info, bstack11llll111ll_opy_, bstack11111ll1_opy_, bstack111l1lllll_opy_, bstack11l11llll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11ll1ll1l1_opy_ import get_logger
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lllll11lll_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1lll11ll11_opy_ = bstack1lllll11lll_opy_()
@bstack111l1lllll_opy_(class_method=False)
def _11lll1l1lll_opy_(driver, bstack1111llllll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11111l_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬᕟ"): caps.get(bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᕠ"), None),
        bstack11111l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᕡ"): bstack1111llllll_opy_.get(bstack11111l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᕢ"), None),
        bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᕣ"): caps.get(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᕤ"), None),
        bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᕥ"): caps.get(bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᕦ"), None)
    }
  except Exception as error:
    logger.debug(bstack11111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᕧ") + str(error))
  return response
def on():
    if os.environ.get(bstack11111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᕨ"), None) is None or os.environ[bstack11111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᕩ")] == bstack11111l_opy_ (u"ࠣࡰࡸࡰࡱࠨᕪ"):
        return False
    return True
def bstack1l1l11111_opy_(config):
  return config.get(bstack11111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᕫ"), False) or any([p.get(bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᕬ"), False) == True for p in config.get(bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕭ"), [])])
def bstack111l111ll_opy_(config, bstack1llll1l1ll_opy_):
  try:
    if not bstack11l1l1l11l_opy_(config):
      return False
    bstack11lll1llll1_opy_ = config.get(bstack11111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕮ"), False)
    if int(bstack1llll1l1ll_opy_) < len(config.get(bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᕯ"), [])) and config[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᕰ")][bstack1llll1l1ll_opy_]:
      bstack11lll1ll111_opy_ = config[bstack11111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᕱ")][bstack1llll1l1ll_opy_].get(bstack11111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᕲ"), None)
    else:
      bstack11lll1ll111_opy_ = config.get(bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᕳ"), None)
    if bstack11lll1ll111_opy_ != None:
      bstack11lll1llll1_opy_ = bstack11lll1ll111_opy_
    bstack11lll1lll1l_opy_ = os.getenv(bstack11111l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᕴ")) is not None and len(os.getenv(bstack11111l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᕵ"))) > 0 and os.getenv(bstack11111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᕶ")) != bstack11111l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᕷ")
    return bstack11lll1llll1_opy_ and bstack11lll1lll1l_opy_
  except Exception as error:
    logger.debug(bstack11111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᕸ") + str(error))
  return False
def bstack11l111ll_opy_(test_tags):
  bstack1ll1ll111l1_opy_ = os.getenv(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᕹ"))
  if bstack1ll1ll111l1_opy_ is None:
    return True
  bstack1ll1ll111l1_opy_ = json.loads(bstack1ll1ll111l1_opy_)
  try:
    include_tags = bstack1ll1ll111l1_opy_[bstack11111l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᕺ")] if bstack11111l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᕻ") in bstack1ll1ll111l1_opy_ and isinstance(bstack1ll1ll111l1_opy_[bstack11111l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᕼ")], list) else []
    exclude_tags = bstack1ll1ll111l1_opy_[bstack11111l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᕽ")] if bstack11111l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᕾ") in bstack1ll1ll111l1_opy_ and isinstance(bstack1ll1ll111l1_opy_[bstack11111l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᕿ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᖀ") + str(error))
  return False
def bstack11llll1ll1l_opy_(config, bstack11lll1lllll_opy_, bstack11lllll11l1_opy_, bstack11llll11l11_opy_):
  bstack11lll1ll11l_opy_ = bstack11lllll1111_opy_(config)
  bstack11llll1llll_opy_ = bstack11lllll1l11_opy_(config)
  if bstack11lll1ll11l_opy_ is None or bstack11llll1llll_opy_ is None:
    logger.error(bstack11111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᖁ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᖂ"), bstack11111l_opy_ (u"ࠬࢁࡽࠨᖃ")))
    data = {
        bstack11111l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᖄ"): config[bstack11111l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᖅ")],
        bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᖆ"): config.get(bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᖇ"), os.path.basename(os.getcwd())),
        bstack11111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ᖈ"): bstack1l11l1lll_opy_(),
        bstack11111l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᖉ"): config.get(bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᖊ"), bstack11111l_opy_ (u"࠭ࠧᖋ")),
        bstack11111l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᖌ"): {
            bstack11111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᖍ"): bstack11lll1lllll_opy_,
            bstack11111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᖎ"): bstack11lllll11l1_opy_,
            bstack11111l_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᖏ"): __version__,
            bstack11111l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᖐ"): bstack11111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᖑ"),
            bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᖒ"): bstack11111l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᖓ"),
            bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖔ"): bstack11llll11l11_opy_
        },
        bstack11111l_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᖕ"): settings,
        bstack11111l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᖖ"): bstack11llll111ll_opy_(),
        bstack11111l_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᖗ"): bstack1lll11l1l1_opy_(),
        bstack11111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᖘ"): get_host_info(),
        bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᖙ"): bstack11l1l1l11l_opy_(config)
    }
    headers = {
        bstack11111l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᖚ"): bstack11111l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᖛ"),
    }
    config = {
        bstack11111l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᖜ"): (bstack11lll1ll11l_opy_, bstack11llll1llll_opy_),
        bstack11111l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᖝ"): headers
    }
    response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠫࡕࡕࡓࡕࠩᖞ"), bstack11llll11l1l_opy_ + bstack11111l_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᖟ"), data, config)
    bstack11llll1l1l1_opy_ = response.json()
    if bstack11llll1l1l1_opy_[bstack11111l_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᖠ")]:
      parsed = json.loads(os.getenv(bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᖡ"), bstack11111l_opy_ (u"ࠨࡽࢀࠫᖢ")))
      parsed[bstack11111l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᖣ")] = bstack11llll1l1l1_opy_[bstack11111l_opy_ (u"ࠪࡨࡦࡺࡡࠨᖤ")][bstack11111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᖥ")]
      os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᖦ")] = json.dumps(parsed)
      bstack1l1l1ll111_opy_.bstack11lll1111_opy_(bstack11llll1l1l1_opy_[bstack11111l_opy_ (u"࠭ࡤࡢࡶࡤࠫᖧ")][bstack11111l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᖨ")])
      bstack1l1l1ll111_opy_.bstack11lll1l1l11_opy_(bstack11llll1l1l1_opy_[bstack11111l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖩ")][bstack11111l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᖪ")])
      bstack1l1l1ll111_opy_.store()
      return bstack11llll1l1l1_opy_[bstack11111l_opy_ (u"ࠪࡨࡦࡺࡡࠨᖫ")][bstack11111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᖬ")], bstack11llll1l1l1_opy_[bstack11111l_opy_ (u"ࠬࡪࡡࡵࡣࠪᖭ")][bstack11111l_opy_ (u"࠭ࡩࡥࠩᖮ")]
    else:
      logger.error(bstack11111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᖯ") + bstack11llll1l1l1_opy_[bstack11111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖰ")])
      if bstack11llll1l1l1_opy_[bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖱ")] == bstack11111l_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᖲ"):
        for bstack11llll1ll11_opy_ in bstack11llll1l1l1_opy_[bstack11111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᖳ")]:
          logger.error(bstack11llll1ll11_opy_[bstack11111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖴ")])
      return None, None
  except Exception as error:
    logger.error(bstack11111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᖵ") +  str(error))
    return None, None
def bstack11llll1l111_opy_():
  if os.getenv(bstack11111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᖶ")) is None:
    return {
        bstack11111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᖷ"): bstack11111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᖸ"),
        bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖹ"): bstack11111l_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪᖺ")
    }
  data = {bstack11111l_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ᖻ"): bstack1l11l1lll_opy_()}
  headers = {
      bstack11111l_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᖼ"): bstack11111l_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨᖽ") + os.getenv(bstack11111l_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨᖾ")),
      bstack11111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᖿ"): bstack11111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᗀ")
  }
  response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠫࡕ࡛ࡔࠨᗁ"), bstack11llll11l1l_opy_ + bstack11111l_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧᗂ"), data, { bstack11111l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᗃ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣᗄ") + bstack111l11llll_opy_().isoformat() + bstack11111l_opy_ (u"ࠨ࡜ࠪᗅ"))
      return {bstack11111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᗆ"): bstack11111l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᗇ"), bstack11111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᗈ"): bstack11111l_opy_ (u"ࠬ࠭ᗉ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤᗊ") + str(error))
    return {
        bstack11111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᗋ"): bstack11111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᗌ"),
        bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᗍ"): str(error)
    }
def bstack11lll1lll11_opy_(bstack11llll1l1ll_opy_):
    return re.match(bstack11111l_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫᗎ"), bstack11llll1l1ll_opy_.strip()) is not None
def bstack1ll1ll111l_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11llll1111l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11llll1111l_opy_ = desired_capabilities
        else:
          bstack11llll1111l_opy_ = {}
        bstack11llll111l1_opy_ = (bstack11llll1111l_opy_.get(bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᗏ"), bstack11111l_opy_ (u"ࠬ࠭ᗐ")).lower() or caps.get(bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᗑ"), bstack11111l_opy_ (u"ࠧࠨᗒ")).lower())
        if bstack11llll111l1_opy_ == bstack11111l_opy_ (u"ࠨ࡫ࡲࡷࠬᗓ"):
            return True
        if bstack11llll111l1_opy_ == bstack11111l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᗔ"):
            bstack11lll1ll1ll_opy_ = str(float(caps.get(bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗕ")) or bstack11llll1111l_opy_.get(bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᗖ"), {}).get(bstack11111l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗗ"),bstack11111l_opy_ (u"࠭ࠧᗘ"))))
            if bstack11llll111l1_opy_ == bstack11111l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᗙ") and int(bstack11lll1ll1ll_opy_.split(bstack11111l_opy_ (u"ࠨ࠰ࠪᗚ"))[0]) < float(bstack11lll1l1l1l_opy_):
                logger.warning(str(bstack11llll11lll_opy_))
                return False
            return True
        bstack1ll1ll11l1l_opy_ = caps.get(bstack11111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗛ"), {}).get(bstack11111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᗜ"), caps.get(bstack11111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᗝ"), bstack11111l_opy_ (u"ࠬ࠭ᗞ")))
        if bstack1ll1ll11l1l_opy_:
            logger.warn(bstack11111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᗟ"))
            return False
        browser = caps.get(bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᗠ"), bstack11111l_opy_ (u"ࠨࠩᗡ")).lower() or bstack11llll1111l_opy_.get(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᗢ"), bstack11111l_opy_ (u"ࠪࠫᗣ")).lower()
        if browser != bstack11111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᗤ"):
            logger.warning(bstack11111l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᗥ"))
            return False
        browser_version = caps.get(bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗦ")) or caps.get(bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᗧ")) or bstack11llll1111l_opy_.get(bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᗨ")) or bstack11llll1111l_opy_.get(bstack11111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗩ"), {}).get(bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᗪ")) or bstack11llll1111l_opy_.get(bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᗫ"), {}).get(bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᗬ"))
        if browser_version and browser_version != bstack11111l_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᗭ") and int(browser_version.split(bstack11111l_opy_ (u"ࠧ࠯ࠩᗮ"))[0]) <= 98:
            logger.warning(bstack11111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢ࠼࠼࠳ࠨᗯ"))
            return False
        if not options:
            bstack1ll11lll11l_opy_ = caps.get(bstack11111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᗰ")) or bstack11llll1111l_opy_.get(bstack11111l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᗱ"), {})
            if bstack11111l_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᗲ") in bstack1ll11lll11l_opy_.get(bstack11111l_opy_ (u"ࠬࡧࡲࡨࡵࠪᗳ"), []):
                logger.warn(bstack11111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᗴ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack11111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᗵ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll1lll1ll_opy_ = config.get(bstack11111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᗶ"), {})
    bstack1lll1lll1ll_opy_[bstack11111l_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᗷ")] = os.getenv(bstack11111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᗸ"))
    bstack11llll11111_opy_ = json.loads(os.getenv(bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᗹ"), bstack11111l_opy_ (u"ࠬࢁࡽࠨᗺ"))).get(bstack11111l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗻ"))
    caps[bstack11111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᗼ")] = True
    if not config[bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᗽ")].get(bstack11111l_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣᗾ")):
      if bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᗿ") in caps:
        caps[bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘀ")][bstack11111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᘁ")] = bstack1lll1lll1ll_opy_
        caps[bstack11111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘂ")][bstack11111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᘃ")][bstack11111l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᘄ")] = bstack11llll11111_opy_
      else:
        caps[bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᘅ")] = bstack1lll1lll1ll_opy_
        caps[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᘆ")][bstack11111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘇ")] = bstack11llll11111_opy_
  except Exception as error:
    logger.debug(bstack11111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨᘈ") +  str(error))
def bstack1lll1l11_opy_(driver, bstack11lllll11ll_opy_):
  try:
    setattr(driver, bstack11111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᘉ"), True)
    session = driver.session_id
    if session:
      bstack11lllll111l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lllll111l_opy_ = False
      bstack11lllll111l_opy_ = url.scheme in [bstack11111l_opy_ (u"ࠢࡩࡶࡷࡴࠧᘊ"), bstack11111l_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢᘋ")]
      if bstack11lllll111l_opy_:
        if bstack11lllll11ll_opy_:
          logger.info(bstack11111l_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡨࡲࡶࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲ࠥࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡧ࡫ࡧࡪࡰࠣࡱࡴࡳࡥ࡯ࡶࡤࡶ࡮ࡲࡹ࠯ࠤᘌ"))
      return bstack11lllll11ll_opy_
  except Exception as e:
    logger.error(bstack11111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᘍ") + str(e))
    return False
def bstack11ll11l1ll_opy_(driver, name, path):
  try:
    bstack1ll1l111lll_opy_ = {
        bstack11111l_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᘎ"): threading.current_thread().current_test_uuid,
        bstack11111l_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᘏ"): os.environ.get(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᘐ"), bstack11111l_opy_ (u"ࠧࠨᘑ")),
        bstack11111l_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬᘒ"): os.environ.get(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᘓ"), bstack11111l_opy_ (u"ࠪࠫᘔ"))
    }
    bstack1ll1ll111ll_opy_ = bstack1lll11ll11_opy_.bstack1ll1l11l111_opy_(EVENTS.bstack1l1lll1l_opy_.value)
    logger.debug(bstack11111l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᘕ"))
    try:
      if (bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᘖ"), None) and bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᘗ"), None)):
        scripts = {bstack11111l_opy_ (u"ࠧࡴࡥࡤࡲࠬᘘ"): bstack1l1l1ll111_opy_.perform_scan}
        bstack11lll1l1ll1_opy_ = json.loads(scripts[bstack11111l_opy_ (u"ࠣࡵࡦࡥࡳࠨᘙ")].replace(bstack11111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᘚ"), bstack11111l_opy_ (u"ࠥࠦᘛ")))
        bstack11lll1l1ll1_opy_[bstack11111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᘜ")][bstack11111l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᘝ")] = None
        scripts[bstack11111l_opy_ (u"ࠨࡳࡤࡣࡱࠦᘞ")] = bstack11111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘟ") + json.dumps(bstack11lll1l1ll1_opy_)
        bstack1l1l1ll111_opy_.bstack11lll1111_opy_(scripts)
        bstack1l1l1ll111_opy_.store()
        logger.debug(driver.execute_script(bstack1l1l1ll111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1l1ll111_opy_.perform_scan, {bstack11111l_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᘠ"): name}))
      bstack1lll11ll11_opy_.end(EVENTS.bstack1l1lll1l_opy_.value, bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘡ"), bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘢ"), True, None)
    except Exception as error:
      bstack1lll11ll11_opy_.end(EVENTS.bstack1l1lll1l_opy_.value, bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᘣ"), bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᘤ"), False, str(error))
    bstack1ll1ll111ll_opy_ = bstack1lll11ll11_opy_.bstack11llll1lll1_opy_(EVENTS.bstack1ll1l11111l_opy_.value)
    bstack1lll11ll11_opy_.mark(bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᘥ"))
    try:
      if (bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᘦ"), None) and bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᘧ"), None)):
        scripts = {bstack11111l_opy_ (u"ࠩࡶࡧࡦࡴࠧᘨ"): bstack1l1l1ll111_opy_.perform_scan}
        bstack11lll1l1ll1_opy_ = json.loads(scripts[bstack11111l_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᘩ")].replace(bstack11111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᘪ"), bstack11111l_opy_ (u"ࠧࠨᘫ")))
        bstack11lll1l1ll1_opy_[bstack11111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᘬ")][bstack11111l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧᘭ")] = None
        scripts[bstack11111l_opy_ (u"ࠣࡵࡦࡥࡳࠨᘮ")] = bstack11111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᘯ") + json.dumps(bstack11lll1l1ll1_opy_)
        bstack1l1l1ll111_opy_.bstack11lll1111_opy_(scripts)
        bstack1l1l1ll111_opy_.store()
        logger.debug(driver.execute_script(bstack1l1l1ll111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1l1ll111_opy_.bstack11llll1l11l_opy_, bstack1ll1l111lll_opy_))
      bstack1lll11ll11_opy_.end(bstack1ll1ll111ll_opy_, bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᘰ"), bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᘱ"),True, None)
    except Exception as error:
      bstack1lll11ll11_opy_.end(bstack1ll1ll111ll_opy_, bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᘲ"), bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᘳ"),False, str(error))
    logger.info(bstack11111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᘴ"))
  except Exception as bstack1ll1l1l111l_opy_:
    logger.error(bstack11111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᘵ") + str(path) + bstack11111l_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᘶ") + str(bstack1ll1l1l111l_opy_))
def bstack11llll11ll1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᘷ")) and str(caps.get(bstack11111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᘸ"))).lower() == bstack11111l_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨᘹ"):
        bstack11lll1ll1ll_opy_ = caps.get(bstack11111l_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᘺ")) or caps.get(bstack11111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᘻ"))
        if bstack11lll1ll1ll_opy_ and int(str(bstack11lll1ll1ll_opy_)) < bstack11lll1l1l1l_opy_:
            return False
    return True
def bstack1l1l1l1111_opy_(config):
  if bstack11111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᘼ") in config:
        return config[bstack11111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᘽ")]
  for platform in config.get(bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᘾ"), []):
      if bstack11111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘿ") in platform:
          return platform[bstack11111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᙀ")]
  return None