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
import atexit
import signal
import yaml
import socket
import datetime
import string
import random
import collections.abc
import traceback
import copy
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import json
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from browserstack_sdk.bstack11ll1111ll_opy_ import bstack11l11l11_opy_
from browserstack_sdk.bstack1ll1l1ll_opy_ import *
import time
import requests
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.measure import measure
def bstack11lllll111_opy_():
  global CONFIG
  headers = {
        bstack11111l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack11111l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lll111l1_opy_(CONFIG, bstack111l1ll11_opy_)
  try:
    response = requests.get(bstack111l1ll11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1lll11llll_opy_ = response.json()[bstack11111l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack111llll1_opy_.format(response.json()))
      return bstack1lll11llll_opy_
    else:
      logger.debug(bstack1l1lllllll_opy_.format(bstack11111l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l1lllllll_opy_.format(e))
def bstack1l11l1111_opy_(hub_url):
  global CONFIG
  url = bstack11111l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack11111l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack11111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack11111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lll111l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l11ll1lll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll11ll1_opy_.format(hub_url, e))
@measure(event_name=EVENTS.bstack11lllllll1_opy_, stage=STAGE.bstack1l1llll11_opy_)
def bstack1l1l11ll_opy_():
  try:
    global bstack1l1l111ll_opy_
    bstack1lll11llll_opy_ = bstack11lllll111_opy_()
    bstack11l1llll1_opy_ = []
    results = []
    for bstack1l1l11l11_opy_ in bstack1lll11llll_opy_:
      bstack11l1llll1_opy_.append(bstack1l11ll111_opy_(target=bstack1l11l1111_opy_,args=(bstack1l1l11l11_opy_,)))
    for t in bstack11l1llll1_opy_:
      t.start()
    for t in bstack11l1llll1_opy_:
      results.append(t.join())
    bstack11l1llll11_opy_ = {}
    for item in results:
      hub_url = item[bstack11111l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack11111l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11l1llll11_opy_[hub_url] = latency
    bstack1l1l11ll1_opy_ = min(bstack11l1llll11_opy_, key= lambda x: bstack11l1llll11_opy_[x])
    bstack1l1l111ll_opy_ = bstack1l1l11ll1_opy_
    logger.debug(bstack111l11ll1_opy_.format(bstack1l1l11ll1_opy_))
  except Exception as e:
    logger.debug(bstack11l1l11ll1_opy_.format(e))
from browserstack_sdk.bstack1l11l1ll1_opy_ import *
from browserstack_sdk.bstack11l11l1ll_opy_ import *
from browserstack_sdk.bstack1l111l11_opy_ import *
import logging
import requests
from bstack_utils.constants import *
from bstack_utils.bstack11ll1ll1l1_opy_ import get_logger
from bstack_utils.measure import measure
logger = get_logger(__name__)
@measure(event_name=EVENTS.bstack111llll1l_opy_, stage=STAGE.bstack1l1llll11_opy_)
def bstack1ll11ll1l_opy_():
    global bstack1l1l111ll_opy_
    try:
        bstack1l1lll11_opy_ = bstack1ll11llll_opy_()
        bstack1ll1ll11l_opy_(bstack1l1lll11_opy_)
        hub_url = bstack1l1lll11_opy_.get(bstack11111l_opy_ (u"ࠨࡵࡳ࡮ࠥࢀ"), bstack11111l_opy_ (u"ࠢࠣࢁ"))
        if hub_url.endswith(bstack11111l_opy_ (u"ࠨ࠱ࡺࡨ࠴࡮ࡵࡣࠩࢂ")):
            hub_url = hub_url.rsplit(bstack11111l_opy_ (u"ࠩ࠲ࡻࡩ࠵ࡨࡶࡤࠪࢃ"), 1)[0]
        if hub_url.startswith(bstack11111l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࠫࢄ")):
            hub_url = hub_url[7:]
        elif hub_url.startswith(bstack11111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࠭ࢅ")):
            hub_url = hub_url[8:]
        bstack1l1l111ll_opy_ = hub_url
    except Exception as e:
        raise RuntimeError(e)
def bstack1ll11llll_opy_():
    global CONFIG
    bstack1l1l1111l_opy_ = CONFIG.get(bstack11111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢆ"), {}).get(bstack11111l_opy_ (u"࠭ࡧࡳ࡫ࡧࡒࡦࡳࡥࠨࢇ"), bstack11111l_opy_ (u"ࠧࡏࡑࡢࡋࡗࡏࡄࡠࡐࡄࡑࡊࡥࡐࡂࡕࡖࡉࡉ࠭࢈"))
    if not isinstance(bstack1l1l1111l_opy_, str):
        raise ValueError(bstack11111l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡈࡴ࡬ࡨࠥࡴࡡ࡮ࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡦࠦࡶࡢ࡮࡬ࡨࠥࡹࡴࡳ࡫ࡱ࡫ࠧࢉ"))
    try:
        bstack1l1lll11_opy_ = bstack1ll11ll1l1_opy_(bstack1l1l1111l_opy_)
        return bstack1l1lll11_opy_
    except Exception as e:
        logger.error(bstack11111l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣࢊ").format(str(e)))
        return {}
def bstack1ll11ll1l1_opy_(bstack1l1l1111l_opy_):
    global CONFIG
    try:
        if not CONFIG[bstack11111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬࢋ")] or not CONFIG[bstack11111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧࢌ")]:
            raise ValueError(bstack11111l_opy_ (u"ࠧࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠢࢍ"))
        url = bstack1l1lll11l1_opy_ + bstack1l1l1111l_opy_
        auth = (CONFIG[bstack11111l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࢎ")], CONFIG[bstack11111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ࢏")])
        response = requests.get(url, auth=auth)
        if response.status_code == 200 and response.text:
            bstack11lll11l_opy_ = json.loads(response.text)
            return bstack11lll11l_opy_
    except ValueError as ve:
        logger.error(bstack11111l_opy_ (u"ࠣࡃࡗࡗࠥࡀࠠࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬ࡸࡩࡥࠢࡧࡩࡹࡧࡩ࡭ࡵࠣ࠾ࠥࢁࡽࠣ࢐").format(str(ve)))
        raise ValueError(ve)
    except Exception as e:
        logger.error(bstack11111l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡲࡪࡦࠣࡨࡪࡺࡡࡪ࡮ࡶࠤ࠿ࠦࡻࡾࠤ࢑").format(str(e)))
        raise RuntimeError(e)
    return {}
def bstack1ll1ll11l_opy_(bstack1l111111l1_opy_):
    global CONFIG
    if bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ࢒") not in CONFIG or str(CONFIG[bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ࢓")]).lower() == bstack11111l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ࢔"):
        CONFIG[bstack11111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬ࢕")] = False
    elif bstack11111l_opy_ (u"ࠧࡪࡵࡗࡶ࡮ࡧ࡬ࡈࡴ࡬ࡨࠬ࢖") in bstack1l111111l1_opy_:
        bstack1lllll1l11_opy_ = CONFIG.get(bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢗ"), {})
        logger.debug(bstack11111l_opy_ (u"ࠤࡄࡘࡘࠦ࠺ࠡࡇࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴࡩࡡ࡭ࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠪࡹࠢ࢘"), bstack1lllll1l11_opy_)
        bstack1llllll1ll_opy_ = bstack1l111111l1_opy_.get(bstack11111l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡕࡩࡵ࡫ࡡࡵࡧࡵࡷ࢙ࠧ"), [])
        bstack1ll11111ll_opy_ = bstack11111l_opy_ (u"ࠦ࠱ࠨ࢚").join(bstack1llllll1ll_opy_)
        logger.debug(bstack11111l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡈࡻࡳࡵࡱࡰࠤࡷ࡫ࡰࡦࡣࡷࡩࡷࠦࡳࡵࡴ࡬ࡲ࡬ࡀࠠࠦࡵ࢛ࠥ"), bstack1ll11111ll_opy_)
        bstack1l1lll1l11_opy_ = {
            bstack11111l_opy_ (u"ࠨ࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠣ࢜"): bstack11111l_opy_ (u"ࠢࡢࡶࡶ࠱ࡷ࡫ࡰࡦࡣࡷࡩࡷࠨ࢝"),
            bstack11111l_opy_ (u"ࠣࡨࡲࡶࡨ࡫ࡌࡰࡥࡤࡰࠧ࢞"): bstack11111l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ࢟"),
            bstack11111l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠧࢠ"): bstack1ll11111ll_opy_
        }
        bstack1lllll1l11_opy_.update(bstack1l1lll1l11_opy_)
        logger.debug(bstack11111l_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼࡙ࠣࡵࡪࡡࡵࡧࡧࠤࡱࡵࡣࡢ࡮ࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠫࡳࠣࢡ"), bstack1lllll1l11_opy_)
        CONFIG[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢢ")] = bstack1lllll1l11_opy_
        logger.debug(bstack11111l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡌࡩ࡯ࡣ࡯ࠤࡈࡕࡎࡇࡋࡊ࠾ࠥࠫࡳࠣࢣ"), CONFIG)
def bstack1lll1lll1_opy_():
    bstack1l1lll11_opy_ = bstack1ll11llll_opy_()
    if not bstack1l1lll11_opy_[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࡙ࡷࡲࠧࢤ")]:
      raise ValueError(bstack11111l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸ࡚ࡸ࡬ࠡ࡫ࡶࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࡬ࡲࡰ࡯ࠣ࡫ࡷ࡯ࡤࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠥࢥ"))
    return bstack1l1lll11_opy_[bstack11111l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࡛ࡲ࡭ࠩࢦ")] + bstack11111l_opy_ (u"ࠪࡃࡨࡧࡰࡴ࠿ࠪࢧ")
@measure(event_name=EVENTS.bstack11ll11l11l_opy_, stage=STAGE.bstack1l1llll11_opy_)
def bstack11lll1l1ll_opy_() -> list:
    global CONFIG
    result = []
    if CONFIG:
        auth = (CONFIG[bstack11111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ࢨ")], CONFIG[bstack11111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨࢩ")])
        url = bstack1l1l11lll1_opy_
        logger.debug(bstack11111l_opy_ (u"ࠨࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬ࡲࡰ࡯ࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡗࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࠦࡁࡑࡋࠥࢪ"))
        try:
            response = requests.get(url, auth=auth, headers={bstack11111l_opy_ (u"ࠢࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪࠨࢫ"): bstack11111l_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠦࢬ")})
            if response.status_code == 200:
                bstack11l1l11l11_opy_ = json.loads(response.text)
                bstack111l1l1l1_opy_ = bstack11l1l11l11_opy_.get(bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡴࠩࢭ"), [])
                if bstack111l1l1l1_opy_:
                    bstack11l1ll11l_opy_ = bstack111l1l1l1_opy_[0]
                    build_hashed_id = bstack11l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ࢮ"))
                    bstack11l11l1l1_opy_ = bstack1lll1l1l11_opy_ + build_hashed_id
                    result.extend([build_hashed_id, bstack11l11l1l1_opy_])
                    logger.info(bstack1lll1l1111_opy_.format(bstack11l11l1l1_opy_))
                    bstack1ll1111l1_opy_ = CONFIG[bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧࢯ")]
                    if bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࢰ") in CONFIG:
                      bstack1ll1111l1_opy_ += bstack11111l_opy_ (u"࠭ࠠࠨࢱ") + CONFIG[bstack11111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࢲ")]
                    if bstack1ll1111l1_opy_ != bstack11l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ࢳ")):
                      logger.debug(bstack11111l111_opy_.format(bstack11l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࢴ")), bstack1ll1111l1_opy_))
                    return result
                else:
                    logger.debug(bstack11111l_opy_ (u"ࠥࡅ࡙࡙ࠠ࠻ࠢࡑࡳࠥࡨࡵࡪ࡮ࡧࡷࠥ࡬࡯ࡶࡰࡧࠤ࡮ࡴࠠࡵࡪࡨࠤࡷ࡫ࡳࡱࡱࡱࡷࡪ࠴ࠢࢵ"))
            else:
                logger.debug(bstack11111l_opy_ (u"ࠦࡆ࡚ࡓࠡ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢶ"))
        except Exception as e:
            logger.error(bstack11111l_opy_ (u"ࠧࡇࡔࡔࠢ࠽ࠤࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࡹࠠ࠻ࠢࡾࢁࠧࢷ").format(str(e)))
    else:
        logger.debug(bstack11111l_opy_ (u"ࠨࡁࡕࡕࠣ࠾ࠥࡉࡏࡏࡈࡌࡋࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡥࡵ࠰࡙ࠣࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡨࡵࡪ࡮ࡧࡷ࠳ࠨࢸ"))
    return [None, None]
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1111l1l1_opy_ import bstack1111l1l1_opy_, bstack1l1ll1llll_opy_, bstack11l111lll_opy_, bstack1ll11lll11_opy_
from bstack_utils.measure import bstack1lll11ll11_opy_
from bstack_utils.measure import measure
from bstack_utils.percy import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11l11l1ll1_opy_ import bstack11l1lll11l_opy_
from bstack_utils.messages import *
from bstack_utils import bstack11ll1ll1l1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll1llll1_opy_, bstack11111ll1_opy_, bstack11ll11l1l1_opy_, bstack11l11llll1_opy_, \
  bstack11l1l1l11l_opy_, \
  Notset, bstack11llll11l_opy_, \
  bstack1l1111l11l_opy_, bstack111111ll_opy_, bstack1lll111ll1_opy_, bstack1lll11l1l1_opy_, bstack11lll111ll_opy_, bstack11l11l111_opy_, \
  bstack1l1l1lll1l_opy_, \
  bstack1l1111l1ll_opy_, bstack11111llll_opy_, bstack111l1llll_opy_, bstack111ll1l11_opy_, \
  bstack1lllll1111_opy_, bstack1l1lll1l1l_opy_, bstack11ll11l11_opy_, bstack1lll1l111l_opy_
from bstack_utils.bstack1l11ll11l_opy_ import bstack1llll1l1_opy_, bstack1ll111lll_opy_
from bstack_utils.bstack11lll1l1l1_opy_ import bstack11111ll1l_opy_
from bstack_utils.bstack1l1111ll11_opy_ import bstack111ll11l1_opy_, bstack1l1l1l111_opy_
from bstack_utils.bstack1l1l1ll111_opy_ import bstack1l1l1ll111_opy_
from bstack_utils.bstack1l1lll1ll1_opy_ import bstack11ll1lll_opy_
from bstack_utils.proxy import bstack1l111lll1_opy_, bstack1lll111l1_opy_, bstack1l11ll11ll_opy_, bstack1ll11ll11_opy_
from bstack_utils.bstack1ll1l1l1_opy_ import bstack1lllll1l1_opy_
import bstack_utils.bstack1l1l11111l_opy_ as bstack11l11lll1l_opy_
import bstack_utils.bstack11lll11ll_opy_ as bstack11lllll1_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.utils.bstack11l1l11l1_opy_ import bstack11l111111_opy_
if os.getenv(bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡌࡔࡕࡋࡔࠩࢹ")):
  cli.bstack111lllll_opy_()
else:
  os.environ[bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡎࡌࡣࡍࡕࡏࡌࡕࠪࢺ")] = bstack11111l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢻ")
bstack11llllllll_opy_ = bstack11111l_opy_ (u"ࠪࠤࠥ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠣࠤ࡮࡬ࠨࡱࡣࡪࡩࠥࡃ࠽࠾ࠢࡹࡳ࡮ࡪࠠ࠱ࠫࠣࡿࡡࡴࠠࠡࠢࡷࡶࡾࢁ࡜࡯ࠢࡦࡳࡳࡹࡴࠡࡨࡶࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨ࡝ࠩࡩࡷࡡ࠭ࠩ࠼࡞ࡱࠤࠥࠦࠠࠡࡨࡶ࠲ࡦࡶࡰࡦࡰࡧࡊ࡮ࡲࡥࡔࡻࡱࡧ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪ࠯ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡶ࡟ࡪࡰࡧࡩࡽ࠯ࠠࠬࠢࠥ࠾ࠧࠦࠫࠡࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࠨࡢࡹࡤ࡭ࡹࠦ࡮ࡦࡹࡓࡥ࡬࡫࠲࠯ࡧࡹࡥࡱࡻࡡࡵࡧࠫࠦ࠭࠯ࠠ࠾ࡀࠣࡿࢂࠨࠬࠡ࡞ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥ࡫ࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡄࡦࡶࡤ࡭ࡱࡹࠢࡾ࡞ࠪ࠭࠮࠯࡛ࠣࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠦࡢ࠯ࠠࠬࠢࠥ࠰ࡡࡢ࡮ࠣࠫ࡟ࡲࠥࠦࠠࠡࡿࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࢀࡢ࡮ࠡࠢࠣࠤࢂࡢ࡮ࠡࠢࢀࡠࡳࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠪࢼ")
bstack1ll1lll11l_opy_ = bstack11111l_opy_ (u"ࠫࡡࡴ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰࡞ࡱࡧࡴࡴࡳࡵࠢࡥࡷࡹࡧࡣ࡬ࡡࡳࡥࡹ࡮ࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࡜ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮࡭ࡧࡱ࡫ࡹ࡮ࠠ࠮ࠢ࠶ࡡࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠷࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡲࡢ࡭ࡳࡪࡥࡹࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠷ࡣ࡜࡯ࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼࠠ࠾ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯ࡵ࡯࡭ࡨ࡫ࠨ࠱࠮ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸࠯࡜࡯ࡥࡲࡲࡸࡺࠠࡪ࡯ࡳࡳࡷࡺ࡟ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠸ࡤࡨࡳࡵࡣࡦ࡯ࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨࠩ࠼࡞ࡱ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡰࡦࡻ࡮ࡤࡪࠣࡁࠥࡧࡳࡺࡰࡦࠤ࠭ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷ࠮ࠦ࠽࠿ࠢࡾࡠࡳࡲࡥࡵࠢࡦࡥࡵࡹ࠻࡝ࡰࡷࡶࡾࠦࡻ࡝ࡰࡦࡥࡵࡹࠠ࠾ࠢࡍࡗࡔࡔ࠮ࡱࡣࡵࡷࡪ࠮ࡢࡴࡶࡤࡧࡰࡥࡣࡢࡲࡶ࠭ࡡࡴࠠࠡࡿࠣࡧࡦࡺࡣࡩࠪࡨࡼ࠮ࠦࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡦࡽࡡࡪࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫࠯ࡥ࡫ࡶࡴࡳࡩࡶ࡯࠱ࡧࡴࡴ࡮ࡦࡥࡷࠬࢀࡢ࡮ࠡࠢࠣࠤࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴ࠻ࠢࡣࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠩࢁࡥ࡯ࡥࡲࡨࡪ࡛ࡒࡊࡅࡲࡱࡵࡵ࡮ࡦࡰࡷࠬࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡩࡡࡱࡵࠬ࠭ࢂࡦࠬ࡝ࡰࠣࠤࠥࠦ࠮࠯࠰࡯ࡥࡺࡴࡣࡩࡑࡳࡸ࡮ࡵ࡮ࡴ࡞ࡱࠤࠥࢃࠩ࡝ࡰࢀࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࠪࢽ")
from ._version import __version__
bstack1ll1l1111_opy_ = None
CONFIG = {}
bstack1ll1l1l11l_opy_ = {}
bstack1l1ll11l_opy_ = {}
bstack11llll1l1_opy_ = None
bstack1ll1l11l1_opy_ = None
bstack1lllll11ll_opy_ = None
bstack11ll111l_opy_ = -1
bstack1111l1ll1_opy_ = 0
bstack111l1l1ll_opy_ = bstack1ll11ll11l_opy_
bstack1l11l1l11_opy_ = 1
bstack1l11ll111l_opy_ = False
bstack11111111_opy_ = False
bstack1lll11l11l_opy_ = bstack11111l_opy_ (u"ࠬ࠭ࢾ")
bstack11l1lll1ll_opy_ = bstack11111l_opy_ (u"࠭ࠧࢿ")
bstack1lllll1ll_opy_ = False
bstack1ll111l11_opy_ = True
bstack1l1l1l111l_opy_ = bstack11111l_opy_ (u"ࠧࠨࣀ")
bstack1lll1l1l1l_opy_ = []
bstack1l1l111ll_opy_ = bstack11111l_opy_ (u"ࠨࠩࣁ")
bstack1l1lllll1_opy_ = False
bstack1lll1l1l_opy_ = None
bstack111ll1ll1_opy_ = None
bstack11l1l11lll_opy_ = None
bstack1l11111l11_opy_ = -1
bstack11llll1l1l_opy_ = os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠩࢁࠫࣂ")), bstack11111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪࣃ"), bstack11111l_opy_ (u"ࠫ࠳ࡸ࡯ࡣࡱࡷ࠱ࡷ࡫ࡰࡰࡴࡷ࠱࡭࡫࡬ࡱࡧࡵ࠲࡯ࡹ࡯࡯ࠩࣄ"))
bstack111l1l1l_opy_ = 0
bstack1lll1111l1_opy_ = 0
bstack1lllll1lll_opy_ = []
bstack1l1lll111_opy_ = []
bstack11lll11ll1_opy_ = []
bstack1l11llll_opy_ = []
bstack111l1111_opy_ = bstack11111l_opy_ (u"ࠬ࠭ࣅ")
bstack1llll11ll1_opy_ = bstack11111l_opy_ (u"࠭ࠧࣆ")
bstack1lll1llll_opy_ = False
bstack1l1lllll1l_opy_ = False
bstack1lll111111_opy_ = {}
bstack1l11l111l_opy_ = None
bstack1ll1111111_opy_ = None
bstack1l11ll11_opy_ = None
bstack1ll11l11l1_opy_ = None
bstack1ll111ll1_opy_ = None
bstack11l1l111l_opy_ = None
bstack1ll1lll1l1_opy_ = None
bstack1l1ll11l1_opy_ = None
bstack1ll111ll1l_opy_ = None
bstack11lll1ll11_opy_ = None
bstack1l111l1l11_opy_ = None
bstack1l1l1111_opy_ = None
bstack1l1l111l1_opy_ = None
bstack11ll11ll_opy_ = None
bstack1l1ll1l111_opy_ = None
bstack1ll111111_opy_ = None
bstack1lll1111ll_opy_ = None
bstack11l1llllll_opy_ = None
bstack1l1ll1ll1_opy_ = None
bstack1l11ll1l1_opy_ = None
bstack1l1l1lll1_opy_ = None
bstack11l1ll1l1l_opy_ = None
bstack11ll1l1lll_opy_ = None
thread_local = threading.local()
bstack1l1111l1_opy_ = False
bstack1llllll111_opy_ = bstack11111l_opy_ (u"ࠢࠣࣇ")
logger = bstack11ll1ll1l1_opy_.get_logger(__name__, bstack111l1l1ll_opy_)
bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
percy = bstack1l1111111l_opy_()
bstack11ll11l1_opy_ = bstack11l1lll11l_opy_()
bstack1ll1ll1111_opy_ = bstack1l111l11_opy_()
def bstack1lll111l_opy_():
  global CONFIG
  global bstack1lll1llll_opy_
  global bstack1l11l11ll1_opy_
  testContextOptions = bstack1ll11ll1ll_opy_(CONFIG)
  if bstack11l1l1l11l_opy_(CONFIG):
    if (bstack11111l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪࣈ") in testContextOptions and str(testContextOptions[bstack11111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫࣉ")]).lower() == bstack11111l_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊")):
      bstack1lll1llll_opy_ = True
    bstack1l11l11ll1_opy_.bstack1llll11l1l_opy_(testContextOptions.get(bstack11111l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ࣋"), False))
  else:
    bstack1lll1llll_opy_ = True
    bstack1l11l11ll1_opy_.bstack1llll11l1l_opy_(True)
def bstack1llll1l11l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lllll11l1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111l1111l_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11111l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡩ࡯࡯ࡨ࡬࡫࡫࡯࡬ࡦࠤ࣌") == args[i].lower() or bstack11111l_opy_ (u"ࠨ࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡱࡪ࡮࡭ࠢ࣍") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1l1l1l111l_opy_
      bstack1l1l1l111l_opy_ += bstack11111l_opy_ (u"ࠧ࠮࠯ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡄࡱࡱࡪ࡮࡭ࡆࡪ࡮ࡨࠤࠬ࣎") + path
      return path
  return None
bstack1ll1lll1ll_opy_ = re.compile(bstack11111l_opy_ (u"ࡳࠤ࠱࠮ࡄࡢࠤࡼࠪ࠱࠮ࡄ࠯ࡽ࠯ࠬࡂ࣏ࠦ"))
def bstack1l111111ll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1ll1lll1ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11111l_opy_ (u"ࠤࠧࡿ࣐ࠧ") + group + bstack11111l_opy_ (u"ࠥࢁ࣑ࠧ"), os.environ.get(group))
  return value
def bstack111l1l11_opy_():
  global bstack11ll1l1lll_opy_
  if bstack11ll1l1lll_opy_ is None:
        bstack11ll1l1lll_opy_ = bstack111l1111l_opy_()
  bstack1l1lllll_opy_ = bstack11ll1l1lll_opy_
  if bstack1l1lllll_opy_ and os.path.exists(os.path.abspath(bstack1l1lllll_opy_)):
    fileName = bstack1l1lllll_opy_
  if bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨ࣒") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࡣࡋࡏࡌࡆ࣓ࠩ")])) and not bstack11111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡒࡦࡳࡥࠨࣔ") in locals():
    fileName = os.environ[bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫࣕ")]
  if bstack11111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡔࡡ࡮ࡧࠪࣖ") in locals():
    bstack1lllllll_opy_ = os.path.abspath(fileName)
  else:
    bstack1lllllll_opy_ = bstack11111l_opy_ (u"ࠩࠪࣗ")
  bstack1l111ll1l1_opy_ = os.getcwd()
  bstack11l1ll111_opy_ = bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱ࠭ࣘ")
  bstack1lll11l1l_opy_ = bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡦࡳ࡬ࠨࣙ")
  while (not os.path.exists(bstack1lllllll_opy_)) and bstack1l111ll1l1_opy_ != bstack11111l_opy_ (u"ࠧࠨࣚ"):
    bstack1lllllll_opy_ = os.path.join(bstack1l111ll1l1_opy_, bstack11l1ll111_opy_)
    if not os.path.exists(bstack1lllllll_opy_):
      bstack1lllllll_opy_ = os.path.join(bstack1l111ll1l1_opy_, bstack1lll11l1l_opy_)
    if bstack1l111ll1l1_opy_ != os.path.dirname(bstack1l111ll1l1_opy_):
      bstack1l111ll1l1_opy_ = os.path.dirname(bstack1l111ll1l1_opy_)
    else:
      bstack1l111ll1l1_opy_ = bstack11111l_opy_ (u"ࠨࠢࣛ")
  bstack11ll1l1lll_opy_ = bstack1lllllll_opy_ if os.path.exists(bstack1lllllll_opy_) else None
  return bstack11ll1l1lll_opy_
def bstack11ll11ll1l_opy_():
  bstack1lllllll_opy_ = bstack111l1l11_opy_()
  if not os.path.exists(bstack1lllllll_opy_):
    bstack1l1llll11l_opy_(
      bstack1l11l11l_opy_.format(os.getcwd()))
  try:
    with open(bstack1lllllll_opy_, bstack11111l_opy_ (u"ࠧࡳࠩࣜ")) as stream:
      yaml.add_implicit_resolver(bstack11111l_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤࣝ"), bstack1ll1lll1ll_opy_)
      yaml.add_constructor(bstack11111l_opy_ (u"ࠤࠤࡴࡦࡺࡨࡦࡺࠥࣞ"), bstack1l111111ll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1lllllll_opy_, bstack11111l_opy_ (u"ࠪࡶࠬࣟ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1l1llll11l_opy_(bstack1ll11lll_opy_.format(str(exc)))
def bstack1l1lll1l1_opy_(config):
  bstack1ll11l1111_opy_ = bstack11l111l11_opy_(config)
  for option in list(bstack1ll11l1111_opy_):
    if option.lower() in bstack11111l1l_opy_ and option != bstack11111l1l_opy_[option.lower()]:
      bstack1ll11l1111_opy_[bstack11111l1l_opy_[option.lower()]] = bstack1ll11l1111_opy_[option]
      del bstack1ll11l1111_opy_[option]
  return config
def bstack111l111l1_opy_():
  global bstack1l1ll11l_opy_
  for key, bstack1111l111l_opy_ in bstack1l111lll_opy_.items():
    if isinstance(bstack1111l111l_opy_, list):
      for var in bstack1111l111l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l1ll11l_opy_[key] = os.environ[var]
          break
    elif bstack1111l111l_opy_ in os.environ and os.environ[bstack1111l111l_opy_] and str(os.environ[bstack1111l111l_opy_]).strip():
      bstack1l1ll11l_opy_[key] = os.environ[bstack1111l111l_opy_]
  if bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭࣠") in os.environ:
    bstack1l1ll11l_opy_[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࣡")] = {}
    bstack1l1ll11l_opy_[bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ࣢")][bstack11111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")] = os.environ[bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪࣤ")]
def bstack1ll11111l1_opy_():
  global bstack1ll1l1l11l_opy_
  global bstack1l1l1l111l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11111l_opy_ (u"ࠩ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣥ").lower() == val.lower():
      bstack1ll1l1l11l_opy_[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࣦࠧ")] = {}
      bstack1ll1l1l11l_opy_[bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣧ")][bstack11111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣨ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11111l11l_opy_ in bstack1ll11l11l_opy_.items():
    if isinstance(bstack11111l11l_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11111l11l_opy_:
          if idx < len(sys.argv) and bstack11111l_opy_ (u"࠭࠭࠮ࣩࠩ") + var.lower() == val.lower() and not key in bstack1ll1l1l11l_opy_:
            bstack1ll1l1l11l_opy_[key] = sys.argv[idx + 1]
            bstack1l1l1l111l_opy_ += bstack11111l_opy_ (u"ࠧࠡ࠯࠰ࠫ࣪") + var + bstack11111l_opy_ (u"ࠨࠢࠪ࣫") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11111l_opy_ (u"ࠩ࠰࠱ࠬ࣬") + bstack11111l11l_opy_.lower() == val.lower() and not key in bstack1ll1l1l11l_opy_:
          bstack1ll1l1l11l_opy_[key] = sys.argv[idx + 1]
          bstack1l1l1l111l_opy_ += bstack11111l_opy_ (u"ࠪࠤ࠲࠳࣭ࠧ") + bstack11111l11l_opy_ + bstack11111l_opy_ (u"࣮ࠫࠥ࠭") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1ll11llll1_opy_(config):
  bstack11ll1l1l_opy_ = config.keys()
  for bstack1l111lll1l_opy_, bstack11ll11llll_opy_ in bstack11llllll1l_opy_.items():
    if bstack11ll11llll_opy_ in bstack11ll1l1l_opy_:
      config[bstack1l111lll1l_opy_] = config[bstack11ll11llll_opy_]
      del config[bstack11ll11llll_opy_]
  for bstack1l111lll1l_opy_, bstack11ll11llll_opy_ in bstack11ll111l1l_opy_.items():
    if isinstance(bstack11ll11llll_opy_, list):
      for bstack1ll11l111l_opy_ in bstack11ll11llll_opy_:
        if bstack1ll11l111l_opy_ in bstack11ll1l1l_opy_:
          config[bstack1l111lll1l_opy_] = config[bstack1ll11l111l_opy_]
          del config[bstack1ll11l111l_opy_]
          break
    elif bstack11ll11llll_opy_ in bstack11ll1l1l_opy_:
      config[bstack1l111lll1l_opy_] = config[bstack11ll11llll_opy_]
      del config[bstack11ll11llll_opy_]
  for bstack1ll11l111l_opy_ in list(config):
    for bstack1lll111lll_opy_ in bstack1l1l1l11_opy_:
      if bstack1ll11l111l_opy_.lower() == bstack1lll111lll_opy_.lower() and bstack1ll11l111l_opy_ != bstack1lll111lll_opy_:
        config[bstack1lll111lll_opy_] = config[bstack1ll11l111l_opy_]
        del config[bstack1ll11l111l_opy_]
  bstack11l1l1l1ll_opy_ = [{}]
  if not config.get(bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")):
    config[bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ")] = [{}]
  bstack11l1l1l1ll_opy_ = config[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")]
  for platform in bstack11l1l1l1ll_opy_:
    for bstack1ll11l111l_opy_ in list(platform):
      for bstack1lll111lll_opy_ in bstack1l1l1l11_opy_:
        if bstack1ll11l111l_opy_.lower() == bstack1lll111lll_opy_.lower() and bstack1ll11l111l_opy_ != bstack1lll111lll_opy_:
          platform[bstack1lll111lll_opy_] = platform[bstack1ll11l111l_opy_]
          del platform[bstack1ll11l111l_opy_]
  for bstack1l111lll1l_opy_, bstack11ll11llll_opy_ in bstack11ll111l1l_opy_.items():
    for platform in bstack11l1l1l1ll_opy_:
      if isinstance(bstack11ll11llll_opy_, list):
        for bstack1ll11l111l_opy_ in bstack11ll11llll_opy_:
          if bstack1ll11l111l_opy_ in platform:
            platform[bstack1l111lll1l_opy_] = platform[bstack1ll11l111l_opy_]
            del platform[bstack1ll11l111l_opy_]
            break
      elif bstack11ll11llll_opy_ in platform:
        platform[bstack1l111lll1l_opy_] = platform[bstack11ll11llll_opy_]
        del platform[bstack11ll11llll_opy_]
  for bstack1l1l11l1l1_opy_ in bstack1l11ll1l1l_opy_:
    if bstack1l1l11l1l1_opy_ in config:
      if not bstack1l11ll1l1l_opy_[bstack1l1l11l1l1_opy_] in config:
        config[bstack1l11ll1l1l_opy_[bstack1l1l11l1l1_opy_]] = {}
      config[bstack1l11ll1l1l_opy_[bstack1l1l11l1l1_opy_]].update(config[bstack1l1l11l1l1_opy_])
      del config[bstack1l1l11l1l1_opy_]
  for platform in bstack11l1l1l1ll_opy_:
    for bstack1l1l11l1l1_opy_ in bstack1l11ll1l1l_opy_:
      if bstack1l1l11l1l1_opy_ in list(platform):
        if not bstack1l11ll1l1l_opy_[bstack1l1l11l1l1_opy_] in platform:
          platform[bstack1l11ll1l1l_opy_[bstack1l1l11l1l1_opy_]] = {}
        platform[bstack1l11ll1l1l_opy_[bstack1l1l11l1l1_opy_]].update(platform[bstack1l1l11l1l1_opy_])
        del platform[bstack1l1l11l1l1_opy_]
  config = bstack1l1lll1l1_opy_(config)
  return config
def bstack1lllll111_opy_(config):
  global bstack11l1lll1ll_opy_
  bstack1l1ll11lll_opy_ = False
  if bstack11111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࣲࠬ") in config and str(config[bstack11111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ࣳ")]).lower() != bstack11111l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣴ"):
    if bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࣵ") not in config or str(config[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࣶࠩ")]).lower() == bstack11111l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"):
      config[bstack11111l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ࣸ")] = False
    else:
      bstack1l1lll11_opy_ = bstack1ll11llll_opy_()
      if bstack11111l_opy_ (u"ࠨ࡫ࡶࡘࡷ࡯ࡡ࡭ࡉࡵ࡭ࡩࣹ࠭") in bstack1l1lll11_opy_:
        if not bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸࣺ࠭") in config:
          config[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧࣻ")] = {}
        config[bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣼ")][bstack11111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")] = bstack11111l_opy_ (u"࠭ࡡࡵࡵ࠰ࡶࡪࡶࡥࡢࡶࡨࡶࠬࣾ")
        bstack1l1ll11lll_opy_ = True
        bstack11l1lll1ll_opy_ = config[bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࣿ")].get(bstack11111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऀ"))
  if bstack11l1l1l11l_opy_(config) and bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ँ") in config and str(config[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧं")]).lower() != bstack11111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪः") and not bstack1l1ll11lll_opy_:
    if not bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩऄ") in config:
      config[bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪअ")] = {}
    if not config[bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫआ")].get(bstack11111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠬइ")) and not bstack11111l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫई") in config[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧउ")]:
      bstack1l11l1lll_opy_ = datetime.datetime.now()
      bstack1l111111l_opy_ = bstack1l11l1lll_opy_.strftime(bstack11111l_opy_ (u"ࠫࠪࡪ࡟ࠦࡤࡢࠩࡍࠫࡍࠨऊ"))
      hostname = socket.gethostname()
      bstack111l11lll_opy_ = bstack11111l_opy_ (u"ࠬ࠭ऋ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11111l_opy_ (u"࠭ࡻࡾࡡࡾࢁࡤࢁࡽࠨऌ").format(bstack1l111111l_opy_, hostname, bstack111l11lll_opy_)
      config[bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫऍ")][bstack11111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪऎ")] = identifier
    bstack11l1lll1ll_opy_ = config[bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ए")].get(bstack11111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬऐ"))
  return config
def bstack1l1ll111ll_opy_():
  bstack1ll1l1ll1_opy_ =  bstack1lll11l1l1_opy_()[bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠪऑ")]
  return bstack1ll1l1ll1_opy_ if bstack1ll1l1ll1_opy_ else -1
def bstack1l11l1ll_opy_(bstack1ll1l1ll1_opy_):
  global CONFIG
  if not bstack11111l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧऒ") in CONFIG[bstack11111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨओ")]:
    return
  CONFIG[bstack11111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩऔ")] = CONFIG[bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪक")].replace(
    bstack11111l_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫख"),
    str(bstack1ll1l1ll1_opy_)
  )
def bstack1111lll1_opy_():
  global CONFIG
  if not bstack11111l_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩग") in CONFIG[bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭घ")]:
    return
  bstack1l11l1lll_opy_ = datetime.datetime.now()
  bstack1l111111l_opy_ = bstack1l11l1lll_opy_.strftime(bstack11111l_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪङ"))
  CONFIG[bstack11111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨच")] = CONFIG[bstack11111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩछ")].replace(
    bstack11111l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧज"),
    bstack1l111111l_opy_
  )
def bstack1l11l11lll_opy_():
  global CONFIG
  if bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫझ") in CONFIG and not bool(CONFIG[bstack11111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬञ")]):
    del CONFIG[bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ट")]
    return
  if not bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧठ") in CONFIG:
    CONFIG[bstack11111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨड")] = bstack11111l_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪढ")
  if bstack11111l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧण") in CONFIG[bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫत")]:
    bstack1111lll1_opy_()
    os.environ[bstack11111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧथ")] = CONFIG[bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭द")]
  if not bstack11111l_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧध") in CONFIG[bstack11111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨन")]:
    return
  bstack1ll1l1ll1_opy_ = bstack11111l_opy_ (u"ࠧࠨऩ")
  bstack1l11111lll_opy_ = bstack1l1ll111ll_opy_()
  if bstack1l11111lll_opy_ != -1:
    bstack1ll1l1ll1_opy_ = bstack11111l_opy_ (u"ࠨࡅࡌࠤࠬप") + str(bstack1l11111lll_opy_)
  if bstack1ll1l1ll1_opy_ == bstack11111l_opy_ (u"ࠩࠪफ"):
    bstack1l111l1ll1_opy_ = bstack1ll1lll1l_opy_(CONFIG[bstack11111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ब")])
    if bstack1l111l1ll1_opy_ != -1:
      bstack1ll1l1ll1_opy_ = str(bstack1l111l1ll1_opy_)
  if bstack1ll1l1ll1_opy_:
    bstack1l11l1ll_opy_(bstack1ll1l1ll1_opy_)
    os.environ[bstack11111l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨभ")] = CONFIG[bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧम")]
def bstack1l1111llll_opy_(bstack1l111ll1l_opy_, bstack1l1l11l111_opy_, path):
  bstack11l11lll_opy_ = {
    bstack11111l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪय"): bstack1l1l11l111_opy_
  }
  if os.path.exists(path):
    bstack1ll1111l11_opy_ = json.load(open(path, bstack11111l_opy_ (u"ࠧࡳࡤࠪर")))
  else:
    bstack1ll1111l11_opy_ = {}
  bstack1ll1111l11_opy_[bstack1l111ll1l_opy_] = bstack11l11lll_opy_
  with open(path, bstack11111l_opy_ (u"ࠣࡹ࠮ࠦऱ")) as outfile:
    json.dump(bstack1ll1111l11_opy_, outfile)
def bstack1ll1lll1l_opy_(bstack1l111ll1l_opy_):
  bstack1l111ll1l_opy_ = str(bstack1l111ll1l_opy_)
  bstack11lll1ll1l_opy_ = os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠩࢁࠫल")), bstack11111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪळ"))
  try:
    if not os.path.exists(bstack11lll1ll1l_opy_):
      os.makedirs(bstack11lll1ll1l_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠫࢃ࠭ऴ")), bstack11111l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬव"), bstack11111l_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨश"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11111l_opy_ (u"ࠧࡸࠩष")):
        pass
      with open(file_path, bstack11111l_opy_ (u"ࠣࡹ࠮ࠦस")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11111l_opy_ (u"ࠩࡵࠫह")) as bstack1llll1111l_opy_:
      bstack111llllll_opy_ = json.load(bstack1llll1111l_opy_)
    if bstack1l111ll1l_opy_ in bstack111llllll_opy_:
      bstack11l1l111ll_opy_ = bstack111llllll_opy_[bstack1l111ll1l_opy_][bstack11111l_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऺ")]
      bstack1l1111l1l_opy_ = int(bstack11l1l111ll_opy_) + 1
      bstack1l1111llll_opy_(bstack1l111ll1l_opy_, bstack1l1111l1l_opy_, file_path)
      return bstack1l1111l1l_opy_
    else:
      bstack1l1111llll_opy_(bstack1l111ll1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll1ll1lll_opy_.format(str(e)))
    return -1
def bstack1ll1lll11_opy_(config):
  if not config[bstack11111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ऻ")] or not config[bstack11111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ़")]:
    return True
  else:
    return False
def bstack1ll1ll1l1_opy_(config, index=0):
  global bstack1lllll1ll_opy_
  bstack1l11ll1l11_opy_ = {}
  caps = bstack1lll1l111_opy_ + bstack111lll11_opy_
  if config.get(bstack11111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪऽ"), False):
    bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫा")] = True
    bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࡔࡶࡴࡪࡱࡱࡷࠬि")] = config.get(bstack11111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ी"), {})
  if bstack1lllll1ll_opy_:
    caps += bstack1l1l111l_opy_
  for key in config:
    if key in caps + [bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ु")]:
      continue
    bstack1l11ll1l11_opy_[key] = config[key]
  if bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧू") in config:
    for bstack11lll1ll1_opy_ in config[bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨृ")][index]:
      if bstack11lll1ll1_opy_ in caps:
        continue
      bstack1l11ll1l11_opy_[bstack11lll1ll1_opy_] = config[bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩॄ")][index][bstack11lll1ll1_opy_]
  bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩॅ")] = socket.gethostname()
  if bstack11111l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩॆ") in bstack1l11ll1l11_opy_:
    del (bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪे")])
  return bstack1l11ll1l11_opy_
def bstack1lllll11l_opy_(config):
  global bstack1lllll1ll_opy_
  bstack1l1l111111_opy_ = {}
  caps = bstack111lll11_opy_
  if bstack1lllll1ll_opy_:
    caps += bstack1l1l111l_opy_
  for key in caps:
    if key in config:
      bstack1l1l111111_opy_[key] = config[key]
  return bstack1l1l111111_opy_
def bstack11l1l1111_opy_(bstack1l11ll1l11_opy_, bstack1l1l111111_opy_):
  bstack11l1111l_opy_ = {}
  for key in bstack1l11ll1l11_opy_.keys():
    if key in bstack11llllll1l_opy_:
      bstack11l1111l_opy_[bstack11llllll1l_opy_[key]] = bstack1l11ll1l11_opy_[key]
    else:
      bstack11l1111l_opy_[key] = bstack1l11ll1l11_opy_[key]
  for key in bstack1l1l111111_opy_:
    if key in bstack11llllll1l_opy_:
      bstack11l1111l_opy_[bstack11llllll1l_opy_[key]] = bstack1l1l111111_opy_[key]
    else:
      bstack11l1111l_opy_[key] = bstack1l1l111111_opy_[key]
  return bstack11l1111l_opy_
def bstack1l11ll1111_opy_(config, index=0):
  global bstack1lllll1ll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11ll111l1_opy_ = bstack1ll1llll1_opy_(bstack11ll1l111l_opy_, config, logger)
  bstack1l1l111111_opy_ = bstack1lllll11l_opy_(config)
  bstack1l1l111l11_opy_ = bstack111lll11_opy_
  bstack1l1l111l11_opy_ += bstack1l1l1lllll_opy_
  bstack1l1l111111_opy_ = update(bstack1l1l111111_opy_, bstack11ll111l1_opy_)
  if bstack1lllll1ll_opy_:
    bstack1l1l111l11_opy_ += bstack1l1l111l_opy_
  if bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ै") in config:
    if bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩॉ") in config[bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨॊ")][index]:
      caps[bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")] = config[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪौ")][index][bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ्࠭")]
    if bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॎ") in config[bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॏ")][index]:
      caps[bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬॐ")] = str(config[bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ॑")][index][bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ॒ࠧ")])
    bstack1l1ll1l1l1_opy_ = bstack1ll1llll1_opy_(bstack11ll1l111l_opy_, config[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ॓")][index], logger)
    bstack1l1l111l11_opy_ += list(bstack1l1ll1l1l1_opy_.keys())
    for bstack11lll1111l_opy_ in bstack1l1l111l11_opy_:
      if bstack11lll1111l_opy_ in config[bstack11111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ॔")][index]:
        if bstack11lll1111l_opy_ == bstack11111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫॕ"):
          try:
            bstack1l1ll1l1l1_opy_[bstack11lll1111l_opy_] = str(config[bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ॖ")][index][bstack11lll1111l_opy_] * 1.0)
          except:
            bstack1l1ll1l1l1_opy_[bstack11lll1111l_opy_] = str(config[bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ")][index][bstack11lll1111l_opy_])
        else:
          bstack1l1ll1l1l1_opy_[bstack11lll1111l_opy_] = config[bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")][index][bstack11lll1111l_opy_]
        del (config[bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")][index][bstack11lll1111l_opy_])
    bstack1l1l111111_opy_ = update(bstack1l1l111111_opy_, bstack1l1ll1l1l1_opy_)
  bstack1l11ll1l11_opy_ = bstack1ll1ll1l1_opy_(config, index)
  for bstack1ll11l111l_opy_ in bstack111lll11_opy_ + list(bstack11ll111l1_opy_.keys()):
    if bstack1ll11l111l_opy_ in bstack1l11ll1l11_opy_:
      bstack1l1l111111_opy_[bstack1ll11l111l_opy_] = bstack1l11ll1l11_opy_[bstack1ll11l111l_opy_]
      del (bstack1l11ll1l11_opy_[bstack1ll11l111l_opy_])
  if bstack11llll11l_opy_(config):
    bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧग़")] = True
    caps.update(bstack1l1l111111_opy_)
    caps[bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩज़")] = bstack1l11ll1l11_opy_
  else:
    bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩड़")] = False
    caps.update(bstack11l1l1111_opy_(bstack1l11ll1l11_opy_, bstack1l1l111111_opy_))
    if bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़") in caps:
      caps[bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬफ़")] = caps[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪय़")]
      del (caps[bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫॠ")])
    if bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨॡ") in caps:
      caps[bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪॢ")] = caps[bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪॣ")]
      del (caps[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ।")])
  return caps
def bstack1lll1lll11_opy_():
  global bstack1l1l111ll_opy_
  global CONFIG
  if bstack1lllll11l1_opy_() <= version.parse(bstack11111l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ॥")):
    if bstack1l1l111ll_opy_ != bstack11111l_opy_ (u"ࠬ࠭०"):
      return bstack11111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢ१") + bstack1l1l111ll_opy_ + bstack11111l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ२")
    return bstack1ll111l1l_opy_
  if bstack1l1l111ll_opy_ != bstack11111l_opy_ (u"ࠨࠩ३"):
    return bstack11111l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ४") + bstack1l1l111ll_opy_ + bstack11111l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦ५")
  return bstack1l11l1l11l_opy_
def bstack11l1l1ll11_opy_(options):
  return hasattr(options, bstack11111l_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬ६"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll1llll1l_opy_(options, bstack1lll111ll_opy_):
  for bstack1ll111l1ll_opy_ in bstack1lll111ll_opy_:
    if bstack1ll111l1ll_opy_ in [bstack11111l_opy_ (u"ࠬࡧࡲࡨࡵࠪ७"), bstack11111l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ८")]:
      continue
    if bstack1ll111l1ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll111l1ll_opy_] = update(options._experimental_options[bstack1ll111l1ll_opy_],
                                                         bstack1lll111ll_opy_[bstack1ll111l1ll_opy_])
    else:
      options.add_experimental_option(bstack1ll111l1ll_opy_, bstack1lll111ll_opy_[bstack1ll111l1ll_opy_])
  if bstack11111l_opy_ (u"ࠧࡢࡴࡪࡷࠬ९") in bstack1lll111ll_opy_:
    for arg in bstack1lll111ll_opy_[bstack11111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭॰")]:
      options.add_argument(arg)
    del (bstack1lll111ll_opy_[bstack11111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॱ")])
  if bstack11111l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॲ") in bstack1lll111ll_opy_:
    for ext in bstack1lll111ll_opy_[bstack11111l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॳ")]:
      try:
        options.add_extension(ext)
      except OSError:
        options.add_encoded_extension(ext)
    del (bstack1lll111ll_opy_[bstack11111l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩॴ")])
def bstack1l111l1ll_opy_(options, bstack11l1ll1ll_opy_):
  if bstack11111l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬॵ") in bstack11l1ll1ll_opy_:
    for bstack11lll1l111_opy_ in bstack11l1ll1ll_opy_[bstack11111l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ॶ")]:
      if bstack11lll1l111_opy_ in options._preferences:
        options._preferences[bstack11lll1l111_opy_] = update(options._preferences[bstack11lll1l111_opy_], bstack11l1ll1ll_opy_[bstack11111l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧॷ")][bstack11lll1l111_opy_])
      else:
        options.set_preference(bstack11lll1l111_opy_, bstack11l1ll1ll_opy_[bstack11111l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॸ")][bstack11lll1l111_opy_])
  if bstack11111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॹ") in bstack11l1ll1ll_opy_:
    for arg in bstack11l1ll1ll_opy_[bstack11111l_opy_ (u"ࠫࡦࡸࡧࡴࠩॺ")]:
      options.add_argument(arg)
def bstack1l111l11ll_opy_(options, bstack1ll11l1l1_opy_):
  if bstack11111l_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭ॻ") in bstack1ll11l1l1_opy_:
    options.use_webview(bool(bstack1ll11l1l1_opy_[bstack11111l_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧॼ")]))
  bstack1ll1llll1l_opy_(options, bstack1ll11l1l1_opy_)
def bstack1ll111lll1_opy_(options, bstack11l11l1l11_opy_):
  for bstack111111l1_opy_ in bstack11l11l1l11_opy_:
    if bstack111111l1_opy_ in [bstack11111l_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫॽ"), bstack11111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ॾ")]:
      continue
    options.set_capability(bstack111111l1_opy_, bstack11l11l1l11_opy_[bstack111111l1_opy_])
  if bstack11111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॿ") in bstack11l11l1l11_opy_:
    for arg in bstack11l11l1l11_opy_[bstack11111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨঀ")]:
      options.add_argument(arg)
  if bstack11111l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨঁ") in bstack11l11l1l11_opy_:
    options.bstack11l1l1111l_opy_(bool(bstack11l11l1l11_opy_[bstack11111l_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩং")]))
def bstack1111ll1l_opy_(options, bstack11l11ll1l1_opy_):
  for bstack1l11l1ll11_opy_ in bstack11l11ll1l1_opy_:
    if bstack1l11l1ll11_opy_ in [bstack11111l_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪঃ"), bstack11111l_opy_ (u"ࠧࡢࡴࡪࡷࠬ঄")]:
      continue
    options._options[bstack1l11l1ll11_opy_] = bstack11l11ll1l1_opy_[bstack1l11l1ll11_opy_]
  if bstack11111l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬঅ") in bstack11l11ll1l1_opy_:
    for bstack11lll11l1_opy_ in bstack11l11ll1l1_opy_[bstack11111l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭আ")]:
      options.bstack1l1l1ll1ll_opy_(
        bstack11lll11l1_opy_, bstack11l11ll1l1_opy_[bstack11111l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧই")][bstack11lll11l1_opy_])
  if bstack11111l_opy_ (u"ࠫࡦࡸࡧࡴࠩঈ") in bstack11l11ll1l1_opy_:
    for arg in bstack11l11ll1l1_opy_[bstack11111l_opy_ (u"ࠬࡧࡲࡨࡵࠪউ")]:
      options.add_argument(arg)
def bstack11llll111l_opy_(options, caps):
  if not hasattr(options, bstack11111l_opy_ (u"࠭ࡋࡆ࡛ࠪঊ")):
    return
  if options.KEY == bstack11111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬঋ") and options.KEY in caps:
    bstack1ll1llll1l_opy_(options, caps[bstack11111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ঌ")])
  elif options.KEY == bstack11111l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ঍") and options.KEY in caps:
    bstack1l111l1ll_opy_(options, caps[bstack11111l_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ঎")])
  elif options.KEY == bstack11111l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬএ") and options.KEY in caps:
    bstack1ll111lll1_opy_(options, caps[bstack11111l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭ঐ")])
  elif options.KEY == bstack11111l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ঑") and options.KEY in caps:
    bstack1l111l11ll_opy_(options, caps[bstack11111l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ঒")])
  elif options.KEY == bstack11111l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧও") and options.KEY in caps:
    bstack1111ll1l_opy_(options, caps[bstack11111l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨঔ")])
def bstack1l111l11l_opy_(caps):
  global bstack1lllll1ll_opy_
  if isinstance(os.environ.get(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫক")), str):
    bstack1lllll1ll_opy_ = eval(os.getenv(bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬখ")))
  if bstack1lllll1ll_opy_:
    if bstack1llll1l11l_opy_() < version.parse(bstack11111l_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫগ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ঘ")
    if bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬঙ") in caps:
      browser = caps[bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭চ")]
    elif bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪছ") in caps:
      browser = caps[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫজ")]
    browser = str(browser).lower()
    if browser == bstack11111l_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫঝ") or browser == bstack11111l_opy_ (u"ࠬ࡯ࡰࡢࡦࠪঞ"):
      browser = bstack11111l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ট")
    if browser == bstack11111l_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨঠ"):
      browser = bstack11111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨড")
    if browser not in [bstack11111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩঢ"), bstack11111l_opy_ (u"ࠪࡩࡩ࡭ࡥࠨণ"), bstack11111l_opy_ (u"ࠫ࡮࡫ࠧত"), bstack11111l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬথ"), bstack11111l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧদ")]:
      return None
    try:
      package = bstack11111l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩধ").format(browser)
      name = bstack11111l_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩন")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11l1l1ll11_opy_(options):
        return None
      for bstack1ll11l111l_opy_ in caps.keys():
        options.set_capability(bstack1ll11l111l_opy_, caps[bstack1ll11l111l_opy_])
      bstack11llll111l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1ll11l11_opy_(options, bstack1111l1111_opy_):
  if not bstack11l1l1ll11_opy_(options):
    return
  for bstack1ll11l111l_opy_ in bstack1111l1111_opy_.keys():
    if bstack1ll11l111l_opy_ in bstack1l1l1lllll_opy_:
      continue
    if bstack1ll11l111l_opy_ in options._caps and type(options._caps[bstack1ll11l111l_opy_]) in [dict, list]:
      options._caps[bstack1ll11l111l_opy_] = update(options._caps[bstack1ll11l111l_opy_], bstack1111l1111_opy_[bstack1ll11l111l_opy_])
    else:
      options.set_capability(bstack1ll11l111l_opy_, bstack1111l1111_opy_[bstack1ll11l111l_opy_])
  bstack11llll111l_opy_(options, bstack1111l1111_opy_)
  if bstack11111l_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨ঩") in options._caps:
    if options._caps[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨপ")] and options._caps[bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩফ")].lower() != bstack11111l_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ব"):
      del options._caps[bstack11111l_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬভ")]
def bstack11llll1ll1_opy_(proxy_config):
  if bstack11111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫম") in proxy_config:
    proxy_config[bstack11111l_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪয")] = proxy_config[bstack11111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭র")]
    del (proxy_config[bstack11111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঱")])
  if bstack11111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧল") in proxy_config and proxy_config[bstack11111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ঳")].lower() != bstack11111l_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭঴"):
    proxy_config[bstack11111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঵")] = bstack11111l_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨশ")
  if bstack11111l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧষ") in proxy_config:
    proxy_config[bstack11111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭স")] = bstack11111l_opy_ (u"ࠫࡵࡧࡣࠨহ")
  return proxy_config
def bstack1l1ll11111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ঺") in config:
    return proxy
  config[bstack11111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ঻")] = bstack11llll1ll1_opy_(config[bstack11111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ়࠭")])
  if proxy == None:
    proxy = Proxy(config[bstack11111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧঽ")])
  return proxy
def bstack1ll11l1ll_opy_(self):
  global CONFIG
  global bstack1l1l1111_opy_
  try:
    proxy = bstack1l11ll11ll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11111l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧা")):
        proxies = bstack1l111lll1_opy_(proxy, bstack1lll1lll11_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll1llll1_opy_ = proxies.popitem()
          if bstack11111l_opy_ (u"ࠥ࠾࠴࠵ࠢি") in bstack11ll1llll1_opy_:
            return bstack11ll1llll1_opy_
          else:
            return bstack11111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧী") + bstack11ll1llll1_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤু").format(str(e)))
  return bstack1l1l1111_opy_(self)
def bstack11l1lll1l_opy_():
  global CONFIG
  return bstack1ll11ll11_opy_(CONFIG) and bstack11l11l111_opy_() and bstack1lllll11l1_opy_() >= version.parse(bstack1l1llllll_opy_)
def bstack11l1l11ll_opy_():
  global CONFIG
  return (bstack11111l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩূ") in CONFIG or bstack11111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫৃ") in CONFIG) and bstack1l1l1lll1l_opy_()
def bstack11l111l11_opy_(config):
  bstack1ll11l1111_opy_ = {}
  if bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬৄ") in config:
    bstack1ll11l1111_opy_ = config[bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭৅")]
  if bstack11111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ৆") in config:
    bstack1ll11l1111_opy_ = config[bstack11111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪে")]
  proxy = bstack1l11ll11ll_opy_(config)
  if proxy:
    if proxy.endswith(bstack11111l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪৈ")) and os.path.isfile(proxy):
      bstack1ll11l1111_opy_[bstack11111l_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩ৉")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11111l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ৊")):
        proxies = bstack1lll111l1_opy_(config, bstack1lll1lll11_opy_())
        if len(proxies) > 0:
          protocol, bstack11ll1llll1_opy_ = proxies.popitem()
          if bstack11111l_opy_ (u"ࠣ࠼࠲࠳ࠧো") in bstack11ll1llll1_opy_:
            parsed_url = urlparse(bstack11ll1llll1_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11111l_opy_ (u"ࠤ࠽࠳࠴ࠨৌ") + bstack11ll1llll1_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll11l1111_opy_[bstack11111l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ্࠭")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll11l1111_opy_[bstack11111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧৎ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll11l1111_opy_[bstack11111l_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ৏")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll11l1111_opy_[bstack11111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ৐")] = str(parsed_url.password)
  return bstack1ll11l1111_opy_
def bstack1ll11ll1ll_opy_(config):
  if bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ৑") in config:
    return config[bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭৒")]
  return {}
def bstack1lll1ll11l_opy_(caps):
  global bstack11l1lll1ll_opy_
  if bstack11111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৓") in caps:
    caps[bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ৔")][bstack11111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࠪ৕")] = True
    if bstack11l1lll1ll_opy_:
      caps[bstack11111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭৖")][bstack11111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨৗ")] = bstack11l1lll1ll_opy_
  else:
    caps[bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࠬ৘")] = True
    if bstack11l1lll1ll_opy_:
      caps[bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৙")] = bstack11l1lll1ll_opy_
@measure(event_name=EVENTS.bstack1ll1ll11ll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11l11l11l1_opy_():
  global CONFIG
  if not bstack11l1l1l11l_opy_(CONFIG) or cli.is_enabled(CONFIG):
    return
  if bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭৚") in CONFIG and bstack11ll11l11_opy_(CONFIG[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ৛")]):
    if (
      bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨড়") in CONFIG
      and bstack11ll11l11_opy_(CONFIG[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩঢ়")].get(bstack11111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪ৞")))
    ):
      logger.debug(bstack11111l_opy_ (u"ࠢࡍࡱࡦࡥࡱࠦࡢࡪࡰࡤࡶࡾࠦ࡮ࡰࡶࠣࡷࡹࡧࡲࡵࡧࡧࠤࡦࡹࠠࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡦࡰࡤࡦࡱ࡫ࡤࠣয়"))
      return
    bstack1ll11l1111_opy_ = bstack11l111l11_opy_(CONFIG)
    bstack1l1ll11ll_opy_(CONFIG[bstack11111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫৠ")], bstack1ll11l1111_opy_)
def bstack1l1ll11ll_opy_(key, bstack1ll11l1111_opy_):
  global bstack1ll1l1111_opy_
  logger.info(bstack11llllll1_opy_)
  try:
    bstack1ll1l1111_opy_ = Local()
    bstack11l1111ll_opy_ = {bstack11111l_opy_ (u"ࠩ࡮ࡩࡾ࠭ৡ"): key}
    bstack11l1111ll_opy_.update(bstack1ll11l1111_opy_)
    logger.debug(bstack1ll1llll_opy_.format(str(bstack11l1111ll_opy_)).replace(key, bstack11111l_opy_ (u"ࠪ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧৢ")))
    bstack1ll1l1111_opy_.start(**bstack11l1111ll_opy_)
    if bstack1ll1l1111_opy_.isRunning():
      logger.info(bstack111ll11ll_opy_)
  except Exception as e:
    bstack1l1llll11l_opy_(bstack1lll1ll11_opy_.format(str(e)))
def bstack1l111ll1ll_opy_():
  global bstack1ll1l1111_opy_
  if bstack1ll1l1111_opy_.isRunning():
    logger.info(bstack11l11ll1ll_opy_)
    bstack1ll1l1111_opy_.stop()
  bstack1ll1l1111_opy_ = None
def bstack1lll1ll1ll_opy_(bstack1ll1llll11_opy_=[]):
  global CONFIG
  bstack11lll1l1l_opy_ = []
  bstack1111111l1_opy_ = [bstack11111l_opy_ (u"ࠫࡴࡹࠧৣ"), bstack11111l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৤"), bstack11111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ৥"), bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ০"), bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭১"), bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ২")]
  try:
    for err in bstack1ll1llll11_opy_:
      bstack1l111l11l1_opy_ = {}
      for k in bstack1111111l1_opy_:
        val = CONFIG[bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭৩")][int(err[bstack11111l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ৪")])].get(k)
        if val:
          bstack1l111l11l1_opy_[k] = val
      if(err[bstack11111l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ৫")] != bstack11111l_opy_ (u"࠭ࠧ৬")):
        bstack1l111l11l1_opy_[bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭৭")] = {
          err[bstack11111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭৮")]: err[bstack11111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ৯")]
        }
        bstack11lll1l1l_opy_.append(bstack1l111l11l1_opy_)
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬৰ") + str(e))
  finally:
    return bstack11lll1l1l_opy_
def bstack1l11111l1_opy_(file_name):
  bstack1ll111ll_opy_ = []
  try:
    bstack11l1l11l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack11l1l11l_opy_):
      with open(bstack11l1l11l_opy_) as f:
        bstack1ll1lll111_opy_ = json.load(f)
        bstack1ll111ll_opy_ = bstack1ll1lll111_opy_
      os.remove(bstack11l1l11l_opy_)
    return bstack1ll111ll_opy_
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭ৱ") + str(e))
    return bstack1ll111ll_opy_
def bstack11lllll11_opy_():
  try:
      from bstack_utils.constants import bstack1l1ll1111_opy_, EVENTS
      from bstack_utils.helper import bstack11111ll1_opy_, get_host_info, bstack1l11l11ll1_opy_
      from datetime import datetime
      from filelock import FileLock
      bstack1lll1ll1_opy_ = os.path.join(os.getcwd(), bstack11111l_opy_ (u"ࠬࡲ࡯ࡨࠩ৲"), bstack11111l_opy_ (u"࠭࡫ࡦࡻ࠰ࡱࡪࡺࡲࡪࡥࡶ࠲࡯ࡹ࡯࡯ࠩ৳"))
      lock = FileLock(bstack1lll1ll1_opy_+bstack11111l_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨ৴"))
      def bstack1l1l1l1l1_opy_():
          try:
              with lock:
                  with open(bstack1lll1ll1_opy_, bstack11111l_opy_ (u"ࠣࡴࠥ৵"), encoding=bstack11111l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ৶")) as file:
                      data = json.load(file)
                      config = {
                          bstack11111l_opy_ (u"ࠥ࡬ࡪࡧࡤࡦࡴࡶࠦ৷"): {
                              bstack11111l_opy_ (u"ࠦࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠥ৸"): bstack11111l_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠣ৹"),
                          }
                      }
                      bstack11l1l1lll1_opy_ = datetime.utcnow()
                      bstack1l11l1lll_opy_ = bstack11l1l1lll1_opy_.strftime(bstack11111l_opy_ (u"ࠨ࡚ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫ࠦࡕࡕࡅࠥ৺"))
                      bstack11lll1l1_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ৻")) if os.environ.get(bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ৼ")) else bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠤࡶࡨࡰࡘࡵ࡯ࡋࡧࠦ৽"))
                      payload = {
                          bstack11111l_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠢ৾"): bstack11111l_opy_ (u"ࠦࡸࡪ࡫ࡠࡧࡹࡩࡳࡺࡳࠣ৿"),
                          bstack11111l_opy_ (u"ࠧࡪࡡࡵࡣࠥ਀"): {
                              bstack11111l_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠧਁ"): bstack11lll1l1_opy_,
                              bstack11111l_opy_ (u"ࠢࡤࡴࡨࡥࡹ࡫ࡤࡠࡦࡤࡽࠧਂ"): bstack1l11l1lll_opy_,
                              bstack11111l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟࡯ࡣࡰࡩࠧਃ"): bstack11111l_opy_ (u"ࠤࡖࡈࡐࡌࡥࡢࡶࡸࡶࡪࡖࡥࡳࡨࡲࡶࡲࡧ࡮ࡤࡧࠥ਄"),
                              bstack11111l_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡ࡭ࡷࡴࡴࠢਅ"): {
                                  bstack11111l_opy_ (u"ࠦࡲ࡫ࡡࡴࡷࡵࡩࡸࠨਆ"): data,
                                  bstack11111l_opy_ (u"ࠧࡹࡤ࡬ࡔࡸࡲࡎࡪࠢਇ"): bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠨࡳࡥ࡭ࡕࡹࡳࡏࡤࠣਈ"))
                              },
                              bstack11111l_opy_ (u"ࠢࡶࡵࡨࡶࡤࡪࡡࡵࡣࠥਉ"): bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠣࡷࡶࡩࡷࡔࡡ࡮ࡧࠥਊ")),
                              bstack11111l_opy_ (u"ࠤ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠧ਋"): get_host_info()
                          }
                      }
                      response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠥࡔࡔ࡙ࡔࠣ਌"), bstack1l1ll1111_opy_, payload, config)
                      if(response.status_code >= 200 and response.status_code < 300):
                          logger.debug(bstack11111l_opy_ (u"ࠦࡉࡧࡴࡢࠢࡶࡩࡳࡺࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾࠦࡴࡰࠢࡾࢁࠥࡽࡩࡵࡪࠣࡨࡦࡺࡡࠡࡽࢀࠦ਍").format(bstack1l1ll1111_opy_, payload))
                      else:
                          logger.debug(bstack11111l_opy_ (u"ࠧࡘࡥࡲࡷࡨࡷࡹࠦࡦࡢ࡫࡯ࡩࡩࠦࡦࡰࡴࠣࡿࢂࠦࡷࡪࡶ࡫ࠤࡩࡧࡴࡢࠢࡾࢁࠧ਎").format(bstack1l1ll1111_opy_, payload))
          except Exception as e:
              logger.debug(bstack11111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡳࡪࠠ࡬ࡧࡼࠤࡲ࡫ࡴࡳ࡫ࡦࡷࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠࡼࡿࠥਏ").format(e))
      bstack1l1l1l1l1_opy_()
      bstack111111ll_opy_(bstack1lll1ll1_opy_, logger)
  except:
    pass
def bstack1l11l1111l_opy_():
  global bstack1llllll111_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1lllll1lll_opy_
  global bstack1l1lll111_opy_
  global bstack11lll11ll1_opy_
  global bstack1llll11ll1_opy_
  global CONFIG
  bstack111l11ll_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਐ"))
  if bstack111l11ll_opy_ in [bstack11111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ਑"), bstack11111l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ਒")]:
    bstack11ll1l11l_opy_()
  percy.shutdown()
  if bstack1llllll111_opy_:
    logger.warning(bstack11l1ll1l_opy_.format(str(bstack1llllll111_opy_)))
  else:
    try:
      bstack1ll1111l11_opy_ = bstack1l1111l11l_opy_(bstack11111l_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩਓ"), logger)
      if bstack1ll1111l11_opy_.get(bstack11111l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩਔ")) and bstack1ll1111l11_opy_.get(bstack11111l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪਕ")).get(bstack11111l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨਖ")):
        logger.warning(bstack11l1ll1l_opy_.format(str(bstack1ll1111l11_opy_[bstack11111l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬਗ")][bstack11111l_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪਘ")])))
    except Exception as e:
      logger.error(e)
  if cli.is_running():
    bstack1111l1l1_opy_.invoke(bstack1l1ll1llll_opy_.bstack11l1lllll1_opy_)
  logger.info(bstack1llll11111_opy_)
  global bstack1ll1l1111_opy_
  if bstack1ll1l1111_opy_:
    bstack1l111ll1ll_opy_()
  try:
    for driver in bstack1lll1l1l1l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l111ll11_opy_)
  if bstack1llll11ll1_opy_ == bstack11111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨਙ"):
    bstack11lll11ll1_opy_ = bstack1l11111l1_opy_(bstack11111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫਚ"))
  if bstack1llll11ll1_opy_ == bstack11111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫਛ") and len(bstack1l1lll111_opy_) == 0:
    bstack1l1lll111_opy_ = bstack1l11111l1_opy_(bstack11111l_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪਜ"))
    if len(bstack1l1lll111_opy_) == 0:
      bstack1l1lll111_opy_ = bstack1l11111l1_opy_(bstack11111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬਝ"))
  bstack111l11l11_opy_ = bstack11111l_opy_ (u"ࠧࠨਞ")
  if len(bstack1lllll1lll_opy_) > 0:
    bstack111l11l11_opy_ = bstack1lll1ll1ll_opy_(bstack1lllll1lll_opy_)
  elif len(bstack1l1lll111_opy_) > 0:
    bstack111l11l11_opy_ = bstack1lll1ll1ll_opy_(bstack1l1lll111_opy_)
  elif len(bstack11lll11ll1_opy_) > 0:
    bstack111l11l11_opy_ = bstack1lll1ll1ll_opy_(bstack11lll11ll1_opy_)
  elif len(bstack1l11llll_opy_) > 0:
    bstack111l11l11_opy_ = bstack1lll1ll1ll_opy_(bstack1l11llll_opy_)
  if bool(bstack111l11l11_opy_):
    bstack11lll1llll_opy_(bstack111l11l11_opy_)
  else:
    bstack11lll1llll_opy_()
  bstack111111ll_opy_(bstack1lll11ll1_opy_, logger)
  if bstack111l11ll_opy_ not in [bstack11111l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩਟ")]:
    bstack11lllll11_opy_()
  bstack11ll1ll1l1_opy_.bstack1l1lll1111_opy_(CONFIG)
  if len(bstack11lll11ll1_opy_) > 0:
    sys.exit(len(bstack11lll11ll1_opy_))
def bstack11ll1l1l11_opy_(bstack11ll1lllll_opy_, frame):
  global bstack1l11l11ll1_opy_
  logger.error(bstack1l1l11l1l_opy_)
  bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬਠ"), bstack11ll1lllll_opy_)
  if hasattr(signal, bstack11111l_opy_ (u"ࠪࡗ࡮࡭࡮ࡢ࡮ࡶࠫਡ")):
    bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠫࡸࡪ࡫ࡌ࡫࡯ࡰࡘ࡯ࡧ࡯ࡣ࡯ࠫਢ"), signal.Signals(bstack11ll1lllll_opy_).name)
  else:
    bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬਣ"), bstack11111l_opy_ (u"࠭ࡓࡊࡉࡘࡒࡐࡔࡏࡘࡐࠪਤ"))
  if cli.is_running():
    bstack1111l1l1_opy_.invoke(bstack1l1ll1llll_opy_.bstack11l1lllll1_opy_)
  bstack111l11ll_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨਥ"))
  if bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਦ") and not cli.is_enabled(CONFIG):
    bstack1111lll11_opy_.stop(bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩਧ")))
  bstack1l11l1111l_opy_()
  sys.exit(1)
def bstack1l1llll11l_opy_(err):
  logger.critical(bstack1l1ll111l1_opy_.format(str(err)))
  bstack11lll1llll_opy_(bstack1l1ll111l1_opy_.format(str(err)), True)
  atexit.unregister(bstack1l11l1111l_opy_)
  bstack11ll1l11l_opy_()
  sys.exit(1)
def bstack11l1l1l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack11lll1llll_opy_(message, True)
  atexit.unregister(bstack1l11l1111l_opy_)
  bstack11ll1l11l_opy_()
  sys.exit(1)
def bstack1lll11111l_opy_():
  global CONFIG
  global bstack1ll1l1l11l_opy_
  global bstack1l1ll11l_opy_
  global bstack1ll111l11_opy_
  CONFIG = bstack11ll11ll1l_opy_()
  load_dotenv(CONFIG.get(bstack11111l_opy_ (u"ࠪࡩࡳࡼࡆࡪ࡮ࡨࠫਨ")))
  bstack111l111l1_opy_()
  bstack1ll11111l1_opy_()
  CONFIG = bstack1ll11llll1_opy_(CONFIG)
  update(CONFIG, bstack1l1ll11l_opy_)
  update(CONFIG, bstack1ll1l1l11l_opy_)
  if not cli.is_enabled(CONFIG):
    CONFIG = bstack1lllll111_opy_(CONFIG)
  bstack1ll111l11_opy_ = bstack11l1l1l11l_opy_(CONFIG)
  os.environ[bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ਩")] = bstack1ll111l11_opy_.__str__().lower()
  bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ਪ"), bstack1ll111l11_opy_)
  if (bstack11111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩਫ") in CONFIG and bstack11111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪਬ") in bstack1ll1l1l11l_opy_) or (
          bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫਭ") in CONFIG and bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬਮ") not in bstack1l1ll11l_opy_):
    if os.getenv(bstack11111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧਯ")):
      CONFIG[bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ਰ")] = os.getenv(bstack11111l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ਱"))
    else:
      if not CONFIG.get(bstack11111l_opy_ (u"ࠨࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠤਲ"), bstack11111l_opy_ (u"ࠢࠣਲ਼")) in bstack11llllll_opy_:
        bstack1l11l11lll_opy_()
  elif (bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ਴") not in CONFIG and bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫਵ") in CONFIG) or (
          bstack11111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ਸ਼") in bstack1l1ll11l_opy_ and bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ਷") not in bstack1ll1l1l11l_opy_):
    del (CONFIG[bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧਸ")])
  if bstack1ll1lll11_opy_(CONFIG):
    bstack1l1llll11l_opy_(bstack1ll1l11ll1_opy_)
  Config.bstack1l11l111_opy_().bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠨࡵࡴࡧࡵࡒࡦࡳࡥࠣਹ"), CONFIG[bstack11111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ਺")])
  bstack11l1llll1l_opy_()
  bstack1l11lll1ll_opy_()
  if bstack1lllll1ll_opy_ and not CONFIG.get(bstack11111l_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠦ਻"), bstack11111l_opy_ (u"ࠤ਼ࠥ")) in bstack11llllll_opy_:
    CONFIG[bstack11111l_opy_ (u"ࠪࡥࡵࡶࠧ਽")] = bstack1llll1l1l1_opy_(CONFIG)
    logger.info(bstack11l11ll1_opy_.format(CONFIG[bstack11111l_opy_ (u"ࠫࡦࡶࡰࠨਾ")]))
  if not bstack1ll111l11_opy_:
    CONFIG[bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਿ")] = [{}]
def bstack1lll1l1lll_opy_(config, bstack11l11l11ll_opy_):
  global CONFIG
  global bstack1lllll1ll_opy_
  CONFIG = config
  bstack1lllll1ll_opy_ = bstack11l11l11ll_opy_
def bstack1l11lll1ll_opy_():
  global CONFIG
  global bstack1lllll1ll_opy_
  if bstack11111l_opy_ (u"࠭ࡡࡱࡲࠪੀ") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack11ll111l11_opy_)
    bstack1lllll1ll_opy_ = True
    bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ੁ"), True)
def bstack1llll1l1l1_opy_(config):
  bstack1l1l1lll11_opy_ = bstack11111l_opy_ (u"ࠨࠩੂ")
  app = config[bstack11111l_opy_ (u"ࠩࡤࡴࡵ࠭੃")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l11lll11_opy_:
      if os.path.exists(app):
        bstack1l1l1lll11_opy_ = bstack11l1l1ll1l_opy_(config, app)
      elif bstack11111l11_opy_(app):
        bstack1l1l1lll11_opy_ = app
      else:
        bstack1l1llll11l_opy_(bstack111111l11_opy_.format(app))
    else:
      if bstack11111l11_opy_(app):
        bstack1l1l1lll11_opy_ = app
      elif os.path.exists(app):
        bstack1l1l1lll11_opy_ = bstack11l1l1ll1l_opy_(app)
      else:
        bstack1l1llll11l_opy_(bstack11ll1lll11_opy_)
  else:
    if len(app) > 2:
      bstack1l1llll11l_opy_(bstack1l111llll1_opy_)
    elif len(app) == 2:
      if bstack11111l_opy_ (u"ࠪࡴࡦࡺࡨࠨ੄") in app and bstack11111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧ੅") in app:
        if os.path.exists(app[bstack11111l_opy_ (u"ࠬࡶࡡࡵࡪࠪ੆")]):
          bstack1l1l1lll11_opy_ = bstack11l1l1ll1l_opy_(config, app[bstack11111l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫੇ")], app[bstack11111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪੈ")])
        else:
          bstack1l1llll11l_opy_(bstack111111l11_opy_.format(app))
      else:
        bstack1l1llll11l_opy_(bstack1l111llll1_opy_)
    else:
      for key in app:
        if key in bstack1l11l1l1l_opy_:
          if key == bstack11111l_opy_ (u"ࠨࡲࡤࡸ࡭࠭੉"):
            if os.path.exists(app[key]):
              bstack1l1l1lll11_opy_ = bstack11l1l1ll1l_opy_(config, app[key])
            else:
              bstack1l1llll11l_opy_(bstack111111l11_opy_.format(app))
          else:
            bstack1l1l1lll11_opy_ = app[key]
        else:
          bstack1l1llll11l_opy_(bstack1llll1ll_opy_)
  return bstack1l1l1lll11_opy_
def bstack11111l11_opy_(bstack1l1l1lll11_opy_):
  import re
  bstack1ll1l11ll_opy_ = re.compile(bstack11111l_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ੊"))
  bstack11lll1l11_opy_ = re.compile(bstack11111l_opy_ (u"ࡵࠦࡣࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫ࠱࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢੋ"))
  if bstack11111l_opy_ (u"ࠫࡧࡹ࠺࠰࠱ࠪੌ") in bstack1l1l1lll11_opy_ or re.fullmatch(bstack1ll1l11ll_opy_, bstack1l1l1lll11_opy_) or re.fullmatch(bstack11lll1l11_opy_, bstack1l1l1lll11_opy_):
    return True
  else:
    return False
@measure(event_name=EVENTS.bstack1l1l1l11l_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11l1l1ll1l_opy_(config, path, bstack1111l11l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11111l_opy_ (u"ࠬࡸࡢࠨ੍")).read()).hexdigest()
  bstack1l11ll1ll_opy_ = bstack1l111l1lll_opy_(md5_hash)
  bstack1l1l1lll11_opy_ = None
  if bstack1l11ll1ll_opy_:
    logger.info(bstack1l1lll1lll_opy_.format(bstack1l11ll1ll_opy_, md5_hash))
    return bstack1l11ll1ll_opy_
  bstack1l1l1l1l_opy_ = datetime.datetime.now()
  bstack1ll111l111_opy_ = MultipartEncoder(
    fields={
      bstack11111l_opy_ (u"࠭ࡦࡪ࡮ࡨࠫ੎"): (os.path.basename(path), open(os.path.abspath(path), bstack11111l_opy_ (u"ࠧࡳࡤࠪ੏")), bstack11111l_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡰ࡭ࡣ࡬ࡲࠬ੐")),
      bstack11111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬੑ"): bstack1111l11l_opy_
    }
  )
  response = requests.post(bstack1l11l11ll_opy_, data=bstack1ll111l111_opy_,
                           headers={bstack11111l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ੒"): bstack1ll111l111_opy_.content_type},
                           auth=(config[bstack11111l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭੓")], config[bstack11111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ੔")]))
  try:
    res = json.loads(response.text)
    bstack1l1l1lll11_opy_ = res[bstack11111l_opy_ (u"࠭ࡡࡱࡲࡢࡹࡷࡲࠧ੕")]
    logger.info(bstack11l11ll111_opy_.format(bstack1l1l1lll11_opy_))
    bstack111ll111_opy_(md5_hash, bstack1l1l1lll11_opy_)
    cli.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠢࡩࡶࡷࡴ࠿ࡻࡰ࡭ࡱࡤࡨࡤࡧࡰࡱࠤ੖"), datetime.datetime.now() - bstack1l1l1l1l_opy_)
  except ValueError as err:
    bstack1l1llll11l_opy_(bstack1lllllll1_opy_.format(str(err)))
  return bstack1l1l1lll11_opy_
def bstack11l1llll1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1l11l1l11_opy_
  bstack1l11lll1_opy_ = 1
  bstack1ll11lll1l_opy_ = 1
  if bstack11111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ੗") in CONFIG:
    bstack1ll11lll1l_opy_ = CONFIG[bstack11111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ੘")]
  else:
    bstack1ll11lll1l_opy_ = bstack11ll1l1l1l_opy_(framework_name, args) or 1
  if bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਖ਼") in CONFIG:
    bstack1l11lll1_opy_ = len(CONFIG[bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")])
  bstack1l11l1l11_opy_ = int(bstack1ll11lll1l_opy_) * int(bstack1l11lll1_opy_)
def bstack11ll1l1l1l_opy_(framework_name, args):
  if framework_name == bstack11l1111l1_opy_ and args and bstack11111l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪਜ਼") in args:
      bstack1l111l111_opy_ = args.index(bstack11111l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫੜ"))
      return int(args[bstack1l111l111_opy_ + 1]) or 1
  return 1
def bstack1l111l1lll_opy_(md5_hash):
  bstack1l11111l_opy_ = os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠧࡿࠩ੝")), bstack11111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack11111l_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ੟"))
  if os.path.exists(bstack1l11111l_opy_):
    bstack1ll11l111_opy_ = json.load(open(bstack1l11111l_opy_, bstack11111l_opy_ (u"ࠪࡶࡧ࠭੠")))
    if md5_hash in bstack1ll11l111_opy_:
      bstack1llll111l1_opy_ = bstack1ll11l111_opy_[md5_hash]
      bstack1l11l1lll1_opy_ = datetime.datetime.now()
      bstack11llll1l_opy_ = datetime.datetime.strptime(bstack1llll111l1_opy_[bstack11111l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ੡")], bstack11111l_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ੢"))
      if (bstack1l11l1lll1_opy_ - bstack11llll1l_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1llll111l1_opy_[bstack11111l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ੣")]):
        return None
      return bstack1llll111l1_opy_[bstack11111l_opy_ (u"ࠧࡪࡦࠪ੤")]
  else:
    return None
def bstack111ll111_opy_(md5_hash, bstack1l1l1lll11_opy_):
  bstack11lll1ll1l_opy_ = os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠨࢀࠪ੥")), bstack11111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ੦"))
  if not os.path.exists(bstack11lll1ll1l_opy_):
    os.makedirs(bstack11lll1ll1l_opy_)
  bstack1l11111l_opy_ = os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠪࢂࠬ੧")), bstack11111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ੨"), bstack11111l_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭੩"))
  bstack1ll1l11l1l_opy_ = {
    bstack11111l_opy_ (u"࠭ࡩࡥࠩ੪"): bstack1l1l1lll11_opy_,
    bstack11111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ੫"): datetime.datetime.strftime(datetime.datetime.now(), bstack11111l_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬ੬")),
    bstack11111l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ੭"): str(__version__)
  }
  if os.path.exists(bstack1l11111l_opy_):
    bstack1ll11l111_opy_ = json.load(open(bstack1l11111l_opy_, bstack11111l_opy_ (u"ࠪࡶࡧ࠭੮")))
  else:
    bstack1ll11l111_opy_ = {}
  bstack1ll11l111_opy_[md5_hash] = bstack1ll1l11l1l_opy_
  with open(bstack1l11111l_opy_, bstack11111l_opy_ (u"ࠦࡼ࠱ࠢ੯")) as outfile:
    json.dump(bstack1ll11l111_opy_, outfile)
def bstack1ll11lllll_opy_(self):
  return
def bstack1llllll11l_opy_(self):
  return
def bstack111l1l11l_opy_(self):
  global bstack1l1l111l1_opy_
  bstack1l1l111l1_opy_(self)
def bstack1lll11lll1_opy_():
  global bstack11l1l11lll_opy_
  bstack11l1l11lll_opy_ = True
@measure(event_name=EVENTS.bstack1l11lllll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack1l1ll1111l_opy_(self):
  global bstack1lll11l11l_opy_
  global bstack11llll1l1_opy_
  global bstack1ll1111111_opy_
  try:
    if bstack11111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬੰ") in bstack1lll11l11l_opy_ and self.session_id != None and bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪੱ"), bstack11111l_opy_ (u"ࠧࠨੲ")) != bstack11111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩੳ"):
      bstack11llll1111_opy_ = bstack11111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩੴ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪੵ")
      if bstack11llll1111_opy_ == bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੶"):
        bstack1lllll1111_opy_(logger)
      if self != None:
        bstack111ll11l1_opy_(self, bstack11llll1111_opy_, bstack11111l_opy_ (u"ࠬ࠲ࠠࠨ੷").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11111l_opy_ (u"࠭ࠧ੸")
    if bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ੹") in bstack1lll11l11l_opy_ and getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ੺"), None):
      bstack1llllll11_opy_.bstack1ll1111ll_opy_(self, bstack1lll111111_opy_, logger, wait=True)
    if bstack11111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ੻") in bstack1lll11l11l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack111ll11l1_opy_(self, bstack11111l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ੼"))
      bstack11lllll1_opy_.bstack11l11lll11_opy_(self)
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧ੽") + str(e))
  bstack1ll1111111_opy_(self)
  self.session_id = None
def bstack11l11l1lll_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1l11ll11_opy_
    global bstack1lll11l11l_opy_
    command_executor = kwargs.get(bstack11111l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠨ੾"), bstack11111l_opy_ (u"࠭ࠧ੿"))
    bstack1l1lll11l_opy_ = False
    if type(command_executor) == str and bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઀") in command_executor:
      bstack1l1lll11l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫઁ") in str(getattr(command_executor, bstack11111l_opy_ (u"ࠩࡢࡹࡷࡲࠧં"), bstack11111l_opy_ (u"ࠪࠫઃ"))):
      bstack1l1lll11l_opy_ = True
    else:
      return bstack1l11l111l_opy_(self, *args, **kwargs)
    if bstack1l1lll11l_opy_:
      bstack1llll111l_opy_ = bstack11l11lll1l_opy_.bstack1l1llll1l_opy_(CONFIG, bstack1lll11l11l_opy_)
      if kwargs.get(bstack11111l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ઄")):
        kwargs[bstack11111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭અ")] = bstack1l1l11ll11_opy_(kwargs[bstack11111l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧઆ")], bstack1lll11l11l_opy_, bstack1llll111l_opy_)
      elif kwargs.get(bstack11111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧઇ")):
        kwargs[bstack11111l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨઈ")] = bstack1l1l11ll11_opy_(kwargs[bstack11111l_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩઉ")], bstack1lll11l11l_opy_, bstack1llll111l_opy_)
  except Exception as e:
    logger.error(bstack11111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥઊ").format(str(e)))
  return bstack1l11l111l_opy_(self, *args, **kwargs)
@measure(event_name=EVENTS.bstack11ll1ll1ll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack111l111l_opy_(self, command_executor=bstack11111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧઋ"), *args, **kwargs):
  bstack11ll11lll_opy_ = bstack11l11l1lll_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1l1ll11l1l_opy_.on():
    return bstack11ll11lll_opy_
  try:
    logger.debug(bstack11111l_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩઌ").format(str(command_executor)))
    logger.debug(bstack11111l_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨઍ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ઎") in command_executor._url:
      bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩએ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬઐ") in command_executor):
    bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫઑ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1lll11111_opy_ = getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ઒"), None)
  if bstack11111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬઓ") in bstack1lll11l11l_opy_ or bstack11111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઔ") in bstack1lll11l11l_opy_:
    bstack1111lll11_opy_.bstack111lllll1_opy_(self)
  if bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧક") in bstack1lll11l11l_opy_ and bstack1lll11111_opy_ and bstack1lll11111_opy_.get(bstack11111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ"), bstack11111l_opy_ (u"ࠩࠪગ")) == bstack11111l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫઘ"):
    bstack1111lll11_opy_.bstack111lllll1_opy_(self)
  return bstack11ll11lll_opy_
def bstack1lll1lll_opy_(args):
  return bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬઙ") in str(args)
def bstack1lll11l111_opy_(self, driver_command, *args, **kwargs):
  global bstack1l11ll1l1_opy_
  global bstack1l1111l1_opy_
  bstack1l1lll1ll_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩચ"), None) and bstack11l11llll1_opy_(
          threading.current_thread(), bstack11111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬછ"), None)
  bstack1ll1l1l1l1_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧજ"), None) and bstack11l11llll1_opy_(
          threading.current_thread(), bstack11111l_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪઝ"), None)
  bstack11111ll11_opy_ = getattr(self, bstack11111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩઞ"), None) != None and getattr(self, bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪટ"), None) == True
  if not bstack1l1111l1_opy_ and bstack1ll111l11_opy_ and bstack11l1ll1l1_opy_.bstack1l1l11111_opy_(CONFIG) and bstack1l1l1ll111_opy_.bstack11l1l1l111_opy_(driver_command) and (bstack11111ll11_opy_ or bstack1l1lll1ll_opy_ or bstack1ll1l1l1l1_opy_) and not bstack1lll1lll_opy_(args):
    try:
      bstack1l1111l1_opy_ = True
      logger.debug(bstack11111l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ઠ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11111l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪડ").format(str(err)))
    bstack1l1111l1_opy_ = False
  response = bstack1l11ll1l1_opy_(self, driver_command, *args, **kwargs)
  if (bstack11111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઢ") in str(bstack1lll11l11l_opy_).lower() or bstack11111l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧણ") in str(bstack1lll11l11l_opy_).lower()) and bstack1l1ll11l1l_opy_.on():
    try:
      if driver_command == bstack11111l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬત"):
        bstack1111lll11_opy_.bstack1ll1ll11_opy_({
            bstack11111l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨથ"): response[bstack11111l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩદ")],
            bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫધ"): bstack1111lll11_opy_.current_test_uuid() if bstack1111lll11_opy_.current_test_uuid() else bstack1l1ll11l1l_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
@measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11ll1llll_opy_(self, command_executor,
             desired_capabilities=None, bstack11ll1l11_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None, *args, **kwargs):
  global CONFIG
  global bstack11llll1l1_opy_
  global bstack11ll111l_opy_
  global bstack1lllll11ll_opy_
  global bstack1l11ll111l_opy_
  global bstack11111111_opy_
  global bstack1lll11l11l_opy_
  global bstack1l11l111l_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1l11111l11_opy_
  global bstack1lll111111_opy_
  CONFIG[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧન")] = str(bstack1lll11l11l_opy_) + str(__version__)
  bstack1l11l1l1_opy_ = os.environ[bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ઩")]
  bstack1llll111l_opy_ = bstack11l11lll1l_opy_.bstack1l1llll1l_opy_(CONFIG, bstack1lll11l11l_opy_)
  CONFIG[bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪપ")] = bstack1l11l1l1_opy_
  CONFIG[bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪફ")] = bstack1llll111l_opy_
  if CONFIG.get(bstack11111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩબ"),bstack11111l_opy_ (u"ࠪࠫભ")) and bstack11111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪમ") in bstack1lll11l11l_opy_:
    CONFIG[bstack11111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬય")].pop(bstack11111l_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫર"), None)
    CONFIG[bstack11111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ઱")].pop(bstack11111l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭લ"), None)
  command_executor = bstack1lll1lll11_opy_()
  logger.debug(bstack1111l11l1_opy_.format(command_executor))
  proxy = bstack1l1ll11111_opy_(CONFIG, proxy)
  bstack1llll1l1ll_opy_ = 0 if bstack11ll111l_opy_ < 0 else bstack11ll111l_opy_
  try:
    if bstack1l11ll111l_opy_ is True:
      bstack1llll1l1ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack11111111_opy_ is True:
      bstack1llll1l1ll_opy_ = int(threading.current_thread().name)
  except:
    bstack1llll1l1ll_opy_ = 0
  bstack1111l1111_opy_ = bstack1l11ll1111_opy_(CONFIG, bstack1llll1l1ll_opy_)
  logger.debug(bstack1ll1l111l1_opy_.format(str(bstack1111l1111_opy_)))
  if bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ળ") in CONFIG and bstack11ll11l11_opy_(CONFIG[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ઴")]):
    bstack1lll1ll11l_opy_(bstack1111l1111_opy_)
  if bstack11l1ll1l1_opy_.bstack111l111ll_opy_(CONFIG, bstack1llll1l1ll_opy_) and bstack11l1ll1l1_opy_.bstack1ll1ll111l_opy_(bstack1111l1111_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    if cli.accessibility is None or not cli.accessibility.is_enabled():
      bstack11l1ll1l1_opy_.set_capabilities(bstack1111l1111_opy_, CONFIG)
  if desired_capabilities:
    bstack1l1ll1ll1l_opy_ = bstack1ll11llll1_opy_(desired_capabilities)
    bstack1l1ll1ll1l_opy_[bstack11111l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫવ")] = bstack11llll11l_opy_(CONFIG)
    bstack11l1l111l1_opy_ = bstack1l11ll1111_opy_(bstack1l1ll1ll1l_opy_)
    if bstack11l1l111l1_opy_:
      bstack1111l1111_opy_ = update(bstack11l1l111l1_opy_, bstack1111l1111_opy_)
    desired_capabilities = None
  if options:
    bstack1l1ll11l11_opy_(options, bstack1111l1111_opy_)
  if not options:
    options = bstack1l111l11l_opy_(bstack1111l1111_opy_)
  bstack1lll111111_opy_ = CONFIG.get(bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ"))[bstack1llll1l1ll_opy_]
  if proxy and bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ષ")):
    options.proxy(proxy)
  if options and bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭સ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1lllll11l1_opy_() < version.parse(bstack11111l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧહ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1111l1111_opy_)
  logger.info(bstack1l11llllll_opy_)
  bstack1lll11ll11_opy_.end(EVENTS.bstack1ll1l11l_opy_.value, EVENTS.bstack1ll1l11l_opy_.value + bstack11111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ઺"), EVENTS.bstack1ll1l11l_opy_.value + bstack11111l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ઻"), status=True, failure=None, test_name=bstack1lllll11ll_opy_)
  if bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡶࡲࡰࡨ࡬ࡰࡪ઼࠭") in kwargs:
    del kwargs[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡰࡳࡱࡩ࡭ࡱ࡫ࠧઽ")]
  if bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ા")):
    bstack1l11l111l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector, *args, **kwargs)
  elif bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭િ")):
    bstack1l11l111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              bstack11ll1l11_opy_=bstack11ll1l11_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨી")):
    bstack1l11l111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11ll1l11_opy_=bstack11ll1l11_opy_, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1l11l111l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              bstack11ll1l11_opy_=bstack11ll1l11_opy_, proxy=proxy,
              keep_alive=keep_alive)
  if bstack11l1ll1l1_opy_.bstack111l111ll_opy_(CONFIG, bstack1llll1l1ll_opy_) and bstack11l1ll1l1_opy_.bstack1ll1ll111l_opy_(self.caps, options, desired_capabilities):
    if CONFIG[bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫુ")][bstack11111l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩૂ")] == True:
      threading.current_thread().appA11yPlatform = True
      if cli.accessibility is None or not cli.accessibility.is_enabled():
        bstack11l1ll1l1_opy_.set_capabilities(bstack1111l1111_opy_, CONFIG)
  try:
    bstack1l1ll1l1_opy_ = bstack11111l_opy_ (u"ࠫࠬૃ")
    if bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ૄ")):
      bstack1l1ll1l1_opy_ = self.caps.get(bstack11111l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨૅ"))
    else:
      bstack1l1ll1l1_opy_ = self.capabilities.get(bstack11111l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢ૆"))
    if bstack1l1ll1l1_opy_:
      bstack111l1llll_opy_(bstack1l1ll1l1_opy_)
      if bstack1lllll11l1_opy_() <= version.parse(bstack11111l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨે")):
        self.command_executor._url = bstack11111l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥૈ") + bstack1l1l111ll_opy_ + bstack11111l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢૉ")
      else:
        self.command_executor._url = bstack11111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ૊") + bstack1l1ll1l1_opy_ + bstack11111l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨો")
      logger.debug(bstack11ll1111l_opy_.format(bstack1l1ll1l1_opy_))
    else:
      logger.debug(bstack1ll11l1l11_opy_.format(bstack11111l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢૌ")))
  except Exception as e:
    logger.debug(bstack1ll11l1l11_opy_.format(e))
  if bstack11111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ્࠭") in bstack1lll11l11l_opy_:
    bstack11ll11111_opy_(bstack11ll111l_opy_, bstack1l11111l11_opy_)
  bstack11llll1l1_opy_ = self.session_id
  if bstack11111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ૎") in bstack1lll11l11l_opy_ or bstack11111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ૏") in bstack1lll11l11l_opy_ or bstack11111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩૐ") in bstack1lll11l11l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
  bstack1lll11111_opy_ = getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡘࡪࡹࡴࡎࡧࡷࡥࠬ૑"), None)
  if bstack11111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ૒") in bstack1lll11l11l_opy_ or bstack11111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ૓") in bstack1lll11l11l_opy_:
    bstack1111lll11_opy_.bstack111lllll1_opy_(self)
  if bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ૔") in bstack1lll11l11l_opy_ and bstack1lll11111_opy_ and bstack1lll11111_opy_.get(bstack11111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ૕"), bstack11111l_opy_ (u"ࠩࠪ૖")) == bstack11111l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ૗"):
    bstack1111lll11_opy_.bstack111lllll1_opy_(self)
  bstack1lll1l1l1l_opy_.append(self)
  if bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ૘") in CONFIG and bstack11111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ૙") in CONFIG[bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૚")][bstack1llll1l1ll_opy_]:
    bstack1lllll11ll_opy_ = CONFIG[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૛")][bstack1llll1l1ll_opy_][bstack11111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭૜")]
  logger.debug(bstack11l1l111_opy_.format(bstack11llll1l1_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    from browserstack_sdk.__init__ import bstack1lll1lll1_opy_
    def bstack11111l1ll_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1lllll1_opy_
      if(bstack11111l_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸ࠯࡬ࡶࠦ૝") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠪࢂࠬ૞")), bstack11111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ૟"), bstack11111l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧૠ")), bstack11111l_opy_ (u"࠭ࡷࠨૡ")) as fp:
          fp.write(bstack11111l_opy_ (u"ࠢࠣૢ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11111l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥૣ")))):
          with open(args[1], bstack11111l_opy_ (u"ࠩࡵࠫ૤")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11111l_opy_ (u"ࠪࡥࡸࡿ࡮ࡤࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࡤࡴࡥࡸࡒࡤ࡫ࡪ࠮ࡣࡰࡰࡷࡩࡽࡺࠬࠡࡲࡤ࡫ࡪࠦ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠩ૥") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11llllllll_opy_)
            if bstack11111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ૦") in CONFIG and str(CONFIG[bstack11111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ૧")]).lower() != bstack11111l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ૨"):
                bstack1l111l111l_opy_ = bstack1lll1lll1_opy_()
                bstack1ll1lll11l_opy_ = bstack11111l_opy_ (u"ࠧࠨࠩࠍ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴ࠐࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࠼ࠌࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠ࠿ࠏࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࠾ࠎࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࠾ࠎࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࠏ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࢁࠊࠡࠢ࡯ࡩࡹࠦࡣࡢࡲࡶ࠿ࠏࠦࠠࡵࡴࡼࠤࢀࢁࠊࠡࠢࠣࠤࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࠻ࠋࠢࠣࢁࢂࠦࡣࡢࡶࡦ࡬ࠥ࠮ࡥࡹࠫࠣࡿࢀࠐࠠࠡࠢࠣࡧࡴࡴࡳࡰ࡮ࡨ࠲ࡪࡸࡲࡰࡴࠫࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠿ࠨࠬࠡࡧࡻ࠭ࡀࠐࠠࠡࡿࢀࠎࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻࡼࠌࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࠬࢁࡣࡥࡲࡘࡶࡱࢃࠧࠡ࠭ࠣࡩࡳࡩ࡯ࡥࡧࡘࡖࡎࡉ࡯࡮ࡲࡲࡲࡪࡴࡴࠩࡌࡖࡓࡓ࠴ࡳࡵࡴ࡬ࡲ࡬࡯ࡦࡺࠪࡦࡥࡵࡹࠩࠪ࠮ࠍࠤࠥࠦࠠ࠯࠰࠱ࡰࡦࡻ࡮ࡤࡪࡒࡴࡹ࡯࡯࡯ࡵࠍࠤࠥࢃࡽࠪ࠽ࠍࢁࢂࡁࠊ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱ࠍࠫࠬ࠭૩").format(bstack1l111l111l_opy_=bstack1l111l111l_opy_)
            lines.insert(1, bstack1ll1lll11l_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11111l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ૪")), bstack11111l_opy_ (u"ࠩࡺࠫ૫")) as bstack1llll1l1l_opy_:
              bstack1llll1l1l_opy_.writelines(lines)
        CONFIG[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ૬")] = str(bstack1lll11l11l_opy_) + str(__version__)
        bstack1l11l1l1_opy_ = os.environ[bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ૭")]
        bstack1llll111l_opy_ = bstack11l11lll1l_opy_.bstack1l1llll1l_opy_(CONFIG, bstack1lll11l11l_opy_)
        CONFIG[bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ૮")] = bstack1l11l1l1_opy_
        CONFIG[bstack11111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ૯")] = bstack1llll111l_opy_
        bstack1llll1l1ll_opy_ = 0 if bstack11ll111l_opy_ < 0 else bstack11ll111l_opy_
        try:
          if bstack1l11ll111l_opy_ is True:
            bstack1llll1l1ll_opy_ = int(multiprocessing.current_process().name)
          elif bstack11111111_opy_ is True:
            bstack1llll1l1ll_opy_ = int(threading.current_thread().name)
        except:
          bstack1llll1l1ll_opy_ = 0
        CONFIG[bstack11111l_opy_ (u"ࠢࡶࡵࡨ࡛࠸ࡉࠢ૰")] = False
        CONFIG[bstack11111l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ૱")] = True
        bstack1111l1111_opy_ = bstack1l11ll1111_opy_(CONFIG, bstack1llll1l1ll_opy_)
        logger.debug(bstack1ll1l111l1_opy_.format(str(bstack1111l1111_opy_)))
        if CONFIG.get(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭૲")):
          bstack1lll1ll11l_opy_(bstack1111l1111_opy_)
        if bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૳") in CONFIG and bstack11111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ૴") in CONFIG[bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ૵")][bstack1llll1l1ll_opy_]:
          bstack1lllll11ll_opy_ = CONFIG[bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ૶")][bstack1llll1l1ll_opy_][bstack11111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ૷")]
        args.append(os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠨࢀࠪ૸")), bstack11111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩૹ"), bstack11111l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬૺ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1111l1111_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11111l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺࡢࡦࡸࡺࡡࡤ࡭࠱࡮ࡸࠨૻ"))
      bstack1l1lllll1_opy_ = True
      return bstack1l1ll1l111_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack11l1l1l1l_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11ll111l_opy_
    global bstack1lllll11ll_opy_
    global bstack1l11ll111l_opy_
    global bstack11111111_opy_
    global bstack1lll11l11l_opy_
    CONFIG[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧૼ")] = str(bstack1lll11l11l_opy_) + str(__version__)
    bstack1l11l1l1_opy_ = os.environ[bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ૽")]
    bstack1llll111l_opy_ = bstack11l11lll1l_opy_.bstack1l1llll1l_opy_(CONFIG, bstack1lll11l11l_opy_)
    CONFIG[bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ૾")] = bstack1l11l1l1_opy_
    CONFIG[bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ૿")] = bstack1llll111l_opy_
    bstack1llll1l1ll_opy_ = 0 if bstack11ll111l_opy_ < 0 else bstack11ll111l_opy_
    try:
      if bstack1l11ll111l_opy_ is True:
        bstack1llll1l1ll_opy_ = int(multiprocessing.current_process().name)
      elif bstack11111111_opy_ is True:
        bstack1llll1l1ll_opy_ = int(threading.current_thread().name)
    except:
      bstack1llll1l1ll_opy_ = 0
    CONFIG[bstack11111l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣ଀")] = True
    bstack1111l1111_opy_ = bstack1l11ll1111_opy_(CONFIG, bstack1llll1l1ll_opy_)
    logger.debug(bstack1ll1l111l1_opy_.format(str(bstack1111l1111_opy_)))
    if CONFIG.get(bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଁ")):
      bstack1lll1ll11l_opy_(bstack1111l1111_opy_)
    if bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧଂ") in CONFIG and bstack11111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪଃ") in CONFIG[bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ଄")][bstack1llll1l1ll_opy_]:
      bstack1lllll11ll_opy_ = CONFIG[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪଅ")][bstack1llll1l1ll_opy_][bstack11111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଆ")]
    import urllib
    import json
    if bstack11111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ଇ") in CONFIG and str(CONFIG[bstack11111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧଈ")]).lower() != bstack11111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪଉ"):
        bstack1lll11ll1l_opy_ = bstack1lll1lll1_opy_()
        bstack1l111l111l_opy_ = bstack1lll11ll1l_opy_ + urllib.parse.quote(json.dumps(bstack1111l1111_opy_))
    else:
        bstack1l111l111l_opy_ = bstack11111l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧଊ") + urllib.parse.quote(json.dumps(bstack1111l1111_opy_))
    browser = self.connect(bstack1l111l111l_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1111111_opy_():
    global bstack1l1lllll1_opy_
    global bstack1lll11l11l_opy_
    global CONFIG
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11111lll1_opy_
        global bstack1l11l11ll1_opy_
        if not bstack1ll111l11_opy_:
          global bstack11l1ll1l1l_opy_
          if not bstack11l1ll1l1l_opy_:
            from bstack_utils.helper import bstack11l1ll1ll1_opy_, bstack1llllllll1_opy_, bstack1111l1l11_opy_
            bstack11l1ll1l1l_opy_ = bstack11l1ll1ll1_opy_()
            bstack1llllllll1_opy_(bstack1lll11l11l_opy_)
            bstack1llll111l_opy_ = bstack11l11lll1l_opy_.bstack1l1llll1l_opy_(CONFIG, bstack1lll11l11l_opy_)
            bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠨࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡔࡗࡕࡄࡖࡅࡗࡣࡒࡇࡐࠣଋ"), bstack1llll111l_opy_)
          BrowserType.connect = bstack11111lll1_opy_
          return
        BrowserType.launch = bstack11l1l1l1l_opy_
        bstack1l1lllll1_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack11111l1ll_opy_
      bstack1l1lllll1_opy_ = True
    except Exception as e:
      pass
def bstack1l111111_opy_(context, bstack1l11ll1ll1_opy_):
  try:
    context.page.evaluate(bstack11111l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣଌ"), bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬ଍")+ json.dumps(bstack1l11ll1ll1_opy_) + bstack11111l_opy_ (u"ࠤࢀࢁࠧ଎"))
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽ࠻ࠢࡾࢁࠧଏ").format(str(e), traceback.format_exc()))
def bstack1l1l111lll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11111l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧଐ"), bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ଑") + json.dumps(message) + bstack11111l_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩ଒") + json.dumps(level) + bstack11111l_opy_ (u"ࠧࡾࡿࠪଓ"))
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠾ࠥࢁࡽࠣଔ").format(str(e), traceback.format_exc()))
@measure(event_name=EVENTS.bstack11lll111l_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11llll111_opy_(self, url):
  global bstack11ll11ll_opy_
  try:
    bstack1llll1111_opy_(url)
  except Exception as err:
    logger.debug(bstack1llll111_opy_.format(str(err)))
  try:
    bstack11ll11ll_opy_(self, url)
  except Exception as e:
    try:
      bstack1llll11l_opy_ = str(e)
      if any(err_msg in bstack1llll11l_opy_ for err_msg in bstack1lll1l11l1_opy_):
        bstack1llll1111_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1llll111_opy_.format(str(err)))
    raise e
def bstack1l111l1l_opy_(self):
  global bstack111ll1ll1_opy_
  bstack111ll1ll1_opy_ = self
  return
def bstack1l1l1ll11_opy_(self):
  global bstack1lll1l1l_opy_
  bstack1lll1l1l_opy_ = self
  return
def bstack1ll1l1lll1_opy_(test_name, bstack1l111ll111_opy_):
  global CONFIG
  if percy.bstack111l1ll1l_opy_() == bstack11111l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢକ"):
    bstack11ll111ll_opy_ = os.path.relpath(bstack1l111ll111_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11ll111ll_opy_)
    bstack1l1ll1ll_opy_ = suite_name + bstack11111l_opy_ (u"ࠥ࠱ࠧଖ") + test_name
    threading.current_thread().percySessionName = bstack1l1ll1ll_opy_
def bstack1lll11lll_opy_(self, test, *args, **kwargs):
  global bstack1l11ll11_opy_
  test_name = None
  bstack1l111ll111_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l111ll111_opy_ = str(test.source)
  bstack1ll1l1lll1_opy_(test_name, bstack1l111ll111_opy_)
  bstack1l11ll11_opy_(self, test, *args, **kwargs)
@measure(event_name=EVENTS.bstack1l1ll1lll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack1ll1l11111_opy_(driver, bstack1l1ll1ll_opy_):
  if not bstack1lll1llll_opy_ and bstack1l1ll1ll_opy_:
      bstack1ll1l11l11_opy_ = {
          bstack11111l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫଗ"): bstack11111l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଘ"),
          bstack11111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଙ"): {
              bstack11111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬଚ"): bstack1l1ll1ll_opy_
          }
      }
      bstack11l1ll1lll_opy_ = bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ଛ").format(json.dumps(bstack1ll1l11l11_opy_))
      driver.execute_script(bstack11l1ll1lll_opy_)
  if bstack1ll1l11l1_opy_:
      bstack111111l1l_opy_ = {
          bstack11111l_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩଜ"): bstack11111l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬଝ"),
          bstack11111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଞ"): {
              bstack11111l_opy_ (u"ࠬࡪࡡࡵࡣࠪଟ"): bstack1l1ll1ll_opy_ + bstack11111l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨଠ"),
              bstack11111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ଡ"): bstack11111l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ଢ")
          }
      }
      if bstack1ll1l11l1_opy_.status == bstack11111l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧଣ"):
          bstack11ll11lll1_opy_ = bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨତ").format(json.dumps(bstack111111l1l_opy_))
          driver.execute_script(bstack11ll11lll1_opy_)
          bstack111ll11l1_opy_(driver, bstack11111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫଥ"))
      elif bstack1ll1l11l1_opy_.status == bstack11111l_opy_ (u"ࠬࡌࡁࡊࡎࠪଦ"):
          reason = bstack11111l_opy_ (u"ࠨࠢଧ")
          bstack1l1ll1l1l_opy_ = bstack1l1ll1ll_opy_ + bstack11111l_opy_ (u"ࠧࠡࡨࡤ࡭ࡱ࡫ࡤࠨନ")
          if bstack1ll1l11l1_opy_.message:
              reason = str(bstack1ll1l11l1_opy_.message)
              bstack1l1ll1l1l_opy_ = bstack1l1ll1l1l_opy_ + bstack11111l_opy_ (u"ࠨࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࠨ଩") + reason
          bstack111111l1l_opy_[bstack11111l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬପ")] = {
              bstack11111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩଫ"): bstack11111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪବ"),
              bstack11111l_opy_ (u"ࠬࡪࡡࡵࡣࠪଭ"): bstack1l1ll1l1l_opy_
          }
          bstack11ll11lll1_opy_ = bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫମ").format(json.dumps(bstack111111l1l_opy_))
          driver.execute_script(bstack11ll11lll1_opy_)
          bstack111ll11l1_opy_(driver, bstack11111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧଯ"), reason)
          bstack1l1lll1l1l_opy_(reason, str(bstack1ll1l11l1_opy_), str(bstack11ll111l_opy_), logger)
@measure(event_name=EVENTS.bstack1l11111ll1_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11ll11l1l_opy_(driver, test):
  if percy.bstack111l1ll1l_opy_() == bstack11111l_opy_ (u"ࠣࡶࡵࡹࡪࠨର") and percy.bstack11llll1ll_opy_() == bstack11111l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ଱"):
      bstack1l111l1111_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ଲ"), None)
      bstack1lll1l1ll_opy_(driver, bstack1l111l1111_opy_, test)
  if (bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨଳ"), None) and
      bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ଴"), None)) or (
      bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ଵ"), None) and
      bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩଶ"), None)):
      logger.info(bstack11111l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣଷ"))
      bstack11l1ll1l1_opy_.bstack11ll11l1ll_opy_(driver, name=test.name, path=test.source)
def bstack1ll11l11_opy_(test, bstack1l1ll1ll_opy_):
    try:
      bstack1l1l1l1l_opy_ = datetime.datetime.now()
      data = {}
      if test:
        data[bstack11111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧସ")] = bstack1l1ll1ll_opy_
      if bstack1ll1l11l1_opy_:
        if bstack1ll1l11l1_opy_.status == bstack11111l_opy_ (u"ࠪࡔࡆ࡙ࡓࠨହ"):
          data[bstack11111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ଺")] = bstack11111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ଻")
        elif bstack1ll1l11l1_opy_.status == bstack11111l_opy_ (u"࠭ࡆࡂࡋࡏ଼ࠫ"):
          data[bstack11111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧଽ")] = bstack11111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨା")
          if bstack1ll1l11l1_opy_.message:
            data[bstack11111l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩି")] = str(bstack1ll1l11l1_opy_.message)
      user = CONFIG[bstack11111l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬୀ")]
      key = CONFIG[bstack11111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧୁ")]
      url = bstack11111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪୂ").format(user, key, bstack11llll1l1_opy_)
      headers = {
        bstack11111l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬୃ"): bstack11111l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪୄ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
        cli.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠣࡪࡷࡸࡵࡀࡵࡱࡦࡤࡸࡪࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡴࡢࡶࡸࡷࠧ୅"), datetime.datetime.now() - bstack1l1l1l1l_opy_)
    except Exception as e:
      logger.error(bstack11lll11l1l_opy_.format(str(e)))
def bstack1l1ll1l11_opy_(test, bstack1l1ll1ll_opy_):
  global CONFIG
  global bstack1lll1l1l_opy_
  global bstack111ll1ll1_opy_
  global bstack11llll1l1_opy_
  global bstack1ll1l11l1_opy_
  global bstack1lllll11ll_opy_
  global bstack1ll11l11l1_opy_
  global bstack1ll111ll1_opy_
  global bstack11l1l111l_opy_
  global bstack1l1l1lll1_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1lll111111_opy_
  try:
    if not bstack11llll1l1_opy_:
      with open(os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠩࢁࠫ୆")), bstack11111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪେ"), bstack11111l_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ୈ"))) as f:
        bstack1llll11l11_opy_ = json.loads(bstack11111l_opy_ (u"ࠧࢁࠢ୉") + f.read().strip() + bstack11111l_opy_ (u"࠭ࠢࡹࠤ࠽ࠤࠧࡿࠢࠨ୊") + bstack11111l_opy_ (u"ࠢࡾࠤୋ"))
        bstack11llll1l1_opy_ = bstack1llll11l11_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1lll1l1l1l_opy_:
    for driver in bstack1lll1l1l1l_opy_:
      if bstack11llll1l1_opy_ == driver.session_id:
        if test:
          bstack11ll11l1l_opy_(driver, test)
        bstack1ll1l11111_opy_(driver, bstack1l1ll1ll_opy_)
  elif bstack11llll1l1_opy_:
    bstack1ll11l11_opy_(test, bstack1l1ll1ll_opy_)
  if bstack1lll1l1l_opy_:
    bstack1ll111ll1_opy_(bstack1lll1l1l_opy_)
  if bstack111ll1ll1_opy_:
    bstack11l1l111l_opy_(bstack111ll1ll1_opy_)
  if bstack11l1l11lll_opy_:
    bstack1l1l1lll1_opy_()
def bstack1llll11l1_opy_(self, test, *args, **kwargs):
  bstack1l1ll1ll_opy_ = None
  if test:
    bstack1l1ll1ll_opy_ = str(test.name)
  bstack1l1ll1l11_opy_(test, bstack1l1ll1ll_opy_)
  bstack1ll11l11l1_opy_(self, test, *args, **kwargs)
def bstack11ll1l11ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1lll1l1_opy_
  global CONFIG
  global bstack1lll1l1l1l_opy_
  global bstack11llll1l1_opy_
  bstack1l11l1l111_opy_ = None
  try:
    if bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧୌ"), None) or bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰ୍ࠫ"), None):
      try:
        if not bstack11llll1l1_opy_:
          with open(os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠪࢂࠬ୎")), bstack11111l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ୏"), bstack11111l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ୐"))) as f:
            bstack1llll11l11_opy_ = json.loads(bstack11111l_opy_ (u"ࠨࡻࠣ୑") + f.read().strip() + bstack11111l_opy_ (u"ࠧࠣࡺࠥ࠾ࠥࠨࡹࠣࠩ୒") + bstack11111l_opy_ (u"ࠣࡿࠥ୓"))
            bstack11llll1l1_opy_ = bstack1llll11l11_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1lll1l1l1l_opy_:
        for driver in bstack1lll1l1l1l_opy_:
          if bstack11llll1l1_opy_ == driver.session_id:
            bstack1l11l1l111_opy_ = driver
    bstack1111l111_opy_ = bstack11l1ll1l1_opy_.bstack11l111ll_opy_(test.tags)
    if bstack1l11l1l111_opy_:
      threading.current_thread().isA11yTest = bstack11l1ll1l1_opy_.bstack1lll1l11_opy_(bstack1l11l1l111_opy_, bstack1111l111_opy_)
      threading.current_thread().isAppA11yTest = bstack11l1ll1l1_opy_.bstack1lll1l11_opy_(bstack1l11l1l111_opy_, bstack1111l111_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1111l111_opy_
      threading.current_thread().isAppA11yTest = bstack1111l111_opy_
  except:
    pass
  bstack1ll1lll1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll1l11l1_opy_
  try:
    bstack1ll1l11l1_opy_ = self._test
  except:
    bstack1ll1l11l1_opy_ = self.test
def bstack1ll1llllll_opy_():
  global bstack11llll1l1l_opy_
  try:
    if os.path.exists(bstack11llll1l1l_opy_):
      os.remove(bstack11llll1l1l_opy_)
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬ୔") + str(e))
def bstack1l1llll1l1_opy_():
  global bstack11llll1l1l_opy_
  bstack1ll1111l11_opy_ = {}
  try:
    if not os.path.isfile(bstack11llll1l1l_opy_):
      with open(bstack11llll1l1l_opy_, bstack11111l_opy_ (u"ࠪࡻࠬ୕")):
        pass
      with open(bstack11llll1l1l_opy_, bstack11111l_opy_ (u"ࠦࡼ࠱ࠢୖ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11llll1l1l_opy_):
      bstack1ll1111l11_opy_ = json.load(open(bstack11llll1l1l_opy_, bstack11111l_opy_ (u"ࠬࡸࡢࠨୗ")))
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ୘") + str(e))
  finally:
    return bstack1ll1111l11_opy_
def bstack11ll11111_opy_(platform_index, item_index):
  global bstack11llll1l1l_opy_
  try:
    bstack1ll1111l11_opy_ = bstack1l1llll1l1_opy_()
    bstack1ll1111l11_opy_[item_index] = platform_index
    with open(bstack11llll1l1l_opy_, bstack11111l_opy_ (u"ࠢࡸ࠭ࠥ୙")) as outfile:
      json.dump(bstack1ll1111l11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡻࡷ࡯ࡴࡪࡰࡪࠤࡹࡵࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭୚") + str(e))
def bstack1lll1ll111_opy_(bstack11l1l1lll_opy_):
  global CONFIG
  bstack1ll11l11ll_opy_ = bstack11111l_opy_ (u"ࠩࠪ୛")
  if not bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ଡ଼") in CONFIG:
    logger.info(bstack11111l_opy_ (u"ࠫࡓࡵࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠣࡴࡦࡹࡳࡦࡦࠣࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡰࡨࡶࡦࡺࡥࠡࡴࡨࡴࡴࡸࡴࠡࡨࡲࡶࠥࡘ࡯ࡣࡱࡷࠤࡷࡻ࡮ࠨଢ଼"))
  try:
    platform = CONFIG[bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୞")][bstack11l1l1lll_opy_]
    if bstack11111l_opy_ (u"࠭࡯ࡴࠩୟ") in platform:
      bstack1ll11l11ll_opy_ += str(platform[bstack11111l_opy_ (u"ࠧࡰࡵࠪୠ")]) + bstack11111l_opy_ (u"ࠨ࠮ࠣࠫୡ")
    if bstack11111l_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬୢ") in platform:
      bstack1ll11l11ll_opy_ += str(platform[bstack11111l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ୣ")]) + bstack11111l_opy_ (u"ࠫ࠱ࠦࠧ୤")
    if bstack11111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ୥") in platform:
      bstack1ll11l11ll_opy_ += str(platform[bstack11111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ୦")]) + bstack11111l_opy_ (u"ࠧ࠭ࠢࠪ୧")
    if bstack11111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ୨") in platform:
      bstack1ll11l11ll_opy_ += str(platform[bstack11111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ୩")]) + bstack11111l_opy_ (u"ࠪ࠰ࠥ࠭୪")
    if bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ୫") in platform:
      bstack1ll11l11ll_opy_ += str(platform[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ୬")]) + bstack11111l_opy_ (u"࠭ࠬࠡࠩ୭")
    if bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ୮") in platform:
      bstack1ll11l11ll_opy_ += str(platform[bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ୯")]) + bstack11111l_opy_ (u"ࠩ࠯ࠤࠬ୰")
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠪࡗࡴࡳࡥࠡࡧࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡴࡥࡳࡣࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡸࡷ࡯࡮ࡨࠢࡩࡳࡷࠦࡲࡦࡲࡲࡶࡹࠦࡧࡦࡰࡨࡶࡦࡺࡩࡰࡰࠪୱ") + str(e))
  finally:
    if bstack1ll11l11ll_opy_[len(bstack1ll11l11ll_opy_) - 2:] == bstack11111l_opy_ (u"ࠫ࠱ࠦࠧ୲"):
      bstack1ll11l11ll_opy_ = bstack1ll11l11ll_opy_[:-2]
    return bstack1ll11l11ll_opy_
def bstack11l11111l_opy_(path, bstack1ll11l11ll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1lll1l1l1_opy_ = ET.parse(path)
    bstack1llll1ll11_opy_ = bstack1lll1l1l1_opy_.getroot()
    bstack1l1l1111l1_opy_ = None
    for suite in bstack1llll1ll11_opy_.iter(bstack11111l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୳")):
      if bstack11111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭୴") in suite.attrib:
        suite.attrib[bstack11111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ୵")] += bstack11111l_opy_ (u"ࠨࠢࠪ୶") + bstack1ll11l11ll_opy_
        bstack1l1l1111l1_opy_ = suite
    bstack11l1l11l1l_opy_ = None
    for robot in bstack1llll1ll11_opy_.iter(bstack11111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ୷")):
      bstack11l1l11l1l_opy_ = robot
    bstack11ll111ll1_opy_ = len(bstack11l1l11l1l_opy_.findall(bstack11111l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ୸")))
    if bstack11ll111ll1_opy_ == 1:
      bstack11l1l11l1l_opy_.remove(bstack11l1l11l1l_opy_.findall(bstack11111l_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪ୹"))[0])
      bstack1l111lll11_opy_ = ET.Element(bstack11111l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ୺"), attrib={bstack11111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ୻"): bstack11111l_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࡹࠧ୼"), bstack11111l_opy_ (u"ࠨ࡫ࡧࠫ୽"): bstack11111l_opy_ (u"ࠩࡶ࠴ࠬ୾")})
      bstack11l1l11l1l_opy_.insert(1, bstack1l111lll11_opy_)
      bstack1ll1l11lll_opy_ = None
      for suite in bstack11l1l11l1l_opy_.iter(bstack11111l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ୿")):
        bstack1ll1l11lll_opy_ = suite
      bstack1ll1l11lll_opy_.append(bstack1l1l1111l1_opy_)
      bstack11l1ll11l1_opy_ = None
      for status in bstack1l1l1111l1_opy_.iter(bstack11111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ஀")):
        bstack11l1ll11l1_opy_ = status
      bstack1ll1l11lll_opy_.append(bstack11l1ll11l1_opy_)
    bstack1lll1l1l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡱࡣࡵࡷ࡮ࡴࡧࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡱࡩࡷࡧࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠪ஁") + str(e))
def bstack1l1l1l11ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack11l1llllll_opy_
  global CONFIG
  if bstack11111l_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥஂ") in options:
    del options[bstack11111l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࡰࡢࡶ࡫ࠦஃ")]
  bstack11l11lll_opy_ = bstack1l1llll1l1_opy_()
  for bstack11l1lll111_opy_ in bstack11l11lll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11111l_opy_ (u"ࠨࡲࡤࡦࡴࡺ࡟ࡳࡧࡶࡹࡱࡺࡳࠨ஄"), str(bstack11l1lll111_opy_), bstack11111l_opy_ (u"ࠩࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱ࠭அ"))
    bstack11l11111l_opy_(path, bstack1lll1ll111_opy_(bstack11l11lll_opy_[bstack11l1lll111_opy_]))
  bstack1ll1llllll_opy_()
  return bstack11l1llllll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l1ll111l_opy_(self, ff_profile_dir):
  global bstack1l1ll11l1_opy_
  if not ff_profile_dir:
    return None
  return bstack1l1ll11l1_opy_(self, ff_profile_dir)
def bstack11llllll11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack11l1lll1ll_opy_
  bstack1ll1l111ll_opy_ = []
  if bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ஆ") in CONFIG:
    bstack1ll1l111ll_opy_ = CONFIG[bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧஇ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨஈ")],
      pabot_args[bstack11111l_opy_ (u"ࠨࡶࡦࡴࡥࡳࡸ࡫ࠢஉ")],
      argfile,
      pabot_args.get(bstack11111l_opy_ (u"ࠢࡩ࡫ࡹࡩࠧஊ")),
      pabot_args[bstack11111l_opy_ (u"ࠣࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠦ஋")],
      platform[0],
      bstack11l1lll1ll_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11111l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡪ࡮ࡲࡥࡴࠤ஌")] or [(bstack11111l_opy_ (u"ࠥࠦ஍"), None)]
    for platform in enumerate(bstack1ll1l111ll_opy_)
  ]
def bstack11ll1l11l1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1lllll11_opy_=bstack11111l_opy_ (u"ࠫࠬஎ")):
  global bstack11lll1ll11_opy_
  self.platform_index = platform_index
  self.bstack11ll1ll11l_opy_ = bstack1lllll11_opy_
  bstack11lll1ll11_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1llll11ll_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l111l1l11_opy_
  global bstack1l1l1l111l_opy_
  bstack1l1l1l1ll1_opy_ = copy.deepcopy(item)
  if not bstack11111l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧஏ") in item.options:
    bstack1l1l1l1ll1_opy_.options[bstack11111l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨஐ")] = []
  bstack111l1lll1_opy_ = bstack1l1l1l1ll1_opy_.options[bstack11111l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ஑")].copy()
  for v in bstack1l1l1l1ll1_opy_.options[bstack11111l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪஒ")]:
    if bstack11111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨஓ") in v:
      bstack111l1lll1_opy_.remove(v)
    if bstack11111l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡆࡐࡎࡇࡒࡈࡕࠪஔ") in v:
      bstack111l1lll1_opy_.remove(v)
    if bstack11111l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨக") in v:
      bstack111l1lll1_opy_.remove(v)
  bstack111l1lll1_opy_.insert(0, bstack11111l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧ஖").format(bstack1l1l1l1ll1_opy_.platform_index))
  bstack111l1lll1_opy_.insert(0, bstack11111l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔ࠽ࡿࢂ࠭஗").format(bstack1l1l1l1ll1_opy_.bstack11ll1ll11l_opy_))
  bstack1l1l1l1ll1_opy_.options[bstack11111l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ஘")] = bstack111l1lll1_opy_
  if bstack1l1l1l111l_opy_:
    bstack1l1l1l1ll1_opy_.options[bstack11111l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪங")].insert(0, bstack11111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬச").format(bstack1l1l1l111l_opy_))
  return bstack1l111l1l11_opy_(caller_id, datasources, is_last, bstack1l1l1l1ll1_opy_, outs_dir)
def bstack11llll11l1_opy_(command, item_index):
  if bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ஛")):
    os.environ[bstack11111l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬஜ")] = json.dumps(CONFIG[bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ஝")][item_index % bstack1111l1ll1_opy_])
  global bstack1l1l1l111l_opy_
  if bstack1l1l1l111l_opy_:
    command[0] = command[0].replace(bstack11111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬஞ"), bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫட") + str(
      item_index) + bstack11111l_opy_ (u"ࠨࠢࠪ஠") + bstack1l1l1l111l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ஡"),
                                    bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧ஢") + str(item_index), 1)
def bstack1l1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll111ll1l_opy_
  bstack11llll11l1_opy_(command, item_index)
  return bstack1ll111ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11l111l1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1ll111ll1l_opy_
  bstack11llll11l1_opy_(command, item_index)
  return bstack1ll111ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack11lllll1l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1ll111ll1l_opy_
  bstack11llll11l1_opy_(command, item_index)
  return bstack1ll111ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1lll1l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start):
  global bstack1ll111ll1l_opy_
  bstack11llll11l1_opy_(command, item_index)
  return bstack1ll111ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout, sleep_before_start)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1ll1ll11l1_opy_(self, runner, quiet=False, capture=True):
  global bstack11l1lll1_opy_
  bstack1ll1lll1_opy_ = bstack11l1lll1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11111l_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࡟ࡢࡴࡵࠫண")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11111l_opy_ (u"ࠬ࡫ࡸࡤࡡࡷࡶࡦࡩࡥࡣࡣࡦ࡯ࡤࡧࡲࡳࠩத")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1lll1_opy_
def bstack11l1l1l11_opy_(runner, hook_name, context, element, bstack11llll11_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1ll1ll1111_opy_.bstack11ll11111l_opy_(hook_name, element)
    bstack11llll11_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1ll1ll1111_opy_.bstack1ll1ll1l_opy_(element)
      if hook_name not in [bstack11111l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ஥"), bstack11111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪ஦")] and args and hasattr(args[0], bstack11111l_opy_ (u"ࠨࡧࡵࡶࡴࡸ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠨ஧")):
        args[0].error_message = bstack11111l_opy_ (u"ࠩࠪந")
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡨࡢࡰࡧࡰࡪࠦࡨࡰࡱ࡮ࡷࠥ࡯࡮ࠡࡤࡨ࡬ࡦࡼࡥ࠻ࠢࡾࢁࠬன").format(str(e)))
@measure(event_name=EVENTS.bstack1l11lll1l1_opy_, stage=STAGE.bstack1l1llll11_opy_, hook_type=bstack11111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡅࡱࡲࠢப"), bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11lll11111_opy_(runner, name, context, bstack11llll11_opy_, *args):
    if runner.hooks.get(bstack11111l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ஫")).__name__ != bstack11111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢࡨࡪ࡬ࡡࡶ࡮ࡷࡣ࡭ࡵ࡯࡬ࠤ஬"):
      bstack11l1l1l11_opy_(runner, name, context, runner, bstack11llll11_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1lllllll11_opy_(bstack11111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭஭")) else context.browser
      runner.driver_initialised = bstack11111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧம")
    except Exception as e:
      logger.debug(bstack11111l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡧࡶ࡮ࡼࡥࡳࠢ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡪࠦࡡࡵࡶࡵ࡭ࡧࡻࡴࡦ࠼ࠣࡿࢂ࠭ய").format(str(e)))
def bstack1l11l1llll_opy_(runner, name, context, bstack11llll11_opy_, *args):
    bstack11l1l1l11_opy_(runner, name, context, context.feature, bstack11llll11_opy_, *args)
    try:
      if not bstack1lll1llll_opy_:
        bstack1l11l1l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllllll11_opy_(bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩர")) else context.browser
        if is_driver_active(bstack1l11l1l111_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧற")
          bstack1l11ll1ll1_opy_ = str(runner.feature.name)
          bstack1l111111_opy_(context, bstack1l11ll1ll1_opy_)
          bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪல") + json.dumps(bstack1l11ll1ll1_opy_) + bstack11111l_opy_ (u"࠭ࡽࡾࠩள"))
    except Exception as e:
      logger.debug(bstack11111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧழ").format(str(e)))
def bstack111111111_opy_(runner, name, context, bstack11llll11_opy_, *args):
    if hasattr(context, bstack11111l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪவ")):
        bstack1ll1ll1111_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack11111l_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫஶ")) else context.feature
    bstack11l1l1l11_opy_(runner, name, context, target, bstack11llll11_opy_, *args)
@measure(event_name=EVENTS.bstack11l1ll11ll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack1ll1l1llll_opy_(runner, name, context, bstack11llll11_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1ll1ll1111_opy_.start_test(context)
    bstack11l1l1l11_opy_(runner, name, context, context.scenario, bstack11llll11_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack11lllll1_opy_.bstack1l11111111_opy_(context, *args)
    try:
      bstack1l11l1l111_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩஷ"), context.browser)
      if is_driver_active(bstack1l11l1l111_opy_):
        bstack1111lll11_opy_.bstack111lllll1_opy_(bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪஸ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11111l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢஹ")
        if (not bstack1lll1llll_opy_):
          scenario_name = args[0].name
          feature_name = bstack1l11ll1ll1_opy_ = str(runner.feature.name)
          bstack1l11ll1ll1_opy_ = feature_name + bstack11111l_opy_ (u"࠭ࠠ࠮ࠢࠪ஺") + scenario_name
          if runner.driver_initialised == bstack11111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ஻"):
            bstack1l111111_opy_(context, bstack1l11ll1ll1_opy_)
            bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠥ࠭஼") + json.dumps(bstack1l11ll1ll1_opy_) + bstack11111l_opy_ (u"ࠩࢀࢁࠬ஽"))
    except Exception as e:
      logger.debug(bstack11111l_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢ࡬ࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫா").format(str(e)))
@measure(event_name=EVENTS.bstack1l11lll1l1_opy_, stage=STAGE.bstack1l1llll11_opy_, hook_type=bstack11111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡗࡹ࡫ࡰࠣி"), bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11l1l1llll_opy_(runner, name, context, bstack11llll11_opy_, *args):
    bstack11l1l1l11_opy_(runner, name, context, args[0], bstack11llll11_opy_, *args)
    try:
      bstack1l11l1l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllllll11_opy_(bstack11111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫீ")) else context.browser
      if is_driver_active(bstack1l11l1l111_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦு")
        bstack1ll1ll1111_opy_.bstack1ll1l1ll11_opy_(args[0])
        if runner.driver_initialised == bstack11111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧூ"):
          feature_name = bstack1l11ll1ll1_opy_ = str(runner.feature.name)
          bstack1l11ll1ll1_opy_ = feature_name + bstack11111l_opy_ (u"ࠨࠢ࠰ࠤࠬ௃") + context.scenario.name
          bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ௄") + json.dumps(bstack1l11ll1ll1_opy_) + bstack11111l_opy_ (u"ࠪࢁࢂ࠭௅"))
    except Exception as e:
      logger.debug(bstack11111l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨெ").format(str(e)))
@measure(event_name=EVENTS.bstack1l11lll1l1_opy_, stage=STAGE.bstack1l1llll11_opy_, hook_type=bstack11111l_opy_ (u"ࠧࡧࡦࡵࡧࡵࡗࡹ࡫ࡰࠣே"), bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack1llll1ll1_opy_(runner, name, context, bstack11llll11_opy_, *args):
  bstack1ll1ll1111_opy_.bstack1l111llll_opy_(args[0])
  try:
    bstack1l1l1l11l1_opy_ = args[0].status.name
    bstack1l11l1l111_opy_ = threading.current_thread().bstackSessionDriver if bstack11111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬை") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l11l1l111_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11111l_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧ௉")
        feature_name = bstack1l11ll1ll1_opy_ = str(runner.feature.name)
        bstack1l11ll1ll1_opy_ = feature_name + bstack11111l_opy_ (u"ࠨࠢ࠰ࠤࠬொ") + context.scenario.name
        bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧோ") + json.dumps(bstack1l11ll1ll1_opy_) + bstack11111l_opy_ (u"ࠪࢁࢂ࠭ௌ"))
    if str(bstack1l1l1l11l1_opy_).lower() == bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧ்ࠫ"):
      bstack1lllllllll_opy_ = bstack11111l_opy_ (u"ࠬ࠭௎")
      bstack1llll1l11_opy_ = bstack11111l_opy_ (u"࠭ࠧ௏")
      bstack1ll1ll1ll1_opy_ = bstack11111l_opy_ (u"ࠧࠨௐ")
      try:
        import traceback
        bstack1lllllllll_opy_ = runner.exception.__class__.__name__
        bstack1l1111l11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1llll1l11_opy_ = bstack11111l_opy_ (u"ࠨࠢࠪ௑").join(bstack1l1111l11_opy_)
        bstack1ll1ll1ll1_opy_ = bstack1l1111l11_opy_[-1]
      except Exception as e:
        logger.debug(bstack11lllllll_opy_.format(str(e)))
      bstack1lllllllll_opy_ += bstack1ll1ll1ll1_opy_
      bstack1l1l111lll_opy_(context, json.dumps(str(args[0].name) + bstack11111l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௒") + str(bstack1llll1l11_opy_)),
                          bstack11111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ௓"))
      if runner.driver_initialised == bstack11111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ௔"):
        bstack1l1l1l111_opy_(getattr(context, bstack11111l_opy_ (u"ࠬࡶࡡࡨࡧࠪ௕"), None), bstack11111l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ௖"), bstack1lllllllll_opy_)
        bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬௗ") + json.dumps(str(args[0].name) + bstack11111l_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ௘") + str(bstack1llll1l11_opy_)) + bstack11111l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ௙"))
      if runner.driver_initialised == bstack11111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣ௚"):
        bstack111ll11l1_opy_(bstack1l11l1l111_opy_, bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௛"), bstack11111l_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ௜") + str(bstack1lllllllll_opy_))
    else:
      bstack1l1l111lll_opy_(context, bstack11111l_opy_ (u"ࠨࡐࡢࡵࡶࡩࡩࠧࠢ௝"), bstack11111l_opy_ (u"ࠢࡪࡰࡩࡳࠧ௞"))
      if runner.driver_initialised == bstack11111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ௟"):
        bstack1l1l1l111_opy_(getattr(context, bstack11111l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ௠"), None), bstack11111l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ௡"))
      bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ௢") + json.dumps(str(args[0].name) + bstack11111l_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤ௣")) + bstack11111l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ௤"))
      if runner.driver_initialised == bstack11111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧ௥"):
        bstack111ll11l1_opy_(bstack1l11l1l111_opy_, bstack11111l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣ௦"))
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡳࡵࡧࡳ࠾ࠥࢁࡽࠨ௧").format(str(e)))
  bstack11l1l1l11_opy_(runner, name, context, args[0], bstack11llll11_opy_, *args)
@measure(event_name=EVENTS.bstack1lll1lll1l_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack1l11l11l1_opy_(runner, name, context, bstack11llll11_opy_, *args):
  bstack1ll1ll1111_opy_.end_test(args[0])
  try:
    bstack11ll11ll11_opy_ = args[0].status.name
    bstack1l11l1l111_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ௨"), context.browser)
    bstack11lllll1_opy_.bstack11l11lll11_opy_(bstack1l11l1l111_opy_)
    if str(bstack11ll11ll11_opy_).lower() == bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௩"):
      bstack1lllllllll_opy_ = bstack11111l_opy_ (u"ࠬ࠭௪")
      bstack1llll1l11_opy_ = bstack11111l_opy_ (u"࠭ࠧ௫")
      bstack1ll1ll1ll1_opy_ = bstack11111l_opy_ (u"ࠧࠨ௬")
      try:
        import traceback
        bstack1lllllllll_opy_ = runner.exception.__class__.__name__
        bstack1l1111l11_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1llll1l11_opy_ = bstack11111l_opy_ (u"ࠨࠢࠪ௭").join(bstack1l1111l11_opy_)
        bstack1ll1ll1ll1_opy_ = bstack1l1111l11_opy_[-1]
      except Exception as e:
        logger.debug(bstack11lllllll_opy_.format(str(e)))
      bstack1lllllllll_opy_ += bstack1ll1ll1ll1_opy_
      bstack1l1l111lll_opy_(context, json.dumps(str(args[0].name) + bstack11111l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௮") + str(bstack1llll1l11_opy_)),
                          bstack11111l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤ௯"))
      if runner.driver_initialised == bstack11111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௰") or runner.driver_initialised == bstack11111l_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ௱"):
        bstack1l1l1l111_opy_(getattr(context, bstack11111l_opy_ (u"࠭ࡰࡢࡩࡨࠫ௲"), None), bstack11111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ௳"), bstack1lllllllll_opy_)
        bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭௴") + json.dumps(str(args[0].name) + bstack11111l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣ௵") + str(bstack1llll1l11_opy_)) + bstack11111l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪ௶"))
      if runner.driver_initialised == bstack11111l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨ௷") or runner.driver_initialised == bstack11111l_opy_ (u"ࠬ࡯࡮ࡴࡶࡨࡴࠬ௸"):
        bstack111ll11l1_opy_(bstack1l11l1l111_opy_, bstack11111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭௹"), bstack11111l_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ௺") + str(bstack1lllllllll_opy_))
    else:
      bstack1l1l111lll_opy_(context, bstack11111l_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤ௻"), bstack11111l_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ௼"))
      if runner.driver_initialised == bstack11111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ௽") or runner.driver_initialised == bstack11111l_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫ௾"):
        bstack1l1l1l111_opy_(getattr(context, bstack11111l_opy_ (u"ࠬࡶࡡࡨࡧࠪ௿"), None), bstack11111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨఀ"))
      bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬఁ") + json.dumps(str(args[0].name) + bstack11111l_opy_ (u"ࠣࠢ࠰ࠤࡕࡧࡳࡴࡧࡧࠥࠧం")) + bstack11111l_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡪࡰࡩࡳࠧࢃࡽࠨః"))
      if runner.driver_initialised == bstack11111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧఄ") or runner.driver_initialised == bstack11111l_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫఅ"):
        bstack111ll11l1_opy_(bstack1l11l1l111_opy_, bstack11111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧఆ"))
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨఇ").format(str(e)))
  bstack11l1l1l11_opy_(runner, name, context, context.scenario, bstack11llll11_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1lllll11_opy_(runner, name, context, bstack11llll11_opy_, *args):
    target = context.scenario if hasattr(context, bstack11111l_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩఈ")) else context.feature
    bstack11l1l1l11_opy_(runner, name, context, target, bstack11llll11_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack111lll1ll_opy_(runner, name, context, bstack11llll11_opy_, *args):
    try:
      bstack1l11l1l111_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧఉ"), context.browser)
      bstack11l111ll1_opy_ = bstack11111l_opy_ (u"ࠩࠪఊ")
      if context.failed is True:
        bstack1ll1lllll1_opy_ = []
        bstack11ll1111l1_opy_ = []
        bstack111lll111_opy_ = []
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1ll1lllll1_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l1111l11_opy_ = traceback.format_tb(exc_tb)
            bstack11l1l1ll_opy_ = bstack11111l_opy_ (u"ࠪࠤࠬఋ").join(bstack1l1111l11_opy_)
            bstack11ll1111l1_opy_.append(bstack11l1l1ll_opy_)
            bstack111lll111_opy_.append(bstack1l1111l11_opy_[-1])
        except Exception as e:
          logger.debug(bstack11lllllll_opy_.format(str(e)))
        bstack1lllllllll_opy_ = bstack11111l_opy_ (u"ࠫࠬఌ")
        for i in range(len(bstack1ll1lllll1_opy_)):
          bstack1lllllllll_opy_ += bstack1ll1lllll1_opy_[i] + bstack111lll111_opy_[i] + bstack11111l_opy_ (u"ࠬࡢ࡮ࠨ఍")
        bstack11l111ll1_opy_ = bstack11111l_opy_ (u"࠭ࠠࠨఎ").join(bstack11ll1111l1_opy_)
        if runner.driver_initialised in [bstack11111l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠣఏ"), bstack11111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧఐ")]:
          bstack1l1l111lll_opy_(context, bstack11l111ll1_opy_, bstack11111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ఑"))
          bstack1l1l1l111_opy_(getattr(context, bstack11111l_opy_ (u"ࠪࡴࡦ࡭ࡥࠨఒ"), None), bstack11111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦఓ"), bstack1lllllllll_opy_)
          bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪఔ") + json.dumps(bstack11l111ll1_opy_) + bstack11111l_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭క"))
          bstack111ll11l1_opy_(bstack1l11l1l111_opy_, bstack11111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢఖ"), bstack11111l_opy_ (u"ࠣࡕࡲࡱࡪࠦࡳࡤࡧࡱࡥࡷ࡯࡯ࡴࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣࡠࡳࠨగ") + str(bstack1lllllllll_opy_))
          bstack1l1111lll1_opy_ = bstack111ll1l11_opy_(bstack11l111ll1_opy_, runner.feature.name, logger)
          if (bstack1l1111lll1_opy_ != None):
            bstack1l11llll_opy_.append(bstack1l1111lll1_opy_)
      else:
        if runner.driver_initialised in [bstack11111l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥఘ"), bstack11111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢఙ")]:
          bstack1l1l111lll_opy_(context, bstack11111l_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢచ") + str(runner.feature.name) + bstack11111l_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢఛ"), bstack11111l_opy_ (u"ࠨࡩ࡯ࡨࡲࠦజ"))
          bstack1l1l1l111_opy_(getattr(context, bstack11111l_opy_ (u"ࠧࡱࡣࡪࡩࠬఝ"), None), bstack11111l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣఞ"))
          bstack1l11l1l111_opy_.execute_script(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧట") + json.dumps(bstack11111l_opy_ (u"ࠥࡊࡪࡧࡴࡶࡴࡨ࠾ࠥࠨఠ") + str(runner.feature.name) + bstack11111l_opy_ (u"ࠦࠥࡶࡡࡴࡵࡨࡨࠦࠨడ")) + bstack11111l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣࡿࢀࠫఢ"))
          bstack111ll11l1_opy_(bstack1l11l1l111_opy_, bstack11111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ణ"))
          bstack1l1111lll1_opy_ = bstack111ll1l11_opy_(bstack11l111ll1_opy_, runner.feature.name, logger)
          if (bstack1l1111lll1_opy_ != None):
            bstack1l11llll_opy_.append(bstack1l1111lll1_opy_)
    except Exception as e:
      logger.debug(bstack11111l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡶࡸࡦࡺࡵࡴࠢ࡬ࡲࠥࡧࡦࡵࡧࡵࠤ࡫࡫ࡡࡵࡷࡵࡩ࠿ࠦࡻࡾࠩత").format(str(e)))
    bstack11l1l1l11_opy_(runner, name, context, context.feature, bstack11llll11_opy_, *args)
@measure(event_name=EVENTS.bstack1l11lll1l1_opy_, stage=STAGE.bstack1l1llll11_opy_, hook_type=bstack11111l_opy_ (u"ࠣࡣࡩࡸࡪࡸࡁ࡭࡮ࠥథ"), bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack1lll1111l_opy_(runner, name, context, bstack11llll11_opy_, *args):
    bstack11l1l1l11_opy_(runner, name, context, runner, bstack11llll11_opy_, *args)
def bstack1ll1l111_opy_(self, name, context, *args):
  if bstack1ll111l11_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1111l1ll1_opy_
    bstack11ll11ll1_opy_ = CONFIG[bstack11111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬద")][platform_index]
    os.environ[bstack11111l_opy_ (u"ࠪࡇ࡚ࡘࡒࡆࡐࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡄࡂࡖࡄࠫధ")] = json.dumps(bstack11ll11ll1_opy_)
  global bstack11llll11_opy_
  if not hasattr(self, bstack11111l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡥࡥࠩన")):
    self.driver_initialised = None
  bstack1l111ll11l_opy_ = {
      bstack11111l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ఩"): bstack11lll11111_opy_,
      bstack11111l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠧప"): bstack1l11l1llll_opy_,
      bstack11111l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡵࡣࡪࠫఫ"): bstack111111111_opy_,
      bstack11111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪబ"): bstack1ll1l1llll_opy_,
      bstack11111l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠧభ"): bstack11l1l1llll_opy_,
      bstack11111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡸࡪࡶࠧమ"): bstack1llll1ll1_opy_,
      bstack11111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬయ"): bstack1l11l11l1_opy_,
      bstack11111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡹࡧࡧࠨర"): bstack1l1lllll11_opy_,
      bstack11111l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ఱ"): bstack111lll1ll_opy_,
      bstack11111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪల"): bstack1lll1111l_opy_
  }
  handler = bstack1l111ll11l_opy_.get(name, bstack11llll11_opy_)
  handler(self, name, context, bstack11llll11_opy_, *args)
  if name in [bstack11111l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨళ"), bstack11111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪఴ"), bstack11111l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡤࡰࡱ࠭వ")]:
    try:
      bstack1l11l1l111_opy_ = threading.current_thread().bstackSessionDriver if bstack1lllllll11_opy_(bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪశ")) else context.browser
      bstack11111l1l1_opy_ = (
        (name == bstack11111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨష") and self.driver_initialised == bstack11111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥస")) or
        (name == bstack11111l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧహ") and self.driver_initialised == bstack11111l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ఺")) or
        (name == bstack11111l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ఻") and self.driver_initialised in [bstack11111l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ఼ࠧ"), bstack11111l_opy_ (u"ࠦ࡮ࡴࡳࡵࡧࡳࠦఽ")]) or
        (name == bstack11111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩా") and self.driver_initialised == bstack11111l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦి"))
      )
      if bstack11111l1l1_opy_:
        self.driver_initialised = None
        bstack1l11l1l111_opy_.quit()
    except Exception:
      pass
def bstack11l11ll11_opy_(config, startdir):
  return bstack11111l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࠳ࢁࠧీ").format(bstack11111l_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢు"))
notset = Notset()
def bstack1l1l1llll1_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll111111_opy_
  if str(name).lower() == bstack11111l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࠩూ"):
    return bstack11111l_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤృ")
  else:
    return bstack1ll111111_opy_(self, name, default, skip)
def bstack1lll1l11ll_opy_(item, when):
  global bstack1lll1111ll_opy_
  try:
    bstack1lll1111ll_opy_(item, when)
  except Exception as e:
    pass
def bstack1111ll11l_opy_():
  return
def bstack11l1llll_opy_(type, name, status, reason, bstack1ll11ll111_opy_, bstack1l1ll11ll1_opy_):
  bstack1ll1l11l11_opy_ = {
    bstack11111l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫౄ"): type,
    bstack11111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ౅"): {}
  }
  if type == bstack11111l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨె"):
    bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪే")][bstack11111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧై")] = bstack1ll11ll111_opy_
    bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ౉")][bstack11111l_opy_ (u"ࠪࡨࡦࡺࡡࠨొ")] = json.dumps(str(bstack1l1ll11ll1_opy_))
  if type == bstack11111l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬో"):
    bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨౌ")][bstack11111l_opy_ (u"࠭࡮ࡢ࡯ࡨ్ࠫ")] = name
  if type == bstack11111l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ౎"):
    bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ౏")][bstack11111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ౐")] = status
    if status == bstack11111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౑"):
      bstack1ll1l11l11_opy_[bstack11111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ౒")][bstack11111l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬ౓")] = json.dumps(str(reason))
  bstack11l1ll1lll_opy_ = bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫ౔").format(json.dumps(bstack1ll1l11l11_opy_))
  return bstack11l1ll1lll_opy_
def bstack1ll1l111l_opy_(driver_command, response):
    if driver_command == bstack11111l_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷౕࠫ"):
        bstack1111lll11_opy_.bstack1ll1ll11_opy_({
            bstack11111l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ౖࠧ"): response[bstack11111l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ౗")],
            bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪౘ"): bstack1111lll11_opy_.current_test_uuid()
        })
def bstack1l111lllll_opy_(item, call, rep):
  global bstack1l1ll1ll1_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1lll1llll_opy_
  name = bstack11111l_opy_ (u"ࠫࠬౙ")
  try:
    if rep.when == bstack11111l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪౚ"):
      bstack11llll1l1_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1lll1llll_opy_:
          name = str(rep.nodeid)
          bstack111ll1l1l_opy_ = bstack11l1llll_opy_(bstack11111l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ౛"), name, bstack11111l_opy_ (u"ࠧࠨ౜"), bstack11111l_opy_ (u"ࠨࠩౝ"), bstack11111l_opy_ (u"ࠩࠪ౞"), bstack11111l_opy_ (u"ࠪࠫ౟"))
          threading.current_thread().bstack11l1l11111_opy_ = name
          for driver in bstack1lll1l1l1l_opy_:
            if bstack11llll1l1_opy_ == driver.session_id:
              driver.execute_script(bstack111ll1l1l_opy_)
      except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫౠ").format(str(e)))
      try:
        bstack1lllll1l1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11111l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ౡ"):
          status = bstack11111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ౢ") if rep.outcome.lower() == bstack11111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧౣ") else bstack11111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౤")
          reason = bstack11111l_opy_ (u"ࠩࠪ౥")
          if status == bstack11111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ౦"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11111l_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ౧") if status == bstack11111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ౨") else bstack11111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ౩")
          data = name + bstack11111l_opy_ (u"ࠧࠡࡲࡤࡷࡸ࡫ࡤࠢࠩ౪") if status == bstack11111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౫") else name + bstack11111l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠤࠤࠬ౬") + reason
          bstack1l1l1l1lll_opy_ = bstack11l1llll_opy_(bstack11111l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬ౭"), bstack11111l_opy_ (u"ࠫࠬ౮"), bstack11111l_opy_ (u"ࠬ࠭౯"), bstack11111l_opy_ (u"࠭ࠧ౰"), level, data)
          for driver in bstack1lll1l1l1l_opy_:
            if bstack11llll1l1_opy_ == driver.session_id:
              driver.execute_script(bstack1l1l1l1lll_opy_)
      except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡨࡵ࡮ࡵࡧࡻࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡳࡦࡵࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠫ౱").format(str(e)))
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡸࡺࡡࡵࡧࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾࢁࠬ౲").format(str(e)))
  bstack1l1ll1ll1_opy_(item, call, rep)
def bstack1lll1l1ll_opy_(driver, bstack11llll1l11_opy_, test=None):
  global bstack11ll111l_opy_
  if test != None:
    bstack1l1l11llll_opy_ = getattr(test, bstack11111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ౳"), None)
    bstack1lll11ll_opy_ = getattr(test, bstack11111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ౴"), None)
    PercySDK.screenshot(driver, bstack11llll1l11_opy_, bstack1l1l11llll_opy_=bstack1l1l11llll_opy_, bstack1lll11ll_opy_=bstack1lll11ll_opy_, bstack1ll111l1l1_opy_=bstack11ll111l_opy_)
  else:
    PercySDK.screenshot(driver, bstack11llll1l11_opy_)
@measure(event_name=EVENTS.bstack1l111ll1_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11l11l1l_opy_(driver):
  if bstack11ll11l1_opy_.bstack1ll1111l1l_opy_() is True or bstack11ll11l1_opy_.capturing() is True:
    return
  bstack11ll11l1_opy_.bstack1l1llll111_opy_()
  while not bstack11ll11l1_opy_.bstack1ll1111l1l_opy_():
    bstack1ll11111l_opy_ = bstack11ll11l1_opy_.bstack1ll1ll1l1l_opy_()
    bstack1lll1l1ll_opy_(driver, bstack1ll11111l_opy_)
  bstack11ll11l1_opy_.bstack111ll11l_opy_()
def bstack111l1l111_opy_(sequence, driver_command, response = None, bstack11ll1lll1l_opy_ = None, args = None):
    try:
      if sequence != bstack11111l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫ౵"):
        return
      if percy.bstack111l1ll1l_opy_() == bstack11111l_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦ౶"):
        return
      bstack1ll11111l_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ౷"), None)
      for command in bstack11l1lllll_opy_:
        if command == driver_command:
          for driver in bstack1lll1l1l1l_opy_:
            bstack11l11l1l_opy_(driver)
      bstack1lll11l11_opy_ = percy.bstack11llll1ll_opy_()
      if driver_command in bstack1ll111l11l_opy_[bstack1lll11l11_opy_]:
        bstack11ll11l1_opy_.bstack1l1111ll1_opy_(bstack1ll11111l_opy_, driver_command)
    except Exception as e:
      pass
def bstack11l11l11l_opy_(framework_name):
  if bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ౸")):
      return
  bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬ౹"), True)
  global bstack1lll11l11l_opy_
  global bstack1l1lllll1_opy_
  global bstack1l1lllll1l_opy_
  bstack1lll11l11l_opy_ = framework_name
  logger.info(bstack11lll1lll_opy_.format(bstack1lll11l11l_opy_.split(bstack11111l_opy_ (u"ࠩ࠰ࠫ౺"))[0]))
  bstack1lll111l_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll111l11_opy_:
      Service.start = bstack1ll11lllll_opy_
      Service.stop = bstack1llllll11l_opy_
      webdriver.Remote.get = bstack11llll111_opy_
      WebDriver.close = bstack111l1l11l_opy_
      WebDriver.quit = bstack1l1ll1111l_opy_
      webdriver.Remote.__init__ = bstack11ll1llll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1ll111l11_opy_:
        webdriver.Remote.__init__ = bstack111l111l_opy_
    WebDriver.execute = bstack1lll11l111_opy_
    bstack1l1lllll1_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1ll111l11_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1lll11lll1_opy_
  except Exception as e:
    pass
  bstack1l1111111_opy_()
  if not bstack1l1lllll1_opy_:
    bstack11l1l1l1_opy_(bstack11111l_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧ౻"), bstack111ll1ll_opy_)
  if bstack11l1lll1l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._1ll1111l_opy_ = bstack1ll11l1ll_opy_
    except Exception as e:
      logger.error(bstack1lll1llll1_opy_.format(str(e)))
  if bstack11l1l11ll_opy_():
    bstack1l1111l1ll_opy_(CONFIG, logger)
  if (bstack11111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ౼") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack111l1ll1l_opy_() == bstack11111l_opy_ (u"ࠧࡺࡲࡶࡧࠥ౽"):
          bstack11111ll1l_opy_(bstack111l1l111_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l1ll111l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l1l1ll11_opy_
      except Exception as e:
        logger.warn(bstack1111l1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack1l111l1l_opy_
      except Exception as e:
        logger.debug(bstack11l11lllll_opy_ + str(e))
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1111l1ll_opy_)
    Output.start_test = bstack1lll11lll_opy_
    Output.end_test = bstack1llll11l1_opy_
    TestStatus.__init__ = bstack11ll1l11ll_opy_
    QueueItem.__init__ = bstack11ll1l11l1_opy_
    pabot._create_items = bstack11llllll11_opy_
    try:
      from pabot import __version__ as bstack1ll1lllll_opy_
      if version.parse(bstack1ll1lllll_opy_) >= version.parse(bstack11111l_opy_ (u"࠭࠴࠯࠴࠱࠴ࠬ౾")):
        pabot._run = bstack1lll1l11l_opy_
      elif version.parse(bstack1ll1lllll_opy_) >= version.parse(bstack11111l_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧ౿")):
        pabot._run = bstack11lllll1l1_opy_
      elif version.parse(bstack1ll1lllll_opy_) >= version.parse(bstack11111l_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨಀ")):
        pabot._run = bstack11l111l1l_opy_
      else:
        pabot._run = bstack1l1l1lll_opy_
    except Exception as e:
      pabot._run = bstack1l1l1lll_opy_
    pabot._create_command_for_execution = bstack1llll11ll_opy_
    pabot._report_results = bstack1l1l1l11ll_opy_
  if bstack11111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩಁ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1llllll1l1_opy_)
    Runner.run_hook = bstack1ll1l111_opy_
    Step.run = bstack1ll1ll11l1_opy_
  if bstack11111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪಂ") in str(framework_name).lower():
    if not bstack1ll111l11_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l11ll11_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1111ll11l_opy_
      Config.getoption = bstack1l1l1llll1_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1l111lllll_opy_
    except Exception as e:
      pass
def bstack11l11111_opy_():
  global CONFIG
  if bstack11111l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫಃ") in CONFIG and int(CONFIG[bstack11111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ಄")]) > 1:
    logger.warn(bstack11ll1l111_opy_)
def bstack1l1l11ll1l_opy_(arg, bstack11llll11ll_opy_, bstack1ll111ll_opy_=None):
  global CONFIG
  global bstack1l1l111ll_opy_
  global bstack1lllll1ll_opy_
  global bstack1ll111l11_opy_
  global bstack1l11l11ll1_opy_
  bstack111l11ll_opy_ = bstack11111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ಅ")
  if bstack11llll11ll_opy_ and isinstance(bstack11llll11ll_opy_, str):
    bstack11llll11ll_opy_ = eval(bstack11llll11ll_opy_)
  CONFIG = bstack11llll11ll_opy_[bstack11111l_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧಆ")]
  bstack1l1l111ll_opy_ = bstack11llll11ll_opy_[bstack11111l_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩಇ")]
  bstack1lllll1ll_opy_ = bstack11llll11ll_opy_[bstack11111l_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫಈ")]
  bstack1ll111l11_opy_ = bstack11llll11ll_opy_[bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ಉ")]
  bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬಊ"), bstack1ll111l11_opy_)
  os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧಋ")] = bstack111l11ll_opy_
  os.environ[bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬಌ")] = json.dumps(CONFIG)
  os.environ[bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ಍")] = bstack1l1l111ll_opy_
  os.environ[bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩಎ")] = str(bstack1lllll1ll_opy_)
  os.environ[bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨಏ")] = str(True)
  if bstack1lll111ll1_opy_(arg, [bstack11111l_opy_ (u"ࠪ࠱ࡳ࠭ಐ"), bstack11111l_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ಑")]) != -1:
    os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ಒ")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1lll1ll1l_opy_)
    return
  bstack1ll11l1l_opy_()
  global bstack1l11l1l11_opy_
  global bstack11ll111l_opy_
  global bstack11l1lll1ll_opy_
  global bstack1l1l1l111l_opy_
  global bstack1l1lll111_opy_
  global bstack1l1lllll1l_opy_
  global bstack1l11ll111l_opy_
  arg.append(bstack11111l_opy_ (u"ࠨ࠭ࡘࠤಓ"))
  arg.append(bstack11111l_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡎࡱࡧࡹࡱ࡫ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡰࡴࡴࡸࡴࡦࡦ࠽ࡴࡾࡺࡥࡴࡶ࠱ࡔࡾࡺࡥࡴࡶ࡚ࡥࡷࡴࡩ࡯ࡩࠥಔ"))
  arg.append(bstack11111l_opy_ (u"ࠣ࠯࡚ࠦಕ"))
  arg.append(bstack11111l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡗ࡬ࡪࠦࡨࡰࡱ࡮࡭ࡲࡶ࡬ࠣಖ"))
  global bstack1l11l111l_opy_
  global bstack1ll1111111_opy_
  global bstack1l11ll1l1_opy_
  global bstack1ll1lll1l1_opy_
  global bstack1l1ll11l1_opy_
  global bstack11lll1ll11_opy_
  global bstack1l111l1l11_opy_
  global bstack1l1l111l1_opy_
  global bstack11ll11ll_opy_
  global bstack1l1l1111_opy_
  global bstack1ll111111_opy_
  global bstack1lll1111ll_opy_
  global bstack1l1ll1ll1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11l111l_opy_ = webdriver.Remote.__init__
    bstack1ll1111111_opy_ = WebDriver.quit
    bstack1l1l111l1_opy_ = WebDriver.close
    bstack11ll11ll_opy_ = WebDriver.get
    bstack1l11ll1l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1ll11ll11_opy_(CONFIG) and bstack11l11l111_opy_():
    if bstack1lllll11l1_opy_() < version.parse(bstack1l1llllll_opy_):
      logger.error(bstack1l1l11l11l_opy_.format(bstack1lllll11l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l1111_opy_ = RemoteConnection._1ll1111l_opy_
      except Exception as e:
        logger.error(bstack1lll1llll1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll111111_opy_ = Config.getoption
    from _pytest import runner
    bstack1lll1111ll_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11l1l1l1l1_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l1ll1ll1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11111l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫಗ"))
  bstack11l1lll1ll_opy_ = CONFIG.get(bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨಘ"), {}).get(bstack11111l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಙ"))
  bstack1l11ll111l_opy_ = True
  if cli.is_enabled(CONFIG):
    if cli.bstack1111llll1_opy_():
      bstack1111l1l1_opy_.invoke(bstack1l1ll1llll_opy_.CONNECT, bstack1ll11lll11_opy_())
    platform_index = int(os.environ.get(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ಚ"), bstack11111l_opy_ (u"ࠧ࠱ࠩಛ")))
  else:
    bstack11l11l11l_opy_(bstack1l111l1l1l_opy_)
  os.environ[bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩಜ")] = CONFIG[bstack11111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫಝ")]
  os.environ[bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭ಞ")] = CONFIG[bstack11111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧಟ")]
  os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨಠ")] = bstack1ll111l11_opy_.__str__()
  from _pytest.config import main as bstack11ll1lll1_opy_
  bstack111ll1l1_opy_ = []
  try:
    bstack1l1l1l1ll_opy_ = bstack11ll1lll1_opy_(arg)
    if cli.is_enabled(CONFIG):
      cli.bstack1111lllll_opy_()
    if bstack11111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪಡ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1l1ll11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack111ll1l1_opy_.append(bstack1l1l1ll11l_opy_)
    try:
      bstack111lll1l1_opy_ = (bstack111ll1l1_opy_, int(bstack1l1l1l1ll_opy_))
      bstack1ll111ll_opy_.append(bstack111lll1l1_opy_)
    except:
      bstack1ll111ll_opy_.append((bstack111ll1l1_opy_, bstack1l1l1l1ll_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack111ll1l1_opy_.append({bstack11111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಢ"): bstack11111l_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪಣ") + os.environ.get(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩತ")), bstack11111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩಥ"): traceback.format_exc(), bstack11111l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪದ"): int(os.environ.get(bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬಧ")))})
    bstack1ll111ll_opy_.append((bstack111ll1l1_opy_, 1))
def bstack1l11l11l1l_opy_(arg):
  global bstack1lll1111l1_opy_
  bstack11l11l11l_opy_(bstack1l1l1ll1l1_opy_)
  os.environ[bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧನ")] = str(bstack1lllll1ll_opy_)
  from behave.__main__ import main as bstack1llll111ll_opy_
  status_code = bstack1llll111ll_opy_(arg)
  if status_code != 0:
    bstack1lll1111l1_opy_ = status_code
def bstack11ll1ll111_opy_():
  logger.info(bstack111ll1111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭಩"), help=bstack11111l_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩಪ"))
  parser.add_argument(bstack11111l_opy_ (u"ࠩ࠰ࡹࠬಫ"), bstack11111l_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧಬ"), help=bstack11111l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪಭ"))
  parser.add_argument(bstack11111l_opy_ (u"ࠬ࠳࡫ࠨಮ"), bstack11111l_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬಯ"), help=bstack11111l_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨರ"))
  parser.add_argument(bstack11111l_opy_ (u"ࠨ࠯ࡩࠫಱ"), bstack11111l_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧಲ"), help=bstack11111l_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩಳ"))
  bstack11lll11lll_opy_ = parser.parse_args()
  try:
    bstack1lllll111l_opy_ = bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨ಴")
    if bstack11lll11lll_opy_.framework and bstack11lll11lll_opy_.framework not in (bstack11111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬವ"), bstack11111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧಶ")):
      bstack1lllll111l_opy_ = bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ಷ")
    bstack1llll11lll_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lllll111l_opy_)
    bstack11l111l1_opy_ = open(bstack1llll11lll_opy_, bstack11111l_opy_ (u"ࠨࡴࠪಸ"))
    bstack11ll1l1l1_opy_ = bstack11l111l1_opy_.read()
    bstack11l111l1_opy_.close()
    if bstack11lll11lll_opy_.username:
      bstack11ll1l1l1_opy_ = bstack11ll1l1l1_opy_.replace(bstack11111l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩಹ"), bstack11lll11lll_opy_.username)
    if bstack11lll11lll_opy_.key:
      bstack11ll1l1l1_opy_ = bstack11ll1l1l1_opy_.replace(bstack11111l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬ಺"), bstack11lll11lll_opy_.key)
    if bstack11lll11lll_opy_.framework:
      bstack11ll1l1l1_opy_ = bstack11ll1l1l1_opy_.replace(bstack11111l_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬ಻"), bstack11lll11lll_opy_.framework)
    file_name = bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ಼")
    file_path = os.path.abspath(file_name)
    bstack1111l1l1l_opy_ = open(file_path, bstack11111l_opy_ (u"࠭ࡷࠨಽ"))
    bstack1111l1l1l_opy_.write(bstack11ll1l1l1_opy_)
    bstack1111l1l1l_opy_.close()
    logger.info(bstack1lll1lllll_opy_)
    try:
      os.environ[bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩಾ")] = bstack11lll11lll_opy_.framework if bstack11lll11lll_opy_.framework != None else bstack11111l_opy_ (u"ࠣࠤಿ")
      config = yaml.safe_load(bstack11ll1l1l1_opy_)
      config[bstack11111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩೀ")] = bstack11111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩು")
      bstack11lll1l11l_opy_(bstack1l11lll11l_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1llll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack111ll1lll_opy_.format(str(e)))
def bstack11lll1l11l_opy_(bstack1111111l_opy_, config, bstack1ll11lll1_opy_={}):
  global bstack1ll111l11_opy_
  global bstack1llll11ll1_opy_
  global bstack1l11l11ll1_opy_
  if not config:
    return
  bstack11l1ll1111_opy_ = bstack1llll1ll1l_opy_ if not bstack1ll111l11_opy_ else (
    bstack1l1ll1l1ll_opy_ if bstack11111l_opy_ (u"ࠫࡦࡶࡰࠨೂ") in config else (
        bstack1l1ll111l_opy_ if config.get(bstack11111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩೃ")) else bstack1l1l1l1l1l_opy_
    )
)
  bstack1111111ll_opy_ = False
  bstack1111l1lll_opy_ = False
  if bstack1ll111l11_opy_ is True:
      if bstack11111l_opy_ (u"࠭ࡡࡱࡲࠪೄ") in config:
          bstack1111111ll_opy_ = True
      else:
          bstack1111l1lll_opy_ = True
  bstack1llll111l_opy_ = bstack11l11lll1l_opy_.bstack1l1llll1l_opy_(config, bstack1llll11ll1_opy_)
  bstack1l11l1ll1l_opy_ = bstack1ll111lll_opy_()
  data = {
    bstack11111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ೅"): config[bstack11111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪೆ")],
    bstack11111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬೇ"): config[bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ೈ")],
    bstack11111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ೉"): bstack1111111l_opy_,
    bstack11111l_opy_ (u"ࠬࡪࡥࡵࡧࡦࡸࡪࡪࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩೊ"): os.environ.get(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨೋ"), bstack1llll11ll1_opy_),
    bstack11111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩೌ"): bstack111l1111_opy_,
    bstack11111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮್ࠪ"): bstack11111llll_opy_(),
    bstack11111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ೎"): {
      bstack11111l_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ೏"): str(config[bstack11111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ೐")]) if bstack11111l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ೑") in config else bstack11111l_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ೒"),
      bstack11111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࡘࡨࡶࡸ࡯࡯࡯ࠩ೓"): sys.version,
      bstack11111l_opy_ (u"ࠨࡴࡨࡪࡪࡸࡲࡦࡴࠪ೔"): bstack111111lll_opy_(os.environ.get(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫೕ"), bstack1llll11ll1_opy_)),
      bstack11111l_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬೖ"): bstack11111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ೗"),
      bstack11111l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭೘"): bstack11l1ll1111_opy_,
      bstack11111l_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ೙"): bstack1llll111l_opy_,
      bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩ࠭೚"): os.environ[bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭೛")],
      bstack11111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ೜"): os.environ.get(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬೝ"), bstack1llll11ll1_opy_),
      bstack11111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧೞ"): bstack1llll1l1_opy_(os.environ.get(bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ೟"), bstack1llll11ll1_opy_)),
      bstack11111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬೠ"): bstack1l11l1ll1l_opy_.get(bstack11111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬೡ")),
      bstack11111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧೢ"): bstack1l11l1ll1l_opy_.get(bstack11111l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪೣ")),
      bstack11111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭೤"): config[bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೥")] if config[bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ೦")] else bstack11111l_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢ೧"),
      bstack11111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ೨"): str(config[bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೩")]) if bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೪") in config else bstack11111l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦ೫"),
      bstack11111l_opy_ (u"ࠫࡴࡹࠧ೬"): sys.platform,
      bstack11111l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧ೭"): socket.gethostname(),
      bstack11111l_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨ೮"): bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩ೯"))
    }
  }
  if not bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨ೰")) is None:
    data[bstack11111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬೱ")][bstack11111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡒ࡫ࡴࡢࡦࡤࡸࡦ࠭ೲ")] = {
      bstack11111l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫೳ"): bstack11111l_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪ೴"),
      bstack11111l_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭೵"): bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧ೶")),
      bstack11111l_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࡏࡷࡰࡦࡪࡸࠧ೷"): bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬ೸"))
    }
  if bstack1111111l_opy_ == bstack1l11llll11_opy_:
    data[bstack11111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭೹")][bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡆࡳࡳ࡬ࡩࡨࠩ೺")] = bstack1lll1l111l_opy_(config)
    data[bstack11111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ೻")][bstack11111l_opy_ (u"࠭ࡩࡴࡒࡨࡶࡨࡿࡁࡶࡶࡲࡉࡳࡧࡢ࡭ࡧࡧࠫ೼")] = percy.bstack1ll111llll_opy_
    data[bstack11111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪ೽")][bstack11111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡂࡶ࡫࡯ࡨࡎࡪࠧ೾")] = percy.percy_build_id
  update(data[bstack11111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬ೿")], bstack1ll11lll1_opy_)
  try:
    response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨഀ"), bstack11ll11l1l1_opy_(bstack111lll1l_opy_), data, {
      bstack11111l_opy_ (u"ࠫࡦࡻࡴࡩࠩഁ"): (config[bstack11111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧം")], config[bstack11111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩഃ")])
    })
    if response:
      logger.debug(bstack11l11lll1_opy_.format(bstack1111111l_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack11l1lll1l1_opy_.format(str(e)))
def bstack111111lll_opy_(framework):
  return bstack11111l_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦഄ").format(str(framework), __version__) if framework else bstack11111l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤഅ").format(
    __version__)
def bstack1ll11l1l_opy_():
  global CONFIG
  global bstack111l1l1ll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1lll11111l_opy_()
    logger.debug(bstack1lllll1ll1_opy_.format(str(CONFIG)))
    bstack111l1l1ll_opy_ = bstack11ll1ll1l1_opy_.bstack1l1ll1l11l_opy_(CONFIG, bstack111l1l1ll_opy_)
    bstack1lll111l_opy_()
  except Exception as e:
    logger.error(bstack11111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨആ") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1ll1l1lll_opy_
  atexit.register(bstack1l11l1111l_opy_)
  signal.signal(signal.SIGINT, bstack11ll1l1l11_opy_)
  signal.signal(signal.SIGTERM, bstack11ll1l1l11_opy_)
def bstack1ll1l1lll_opy_(exctype, value, traceback):
  global bstack1lll1l1l1l_opy_
  try:
    for driver in bstack1lll1l1l1l_opy_:
      bstack111ll11l1_opy_(driver, bstack11111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪഇ"), bstack11111l_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢഈ") + str(value))
  except Exception:
    pass
  logger.info(bstack11ll1ll11_opy_)
  bstack11lll1llll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack11lll1llll_opy_(message=bstack11111l_opy_ (u"ࠬ࠭ഉ"), bstack11111111l_opy_ = False):
  global CONFIG
  bstack1l11ll11l1_opy_ = bstack11111l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨഊ") if bstack11111111l_opy_ else bstack11111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ഋ")
  try:
    if message:
      bstack1ll11lll1_opy_ = {
        bstack1l11ll11l1_opy_ : str(message)
      }
      bstack11lll1l11l_opy_(bstack1l11llll11_opy_, CONFIG, bstack1ll11lll1_opy_)
    else:
      bstack11lll1l11l_opy_(bstack1l11llll11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll1111ll1_opy_.format(str(e)))
def bstack1ll1l1l11_opy_(bstack11lllll1ll_opy_, size):
  bstack1ll111111l_opy_ = []
  while len(bstack11lllll1ll_opy_) > size:
    bstack1ll1l1l1l_opy_ = bstack11lllll1ll_opy_[:size]
    bstack1ll111111l_opy_.append(bstack1ll1l1l1l_opy_)
    bstack11lllll1ll_opy_ = bstack11lllll1ll_opy_[size:]
  bstack1ll111111l_opy_.append(bstack11lllll1ll_opy_)
  return bstack1ll111111l_opy_
def bstack1llllllll_opy_(args):
  if bstack11111l_opy_ (u"ࠨ࠯ࡰࠫഌ") in args and bstack11111l_opy_ (u"ࠩࡳࡨࡧ࠭഍") in args:
    return True
  return False
@measure(event_name=EVENTS.bstack1ll1l11l_opy_, stage=STAGE.bstack1ll111l1_opy_)
def run_on_browserstack(bstack11l1ll11_opy_=None, bstack1ll111ll_opy_=None, bstack1l11l11l11_opy_=False):
  global CONFIG
  global bstack1l1l111ll_opy_
  global bstack1lllll1ll_opy_
  global bstack1llll11ll1_opy_
  global bstack1l11l11ll1_opy_
  bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠪࠫഎ")
  bstack111111ll_opy_(bstack1lll11ll1_opy_, logger)
  if bstack11l1ll11_opy_ and isinstance(bstack11l1ll11_opy_, str):
    bstack11l1ll11_opy_ = eval(bstack11l1ll11_opy_)
  if bstack11l1ll11_opy_:
    CONFIG = bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫഏ")]
    bstack1l1l111ll_opy_ = bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭ഐ")]
    bstack1lllll1ll_opy_ = bstack11l1ll11_opy_[bstack11111l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ഑")]
    bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩഒ"), bstack1lllll1ll_opy_)
    bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨഓ")
  bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫഔ"), uuid4().__str__())
  logger.info(bstack11111l_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨക") + bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ഖ")));
  logger.debug(bstack11111l_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪ࠽ࠨഗ") + bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨഘ")))
  if not bstack1l11l11l11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1lll1ll1l_opy_)
      return
    if sys.argv[1] == bstack11111l_opy_ (u"ࠧ࠮࠯ࡹࡩࡷࡹࡩࡰࡰࠪങ") or sys.argv[1] == bstack11111l_opy_ (u"ࠨ࠯ࡹࠫച"):
      logger.info(bstack11111l_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡕࡇࡏࠥࡼࡻࡾࠩഛ").format(__version__))
      return
    if sys.argv[1] == bstack11111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩജ"):
      bstack11ll1ll111_opy_()
      return
  args = sys.argv
  bstack1ll11l1l_opy_()
  global bstack1l11l1l11_opy_
  global bstack1111l1ll1_opy_
  global bstack1l11ll111l_opy_
  global bstack11111111_opy_
  global bstack11ll111l_opy_
  global bstack11l1lll1ll_opy_
  global bstack1l1l1l111l_opy_
  global bstack1lllll1lll_opy_
  global bstack1l1lll111_opy_
  global bstack1l1lllll1l_opy_
  global bstack111l1l1l_opy_
  bstack1111l1ll1_opy_ = len(CONFIG.get(bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഝ"), []))
  if not bstack111l11ll_opy_:
    if args[1] == bstack11111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬഞ") or args[1] == bstack11111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧട"):
      bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧഠ")
      args = args[2:]
    elif args[1] == bstack11111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧഡ"):
      bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨഢ")
      args = args[2:]
    elif args[1] == bstack11111l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩണ"):
      bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪത")
      args = args[2:]
    elif args[1] == bstack11111l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ഥ"):
      bstack111l11ll_opy_ = bstack11111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧദ")
      args = args[2:]
    elif args[1] == bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧധ"):
      bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨന")
      args = args[2:]
    elif args[1] == bstack11111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩഩ"):
      bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪപ")
      args = args[2:]
    else:
      if not bstack11111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഫ") in CONFIG or str(CONFIG[bstack11111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨബ")]).lower() in [bstack11111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ഭ"), bstack11111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠳ࠨമ")]:
        bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨയ")
        args = args[1:]
      elif str(CONFIG[bstack11111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬര")]).lower() == bstack11111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩറ"):
        bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪല")
        args = args[1:]
      elif str(CONFIG[bstack11111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨള")]).lower() == bstack11111l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬഴ"):
        bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭വ")
        args = args[1:]
      elif str(CONFIG[bstack11111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫശ")]).lower() == bstack11111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩഷ"):
        bstack111l11ll_opy_ = bstack11111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪസ")
        args = args[1:]
      elif str(CONFIG[bstack11111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഹ")]).lower() == bstack11111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬഺ"):
        bstack111l11ll_opy_ = bstack11111l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ഻࠭")
        args = args[1:]
      else:
        os.environ[bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌ഼ࠩ")] = bstack111l11ll_opy_
        bstack1l1llll11l_opy_(bstack1l1111lll_opy_)
  os.environ[bstack11111l_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩഽ")] = bstack111l11ll_opy_
  bstack1llll11ll1_opy_ = bstack111l11ll_opy_
  if cli.is_enabled(CONFIG):
    try:
      bstack1ll1l1l111_opy_ = bstack1lll111l11_opy_[bstack11111l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕ࠯ࡅࡈࡉ࠭ാ")] if bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪി") and bstack11lll111ll_opy_() else bstack111l11ll_opy_
      bstack1111l1l1_opy_.invoke(bstack1l1ll1llll_opy_.bstack11ll111111_opy_, bstack11l111lll_opy_(
        sdk_version=__version__,
        path_config=bstack111l1l11_opy_(),
        path_project=os.getcwd(),
        test_framework=bstack1ll1l1l111_opy_,
        frameworks=[bstack1ll1l1l111_opy_],
        framework_versions={
          bstack1ll1l1l111_opy_: bstack1llll1l1_opy_(bstack11111l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪീ") if bstack111l11ll_opy_ in [bstack11111l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫു"), bstack11111l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬൂ"), bstack11111l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨൃ")] else bstack111l11ll_opy_)
        },
        bs_config=CONFIG
      ))
      if cli.config.get(bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠥൄ"), None):
        CONFIG[bstack11111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠦ൅")] = cli.config.get(bstack11111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠧെ"), None)
    except Exception as e:
      bstack1111l1l1_opy_.invoke(bstack1l1ll1llll_opy_.bstack1llll1lll1_opy_, e.__traceback__, 1)
    if bstack1lllll1ll_opy_:
      CONFIG[bstack11111l_opy_ (u"ࠦࡦࡶࡰࠣേ")] = cli.config[bstack11111l_opy_ (u"ࠧࡧࡰࡱࠤൈ")]
      logger.info(bstack11l11ll1_opy_.format(CONFIG[bstack11111l_opy_ (u"࠭ࡡࡱࡲࠪ൉")]))
  else:
    bstack1111l1l1_opy_.clear()
  global bstack1l1ll1l111_opy_
  global bstack11l1ll1l1l_opy_
  if bstack11l1ll11_opy_:
    try:
      bstack1l1l1l1l_opy_ = datetime.datetime.now()
      os.environ[bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩൊ")] = bstack111l11ll_opy_
      bstack11lll1l11l_opy_(bstack1l1ll1lll1_opy_, CONFIG)
      cli.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠣࡪࡷࡸࡵࡀࡳࡥ࡭ࡢࡸࡪࡹࡴࡠࡣࡷࡸࡪࡳࡰࡵࡧࡧࠦോ"), datetime.datetime.now() - bstack1l1l1l1l_opy_)
    except Exception as e:
      logger.debug(bstack1l11l1l1l1_opy_.format(str(e)))
  global bstack1l11l111l_opy_
  global bstack1ll1111111_opy_
  global bstack1l11ll11_opy_
  global bstack1ll11l11l1_opy_
  global bstack11l1l111l_opy_
  global bstack1ll111ll1_opy_
  global bstack1ll1lll1l1_opy_
  global bstack1l1ll11l1_opy_
  global bstack1ll111ll1l_opy_
  global bstack11lll1ll11_opy_
  global bstack1l111l1l11_opy_
  global bstack1l1l111l1_opy_
  global bstack11llll11_opy_
  global bstack11l1lll1_opy_
  global bstack11ll11ll_opy_
  global bstack1l1l1111_opy_
  global bstack1ll111111_opy_
  global bstack1lll1111ll_opy_
  global bstack11l1llllll_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1l11ll1l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1l11l111l_opy_ = webdriver.Remote.__init__
    bstack1ll1111111_opy_ = WebDriver.quit
    bstack1l1l111l1_opy_ = WebDriver.close
    bstack11ll11ll_opy_ = WebDriver.get
    bstack1l11ll1l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1l1ll1l111_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11l1ll1ll1_opy_
    bstack11l1ll1l1l_opy_ = bstack11l1ll1ll1_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1l1lll1_opy_
    from QWeb.keywords import browser
    bstack1l1l1lll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1ll11ll11_opy_(CONFIG) and bstack11l11l111_opy_():
    if bstack1lllll11l1_opy_() < version.parse(bstack1l1llllll_opy_):
      logger.error(bstack1l1l11l11l_opy_.format(bstack1lllll11l1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l1111_opy_ = RemoteConnection._1ll1111l_opy_
      except Exception as e:
        logger.error(bstack1lll1llll1_opy_.format(str(e)))
  if not CONFIG.get(bstack11111l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫൌ"), False) and not bstack11l1ll11_opy_:
    logger.info(bstack11l11ll1l_opy_)
  if not cli.is_enabled(CONFIG):
    if bstack11111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫്ࠧ") in CONFIG and str(CONFIG[bstack11111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨൎ")]).lower() != bstack11111l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ൏"):
      bstack1ll11ll1l_opy_()
    elif bstack111l11ll_opy_ != bstack11111l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൐") or (bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ൑") and not bstack11l1ll11_opy_):
      bstack1l1l11ll_opy_()
  if (bstack111l11ll_opy_ in [bstack11111l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ൒"), bstack11111l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൓"), bstack11111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫൔ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l1ll111l_opy_
        bstack1ll111ll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1111l1ll_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11l1l111l_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack11l11lllll_opy_ + str(e))
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1111l1ll_opy_)
    if bstack111l11ll_opy_ != bstack11111l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬൕ"):
      bstack1ll1llllll_opy_()
    bstack1l11ll11_opy_ = Output.start_test
    bstack1ll11l11l1_opy_ = Output.end_test
    bstack1ll1lll1l1_opy_ = TestStatus.__init__
    bstack1ll111ll1l_opy_ = pabot._run
    bstack11lll1ll11_opy_ = QueueItem.__init__
    bstack1l111l1l11_opy_ = pabot._create_command_for_execution
    bstack11l1llllll_opy_ = pabot._report_results
  if bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬൖ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1llllll1l1_opy_)
    bstack11llll11_opy_ = Runner.run_hook
    bstack11l1lll1_opy_ = Step.run
  if bstack111l11ll_opy_ == bstack11111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ൗ"):
    try:
      from _pytest.config import Config
      bstack1ll111111_opy_ = Config.getoption
      from _pytest import runner
      bstack1lll1111ll_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l1l1l1l1_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l1ll1ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11111l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨ൘"))
  try:
    framework_name = bstack11111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൙") if bstack111l11ll_opy_ in [bstack11111l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ൚"), bstack11111l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ൛"), bstack11111l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ൜")] else bstack1l1llll1ll_opy_(bstack111l11ll_opy_)
    bstack1lll111l1l_opy_ = {
      bstack11111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭൝"): bstack11111l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ൞") if bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧൟ") and bstack11lll111ll_opy_() else framework_name,
      bstack11111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬൠ"): bstack1llll1l1_opy_(framework_name),
      bstack11111l_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧൡ"): __version__,
      bstack11111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫൢ"): bstack111l11ll_opy_
    }
    if bstack111l11ll_opy_ in bstack11lll11l11_opy_ + bstack11l11l1l1l_opy_:
      if bstack1ll111l11_opy_ and bstack11l1ll1l1_opy_.bstack1l1l11111_opy_(CONFIG):
        if bstack11111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫൣ") in CONFIG:
          os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭൤")] = os.getenv(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ൥"), json.dumps(CONFIG[bstack11111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ൦")]))
          CONFIG[bstack11111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ൧")].pop(bstack11111l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ൨"), None)
          CONFIG[bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ൩")].pop(bstack11111l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ൪"), None)
        bstack1lll111l1l_opy_[bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൫")] = {
          bstack11111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ൬"): bstack11111l_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ൭"),
          bstack11111l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩ൮"): str(bstack1lllll11l1_opy_())
        }
    if bstack111l11ll_opy_ not in [bstack11111l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ൯")] and not cli.is_running():
      bstack1111lll1l_opy_, bstack1lll11l1_opy_ = bstack1111lll11_opy_.launch(CONFIG, bstack1lll111l1l_opy_)
      if bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ൰")) is not None and bstack11l1ll1l1_opy_.bstack1l1l1l1111_opy_(CONFIG) is None:
        value = bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ൱")].get(bstack11111l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭൲"))
        if value is not None:
            CONFIG[bstack11111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭൳")] = value
        else:
          logger.debug(bstack11111l_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡨࡦࡺࡡࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡶࡪࡹࡰࡰࡰࡶࡩࠧ൴"))
  except Exception as e:
    logger.debug(bstack11ll1l1111_opy_.format(bstack11111l_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩ൵"), str(e)))
  if bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ൶"):
    bstack1l11ll111l_opy_ = True
    if bstack11l1ll11_opy_ and bstack1l11l11l11_opy_:
      bstack11l1lll1ll_opy_ = CONFIG.get(bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ൷"), {}).get(bstack11111l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭൸"))
      bstack11l11l11l_opy_(bstack1ll1l1l1ll_opy_)
    elif bstack11l1ll11_opy_:
      bstack11l1lll1ll_opy_ = CONFIG.get(bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ൹"), {}).get(bstack11111l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨൺ"))
      global bstack1lll1l1l1l_opy_
      try:
        if bstack1llllllll_opy_(bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪൻ")]) and multiprocessing.current_process().name == bstack11111l_opy_ (u"ࠨ࠲ࠪർ"):
          bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬൽ")].remove(bstack11111l_opy_ (u"ࠪ࠱ࡲ࠭ൾ"))
          bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧൿ")].remove(bstack11111l_opy_ (u"ࠬࡶࡤࡣࠩ඀"))
          bstack11l1ll11_opy_[bstack11111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඁ")] = bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪං")][0]
          with open(bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඃ")], bstack11111l_opy_ (u"ࠩࡵࠫ඄")) as f:
            bstack1llll1lll_opy_ = f.read()
          bstack11ll111lll_opy_ = bstack11111l_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨඅ").format(str(bstack11l1ll11_opy_))
          bstack1l1l1llll_opy_ = bstack11ll111lll_opy_ + bstack1llll1lll_opy_
          bstack1lll11l1ll_opy_ = bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧආ")] + bstack11111l_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧඇ")
          with open(bstack1lll11l1ll_opy_, bstack11111l_opy_ (u"࠭ࡷࠨඈ")):
            pass
          with open(bstack1lll11l1ll_opy_, bstack11111l_opy_ (u"ࠢࡸ࠭ࠥඉ")) as f:
            f.write(bstack1l1l1llll_opy_)
          import subprocess
          bstack1l1l11l1ll_opy_ = subprocess.run([bstack11111l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣඊ"), bstack1lll11l1ll_opy_])
          if os.path.exists(bstack1lll11l1ll_opy_):
            os.unlink(bstack1lll11l1ll_opy_)
          os._exit(bstack1l1l11l1ll_opy_.returncode)
        else:
          if bstack1llllllll_opy_(bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඋ")]):
            bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ඌ")].remove(bstack11111l_opy_ (u"ࠫ࠲ࡳࠧඍ"))
            bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨඎ")].remove(bstack11111l_opy_ (u"࠭ࡰࡥࡤࠪඏ"))
            bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඐ")] = bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඑ")][0]
          bstack11l11l11l_opy_(bstack1ll1l1l1ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඒ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11111l_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬඓ")] = bstack11111l_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ඔ")
          mod_globals[bstack11111l_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧඕ")] = os.path.abspath(bstack11l1ll11_opy_[bstack11111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඖ")])
          exec(open(bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ඗")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11111l_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨ඘").format(str(e)))
          for driver in bstack1lll1l1l1l_opy_:
            bstack1ll111ll_opy_.append({
              bstack11111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ඙"): bstack11l1ll11_opy_[bstack11111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ක")],
              bstack11111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪඛ"): str(e),
              bstack11111l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫග"): multiprocessing.current_process().name
            })
            bstack111ll11l1_opy_(driver, bstack11111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ඝ"), bstack11111l_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥඞ") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1lll1l1l1l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1lllll1ll_opy_, CONFIG, logger)
      bstack11l11l11l1_opy_()
      bstack11l11111_opy_()
      percy.bstack11ll1l1ll_opy_()
      bstack11llll11ll_opy_ = {
        bstack11111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫඟ"): args[0],
        bstack11111l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩච"): CONFIG,
        bstack11111l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫඡ"): bstack1l1l111ll_opy_,
        bstack11111l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ජ"): bstack1lllll1ll_opy_
      }
      if bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨඣ") in CONFIG:
        bstack1111ll1l1_opy_ = bstack11l11l11_opy_(args, logger, CONFIG, bstack1ll111l11_opy_, bstack1111l1ll1_opy_)
        bstack1lllll1lll_opy_ = bstack1111ll1l1_opy_.bstack111l11111_opy_(run_on_browserstack, bstack11llll11ll_opy_, bstack1llllllll_opy_(args))
      else:
        if bstack1llllllll_opy_(args):
          bstack11llll11ll_opy_[bstack11111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩඤ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11llll11ll_opy_,))
          test.start()
          test.join()
        else:
          bstack11l11l11l_opy_(bstack1ll1l1l1ll_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11111l_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩඥ")] = bstack11111l_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪඦ")
          mod_globals[bstack11111l_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫට")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩඨ") or bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪඩ"):
    percy.init(bstack1lllll1ll_opy_, CONFIG, logger)
    percy.bstack11ll1l1ll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1111l1ll_opy_)
    bstack11l11l11l1_opy_()
    bstack11l11l11l_opy_(bstack11l1111l1_opy_)
    if bstack1ll111l11_opy_:
      bstack11l1llll1l_opy_(bstack11l1111l1_opy_, args)
      if bstack11111l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪඪ") in args:
        i = args.index(bstack11111l_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫණ"))
        args.pop(i)
        args.pop(i)
      if bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪඬ") not in CONFIG:
        CONFIG[bstack11111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫත")] = [{}]
        bstack1111l1ll1_opy_ = 1
      if bstack1l11l1l11_opy_ == 0:
        bstack1l11l1l11_opy_ = 1
      args.insert(0, str(bstack1l11l1l11_opy_))
      args.insert(0, str(bstack11111l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧථ")))
    if bstack1111lll11_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack11ll1ll1l_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack111l11l1_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11111l_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥද"),
        ).parse_args(bstack11ll1ll1l_opy_)
        bstack1l1l1l1l11_opy_ = args.index(bstack11ll1ll1l_opy_[0]) if len(bstack11ll1ll1l_opy_) > 0 else len(args)
        args.insert(bstack1l1l1l1l11_opy_, str(bstack11111l_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨධ")))
        args.insert(bstack1l1l1l1l11_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩන"))))
        if bstack11ll11l11_opy_(os.environ.get(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ඲"))) and str(os.environ.get(bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫඳ"), bstack11111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ප"))) != bstack11111l_opy_ (u"ࠩࡱࡹࡱࡲࠧඵ"):
          for bstack1l11llll1_opy_ in bstack111l11l1_opy_:
            args.remove(bstack1l11llll1_opy_)
          bstack11lll111_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧබ")).split(bstack11111l_opy_ (u"ࠫ࠱࠭භ"))
          for bstack1l11lll111_opy_ in bstack11lll111_opy_:
            args.append(bstack1l11lll111_opy_)
      except Exception as e:
        logger.error(bstack11111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࠣම").format(e))
    pabot.main(args)
  elif bstack111l11ll_opy_ == bstack11111l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧඹ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1111l1ll_opy_)
    for a in args:
      if bstack11111l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ය") in a:
        bstack11ll111l_opy_ = int(a.split(bstack11111l_opy_ (u"ࠨ࠼ࠪර"))[1])
      if bstack11111l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭඼") in a:
        bstack11l1lll1ll_opy_ = str(a.split(bstack11111l_opy_ (u"ࠪ࠾ࠬල"))[1])
      if bstack11111l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫ඾") in a:
        bstack1l1l1l111l_opy_ = str(a.split(bstack11111l_opy_ (u"ࠬࡀࠧ඿"))[1])
    bstack1ll1111lll_opy_ = None
    if bstack11111l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬව") in args:
      i = args.index(bstack11111l_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭ශ"))
      args.pop(i)
      bstack1ll1111lll_opy_ = args.pop(i)
    if bstack1ll1111lll_opy_ is not None:
      global bstack1l11111l11_opy_
      bstack1l11111l11_opy_ = bstack1ll1111lll_opy_
    bstack11l11l11l_opy_(bstack11l1111l1_opy_)
    run_cli(args)
    if bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬෂ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1l1ll11l_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll111ll_opy_.append(bstack1l1l1ll11l_opy_)
  elif bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩස"):
    bstack1l1l1ll1l_opy_ = bstack1llllll11_opy_(args, logger, CONFIG, bstack1ll111l11_opy_)
    bstack1l1l1ll1l_opy_.bstack11lll1lll1_opy_()
    bstack11l11l11l1_opy_()
    bstack11111111_opy_ = True
    bstack1l1lllll1l_opy_ = bstack1l1l1ll1l_opy_.bstack1l1111l1l1_opy_()
    bstack1l1l1ll1l_opy_.bstack11llll11ll_opy_(bstack1lll1llll_opy_)
    bstack1l1l11lll_opy_ = bstack1l1l1ll1l_opy_.bstack111l11111_opy_(bstack1l1l11ll1l_opy_, {
      bstack11111l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫහ"): bstack1l1l111ll_opy_,
      bstack11111l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ළ"): bstack1lllll1ll_opy_,
      bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨෆ"): bstack1ll111l11_opy_
    })
    try:
      bstack111ll1l1_opy_, bstack11lllll11l_opy_ = map(list, zip(*bstack1l1l11lll_opy_))
      bstack1l1lll111_opy_ = bstack111ll1l1_opy_[0]
      for status_code in bstack11lllll11l_opy_:
        if status_code != 0:
          bstack111l1l1l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡦࡴࡵࡳࡷࡹࠠࡢࡰࡧࠤࡸࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠰ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠺ࠡࡽࢀࠦ෇").format(str(e)))
  elif bstack111l11ll_opy_ == bstack11111l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ෈"):
    try:
      from behave.__main__ import main as bstack1llll111ll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l1l1l1_opy_(e, bstack1llllll1l1_opy_)
    bstack11l11l11l1_opy_()
    bstack11111111_opy_ = True
    bstack1l11l111l1_opy_ = 1
    if bstack11111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ෉") in CONFIG:
      bstack1l11l111l1_opy_ = CONFIG[bstack11111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮්ࠩ")]
    if bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෋") in CONFIG:
      bstack1l11l111ll_opy_ = int(bstack1l11l111l1_opy_) * int(len(CONFIG[bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෌")]))
    else:
      bstack1l11l111ll_opy_ = int(bstack1l11l111l1_opy_)
    config = Configuration(args)
    bstack1l1l1ll1_opy_ = config.paths
    if len(bstack1l1l1ll1_opy_) == 0:
      import glob
      pattern = bstack11111l_opy_ (u"ࠬ࠰ࠪ࠰ࠬ࠱ࡪࡪࡧࡴࡶࡴࡨࠫ෍")
      bstack1lllllll1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1lllllll1l_opy_)
      config = Configuration(args)
      bstack1l1l1ll1_opy_ = config.paths
    bstack11lll111l1_opy_ = [os.path.normpath(item) for item in bstack1l1l1ll1_opy_]
    bstack1l1111ll1l_opy_ = [os.path.normpath(item) for item in args]
    bstack1lll1ll1l1_opy_ = [item for item in bstack1l1111ll1l_opy_ if item not in bstack11lll111l1_opy_]
    import platform as pf
    if pf.system().lower() == bstack11111l_opy_ (u"࠭ࡷࡪࡰࡧࡳࡼࡹࠧ෎"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11lll111l1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11l11111_opy_)))
                    for bstack1l11l11111_opy_ in bstack11lll111l1_opy_]
    bstack1l111l1l1_opy_ = []
    for spec in bstack11lll111l1_opy_:
      bstack11lll1ll_opy_ = []
      bstack11lll1ll_opy_ += bstack1lll1ll1l1_opy_
      bstack11lll1ll_opy_.append(spec)
      bstack1l111l1l1_opy_.append(bstack11lll1ll_opy_)
    execution_items = []
    for bstack11lll1ll_opy_ in bstack1l111l1l1_opy_:
      if bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪා") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫැ")]):
          item = {}
          item[bstack11111l_opy_ (u"ࠩࡤࡶ࡬࠭ෑ")] = bstack11111l_opy_ (u"ࠪࠤࠬි").join(bstack11lll1ll_opy_)
          item[bstack11111l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪී")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11111l_opy_ (u"ࠬࡧࡲࡨࠩු")] = bstack11111l_opy_ (u"࠭ࠠࠨ෕").join(bstack11lll1ll_opy_)
        item[bstack11111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ූ")] = 0
        execution_items.append(item)
    bstack11llll1lll_opy_ = bstack1ll1l1l11_opy_(execution_items, bstack1l11l111ll_opy_)
    for execution_item in bstack11llll1lll_opy_:
      bstack1ll11l1l1l_opy_ = []
      for item in execution_item:
        bstack1ll11l1l1l_opy_.append(bstack1l11ll111_opy_(name=str(item[bstack11111l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ෗")]),
                                             target=bstack1l11l11l1l_opy_,
                                             args=(item[bstack11111l_opy_ (u"ࠩࡤࡶ࡬࠭ෘ")],)))
      for t in bstack1ll11l1l1l_opy_:
        t.start()
      for t in bstack1ll11l1l1l_opy_:
        t.join()
  else:
    bstack1l1llll11l_opy_(bstack1l1111lll_opy_)
  if not bstack11l1ll11_opy_:
    bstack11ll1l11l_opy_()
    if(bstack111l11ll_opy_ in [bstack11111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪෙ"), bstack11111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫේ")]):
      bstack11lllll11_opy_()
  bstack11ll1ll1l1_opy_.bstack111l1lll_opy_()
def browserstack_initialize(bstack111111ll1_opy_=None):
  logger.info(bstack11111l_opy_ (u"ࠬࡘࡵ࡯ࡰ࡬ࡲ࡬ࠦࡓࡅࡍࠣࡻ࡮ࡺࡨࠡࡣࡵ࡫ࡸࡀࠠࠨෛ") + str(bstack111111ll1_opy_))
  run_on_browserstack(bstack111111ll1_opy_, None, True)
@measure(event_name=EVENTS.bstack1l1l11l1_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11ll1l11l_opy_():
  global CONFIG
  global bstack1llll11ll1_opy_
  global bstack111l1l1l_opy_
  global bstack1lll1111l1_opy_
  global bstack1l11l11ll1_opy_
  bstack11l111111_opy_.bstack1ll111ll11_opy_()
  if cli.is_running():
    bstack1111l1l1_opy_.invoke(bstack1l1ll1llll_opy_.bstack11l1lllll1_opy_)
  if bstack1llll11ll1_opy_ == bstack11111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ො"):
    if not cli.is_enabled(CONFIG):
      bstack1111lll11_opy_.stop()
  else:
    bstack1111lll11_opy_.stop()
  if not cli.is_enabled(CONFIG):
    bstack1l1ll11l1l_opy_.bstack1lllll1l1l_opy_()
  if bstack11111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫෝ") in CONFIG and str(CONFIG[bstack11111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬෞ")]).lower() != bstack11111l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨෟ"):
    bstack1l11lllll1_opy_, bstack11l11l1l1_opy_ = bstack11lll1l1ll_opy_()
  else:
    bstack1l11lllll1_opy_, bstack11l11l1l1_opy_ = get_build_link()
  bstack1lll1l1ll1_opy_(bstack1l11lllll1_opy_)
  logger.info(bstack11111l_opy_ (u"ࠪࡗࡉࡑࠠࡳࡷࡱࠤࡪࡴࡤࡦࡦࠣࡪࡴࡸࠠࡪࡦ࠽ࠫ෠") + bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭෡"), bstack11111l_opy_ (u"ࠬ࠭෢")) + bstack11111l_opy_ (u"࠭ࠬࠡࡶࡨࡷࡹ࡮ࡵࡣࠢ࡬ࡨ࠿ࠦࠧ෣") + os.getenv(bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ෤"), bstack11111l_opy_ (u"ࠨࠩ෥")))
  if bstack1l11lllll1_opy_ is not None and bstack1l1ll111ll_opy_() != -1:
    sessions = bstack11ll1111_opy_(bstack1l11lllll1_opy_)
    bstack1l11ll1l_opy_(sessions, bstack11l11l1l1_opy_)
  if bstack1llll11ll1_opy_ == bstack11111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ෦") and bstack111l1l1l_opy_ != 0:
    sys.exit(bstack111l1l1l_opy_)
  if bstack1llll11ll1_opy_ == bstack11111l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෧") and bstack1lll1111l1_opy_ != 0:
    sys.exit(bstack1lll1111l1_opy_)
def bstack1lll1l1ll1_opy_(new_id):
    global bstack111l1111_opy_
    bstack111l1111_opy_ = new_id
def bstack1l1llll1ll_opy_(bstack111l11l1l_opy_):
  if bstack111l11l1l_opy_:
    return bstack111l11l1l_opy_.capitalize()
  else:
    return bstack11111l_opy_ (u"ࠫࠬ෨")
@measure(event_name=EVENTS.bstack1l1lll11ll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack111ll111l_opy_(bstack11lllll1l_opy_):
  if bstack11111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ෩") in bstack11lllll1l_opy_ and bstack11lllll1l_opy_[bstack11111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ෪")] != bstack11111l_opy_ (u"ࠧࠨ෫"):
    return bstack11lllll1l_opy_[bstack11111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭෬")]
  else:
    bstack1l1ll1ll_opy_ = bstack11111l_opy_ (u"ࠤࠥ෭")
    if bstack11111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ෮") in bstack11lllll1l_opy_ and bstack11lllll1l_opy_[bstack11111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ෯")] != None:
      bstack1l1ll1ll_opy_ += bstack11lllll1l_opy_[bstack11111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ෰")] + bstack11111l_opy_ (u"ࠨࠬࠡࠤ෱")
      if bstack11lllll1l_opy_[bstack11111l_opy_ (u"ࠧࡰࡵࠪෲ")] == bstack11111l_opy_ (u"ࠣ࡫ࡲࡷࠧෳ"):
        bstack1l1ll1ll_opy_ += bstack11111l_opy_ (u"ࠤ࡬ࡓࡘࠦࠢ෴")
      bstack1l1ll1ll_opy_ += (bstack11lllll1l_opy_[bstack11111l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ෵")] or bstack11111l_opy_ (u"ࠫࠬ෶"))
      return bstack1l1ll1ll_opy_
    else:
      bstack1l1ll1ll_opy_ += bstack1l1llll1ll_opy_(bstack11lllll1l_opy_[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭෷")]) + bstack11111l_opy_ (u"ࠨࠠࠣ෸") + (
              bstack11lllll1l_opy_[bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ෹")] or bstack11111l_opy_ (u"ࠨࠩ෺")) + bstack11111l_opy_ (u"ࠤ࠯ࠤࠧ෻")
      if bstack11lllll1l_opy_[bstack11111l_opy_ (u"ࠪࡳࡸ࠭෼")] == bstack11111l_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧ෽"):
        bstack1l1ll1ll_opy_ += bstack11111l_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥ෾")
      bstack1l1ll1ll_opy_ += bstack11lllll1l_opy_[bstack11111l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ෿")] or bstack11111l_opy_ (u"ࠧࠨ฀")
      return bstack1l1ll1ll_opy_
@measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack111llll11_opy_(bstack1111l11ll_opy_):
  if bstack1111l11ll_opy_ == bstack11111l_opy_ (u"ࠣࡦࡲࡲࡪࠨก"):
    return bstack11111l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬข")
  elif bstack1111l11ll_opy_ == bstack11111l_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥฃ"):
    return bstack11111l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧค")
  elif bstack1111l11ll_opy_ == bstack11111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧฅ"):
    return bstack11111l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ฆ")
  elif bstack1111l11ll_opy_ == bstack11111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨง"):
    return bstack11111l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪจ")
  elif bstack1111l11ll_opy_ == bstack11111l_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥฉ"):
    return bstack11111l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨช")
  elif bstack1111l11ll_opy_ == bstack11111l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧซ"):
    return bstack11111l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ฌ")
  else:
    return bstack11111l_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪญ") + bstack1l1llll1ll_opy_(
      bstack1111l11ll_opy_) + bstack11111l_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ฎ")
def bstack111l1ll1_opy_(session):
  return bstack11111l_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨฏ").format(
    session[bstack11111l_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭ฐ")], bstack111ll111l_opy_(session), bstack111llll11_opy_(session[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩฑ")]),
    bstack111llll11_opy_(session[bstack11111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫฒ")]),
    bstack1l1llll1ll_opy_(session[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ณ")] or session[bstack11111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ด")] or bstack11111l_opy_ (u"ࠧࠨต")) + bstack11111l_opy_ (u"ࠣࠢࠥถ") + (session[bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫท")] or bstack11111l_opy_ (u"ࠪࠫธ")),
    session[bstack11111l_opy_ (u"ࠫࡴࡹࠧน")] + bstack11111l_opy_ (u"ࠧࠦࠢบ") + session[bstack11111l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪป")], session[bstack11111l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩผ")] or bstack11111l_opy_ (u"ࠨࠩฝ"),
    session[bstack11111l_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭พ")] if session[bstack11111l_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧฟ")] else bstack11111l_opy_ (u"ࠫࠬภ"))
@measure(event_name=EVENTS.bstack1l11l1l1ll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack1l11ll1l_opy_(sessions, bstack11l11l1l1_opy_):
  try:
    bstack1l1111ll_opy_ = bstack11111l_opy_ (u"ࠧࠨม")
    if not os.path.exists(bstack1l1lll111l_opy_):
      os.mkdir(bstack1l1lll111l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11111l_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫย")), bstack11111l_opy_ (u"ࠧࡳࠩร")) as f:
      bstack1l1111ll_opy_ = f.read()
    bstack1l1111ll_opy_ = bstack1l1111ll_opy_.replace(bstack11111l_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬฤ"), str(len(sessions)))
    bstack1l1111ll_opy_ = bstack1l1111ll_opy_.replace(bstack11111l_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩล"), bstack11l11l1l1_opy_)
    bstack1l1111ll_opy_ = bstack1l1111ll_opy_.replace(bstack11111l_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫฦ"),
                                              sessions[0].get(bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨว")) if sessions[0] else bstack11111l_opy_ (u"ࠬ࠭ศ"))
    with open(os.path.join(bstack1l1lll111l_opy_, bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪษ")), bstack11111l_opy_ (u"ࠧࡸࠩส")) as stream:
      stream.write(bstack1l1111ll_opy_.split(bstack11111l_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬห"))[0])
      for session in sessions:
        stream.write(bstack111l1ll1_opy_(session))
      stream.write(bstack1l1111ll_opy_.split(bstack11111l_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ฬ"))[1])
    logger.info(bstack11111l_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭อ").format(bstack1l1lll111l_opy_));
  except Exception as e:
    logger.debug(bstack111lll11l_opy_.format(str(e)))
def bstack11ll1111_opy_(bstack1l11lllll1_opy_):
  global CONFIG
  try:
    bstack1l1l1l1l_opy_ = datetime.datetime.now()
    host = bstack11111l_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧฮ") if bstack11111l_opy_ (u"ࠬࡧࡰࡱࠩฯ") in CONFIG else bstack11111l_opy_ (u"࠭ࡡࡱ࡫ࠪะ")
    user = CONFIG[bstack11111l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩั")]
    key = CONFIG[bstack11111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫา")]
    bstack11l1l1ll1_opy_ = bstack11111l_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨำ") if bstack11111l_opy_ (u"ࠪࡥࡵࡶࠧิ") in CONFIG else (bstack11111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨี") if CONFIG.get(bstack11111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩึ")) else bstack11111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨื"))
    url = bstack11111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲุࠬ").format(user, key, host, bstack11l1l1ll1_opy_,
                                                                                bstack1l11lllll1_opy_)
    headers = {
      bstack11111l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ูࠧ"): bstack11111l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲฺࠬ"),
    }
    proxies = bstack1lll111l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      cli.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻ࡩࡨࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡹ࡟࡭࡫ࡶࡸࠧ฻"), datetime.datetime.now() - bstack1l1l1l1l_opy_)
      return list(map(lambda session: session[bstack11111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ฼")], response.json()))
  except Exception as e:
    logger.debug(bstack11l11ll11l_opy_.format(str(e)))
@measure(event_name=EVENTS.bstack1l11111ll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def get_build_link():
  global CONFIG
  global bstack111l1111_opy_
  try:
    if bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ฽") in CONFIG:
      bstack1l1l1l1l_opy_ = datetime.datetime.now()
      host = bstack11111l_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ฾") if bstack11111l_opy_ (u"ࠧࡢࡲࡳࠫ฿") in CONFIG else bstack11111l_opy_ (u"ࠨࡣࡳ࡭ࠬเ")
      user = CONFIG[bstack11111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫแ")]
      key = CONFIG[bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭โ")]
      bstack11l1l1ll1_opy_ = bstack11111l_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪใ") if bstack11111l_opy_ (u"ࠬࡧࡰࡱࠩไ") in CONFIG else bstack11111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨๅ")
      url = bstack11111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠰࡭ࡷࡴࡴࠧๆ").format(user, key, host, bstack11l1l1ll1_opy_)
      if cli.is_enabled(CONFIG):
        bstack11l11l1l1_opy_, bstack1l11lllll1_opy_ = cli.bstack11l11llll_opy_()
        logger.info(bstack1lll1l1111_opy_.format(bstack11l11l1l1_opy_))
        return [bstack1l11lllll1_opy_, bstack11l11l1l1_opy_]
      else:
        headers = {
          bstack11111l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧ็"): bstack11111l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲ่ࠬ"),
        }
        if bstack11111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ้ࠬ") in CONFIG:
          params = {bstack11111l_opy_ (u"ࠫࡳࡧ࡭ࡦ๊ࠩ"): CONFIG[bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ๋")], bstack11111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ์"): CONFIG[bstack11111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩํ")]}
        else:
          params = {bstack11111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭๎"): CONFIG[bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ๏")]}
        proxies = bstack1lll111l1_opy_(CONFIG, url)
        response = requests.get(url, params=params, headers=headers, proxies=proxies)
        if response.json():
          bstack1l1l111l1l_opy_ = response.json()[0][bstack11111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡣࡷ࡬ࡰࡩ࠭๐")]
          if bstack1l1l111l1l_opy_:
            bstack11l11l1l1_opy_ = bstack1l1l111l1l_opy_[bstack11111l_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ๑")].split(bstack11111l_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧ࠲ࡨࡵࡪ࡮ࡧࠫ๒"))[0] + bstack11111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡸ࠵ࠧ๓") + bstack1l1l111l1l_opy_[
              bstack11111l_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ๔")]
            logger.info(bstack1lll1l1111_opy_.format(bstack11l11l1l1_opy_))
            bstack111l1111_opy_ = bstack1l1l111l1l_opy_[bstack11111l_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ๕")]
            bstack1ll1111l1_opy_ = CONFIG[bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ๖")]
            if bstack11111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ๗") in CONFIG:
              bstack1ll1111l1_opy_ += bstack11111l_opy_ (u"ࠫࠥ࠭๘") + CONFIG[bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ๙")]
            if bstack1ll1111l1_opy_ != bstack1l1l111l1l_opy_[bstack11111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ๚")]:
              logger.debug(bstack11111l111_opy_.format(bstack1l1l111l1l_opy_[bstack11111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๛")], bstack1ll1111l1_opy_))
            cli.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠣࡪࡷࡸࡵࡀࡧࡦࡶࡢࡦࡺ࡯࡬ࡥࡡ࡯࡭ࡳࡱࠢ๜"), datetime.datetime.now() - bstack1l1l1l1l_opy_)
            return [bstack1l1l111l1l_opy_[bstack11111l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๝")], bstack11l11l1l1_opy_]
    else:
      logger.warn(bstack11ll11l111_opy_)
  except Exception as e:
    logger.debug(bstack1111ll111_opy_.format(str(e)))
  return [None, None]
def bstack1llll1111_opy_(url, bstack1llllll1l_opy_=False):
  global CONFIG
  global bstack1llllll111_opy_
  if not bstack1llllll111_opy_:
    hostname = bstack11111lll_opy_(url)
    is_private = bstack11ll1ll1_opy_(hostname)
    if (bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ๞") in CONFIG and not bstack11ll11l11_opy_(CONFIG[bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ๟")])) and (is_private or bstack1llllll1l_opy_):
      bstack1llllll111_opy_ = hostname
def bstack11111lll_opy_(url):
  return urlparse(url).hostname
def bstack11ll1ll1_opy_(hostname):
  for bstack1ll11l1lll_opy_ in bstack1ll1ll111_opy_:
    regex = re.compile(bstack1ll11l1lll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1lllllll11_opy_(bstack1l11lll1l_opy_):
  return True if bstack1l11lll1l_opy_ in threading.current_thread().__dict__.keys() else False
@measure(event_name=EVENTS.bstack1lll1111_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11ll111l_opy_
  bstack1l1llllll1_opy_ = not (bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ๠"), None) and bstack11l11llll1_opy_(
          threading.current_thread(), bstack11111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ๡"), None))
  bstack1l1111l111_opy_ = getattr(driver, bstack11111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ๢"), None) != True
  bstack1ll1l1l1l1_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ๣"), None) and bstack11l11llll1_opy_(
          threading.current_thread(), bstack11111l_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ๤"), None)
  if bstack1ll1l1l1l1_opy_:
    if not bstack1ll11l1ll1_opy_():
      logger.warning(bstack11111l_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸ࠴ࠢ๥"))
      return {}
    logger.debug(bstack11111l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨ๦"))
    logger.debug(perform_scan(driver, driver_command=bstack11111l_opy_ (u"ࠬ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠬ๧")))
    results = bstack1l1l1111ll_opy_(bstack11111l_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࡹࠢ๨"))
    if results is not None and results.get(bstack11111l_opy_ (u"ࠢࡪࡵࡶࡹࡪࡹࠢ๩")) is not None:
        return results[bstack11111l_opy_ (u"ࠣ࡫ࡶࡷࡺ࡫ࡳࠣ๪")]
    logger.error(bstack11111l_opy_ (u"ࠤࡑࡳࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡘࡥࡴࡷ࡯ࡸࡸࠦࡷࡦࡴࡨࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦ๫"))
    return []
  if not bstack11l1ll1l1_opy_.bstack111l111ll_opy_(CONFIG, bstack11ll111l_opy_) or (bstack1l1111l111_opy_ and bstack1l1llllll1_opy_):
    logger.warning(bstack11111l_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷ࠳ࠨ๬"))
    return {}
  try:
    logger.debug(bstack11111l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨ๭"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1l1ll111_opy_.bstack1l11llll1l_opy_)
    return results
  except Exception:
    logger.error(bstack11111l_opy_ (u"ࠧࡔ࡯ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡺࡩࡷ࡫ࠠࡧࡱࡸࡲࡩ࠴ࠢ๮"))
    return {}
@measure(event_name=EVENTS.bstack1ll1l1ll1l_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11ll111l_opy_
  bstack1l1llllll1_opy_ = not (bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ๯"), None) and bstack11l11llll1_opy_(
          threading.current_thread(), bstack11111l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭๰"), None))
  bstack1l1111l111_opy_ = getattr(driver, bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ๱"), None) != True
  bstack1ll1l1l1l1_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ๲"), None) and bstack11l11llll1_opy_(
          threading.current_thread(), bstack11111l_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ๳"), None)
  if bstack1ll1l1l1l1_opy_:
    if not bstack1ll11l1ll1_opy_():
      logger.warning(bstack11111l_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤ๴"))
      return {}
    logger.debug(bstack11111l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪ๵"))
    logger.debug(perform_scan(driver, driver_command=bstack11111l_opy_ (u"࠭ࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹ࠭๶")))
    results = bstack1l1l1111ll_opy_(bstack11111l_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡓࡶ࡯ࡰࡥࡷࡿࠢ๷"))
    if results is not None and results.get(bstack11111l_opy_ (u"ࠣࡵࡸࡱࡲࡧࡲࡺࠤ๸")) is not None:
        return results[bstack11111l_opy_ (u"ࠤࡶࡹࡲࡳࡡࡳࡻࠥ๹")]
    logger.error(bstack11111l_opy_ (u"ࠥࡒࡴࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡒࡦࡵࡸࡰࡹࡹࠠࡔࡷࡰࡱࡦࡸࡹࠡࡹࡤࡷࠥ࡬࡯ࡶࡰࡧ࠲ࠧ๺"))
    return {}
  if not bstack11l1ll1l1_opy_.bstack111l111ll_opy_(CONFIG, bstack11ll111l_opy_) or (bstack1l1111l111_opy_ and bstack1l1llllll1_opy_):
    logger.warning(bstack11111l_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿ࠮ࠣ๻"))
    return {}
  try:
    logger.debug(bstack11111l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻࠪ๼"))
    logger.debug(perform_scan(driver))
    bstack11l1lll11_opy_ = driver.execute_async_script(bstack1l1l1ll111_opy_.bstack1ll1l1111l_opy_)
    return bstack11l1lll11_opy_
  except Exception:
    logger.error(bstack11111l_opy_ (u"ࠨࡎࡰࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡹࡲࡳࡡࡳࡻࠣࡻࡦࡹࠠࡧࡱࡸࡲࡩ࠴ࠢ๽"))
    return {}
def bstack1ll11l1ll1_opy_():
  global CONFIG
  global bstack11ll111l_opy_
  bstack1ll11111_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ๾"), None) and bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ๿"), None)
  if not bstack11l1ll1l1_opy_.bstack111l111ll_opy_(CONFIG, bstack11ll111l_opy_) or not bstack1ll11111_opy_:
        logger.warning(bstack11111l_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡴࡵࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤ຀"))
        return False
  return True
def bstack1l1l1111ll_opy_(bstack11l1ll1l11_opy_):
    bstack1llll1llll_opy_ = bstack1111lll11_opy_.current_test_uuid() if bstack1111lll11_opy_.current_test_uuid() else bstack1l1ll11l1l_opy_.current_hook_uuid()
    with ThreadPoolExecutor() as executor:
        future = executor.submit(bstack11ll1lll_opy_(bstack1llll1llll_opy_, bstack11l1ll1l11_opy_))
        try:
            return future.result(timeout=bstack1111llll_opy_)
        except TimeoutError:
            logger.error(bstack11111l_opy_ (u"ࠥࡘ࡮ࡳࡥࡰࡷࡷࠤࡦ࡬ࡴࡦࡴࠣࡿࢂࡹࠠࡸࡪ࡬ࡰࡪࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡔࡨࡷࡺࡲࡴࡴࠤກ").format(bstack1111llll_opy_))
        except Exception as ex:
            logger.debug(bstack11111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡶࡪࡺࡲࡪࡧࡹ࡭ࡳ࡭ࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡽࢀ࠲ࠥࡋࡲࡳࡱࡵࠤ࠲ࠦࡻࡾࠤຂ").format(bstack11l1ll1l11_opy_, str(ex)))
    return {}
@measure(event_name=EVENTS.bstack1l1lll1l_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11ll111l_opy_
  bstack1l1llllll1_opy_ = not (bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ຃"), None) and bstack11l11llll1_opy_(
          threading.current_thread(), bstack11111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬຄ"), None))
  bstack1l1ll111_opy_ = not (bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ຅"), None) and bstack11l11llll1_opy_(
          threading.current_thread(), bstack11111l_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪຆ"), None))
  bstack1l1111l111_opy_ = getattr(driver, bstack11111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩງ"), None) != True
  if not bstack11l1ll1l1_opy_.bstack111l111ll_opy_(CONFIG, bstack11ll111l_opy_) or (bstack1l1111l111_opy_ and bstack1l1llllll1_opy_ and bstack1l1ll111_opy_):
    logger.warning(bstack11111l_opy_ (u"ࠥࡒࡴࡺࠠࡢࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡧࡶࡷ࡮ࡵ࡮࠭ࠢࡦࡥࡳࡴ࡯ࡵࠢࡵࡹࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠧຈ"))
    return {}
  try:
    bstack1111ll1ll_opy_ = bstack11111l_opy_ (u"ࠫࡦࡶࡰࠨຉ") in CONFIG and CONFIG.get(bstack11111l_opy_ (u"ࠬࡧࡰࡱࠩຊ"), bstack11111l_opy_ (u"࠭ࠧ຋"))
    session_id = getattr(driver, bstack11111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫຌ"), None)
    if not session_id:
      logger.warning(bstack11111l_opy_ (u"ࠣࡐࡲࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡏࡄࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤࡩࡸࡩࡷࡧࡵࠦຍ"))
      return {bstack11111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣຎ"): bstack11111l_opy_ (u"ࠥࡒࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡊࡆࠣࡪࡴࡻ࡮ࡥࠤຏ")}
    if bstack1111ll1ll_opy_:
      try:
        bstack1l1l111ll1_opy_ = {
              bstack11111l_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨຐ"): os.environ.get(bstack11111l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪຑ"), os.environ.get(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪຒ"), bstack11111l_opy_ (u"ࠧࠨຓ"))),
              bstack11111l_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨດ"): bstack1111lll11_opy_.current_test_uuid() if bstack1111lll11_opy_.current_test_uuid() else bstack1l1ll11l1l_opy_.current_hook_uuid(),
              bstack11111l_opy_ (u"ࠩࡤࡹࡹ࡮ࡈࡦࡣࡧࡩࡷ࠭ຕ"): os.environ.get(bstack11111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨຖ")),
              bstack11111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫທ"): str(int(datetime.datetime.now().timestamp() * 1000)),
              bstack11111l_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪຘ"): os.environ.get(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫນ"), bstack11111l_opy_ (u"ࠧࠨບ")),
              bstack11111l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨປ"): kwargs.get(bstack11111l_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪຜ"), None) or bstack11111l_opy_ (u"ࠪࠫຝ")
          }
        if not hasattr(thread_local, bstack11111l_opy_ (u"ࠫࡧࡧࡳࡦࡡࡤࡴࡵࡥࡡ࠲࠳ࡼࡣࡸࡩࡲࡪࡲࡷࠫພ")):
            scripts = {bstack11111l_opy_ (u"ࠬࡹࡣࡢࡰࠪຟ"): bstack1l1l1ll111_opy_.perform_scan}
            thread_local.base_app_a11y_script = scripts
        bstack1l11111l1l_opy_ = copy.deepcopy(thread_local.base_app_a11y_script)
        bstack1l11111l1l_opy_[bstack11111l_opy_ (u"࠭ࡳࡤࡣࡱࠫຠ")] = bstack1l11111l1l_opy_[bstack11111l_opy_ (u"ࠧࡴࡥࡤࡲࠬມ")] % json.dumps(bstack1l1l111ll1_opy_)
        bstack1l1l1ll111_opy_.bstack11lll1111_opy_(bstack1l11111l1l_opy_)
        bstack1l1l1ll111_opy_.store()
        bstack11ll1l1ll1_opy_ = driver.execute_script(bstack1l1l1ll111_opy_.perform_scan)
      except Exception as bstack1ll1ll1ll_opy_:
        logger.info(bstack11111l_opy_ (u"ࠣࡃࡳࡴ࡮ࡻ࡭ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࠣຢ") + str(bstack1ll1ll1ll_opy_))
        bstack11ll1l1ll1_opy_ = {bstack11111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣຣ"): str(bstack1ll1ll1ll_opy_)}
    else:
      bstack11ll1l1ll1_opy_ = driver.execute_async_script(bstack1l1l1ll111_opy_.perform_scan, {bstack11111l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪ຤"): kwargs.get(bstack11111l_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࡣࡨࡵ࡭࡮ࡣࡱࡨࠬລ"), None) or bstack11111l_opy_ (u"ࠬ࠭຦")})
    return bstack11ll1l1ll1_opy_
  except Exception as err:
    logger.error(bstack11111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱ࠲ࠥࢁࡽࠣວ").format(str(err)))
    return {}