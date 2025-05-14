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
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lllll11lll_opy_
from bstack_utils.constants import EVENTS
class bstack1lll11l11l1_opy_(bstack11111llll1_opy_):
    bstack1l11lllllll_opy_ = bstack11111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠧᒿ")
    NAME = bstack11111l_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣᓀ")
    bstack1l1ll111ll1_opy_ = bstack11111l_opy_ (u"ࠢࡩࡷࡥࡣࡺࡸ࡬ࠣᓁ")
    bstack1l1ll111111_opy_ = bstack11111l_opy_ (u"ࠣࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠣᓂ")
    bstack1l1111lll1l_opy_ = bstack11111l_opy_ (u"ࠤ࡬ࡲࡵࡻࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢᓃ")
    bstack1l1ll11ll1l_opy_ = bstack11111l_opy_ (u"ࠥࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤᓄ")
    bstack1l1l111l1l1_opy_ = bstack11111l_opy_ (u"ࠦ࡮ࡹ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡨࡶࡤࠥᓅ")
    bstack1l1111lll11_opy_ = bstack11111l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᓆ")
    bstack1l111l11111_opy_ = bstack11111l_opy_ (u"ࠨࡥ࡯ࡦࡨࡨࡤࡧࡴࠣᓇ")
    bstack1ll1l111l1l_opy_ = bstack11111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᓈ")
    bstack1l1l1l11ll1_opy_ = bstack11111l_opy_ (u"ࠣࡰࡨࡻࡸ࡫ࡳࡴ࡫ࡲࡲࠧᓉ")
    bstack1l1111ll1ll_opy_ = bstack11111l_opy_ (u"ࠤࡪࡩࡹࠨᓊ")
    bstack1ll111l1l1l_opy_ = bstack11111l_opy_ (u"ࠥࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢᓋ")
    bstack1l11llll1ll_opy_ = bstack11111l_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࠢᓌ")
    bstack1l11llll11l_opy_ = bstack11111l_opy_ (u"ࠧࡽ࠳ࡤࡧࡻࡩࡨࡻࡴࡦࡵࡦࡶ࡮ࡶࡴࡢࡵࡼࡲࡨࠨᓍ")
    bstack1l1111llll1_opy_ = bstack11111l_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᓎ")
    bstack1l1111l1lll_opy_: Dict[str, List[Callable]] = dict()
    bstack1l1l11ll1ll_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1llll1111l1_opy_: Any
    bstack1l11lllll1l_opy_: Dict
    def __init__(
        self,
        bstack1l1l11ll1ll_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1llll1111l1_opy_: Dict[str, Any],
        methods=[bstack11111l_opy_ (u"ࠢࡠࡡ࡬ࡲ࡮ࡺ࡟ࡠࠤᓏ"), bstack11111l_opy_ (u"ࠣࡵࡷࡥࡷࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠣᓐ"), bstack11111l_opy_ (u"ࠤࡨࡼࡪࡩࡵࡵࡧࠥᓑ"), bstack11111l_opy_ (u"ࠥࡵࡺ࡯ࡴࠣᓒ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack1l1l11ll1ll_opy_ = bstack1l1l11ll1ll_opy_
        self.platform_index = platform_index
        self.bstack111111l111_opy_(methods)
        self.bstack1llll1111l1_opy_ = bstack1llll1111l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack11111llll1_opy_.get_data(bstack1lll11l11l1_opy_.bstack1l1ll111111_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack11111llll1_opy_.get_data(bstack1lll11l11l1_opy_.bstack1l1ll111ll1_opy_, target, strict)
    @staticmethod
    def bstack1l1111lllll_opy_(target: object, strict=True):
        return bstack11111llll1_opy_.get_data(bstack1lll11l11l1_opy_.bstack1l1111lll1l_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack11111llll1_opy_.get_data(bstack1lll11l11l1_opy_.bstack1l1ll11ll1l_opy_, target, strict)
    @staticmethod
    def bstack1ll1l1111ll_opy_(instance: bstack111111ll1l_opy_) -> bool:
        return bstack11111llll1_opy_.bstack1111111l11_opy_(instance, bstack1lll11l11l1_opy_.bstack1l1l111l1l1_opy_, False)
    @staticmethod
    def bstack1ll1l1lllll_opy_(instance: bstack111111ll1l_opy_, default_value=None):
        return bstack11111llll1_opy_.bstack1111111l11_opy_(instance, bstack1lll11l11l1_opy_.bstack1l1ll111ll1_opy_, default_value)
    @staticmethod
    def bstack1ll1ll11ll1_opy_(instance: bstack111111ll1l_opy_, default_value=None):
        return bstack11111llll1_opy_.bstack1111111l11_opy_(instance, bstack1lll11l11l1_opy_.bstack1l1ll11ll1l_opy_, default_value)
    @staticmethod
    def bstack1ll11ll1l1l_opy_(hub_url: str, bstack1l1111ll1l1_opy_=bstack11111l_opy_ (u"ࠦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠣᓓ")):
        try:
            bstack1l1111ll11l_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack1l1111ll11l_opy_.endswith(bstack1l1111ll1l1_opy_)
        except:
            pass
        return False
    @staticmethod
    def bstack1ll1l11llll_opy_(method_name: str):
        return method_name == bstack11111l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᓔ")
    @staticmethod
    def bstack1ll1l111ll1_opy_(method_name: str, *args):
        return (
            bstack1lll11l11l1_opy_.bstack1ll1l11llll_opy_(method_name)
            and bstack1lll11l11l1_opy_.bstack1l1l1l1111l_opy_(*args) == bstack1lll11l11l1_opy_.bstack1l1l1l11ll1_opy_
        )
    @staticmethod
    def bstack1ll1l1ll11l_opy_(method_name: str, *args):
        if not bstack1lll11l11l1_opy_.bstack1ll1l11llll_opy_(method_name):
            return False
        if not bstack1lll11l11l1_opy_.bstack1l11llll1ll_opy_ in bstack1lll11l11l1_opy_.bstack1l1l1l1111l_opy_(*args):
            return False
        bstack1ll11l1lll1_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll11ll_opy_(*args)
        return bstack1ll11l1lll1_opy_ and bstack11111l_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᓕ") in bstack1ll11l1lll1_opy_ and bstack11111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᓖ") in bstack1ll11l1lll1_opy_[bstack11111l_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᓗ")]
    @staticmethod
    def bstack1ll1l11lll1_opy_(method_name: str, *args):
        if not bstack1lll11l11l1_opy_.bstack1ll1l11llll_opy_(method_name):
            return False
        if not bstack1lll11l11l1_opy_.bstack1l11llll1ll_opy_ in bstack1lll11l11l1_opy_.bstack1l1l1l1111l_opy_(*args):
            return False
        bstack1ll11l1lll1_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll11ll_opy_(*args)
        return (
            bstack1ll11l1lll1_opy_
            and bstack11111l_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᓘ") in bstack1ll11l1lll1_opy_
            and bstack11111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᓙ") in bstack1ll11l1lll1_opy_[bstack11111l_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᓚ")]
        )
    @staticmethod
    def bstack1l1l1l1111l_opy_(*args):
        return str(bstack1lll11l11l1_opy_.bstack1ll1l1l1111_opy_(*args)).lower()
    @staticmethod
    def bstack1ll1l1l1111_opy_(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack1ll11ll11ll_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1lll1lll11_opy_(driver):
        command_executor = getattr(driver, bstack11111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᓛ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack11111l_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᓜ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack11111l_opy_ (u"ࠢࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠣᓝ"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack11111l_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡠࡵࡨࡶࡻ࡫ࡲࡠࡣࡧࡨࡷࠨᓞ"), None)
        return hub_url
    def bstack1l1l1l11111_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack11111l_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠧᓟ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack11111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨᓠ"), hub_url)
                result = True
            elif hasattr(command_executor, bstack11111l_opy_ (u"ࠦࡤࡻࡲ࡭ࠤᓡ")):
                setattr(command_executor, bstack11111l_opy_ (u"ࠧࡥࡵࡳ࡮ࠥᓢ"), hub_url)
                result = True
        if result:
            self.bstack1l1l11ll1ll_opy_ = hub_url
            bstack1lll11l11l1_opy_.bstack1llllllll1l_opy_(instance, bstack1lll11l11l1_opy_.bstack1l1ll111ll1_opy_, hub_url)
            bstack1lll11l11l1_opy_.bstack1llllllll1l_opy_(
                instance, bstack1lll11l11l1_opy_.bstack1l1l111l1l1_opy_, bstack1lll11l11l1_opy_.bstack1ll11ll1l1l_opy_(hub_url)
            )
        return result
    @staticmethod
    def bstack1l11llllll1_opy_(bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_]):
        return bstack11111l_opy_ (u"ࠨ࠺ࠣᓣ").join((bstack1111111l1l_opy_(bstack1111111111_opy_[0]).name, bstack1111l11l11_opy_(bstack1111111111_opy_[1]).name))
    @staticmethod
    def bstack1ll1l111111_opy_(bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_], callback: Callable):
        bstack1l11llll1l1_opy_ = bstack1lll11l11l1_opy_.bstack1l11llllll1_opy_(bstack1111111111_opy_)
        if not bstack1l11llll1l1_opy_ in bstack1lll11l11l1_opy_.bstack1l1111l1lll_opy_:
            bstack1lll11l11l1_opy_.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_] = []
        bstack1lll11l11l1_opy_.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_].append(callback)
    def bstack1111111ll1_opy_(self, instance: bstack111111ll1l_opy_, method_name: str, bstack11111111l1_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack11111l_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᓤ")):
            return
        cmd = args[0] if method_name == bstack11111l_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᓥ") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack1l1111ll111_opy_ = bstack11111l_opy_ (u"ࠤ࠽ࠦᓦ").join(map(str, filter(None, [method_name, cmd])))
        instance.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽ࠦᓧ") + bstack1l1111ll111_opy_, bstack11111111l1_opy_)
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
        bstack1l11llll1l1_opy_ = bstack1lll11l11l1_opy_.bstack1l11llllll1_opy_(bstack1111111111_opy_)
        self.logger.debug(bstack11111l_opy_ (u"ࠦࡴࡴ࡟ࡩࡱࡲ࡯࠿ࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᓨ") + str(kwargs) + bstack11111l_opy_ (u"ࠧࠨᓩ"))
        if bstack111111l1ll_opy_ == bstack1111111l1l_opy_.QUIT:
            if bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.PRE:
                bstack1ll1ll111ll_opy_ = bstack1lllll11lll_opy_.bstack1ll1l11l111_opy_(EVENTS.bstack1l11lllll_opy_.value)
                bstack11111llll1_opy_.bstack1llllllll1l_opy_(instance, EVENTS.bstack1l11lllll_opy_.value, bstack1ll1ll111ll_opy_)
                self.logger.debug(bstack11111l_opy_ (u"ࠨࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥᓪ").format(instance, method_name, bstack111111l1ll_opy_, bstack1l11lllll11_opy_))
        if bstack111111l1ll_opy_ == bstack1111111l1l_opy_.bstack1111l11ll1_opy_:
            if bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.POST and not bstack1lll11l11l1_opy_.bstack1l1ll111111_opy_ in instance.data:
                session_id = getattr(target, bstack11111l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠦᓫ"), None)
                if session_id:
                    instance.data[bstack1lll11l11l1_opy_.bstack1l1ll111111_opy_] = session_id
        elif (
            bstack111111l1ll_opy_ == bstack1111111l1l_opy_.bstack1111l111ll_opy_
            and bstack1lll11l11l1_opy_.bstack1l1l1l1111l_opy_(*args) == bstack1lll11l11l1_opy_.bstack1l1l1l11ll1_opy_
        ):
            if bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.PRE:
                hub_url = bstack1lll11l11l1_opy_.bstack1lll1lll11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            bstack1lll11l11l1_opy_.bstack1l1ll111ll1_opy_: hub_url,
                            bstack1lll11l11l1_opy_.bstack1l1l111l1l1_opy_: bstack1lll11l11l1_opy_.bstack1ll11ll1l1l_opy_(hub_url),
                            bstack1lll11l11l1_opy_.bstack1ll1l111l1l_opy_: int(
                                os.environ.get(bstack11111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᓬ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack1ll11l1lll1_opy_ = bstack1lll11l11l1_opy_.bstack1ll11ll11ll_opy_(*args)
                bstack1l1111lllll_opy_ = bstack1ll11l1lll1_opy_.get(bstack11111l_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᓭ"), None) if bstack1ll11l1lll1_opy_ else None
                if isinstance(bstack1l1111lllll_opy_, dict):
                    instance.data[bstack1lll11l11l1_opy_.bstack1l1111lll1l_opy_] = copy.deepcopy(bstack1l1111lllll_opy_)
                    instance.data[bstack1lll11l11l1_opy_.bstack1l1ll11ll1l_opy_] = bstack1l1111lllll_opy_
            elif bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack11111l_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᓮ"), dict()).get(bstack11111l_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢᓯ"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                bstack1lll11l11l1_opy_.bstack1l1ll111111_opy_: framework_session_id,
                                bstack1lll11l11l1_opy_.bstack1l1111lll11_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack111111l1ll_opy_ == bstack1111111l1l_opy_.bstack1111l111ll_opy_
            and bstack1lll11l11l1_opy_.bstack1l1l1l1111l_opy_(*args) == bstack1lll11l11l1_opy_.bstack1l1111llll1_opy_
            and bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.POST
        ):
            instance.data[bstack1lll11l11l1_opy_.bstack1l111l11111_opy_] = datetime.now(tz=timezone.utc)
        if bstack1l11llll1l1_opy_ in bstack1lll11l11l1_opy_.bstack1l1111l1lll_opy_:
            bstack1l1l111111l_opy_ = None
            for callback in bstack1lll11l11l1_opy_.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_]:
                try:
                    bstack1l1l1111111_opy_ = callback(self, target, exec, bstack1111111111_opy_, result, *args, **kwargs)
                    if bstack1l1l111111l_opy_ == None:
                        bstack1l1l111111l_opy_ = bstack1l1l1111111_opy_
                except Exception as e:
                    self.logger.error(bstack11111l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᓰ") + str(e) + bstack11111l_opy_ (u"ࠨࠢᓱ"))
                    traceback.print_exc()
            if bstack111111l1ll_opy_ == bstack1111111l1l_opy_.QUIT:
                if bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.POST:
                    bstack1ll1ll111ll_opy_ = bstack11111llll1_opy_.bstack1111111l11_opy_(instance, EVENTS.bstack1l11lllll_opy_.value)
                    if bstack1ll1ll111ll_opy_!=None:
                        bstack1lllll11lll_opy_.end(EVENTS.bstack1l11lllll_opy_.value, bstack1ll1ll111ll_opy_+bstack11111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᓲ"), bstack1ll1ll111ll_opy_+bstack11111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᓳ"), True, None)
            if bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.PRE and callable(bstack1l1l111111l_opy_):
                return bstack1l1l111111l_opy_
            elif bstack1l11lllll11_opy_ == bstack1111l11l11_opy_.POST and bstack1l1l111111l_opy_:
                return bstack1l1l111111l_opy_
    def bstack11111l1lll_opy_(
        self, method_name, previous_state: bstack1111111l1l_opy_, *args, **kwargs
    ) -> bstack1111111l1l_opy_:
        if method_name == bstack11111l_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦᓴ") or method_name == bstack11111l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࠥᓵ"):
            return bstack1111111l1l_opy_.bstack1111l11ll1_opy_
        if method_name == bstack11111l_opy_ (u"ࠦࡶࡻࡩࡵࠤᓶ"):
            return bstack1111111l1l_opy_.QUIT
        if method_name == bstack11111l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᓷ"):
            if previous_state != bstack1111111l1l_opy_.NONE:
                bstack1ll11llll1l_opy_ = bstack1lll11l11l1_opy_.bstack1l1l1l1111l_opy_(*args)
                if bstack1ll11llll1l_opy_ == bstack1lll11l11l1_opy_.bstack1l1l1l11ll1_opy_:
                    return bstack1111111l1l_opy_.bstack1111l11ll1_opy_
            return bstack1111111l1l_opy_.bstack1111l111ll_opy_
        return bstack1111111l1l_opy_.NONE