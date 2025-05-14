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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.accessibility as bstack11l1ll1l1_opy_
from browserstack_sdk.bstack11l11l1ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1l1l1l1_opy_
class bstack1llllll11_opy_:
    def __init__(self, args, logger, bstack1111ll1l11_opy_, bstack1111llll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111ll1l11_opy_ = bstack1111ll1l11_opy_
        self.bstack1111llll11_opy_ = bstack1111llll11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11lll111l1_opy_ = []
        self.bstack1111llll1l_opy_ = None
        self.bstack1l111l1l1_opy_ = []
        self.bstack111l111l1l_opy_ = self.bstack1l1111l1l1_opy_()
        self.bstack1l11l111l1_opy_ = -1
    def bstack11llll11ll_opy_(self, bstack1111lll1l1_opy_):
        self.parse_args()
        self.bstack111l1111l1_opy_()
        self.bstack1111lllll1_opy_(bstack1111lll1l1_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack1111ll1l1l_opy_():
        import importlib
        if getattr(importlib, bstack11111l_opy_ (u"ࠨࡨ࡬ࡲࡩࡥ࡬ࡰࡣࡧࡩࡷ࠭࿫"), False):
            bstack111l111111_opy_ = importlib.find_loader(bstack11111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ࿬"))
        else:
            bstack111l111111_opy_ = importlib.util.find_spec(bstack11111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ࿭"))
    def bstack1111ll1ll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l11l111l1_opy_ = -1
        if self.bstack1111llll11_opy_ and bstack11111l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ࿮") in self.bstack1111ll1l11_opy_:
            self.bstack1l11l111l1_opy_ = int(self.bstack1111ll1l11_opy_[bstack11111l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ࿯")])
        try:
            bstack111l1111ll_opy_ = [bstack11111l_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ࿰"), bstack11111l_opy_ (u"ࠧ࠮࠯ࡳࡰࡺ࡭ࡩ࡯ࡵࠪ࿱"), bstack11111l_opy_ (u"ࠨ࠯ࡳࠫ࿲")]
            if self.bstack1l11l111l1_opy_ >= 0:
                bstack111l1111ll_opy_.extend([bstack11111l_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ࿳"), bstack11111l_opy_ (u"ࠪ࠱ࡳ࠭࿴")])
            for arg in bstack111l1111ll_opy_:
                self.bstack1111ll1ll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack111l1111l1_opy_(self):
        bstack1111llll1l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1111llll1l_opy_ = bstack1111llll1l_opy_
        return bstack1111llll1l_opy_
    def bstack11lll1lll1_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack1111ll1l1l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l1l1l1l1_opy_)
    def bstack1111lllll1_opy_(self, bstack1111lll1l1_opy_):
        bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
        if bstack1111lll1l1_opy_:
            self.bstack1111llll1l_opy_.append(bstack11111l_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ࿵"))
            self.bstack1111llll1l_opy_.append(bstack11111l_opy_ (u"࡚ࠬࡲࡶࡧࠪ࿶"))
        if bstack1l11l11ll1_opy_.bstack1111lll111_opy_():
            self.bstack1111llll1l_opy_.append(bstack11111l_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ࿷"))
            self.bstack1111llll1l_opy_.append(bstack11111l_opy_ (u"ࠧࡕࡴࡸࡩࠬ࿸"))
        self.bstack1111llll1l_opy_.append(bstack11111l_opy_ (u"ࠨ࠯ࡳࠫ࿹"))
        self.bstack1111llll1l_opy_.append(bstack11111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧ࿺"))
        self.bstack1111llll1l_opy_.append(bstack11111l_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ࿻"))
        self.bstack1111llll1l_opy_.append(bstack11111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ࿼"))
        if self.bstack1l11l111l1_opy_ > 1:
            self.bstack1111llll1l_opy_.append(bstack11111l_opy_ (u"ࠬ࠳࡮ࠨ࿽"))
            self.bstack1111llll1l_opy_.append(str(self.bstack1l11l111l1_opy_))
    def bstack1111lll1ll_opy_(self):
        bstack1l111l1l1_opy_ = []
        for spec in self.bstack11lll111l1_opy_:
            bstack11lll1ll_opy_ = [spec]
            bstack11lll1ll_opy_ += self.bstack1111llll1l_opy_
            bstack1l111l1l1_opy_.append(bstack11lll1ll_opy_)
        self.bstack1l111l1l1_opy_ = bstack1l111l1l1_opy_
        return bstack1l111l1l1_opy_
    def bstack1l1111l1l1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111l111l1l_opy_ = True
            return True
        except Exception as e:
            self.bstack111l111l1l_opy_ = False
        return self.bstack111l111l1l_opy_
    def bstack111l11111_opy_(self, bstack111l11111l_opy_, bstack11llll11ll_opy_):
        bstack11llll11ll_opy_[bstack11111l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭࿾")] = self.bstack1111ll1l11_opy_
        multiprocessing.set_start_method(bstack11111l_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭࿿"))
        bstack1ll11l1l1l_opy_ = []
        manager = multiprocessing.Manager()
        bstack1111ll1lll_opy_ = manager.list()
        if bstack11111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫက") in self.bstack1111ll1l11_opy_:
            for index, platform in enumerate(self.bstack1111ll1l11_opy_[bstack11111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬခ")]):
                bstack1ll11l1l1l_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack111l11111l_opy_,
                                                            args=(self.bstack1111llll1l_opy_, bstack11llll11ll_opy_, bstack1111ll1lll_opy_)))
            bstack111l111l11_opy_ = len(self.bstack1111ll1l11_opy_[bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ဂ")])
        else:
            bstack1ll11l1l1l_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack111l11111l_opy_,
                                                        args=(self.bstack1111llll1l_opy_, bstack11llll11ll_opy_, bstack1111ll1lll_opy_)))
            bstack111l111l11_opy_ = 1
        i = 0
        for t in bstack1ll11l1l1l_opy_:
            os.environ[bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫဃ")] = str(i)
            if bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨင") in self.bstack1111ll1l11_opy_:
                os.environ[bstack11111l_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧစ")] = json.dumps(self.bstack1111ll1l11_opy_[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪဆ")][i % bstack111l111l11_opy_])
            i += 1
            t.start()
        for t in bstack1ll11l1l1l_opy_:
            t.join()
        return list(bstack1111ll1lll_opy_)
    @staticmethod
    def bstack1ll1111ll_opy_(driver, bstack1111llllll_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬဇ"), None)
        if item and getattr(item, bstack11111l_opy_ (u"ࠩࡢࡥ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࠫဈ"), None) and not getattr(item, bstack11111l_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡴࡶ࡟ࡥࡱࡱࡩࠬဉ"), False):
            logger.info(
                bstack11111l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠢࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡮ࡹࠠࡶࡰࡧࡩࡷࡽࡡࡺ࠰ࠥည"))
            bstack1111lll11l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11l1ll1l1_opy_.bstack11ll11l1ll_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)