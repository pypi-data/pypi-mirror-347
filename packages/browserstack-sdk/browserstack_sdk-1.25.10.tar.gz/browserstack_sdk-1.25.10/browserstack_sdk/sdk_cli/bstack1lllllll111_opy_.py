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
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.bstack11111l1111_opy_ import (
    bstack11111llll1_opy_,
    bstack111111ll1l_opy_,
    bstack1111111l1l_opy_,
    bstack1111l11l11_opy_,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack1llllll1lll_opy_(bstack11111llll1_opy_):
    bstack1l11lllllll_opy_ = bstack11111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣፖ")
    bstack1l1ll111111_opy_ = bstack11111l_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤፗ")
    bstack1l1ll111ll1_opy_ = bstack11111l_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦፘ")
    bstack1l1ll11ll1l_opy_ = bstack11111l_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥፙ")
    bstack1l11llll1ll_opy_ = bstack11111l_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࠣፚ")
    bstack1l11llll11l_opy_ = bstack11111l_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࡣࡶࡽࡳࡩࠢ፛")
    NAME = bstack11111l_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ፜")
    bstack1l1l11111l1_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll1111l1_opy_: Any
    bstack1l11lllll1l_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack11111l_opy_ (u"ࠣ࡮ࡤࡹࡳࡩࡨࠣ፝"), bstack11111l_opy_ (u"ࠤࡦࡳࡳࡴࡥࡤࡶࠥ፞"), bstack11111l_opy_ (u"ࠥࡲࡪࡽ࡟ࡱࡣࡪࡩࠧ፟"), bstack11111l_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥ፠"), bstack11111l_opy_ (u"ࠧࡪࡩࡴࡲࡤࡸࡨ࡮ࠢ፡")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack111111l111_opy_(methods)
    def bstack1111111ll1_opy_(self, instance: bstack111111ll1l_opy_, method_name: str, bstack11111111l1_opy_: timedelta, *args, **kwargs):
        pass
    def bstack11111ll1l1_opy_(
        self,
        target: object,
        exec: Tuple[bstack111111ll1l_opy_, str],
        bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack111111l1ll_opy_, bstack1l11lllll11_opy_ = bstack1111111111_opy_
        bstack1l11llll1l1_opy_ = bstack1llllll1lll_opy_.bstack1l11llllll1_opy_(bstack1111111111_opy_)
        if bstack1l11llll1l1_opy_ in bstack1llllll1lll_opy_.bstack1l1l11111l1_opy_:
            bstack1l1l111111l_opy_ = None
            for callback in bstack1llllll1lll_opy_.bstack1l1l11111l1_opy_[bstack1l11llll1l1_opy_]:
                try:
                    bstack1l1l1111111_opy_ = callback(self, target, exec, bstack1111111111_opy_, result, *args, **kwargs)
                    if bstack1l1l111111l_opy_ == None:
                        bstack1l1l111111l_opy_ = bstack1l1l1111111_opy_
                except Exception as e:
                    self.logger.error(bstack11111l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡯࡮ࡷࡱ࡮࡭ࡳ࡭ࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬࠼ࠣࠦ።") + str(e) + bstack11111l_opy_ (u"ࠢࠣ፣"))
                    traceback.print_exc()
            if bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.PRE and callable(bstack1l1l111111l_opy_):
                return bstack1l1l111111l_opy_
            elif bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.POST and bstack1l1l111111l_opy_:
                return bstack1l1l111111l_opy_
    def bstack11111l1lll_opy_(
        self, method_name, previous_state: bstack1111111l1l_opy_, *args, **kwargs
    ) -> bstack1111111l1l_opy_:
        if method_name == bstack11111l_opy_ (u"ࠨ࡮ࡤࡹࡳࡩࡨࠨ፤") or method_name == bstack11111l_opy_ (u"ࠩࡦࡳࡳࡴࡥࡤࡶࠪ፥") or method_name == bstack11111l_opy_ (u"ࠪࡲࡪࡽ࡟ࡱࡣࡪࡩࠬ፦"):
            return bstack1111111l1l_opy_.bstack1111l11ll1_opy_
        if method_name == bstack11111l_opy_ (u"ࠫࡩ࡯ࡳࡱࡣࡷࡧ࡭࠭፧"):
            return bstack1111111l1l_opy_.bstack11111l1l1l_opy_
        if method_name == bstack11111l_opy_ (u"ࠬࡩ࡬ࡰࡵࡨࠫ፨"):
            return bstack1111111l1l_opy_.QUIT
        return bstack1111111l1l_opy_.NONE
    @staticmethod
    def bstack1l11llllll1_opy_(bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_]):
        return bstack11111l_opy_ (u"ࠨ࠺ࠣ፩").join((bstack1111111l1l_opy_(bstack1111111111_opy_[0]).name, bstack1111l11l11_opy_(bstack1111111111_opy_[1]).name))
    @staticmethod
    def bstack1ll1l111111_opy_(bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_], callback: Callable):
        bstack1l11llll1l1_opy_ = bstack1llllll1lll_opy_.bstack1l11llllll1_opy_(bstack1111111111_opy_)
        if not bstack1l11llll1l1_opy_ in bstack1llllll1lll_opy_.bstack1l1l11111l1_opy_:
            bstack1llllll1lll_opy_.bstack1l1l11111l1_opy_[bstack1l11llll1l1_opy_] = []
        bstack1llllll1lll_opy_.bstack1l1l11111l1_opy_[bstack1l11llll1l1_opy_].append(callback)
    @staticmethod
    def bstack1ll1l11llll_opy_(method_name: str):
        return True
    @staticmethod
    def bstack1ll1l111ll1_opy_(method_name: str, *args) -> bool:
        return True
    @staticmethod
    def bstack1ll1ll11ll1_opy_(instance: bstack111111ll1l_opy_, default_value=None):
        return bstack11111llll1_opy_.bstack1111111l11_opy_(instance, bstack1llllll1lll_opy_.bstack1l1ll11ll1l_opy_, default_value)
    @staticmethod
    def bstack1ll1l1111ll_opy_(instance: bstack111111ll1l_opy_) -> bool:
        return True
    @staticmethod
    def bstack1ll1l1lllll_opy_(instance: bstack111111ll1l_opy_, default_value=None):
        return bstack11111llll1_opy_.bstack1111111l11_opy_(instance, bstack1llllll1lll_opy_.bstack1l1ll111ll1_opy_, default_value)
    @staticmethod
    def bstack1ll1l1l1111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll1l1ll11l_opy_(method_name: str, *args):
        if not bstack1llllll1lll_opy_.bstack1ll1l11llll_opy_(method_name):
            return False
        if not bstack1llllll1lll_opy_.bstack1l11llll1ll_opy_ in bstack1llllll1lll_opy_.bstack1l1l1l1111l_opy_(*args):
            return False
        bstack1ll11l1lll1_opy_ = bstack1llllll1lll_opy_.bstack1ll11ll11ll_opy_(*args)
        return bstack1ll11l1lll1_opy_ and bstack11111l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࠢ፪") in bstack1ll11l1lll1_opy_ and bstack11111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠤ፫") in bstack1ll11l1lll1_opy_[bstack11111l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤ፬")]
    @staticmethod
    def bstack1ll1l11lll1_opy_(method_name: str, *args):
        if not bstack1llllll1lll_opy_.bstack1ll1l11llll_opy_(method_name):
            return False
        if not bstack1llllll1lll_opy_.bstack1l11llll1ll_opy_ in bstack1llllll1lll_opy_.bstack1l1l1l1111l_opy_(*args):
            return False
        bstack1ll11l1lll1_opy_ = bstack1llllll1lll_opy_.bstack1ll11ll11ll_opy_(*args)
        return (
            bstack1ll11l1lll1_opy_
            and bstack11111l_opy_ (u"ࠥࡷࡨࡸࡩࡱࡶࠥ፭") in bstack1ll11l1lll1_opy_
            and bstack11111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡥࡵ࡭ࡵࡺࠢ፮") in bstack1ll11l1lll1_opy_[bstack11111l_opy_ (u"ࠧࡹࡣࡳ࡫ࡳࡸࠧ፯")]
        )
    @staticmethod
    def bstack1l1l1l1111l_opy_(*args):
        return str(bstack1llllll1lll_opy_.bstack1ll1l1l1111_opy_(*args)).lower()