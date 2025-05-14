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
from bstack_utils.bstack11ll1ll1l1_opy_ import get_logger
logger = get_logger(__name__)
class bstack11lll1l11l1_opy_(object):
  bstack11lll1ll1l_opy_ = os.path.join(os.path.expanduser(bstack11111l_opy_ (u"࠭ࡾࠨᙁ")), bstack11111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᙂ"))
  bstack11lll1l1111_opy_ = os.path.join(bstack11lll1ll1l_opy_, bstack11111l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨᙃ"))
  commands_to_wrap = None
  perform_scan = None
  bstack1l11llll1l_opy_ = None
  bstack1ll1l1111l_opy_ = None
  bstack11llll1l11l_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11111l_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫᙄ")):
      cls.instance = super(bstack11lll1l11l1_opy_, cls).__new__(cls)
      cls.instance.bstack11lll1l11ll_opy_()
    return cls.instance
  def bstack11lll1l11ll_opy_(self):
    try:
      with open(self.bstack11lll1l1111_opy_, bstack11111l_opy_ (u"ࠪࡶࠬᙅ")) as bstack1llll1111l_opy_:
        bstack11lll1l111l_opy_ = bstack1llll1111l_opy_.read()
        data = json.loads(bstack11lll1l111l_opy_)
        if bstack11111l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᙆ") in data:
          self.bstack11lll1l1l11_opy_(data[bstack11111l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᙇ")])
        if bstack11111l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧᙈ") in data:
          self.bstack11lll1111_opy_(data[bstack11111l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᙉ")])
    except:
      pass
  def bstack11lll1111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts.get(bstack11111l_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᙊ"),bstack11111l_opy_ (u"ࠩࠪᙋ"))
      self.bstack1l11llll1l_opy_ = scripts.get(bstack11111l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧᙌ"),bstack11111l_opy_ (u"ࠫࠬᙍ"))
      self.bstack1ll1l1111l_opy_ = scripts.get(bstack11111l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩᙎ"),bstack11111l_opy_ (u"࠭ࠧᙏ"))
      self.bstack11llll1l11l_opy_ = scripts.get(bstack11111l_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᙐ"),bstack11111l_opy_ (u"ࠨࠩᙑ"))
  def bstack11lll1l1l11_opy_(self, commands_to_wrap):
    if commands_to_wrap != None and len(commands_to_wrap) != 0:
      self.commands_to_wrap = commands_to_wrap
  def store(self):
    try:
      with open(self.bstack11lll1l1111_opy_, bstack11111l_opy_ (u"ࠩࡺࠫᙒ")) as file:
        json.dump({
          bstack11111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧᙓ"): self.commands_to_wrap,
          bstack11111l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧᙔ"): {
            bstack11111l_opy_ (u"ࠧࡹࡣࡢࡰࠥᙕ"): self.perform_scan,
            bstack11111l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᙖ"): self.bstack1l11llll1l_opy_,
            bstack11111l_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᙗ"): self.bstack1ll1l1111l_opy_,
            bstack11111l_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᙘ"): self.bstack11llll1l11l_opy_
          }
        }, file)
    except Exception as e:
      logger.error(bstack11111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡶࡲࡶ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡵ࠽ࠤࢀࢃࠢᙙ").format(e))
      pass
  def bstack11l1l1l111_opy_(self, bstack1ll11llll1l_opy_):
    try:
      return any(command.get(bstack11111l_opy_ (u"ࠪࡲࡦࡳࡥࠨᙚ")) == bstack1ll11llll1l_opy_ for command in self.commands_to_wrap)
    except:
      return False
bstack1l1l1ll111_opy_ = bstack11lll1l11l1_opy_()