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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack11ll11l1l1_opy_, bstack11111ll1_opy_
from bstack_utils.measure import measure
class bstack1l1111111l_opy_:
  working_dir = os.getcwd()
  bstack11l11l11ll_opy_ = False
  config = {}
  bstack11l1l1l1lll_opy_ = bstack11111l_opy_ (u"ࠩࠪ᲎")
  binary_path = bstack11111l_opy_ (u"ࠪࠫ᲏")
  bstack111lll111ll_opy_ = bstack11111l_opy_ (u"ࠫࠬᲐ")
  bstack11ll11l1_opy_ = False
  bstack111ll11ll11_opy_ = None
  bstack111llll1l11_opy_ = {}
  bstack11l111111l1_opy_ = 300
  bstack111ll1l1ll1_opy_ = False
  logger = None
  bstack111ll1l11ll_opy_ = False
  bstack1ll111llll_opy_ = False
  percy_build_id = None
  bstack111lllll1ll_opy_ = bstack11111l_opy_ (u"ࠬ࠭Ბ")
  bstack111lll1lll1_opy_ = {
    bstack11111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭Გ") : 1,
    bstack11111l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᲓ") : 2,
    bstack11111l_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭Ე") : 3,
    bstack11111l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࠩᲕ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111lll11111_opy_(self):
    bstack111ll111lll_opy_ = bstack11111l_opy_ (u"ࠪࠫᲖ")
    bstack111lll1llll_opy_ = sys.platform
    bstack111lll1ll1l_opy_ = bstack11111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᲗ")
    if re.match(bstack11111l_opy_ (u"ࠧࡪࡡࡳࡹ࡬ࡲࢁࡳࡡࡤࠢࡲࡷࠧᲘ"), bstack111lll1llll_opy_) != None:
      bstack111ll111lll_opy_ = bstack11ll1l1l1ll_opy_ + bstack11111l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳࡯ࡴࡺ࠱ࡾ࡮ࡶࠢᲙ")
      self.bstack111lllll1ll_opy_ = bstack11111l_opy_ (u"ࠧ࡮ࡣࡦࠫᲚ")
    elif re.match(bstack11111l_opy_ (u"ࠣ࡯ࡶࡻ࡮ࡴࡼ࡮ࡵࡼࡷࢁࡳࡩ࡯ࡩࡺࢀࡨࡿࡧࡸ࡫ࡱࢀࡧࡩࡣࡸ࡫ࡱࢀࡼ࡯࡮ࡤࡧࡿࡩࡲࡩࡼࡸ࡫ࡱ࠷࠷ࠨᲛ"), bstack111lll1llll_opy_) != None:
      bstack111ll111lll_opy_ = bstack11ll1l1l1ll_opy_ + bstack11111l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯ࡺ࡭ࡳ࠴ࡺࡪࡲࠥᲜ")
      bstack111lll1ll1l_opy_ = bstack11111l_opy_ (u"ࠥࡴࡪࡸࡣࡺ࠰ࡨࡼࡪࠨᲝ")
      self.bstack111lllll1ll_opy_ = bstack11111l_opy_ (u"ࠫࡼ࡯࡮ࠨᲞ")
    else:
      bstack111ll111lll_opy_ = bstack11ll1l1l1ll_opy_ + bstack11111l_opy_ (u"ࠧ࠵ࡰࡦࡴࡦࡽ࠲ࡲࡩ࡯ࡷࡻ࠲ࡿ࡯ࡰࠣᲟ")
      self.bstack111lllll1ll_opy_ = bstack11111l_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬᲠ")
    return bstack111ll111lll_opy_, bstack111lll1ll1l_opy_
  def bstack111llll1lll_opy_(self):
    try:
      bstack11l111111ll_opy_ = [os.path.join(expanduser(bstack11111l_opy_ (u"ࠢࡿࠤᲡ")), bstack11111l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᲢ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack11l111111ll_opy_:
        if(self.bstack111lll11ll1_opy_(path)):
          return path
      raise bstack11111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨᲣ")
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡪࡰࡧࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡳࡩࡷࡩࡹࠡࡦࡲࡻࡳࡲ࡯ࡢࡦ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠ࠮ࠢࡾࢁࠧᲤ").format(e))
  def bstack111lll11ll1_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack111llllllll_opy_(self, bstack11l11111l1l_opy_):
    return os.path.join(bstack11l11111l1l_opy_, self.bstack11l1l1l1lll_opy_ + bstack11111l_opy_ (u"ࠦ࠳࡫ࡴࡢࡩࠥᲥ"))
  def bstack111ll11lll1_opy_(self, bstack11l11111l1l_opy_, bstack111llll1ll1_opy_):
    if not bstack111llll1ll1_opy_: return
    try:
      bstack111lll11l1l_opy_ = self.bstack111llllllll_opy_(bstack11l11111l1l_opy_)
      with open(bstack111lll11l1l_opy_, bstack11111l_opy_ (u"ࠧࡽࠢᲦ")) as f:
        f.write(bstack111llll1ll1_opy_)
        self.logger.debug(bstack11111l_opy_ (u"ࠨࡓࡢࡸࡨࡨࠥࡴࡥࡸࠢࡈࡘࡦ࡭ࠠࡧࡱࡵࠤࡵ࡫ࡲࡤࡻࠥᲧ"))
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡦࡼࡥࠡࡶ࡫ࡩࠥ࡫ࡴࡢࡩ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᲨ").format(e))
  def bstack11l1111111l_opy_(self, bstack11l11111l1l_opy_):
    try:
      bstack111lll11l1l_opy_ = self.bstack111llllllll_opy_(bstack11l11111l1l_opy_)
      if os.path.exists(bstack111lll11l1l_opy_):
        with open(bstack111lll11l1l_opy_, bstack11111l_opy_ (u"ࠣࡴࠥᲩ")) as f:
          bstack111llll1ll1_opy_ = f.read().strip()
          return bstack111llll1ll1_opy_ if bstack111llll1ll1_opy_ else None
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡉ࡙ࡧࡧ࠭ࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧᲪ").format(e))
  def bstack111ll11l111_opy_(self, bstack11l11111l1l_opy_, bstack111ll111lll_opy_):
    bstack111ll1ll1ll_opy_ = self.bstack11l1111111l_opy_(bstack11l11111l1l_opy_)
    if bstack111ll1ll1ll_opy_:
      try:
        bstack111ll1l1111_opy_ = self.bstack111lll11l11_opy_(bstack111ll1ll1ll_opy_, bstack111ll111lll_opy_)
        if not bstack111ll1l1111_opy_:
          self.logger.debug(bstack11111l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡷࠥࡻࡰࠡࡶࡲࠤࡩࡧࡴࡦࠢࠫࡉ࡙ࡧࡧࠡࡷࡱࡧ࡭ࡧ࡮ࡨࡧࡧ࠭ࠧᲫ"))
          return True
        self.logger.debug(bstack11111l_opy_ (u"ࠦࡓ࡫ࡷࠡࡒࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡹࡵࡪࡡࡵࡧࠥᲬ"))
        return False
      except Exception as e:
        self.logger.warn(bstack11111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡥ࡫ࡩࡨࡱࠠࡧࡱࡵࠤࡧ࡯࡮ࡢࡴࡼࠤࡺࡶࡤࡢࡶࡨࡷ࠱ࠦࡵࡴ࡫ࡱ࡫ࠥ࡫ࡸࡪࡵࡷ࡭ࡳ࡭ࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᲭ").format(e))
    return False
  def bstack111lll11l11_opy_(self, bstack111ll1ll1ll_opy_, bstack111ll111lll_opy_):
    try:
      headers = {
        bstack11111l_opy_ (u"ࠨࡉࡧ࠯ࡑࡳࡳ࡫࠭ࡎࡣࡷࡧ࡭ࠨᲮ"): bstack111ll1ll1ll_opy_
      }
      response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠧࡈࡇࡗࠫᲯ"), bstack111ll111lll_opy_, {}, {bstack11111l_opy_ (u"ࠣࡪࡨࡥࡩ࡫ࡲࡴࠤᲰ"): headers})
      if response.status_code == 304:
        return False
      return True
    except Exception as e:
      raise(bstack11111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡪࡴࡸࠠࡑࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡵࡱࡦࡤࡸࡪࡹ࠺ࠡࡽࢀࠦᲱ").format(e))
  @measure(event_name=EVENTS.bstack11ll1lll111_opy_, stage=STAGE.bstack1l1llll11_opy_)
  def bstack111ll1ll111_opy_(self, bstack111ll111lll_opy_, bstack111lll1ll1l_opy_):
    try:
      bstack111lll1ll11_opy_ = self.bstack111llll1lll_opy_()
      bstack111ll1ll1l1_opy_ = os.path.join(bstack111lll1ll11_opy_, bstack11111l_opy_ (u"ࠪࡴࡪࡸࡣࡺ࠰ࡽ࡭ࡵ࠭Ჲ"))
      bstack111ll1l1l11_opy_ = os.path.join(bstack111lll1ll11_opy_, bstack111lll1ll1l_opy_)
      if self.bstack111ll11l111_opy_(bstack111lll1ll11_opy_, bstack111ll111lll_opy_):
        if os.path.exists(bstack111ll1l1l11_opy_):
          self.logger.info(bstack11111l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡴࡻ࡮ࡥࠢ࡬ࡲࠥࢁࡽ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᲳ").format(bstack111ll1l1l11_opy_))
          return bstack111ll1l1l11_opy_
        if os.path.exists(bstack111ll1ll1l1_opy_):
          self.logger.info(bstack11111l_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡿ࡯ࡰࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡶࡰࡽ࡭ࡵࡶࡩ࡯ࡩࠥᲴ").format(bstack111ll1ll1l1_opy_))
          return self.bstack111lll1l1l1_opy_(bstack111ll1ll1l1_opy_, bstack111lll1ll1l_opy_)
      self.logger.info(bstack11111l_opy_ (u"ࠨࡄࡰࡹࡱࡰࡴࡧࡤࡪࡰࡪࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡪࡷࡵ࡭ࠡࡽࢀࠦᲵ").format(bstack111ll111lll_opy_))
      response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠧࡈࡇࡗࠫᲶ"), bstack111ll111lll_opy_, {}, {})
      if response.status_code == 200:
        bstack111llll111l_opy_ = response.headers.get(bstack11111l_opy_ (u"ࠣࡇࡗࡥ࡬ࠨᲷ"), bstack11111l_opy_ (u"ࠤࠥᲸ"))
        if bstack111llll111l_opy_:
          self.bstack111ll11lll1_opy_(bstack111lll1ll11_opy_, bstack111llll111l_opy_)
        with open(bstack111ll1ll1l1_opy_, bstack11111l_opy_ (u"ࠪࡻࡧ࠭Ჹ")) as file:
          file.write(response.content)
        self.logger.info(bstack11111l_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡫ࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿࠠࡢࡰࡧࠤࡸࡧࡶࡦࡦࠣࡥࡹࠦࡻࡾࠤᲺ").format(bstack111ll1ll1l1_opy_))
        return self.bstack111lll1l1l1_opy_(bstack111ll1ll1l1_opy_, bstack111lll1ll1l_opy_)
      else:
        raise(bstack11111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠣࡸ࡭࡫ࠠࡧ࡫࡯ࡩ࠳ࠦࡓࡵࡣࡷࡹࡸࠦࡣࡰࡦࡨ࠾ࠥࢁࡽࠣ᲻").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻ࠽ࠤࢀࢃࠢ᲼").format(e))
  def bstack111llllll11_opy_(self, bstack111ll111lll_opy_, bstack111lll1ll1l_opy_):
    try:
      retry = 2
      bstack111ll1l1l11_opy_ = None
      bstack11l11111ll1_opy_ = False
      while retry > 0:
        bstack111ll1l1l11_opy_ = self.bstack111ll1ll111_opy_(bstack111ll111lll_opy_, bstack111lll1ll1l_opy_)
        bstack11l11111ll1_opy_ = self.bstack111llll11l1_opy_(bstack111ll111lll_opy_, bstack111lll1ll1l_opy_, bstack111ll1l1l11_opy_)
        if bstack11l11111ll1_opy_:
          break
        retry -= 1
      return bstack111ll1l1l11_opy_, bstack11l11111ll1_opy_
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣ࡫ࡪࡺࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠦࡰࡢࡶ࡫ࠦᲽ").format(e))
    return bstack111ll1l1l11_opy_, False
  def bstack111llll11l1_opy_(self, bstack111ll111lll_opy_, bstack111lll1ll1l_opy_, bstack111ll1l1l11_opy_, bstack111lll11lll_opy_ = 0):
    if bstack111lll11lll_opy_ > 1:
      return False
    if bstack111ll1l1l11_opy_ == None or os.path.exists(bstack111ll1l1l11_opy_) == False:
      self.logger.warn(bstack11111l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡱࡣࡷ࡬ࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤ࠭ࠢࡵࡩࡹࡸࡹࡪࡰࡪࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠨᲾ"))
      return False
    bstack111ll1lll11_opy_ = bstack11111l_opy_ (u"ࠤࡡ࠲࠯ࡆࡰࡦࡴࡦࡽࡡ࠵ࡣ࡭࡫ࠣࡠࡩ࠴࡜ࡥ࠭࠱ࡠࡩ࠱ࠢᲿ")
    command = bstack11111l_opy_ (u"ࠪࡿࢂࠦ࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩ᳀").format(bstack111ll1l1l11_opy_)
    bstack111ll11l11l_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack111ll1lll11_opy_, bstack111ll11l11l_opy_) != None:
      return True
    else:
      self.logger.error(bstack11111l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡺࡪࡸࡳࡪࡱࡱࠤࡨ࡮ࡥࡤ࡭ࠣࡪࡦ࡯࡬ࡦࡦࠥ᳁"))
      return False
  def bstack111lll1l1l1_opy_(self, bstack111ll1ll1l1_opy_, bstack111lll1ll1l_opy_):
    try:
      working_dir = os.path.dirname(bstack111ll1ll1l1_opy_)
      shutil.unpack_archive(bstack111ll1ll1l1_opy_, working_dir)
      bstack111ll1l1l11_opy_ = os.path.join(working_dir, bstack111lll1ll1l_opy_)
      os.chmod(bstack111ll1l1l11_opy_, 0o755)
      return bstack111ll1l1l11_opy_
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡷࡱࡾ࡮ࡶࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࠨ᳂"))
  def bstack111ll11llll_opy_(self):
    try:
      bstack111lllll1l1_opy_ = self.config.get(bstack11111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ᳃"))
      bstack111ll11llll_opy_ = bstack111lllll1l1_opy_ or (bstack111lllll1l1_opy_ is None and self.bstack11l11l11ll_opy_)
      if not bstack111ll11llll_opy_ or self.config.get(bstack11111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ᳄"), None) not in bstack11ll1ll1lll_opy_:
        return False
      self.bstack11ll11l1_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ᳅").format(e))
  def bstack111lll1111l_opy_(self):
    try:
      bstack111lll1111l_opy_ = self.percy_capture_mode
      return bstack111lll1111l_opy_
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡦࡸࠥࡶࡥࡳࡥࡼࠤࡨࡧࡰࡵࡷࡵࡩࠥࡳ࡯ࡥࡧ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥ᳆").format(e))
  def init(self, bstack11l11l11ll_opy_, config, logger):
    self.bstack11l11l11ll_opy_ = bstack11l11l11ll_opy_
    self.config = config
    self.logger = logger
    if not self.bstack111ll11llll_opy_():
      return
    self.bstack111llll1l11_opy_ = config.get(bstack11111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳇"), {})
    self.percy_capture_mode = config.get(bstack11111l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧ᳈"))
    try:
      bstack111ll111lll_opy_, bstack111lll1ll1l_opy_ = self.bstack111lll11111_opy_()
      self.bstack11l1l1l1lll_opy_ = bstack111lll1ll1l_opy_
      bstack111ll1l1l11_opy_, bstack11l11111ll1_opy_ = self.bstack111llllll11_opy_(bstack111ll111lll_opy_, bstack111lll1ll1l_opy_)
      if bstack11l11111ll1_opy_:
        self.binary_path = bstack111ll1l1l11_opy_
        thread = Thread(target=self.bstack111ll1lll1l_opy_)
        thread.start()
      else:
        self.bstack111ll1l11ll_opy_ = True
        self.logger.error(bstack11111l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤ᳉").format(bstack111ll1l1l11_opy_))
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢ᳊").format(e))
  def bstack11l11111l11_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack11111l_opy_ (u"ࠧ࡭ࡱࡪࠫ᳋"), bstack11111l_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫ᳌"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack11111l_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨ᳍").format(logfile))
      self.bstack111lll111ll_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦ᳎").format(e))
  @measure(event_name=EVENTS.bstack11ll11ll11l_opy_, stage=STAGE.bstack1l1llll11_opy_)
  def bstack111ll1lll1l_opy_(self):
    bstack111ll1l1lll_opy_ = self.bstack11l11111111_opy_()
    if bstack111ll1l1lll_opy_ == None:
      self.bstack111ll1l11ll_opy_ = True
      self.logger.error(bstack11111l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢ᳏"))
      return False
    command_args = [bstack11111l_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨ᳐") if self.bstack11l11l11ll_opy_ else bstack11111l_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪ᳑")]
    bstack11l111l1l11_opy_ = self.bstack111lll1l1ll_opy_()
    if bstack11l111l1l11_opy_ != None:
      command_args.append(bstack11111l_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨ᳒").format(bstack11l111l1l11_opy_))
    env = os.environ.copy()
    env[bstack11111l_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨ᳓")] = bstack111ll1l1lll_opy_
    env[bstack11111l_opy_ (u"ࠤࡗࡌࡤࡈࡕࡊࡎࡇࡣ࡚࡛ࡉࡅࠤ᳔")] = os.environ.get(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᳕"), bstack11111l_opy_ (u"᳖ࠫࠬ"))
    bstack111ll11l1l1_opy_ = [self.binary_path]
    self.bstack11l11111l11_opy_()
    self.bstack111ll11ll11_opy_ = self.bstack111ll1lllll_opy_(bstack111ll11l1l1_opy_ + command_args, env)
    self.logger.debug(bstack11111l_opy_ (u"࡙ࠧࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠨ᳗"))
    bstack111lll11lll_opy_ = 0
    while self.bstack111ll11ll11_opy_.poll() == None:
      bstack111llll1111_opy_ = self.bstack111ll1l11l1_opy_()
      if bstack111llll1111_opy_:
        self.logger.debug(bstack11111l_opy_ (u"ࠨࡈࡦࡣ࡯ࡸ࡭ࠦࡃࡩࡧࡦ࡯ࠥࡹࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠤ᳘"))
        self.bstack111ll1l1ll1_opy_ = True
        return True
      bstack111lll11lll_opy_ += 1
      self.logger.debug(bstack11111l_opy_ (u"ࠢࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡒࡦࡶࡵࡽࠥ࠳ࠠࡼࡿ᳙ࠥ").format(bstack111lll11lll_opy_))
      time.sleep(2)
    self.logger.error(bstack11111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡴࡪࡸࡣࡺ࠮ࠣࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡉࡥ࡮ࡲࡥࡥࠢࡤࡪࡹ࡫ࡲࠡࡽࢀࠤࡦࡺࡴࡦ࡯ࡳࡸࡸࠨ᳚").format(bstack111lll11lll_opy_))
    self.bstack111ll1l11ll_opy_ = True
    return False
  def bstack111ll1l11l1_opy_(self, bstack111lll11lll_opy_ = 0):
    if bstack111lll11lll_opy_ > 10:
      return False
    try:
      bstack111ll11ll1l_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡕࡈࡖ࡛ࡋࡒࡠࡃࡇࡈࡗࡋࡓࡔࠩ᳛"), bstack11111l_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡰࡴࡩࡡ࡭ࡪࡲࡷࡹࡀ࠵࠴࠵࠻᳜ࠫ"))
      bstack111ll11l1ll_opy_ = bstack111ll11ll1l_opy_ + bstack11ll1l11l11_opy_
      response = requests.get(bstack111ll11l1ll_opy_)
      data = response.json()
      self.percy_build_id = data.get(bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦ᳝ࠪ"), {}).get(bstack11111l_opy_ (u"ࠬ࡯ࡤࠨ᳞"), None)
      return True
    except:
      self.logger.debug(bstack11111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡶࡪࡪࠠࡸࡪ࡬ࡰࡪࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣ࡬ࡪࡧ࡬ࡵࡪࠣࡧ࡭࡫ࡣ࡬ࠢࡵࡩࡸࡶ࡯࡯ࡵࡨ᳟ࠦ"))
      return False
  def bstack11l11111111_opy_(self):
    bstack111lll111l1_opy_ = bstack11111l_opy_ (u"ࠧࡢࡲࡳࠫ᳠") if self.bstack11l11l11ll_opy_ else bstack11111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ᳡")
    bstack111ll1l1l1l_opy_ = bstack11111l_opy_ (u"ࠤࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ᳢ࠧ") if self.config.get(bstack11111l_opy_ (u"ࠪࡴࡪࡸࡣࡺ᳣ࠩ")) is None else True
    bstack11l1ll11ll1_opy_ = bstack11111l_opy_ (u"ࠦࡦࡶࡩ࠰ࡣࡳࡴࡤࡶࡥࡳࡥࡼ࠳࡬࡫ࡴࡠࡲࡵࡳ࡯࡫ࡣࡵࡡࡷࡳࡰ࡫࡮ࡀࡰࡤࡱࡪࡃࡻࡾࠨࡷࡽࡵ࡫࠽ࡼࡿࠩࡴࡪࡸࡣࡺ࠿ࡾࢁ᳤ࠧ").format(self.config[bstack11111l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧ᳥ࠪ")], bstack111lll111l1_opy_, bstack111ll1l1l1l_opy_)
    if self.percy_capture_mode:
      bstack11l1ll11ll1_opy_ += bstack11111l_opy_ (u"ࠨࠦࡱࡧࡵࡧࡾࡥࡣࡢࡲࡷࡹࡷ࡫࡟࡮ࡱࡧࡩࡂࢁࡽ᳦ࠣ").format(self.percy_capture_mode)
    uri = bstack11ll11l1l1_opy_(bstack11l1ll11ll1_opy_)
    try:
      response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠧࡈࡇࡗ᳧ࠫ"), uri, {}, {bstack11111l_opy_ (u"ࠨࡣࡸࡸ࡭᳨࠭"): (self.config[bstack11111l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᳩ")], self.config[bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᳪ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack11ll11l1_opy_ = data.get(bstack11111l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᳫ"))
        self.percy_capture_mode = data.get(bstack11111l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡣࡨࡧࡰࡵࡷࡵࡩࡤࡳ࡯ࡥࡧࠪᳬ"))
        os.environ[bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜᳭ࠫ")] = str(self.bstack11ll11l1_opy_)
        os.environ[bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫᳮ")] = str(self.percy_capture_mode)
        if bstack111ll1l1l1l_opy_ == bstack11111l_opy_ (u"ࠣࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧࠦᳯ") and str(self.bstack11ll11l1_opy_).lower() == bstack11111l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᳰ"):
          self.bstack1ll111llll_opy_ = True
        if bstack11111l_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤᳱ") in data:
          return data[bstack11111l_opy_ (u"ࠦࡹࡵ࡫ࡦࡰࠥᳲ")]
        else:
          raise bstack11111l_opy_ (u"࡚ࠬ࡯࡬ࡧࡱࠤࡓࡵࡴࠡࡈࡲࡹࡳࡪࠠ࠮ࠢࡾࢁࠬᳳ").format(data)
      else:
        raise bstack11111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡲࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡶࡸࡦࡺࡵࡴࠢ࠰ࠤࢀࢃࠬࠡࡔࡨࡷࡵࡵ࡮ࡴࡧࠣࡆࡴࡪࡹࠡ࠯ࠣࡿࢂࠨ᳴").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡨࡶࡨࡿࠠࡱࡴࡲ࡮ࡪࡩࡴࠣᳵ").format(e))
  def bstack111lll1l1ll_opy_(self):
    bstack111lll1l111_opy_ = os.path.join(tempfile.gettempdir(), bstack11111l_opy_ (u"ࠣࡲࡨࡶࡨࡿࡃࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠦᳶ"))
    try:
      if bstack11111l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ᳷") not in self.bstack111llll1l11_opy_:
        self.bstack111llll1l11_opy_[bstack11111l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ᳸")] = 2
      with open(bstack111lll1l111_opy_, bstack11111l_opy_ (u"ࠫࡼ࠭᳹")) as fp:
        json.dump(self.bstack111llll1l11_opy_, fp)
      return bstack111lll1l111_opy_
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡥࡵࡩࡦࡺࡥࠡࡲࡨࡶࡨࡿࠠࡤࡱࡱࡪ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᳺ").format(e))
  def bstack111ll1lllll_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack111lllll1ll_opy_ == bstack11111l_opy_ (u"࠭ࡷࡪࡰࠪ᳻"):
        bstack111ll1l111l_opy_ = [bstack11111l_opy_ (u"ࠧࡤ࡯ࡧ࠲ࡪࡾࡥࠨ᳼"), bstack11111l_opy_ (u"ࠨ࠱ࡦࠫ᳽")]
        cmd = bstack111ll1l111l_opy_ + cmd
      cmd = bstack11111l_opy_ (u"ࠩࠣࠫ᳾").join(cmd)
      self.logger.debug(bstack11111l_opy_ (u"ࠥࡖࡺࡴ࡮ࡪࡰࡪࠤࢀࢃࠢ᳿").format(cmd))
      with open(self.bstack111lll111ll_opy_, bstack11111l_opy_ (u"ࠦࡦࠨᴀ")) as bstack111lllll111_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack111lllll111_opy_, text=True, stderr=bstack111lllll111_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack111ll1l11ll_opy_ = True
      self.logger.error(bstack11111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾࠦࡷࡪࡶ࡫ࠤࡨࡳࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᴁ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack111ll1l1ll1_opy_:
        self.logger.info(bstack11111l_opy_ (u"ࠨࡓࡵࡱࡳࡴ࡮ࡴࡧࠡࡒࡨࡶࡨࡿࠢᴂ"))
        cmd = [self.binary_path, bstack11111l_opy_ (u"ࠢࡦࡺࡨࡧ࠿ࡹࡴࡰࡲࠥᴃ")]
        self.bstack111ll1lllll_opy_(cmd)
        self.bstack111ll1l1ll1_opy_ = False
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸࡺ࡯ࡱࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡥࡲࡱࡲࡧ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠣᴄ").format(cmd, e))
  def bstack11ll1l1ll_opy_(self):
    if not self.bstack11ll11l1_opy_:
      return
    try:
      bstack111lllll11l_opy_ = 0
      while not self.bstack111ll1l1ll1_opy_ and bstack111lllll11l_opy_ < self.bstack11l111111l1_opy_:
        if self.bstack111ll1l11ll_opy_:
          self.logger.info(bstack11111l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡵࡨࡸࡺࡶࠠࡧࡣ࡬ࡰࡪࡪࠢᴅ"))
          return
        time.sleep(1)
        bstack111lllll11l_opy_ += 1
      os.environ[bstack11111l_opy_ (u"ࠪࡔࡊࡘࡃ࡚ࡡࡅࡉࡘ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩᴆ")] = str(self.bstack111llll11ll_opy_())
      self.logger.info(bstack11111l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡷࡪࡺࡵࡱࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠧᴇ"))
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠠࡱࡧࡵࡧࡾ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡿࢂࠨᴈ").format(e))
  def bstack111llll11ll_opy_(self):
    if self.bstack11l11l11ll_opy_:
      return
    try:
      bstack111lllllll1_opy_ = [platform[bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᴉ")].lower() for platform in self.config.get(bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᴊ"), [])]
      bstack111ll1ll11l_opy_ = sys.maxsize
      bstack111lll1l11l_opy_ = bstack11111l_opy_ (u"ࠨࠩᴋ")
      for browser in bstack111lllllll1_opy_:
        if browser in self.bstack111lll1lll1_opy_:
          bstack111ll1llll1_opy_ = self.bstack111lll1lll1_opy_[browser]
        if bstack111ll1llll1_opy_ < bstack111ll1ll11l_opy_:
          bstack111ll1ll11l_opy_ = bstack111ll1llll1_opy_
          bstack111lll1l11l_opy_ = browser
      return bstack111lll1l11l_opy_
    except Exception as e:
      self.logger.error(bstack11111l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡦࡪࡹࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᴌ").format(e))
  @classmethod
  def bstack111l1ll1l_opy_(self):
    return os.getenv(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᴍ"), bstack11111l_opy_ (u"ࠫࡋࡧ࡬ࡴࡧࠪᴎ")).lower()
  @classmethod
  def bstack11llll1ll_opy_(self):
    return os.getenv(bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩᴏ"), bstack11111l_opy_ (u"࠭ࠧᴐ"))
  @classmethod
  def bstack1l1ll1l1l11_opy_(cls, value):
    cls.bstack1ll111llll_opy_ = value
  @classmethod
  def bstack111llllll1l_opy_(cls):
    return cls.bstack1ll111llll_opy_
  @classmethod
  def bstack1l1ll1l1111_opy_(cls, value):
    cls.percy_build_id = value
  @classmethod
  def bstack111llll1l1l_opy_(cls):
    return cls.percy_build_id