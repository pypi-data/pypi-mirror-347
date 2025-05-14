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
import multiprocessing
import os
from bstack_utils.config import Config
class bstack11l11l11_opy_():
  def __init__(self, args, logger, bstack1111ll1l11_opy_, bstack1111llll11_opy_, bstack1111ll11ll_opy_):
    self.args = args
    self.logger = logger
    self.bstack1111ll1l11_opy_ = bstack1111ll1l11_opy_
    self.bstack1111llll11_opy_ = bstack1111llll11_opy_
    self.bstack1111ll11ll_opy_ = bstack1111ll11ll_opy_
  def bstack111l11111_opy_(self, bstack111l11111l_opy_, bstack11llll11ll_opy_, bstack1111ll11l1_opy_=False):
    bstack1ll11l1l1l_opy_ = []
    manager = multiprocessing.Manager()
    bstack1111ll1lll_opy_ = manager.list()
    bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
    if bstack1111ll11l1_opy_:
      for index, platform in enumerate(self.bstack1111ll1l11_opy_[bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨဋ")]):
        if index == 0:
          bstack11llll11ll_opy_[bstack11111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩဌ")] = self.args
        bstack1ll11l1l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l11111l_opy_,
                                                    args=(bstack11llll11ll_opy_, bstack1111ll1lll_opy_)))
    else:
      for index, platform in enumerate(self.bstack1111ll1l11_opy_[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဍ")]):
        bstack1ll11l1l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                    target=bstack111l11111l_opy_,
                                                    args=(bstack11llll11ll_opy_, bstack1111ll1lll_opy_)))
    i = 0
    for t in bstack1ll11l1l1l_opy_:
      try:
        if bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩဎ")):
          os.environ[bstack11111l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪဏ")] = json.dumps(self.bstack1111ll1l11_opy_[bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭တ")][i % self.bstack1111ll11ll_opy_])
      except Exception as e:
        self.logger.debug(bstack11111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹ࠺ࠡࡽࢀࠦထ").format(str(e)))
      i += 1
      t.start()
    for t in bstack1ll11l1l1l_opy_:
      t.join()
    return list(bstack1111ll1lll_opy_)