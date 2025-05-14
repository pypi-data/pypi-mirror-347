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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack11111lllll_opy_ import bstack111111lll1_opy_
from browserstack_sdk.sdk_cli.utils.bstack11l1l11l1_opy_ import bstack1l11ll11l1l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll11l1ll1_opy_,
    bstack1lll1ll1lll_opy_,
    bstack1ll1lll1lll_opy_,
    bstack1l11l1l11l1_opy_,
    bstack1ll1llll111_opy_,
)
import traceback
from bstack_utils.helper import bstack1l1lllll1l1_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lllll11lll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1llll11l111_opy_ import bstack1lll1111l11_opy_
from browserstack_sdk.sdk_cli.bstack1111l1ll1l_opy_ import bstack1111l1l11l_opy_
bstack1l1lll1ll1l_opy_ = bstack1l1lllll1l1_opy_()
bstack1l1llll111l_opy_ = bstack11111l_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨ፰")
bstack1l11l111l1l_opy_ = bstack11111l_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥ፱")
bstack1l111llllll_opy_ = bstack11111l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ፲")
bstack1l11lll1l1l_opy_ = 1.0
_1l1llllll11_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11l1ll1l1_opy_ = bstack11111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤ፳")
    bstack1l11ll111ll_opy_ = bstack11111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣ፴")
    bstack1l11l111ll1_opy_ = bstack11111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥ፵")
    bstack1l111ll1111_opy_ = bstack11111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢ፶")
    bstack1l11ll1l111_opy_ = bstack11111l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤ፷")
    bstack1l11ll1111l_opy_: bool
    bstack1111l1ll1l_opy_: bstack1111l1l11l_opy_  = None
    bstack1l111l1l1l1_opy_ = [
        bstack1lll11l1ll1_opy_.BEFORE_ALL,
        bstack1lll11l1ll1_opy_.AFTER_ALL,
        bstack1lll11l1ll1_opy_.BEFORE_EACH,
        bstack1lll11l1ll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l1ll1l_opy_: Dict[str, str],
        bstack1ll1ll11lll_opy_: List[str]=[bstack11111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ፸")],
        bstack1111l1ll1l_opy_: bstack1111l1l11l_opy_ = None,
        bstack1lll11l11ll_opy_=None
    ):
        super().__init__(bstack1ll1ll11lll_opy_, bstack1l111l1ll1l_opy_, bstack1111l1ll1l_opy_)
        self.bstack1l11ll1111l_opy_ = any(bstack11111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧ፹") in item.lower() for item in bstack1ll1ll11lll_opy_)
        self.bstack1lll11l11ll_opy_ = bstack1lll11l11ll_opy_
    def track_event(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll11l1ll1_opy_,
        test_hook_state: bstack1ll1lll1lll_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll11l1ll1_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l111l1l1l1_opy_:
            bstack1l11ll11l1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll11l1ll1_opy_.NONE:
            self.logger.warning(bstack11111l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥ፺") + str(test_hook_state) + bstack11111l_opy_ (u"ࠥࠦ፻"))
            return
        if not self.bstack1l11ll1111l_opy_:
            self.logger.warning(bstack11111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧ፼") + str(str(self.bstack1ll1ll11lll_opy_)) + bstack11111l_opy_ (u"ࠧࠨ፽"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ፾") + str(kwargs) + bstack11111l_opy_ (u"ࠢࠣ፿"))
            return
        instance = self.__1l111l1l1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11111l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢᎀ") + str(args) + bstack11111l_opy_ (u"ࠤࠥᎁ"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1l1l1_opy_ and test_hook_state == bstack1ll1lll1lll_opy_.PRE:
                bstack1ll1ll111ll_opy_ = bstack1lllll11lll_opy_.bstack1ll1l11l111_opy_(EVENTS.bstack1l11lll1l1_opy_.value)
                name = str(EVENTS.bstack1l11lll1l1_opy_.name)+bstack11111l_opy_ (u"ࠥ࠾ࠧᎂ")+str(test_framework_state.name)
                TestFramework.bstack1l11l111lll_opy_(instance, name, bstack1ll1ll111ll_opy_)
        except Exception as e:
            self.logger.debug(bstack11111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᎃ").format(e))
        try:
            if test_framework_state == bstack1lll11l1ll1_opy_.TEST:
                if not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l11l1lll1l_opy_) and test_hook_state == bstack1ll1lll1lll_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11l1ll11l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack11111l_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᎄ") + str(test_hook_state) + bstack11111l_opy_ (u"ࠨࠢᎅ"))
                if test_hook_state == bstack1ll1lll1lll_opy_.PRE and not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll1111l1ll_opy_):
                    TestFramework.bstack1llllllll1l_opy_(instance, TestFramework.bstack1ll1111l1ll_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11l1lllll_opy_(instance, args)
                    self.logger.debug(bstack11111l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᎆ") + str(test_hook_state) + bstack11111l_opy_ (u"ࠣࠤᎇ"))
                elif test_hook_state == bstack1ll1lll1lll_opy_.POST and not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1lll111l1_opy_):
                    TestFramework.bstack1llllllll1l_opy_(instance, TestFramework.bstack1l1lll111l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11111l_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᎈ") + str(test_hook_state) + bstack11111l_opy_ (u"ࠥࠦᎉ"))
            elif test_framework_state == bstack1lll11l1ll1_opy_.STEP:
                if test_hook_state == bstack1ll1lll1lll_opy_.PRE:
                    PytestBDDFramework.__1l111l1lll1_opy_(instance, args)
                elif test_hook_state == bstack1ll1lll1lll_opy_.POST:
                    PytestBDDFramework.__1l11lll11l1_opy_(instance, args)
            elif test_framework_state == bstack1lll11l1ll1_opy_.LOG and test_hook_state == bstack1ll1lll1lll_opy_.POST:
                PytestBDDFramework.__1l11l1ll111_opy_(instance, *args)
            elif test_framework_state == bstack1lll11l1ll1_opy_.LOG_REPORT and test_hook_state == bstack1ll1lll1lll_opy_.POST:
                self.__1l11ll1ll1l_opy_(instance, *args)
                self.__1l111ll1ll1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l111l1l1l1_opy_:
                self.__1l11l111l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᎊ") + str(instance.ref()) + bstack11111l_opy_ (u"ࠧࠨᎋ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111lll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l111l1l1l1_opy_ and test_hook_state == bstack1ll1lll1lll_opy_.POST:
                name = str(EVENTS.bstack1l11lll1l1_opy_.name)+bstack11111l_opy_ (u"ࠨ࠺ࠣᎌ")+str(test_framework_state.name)
                bstack1ll1ll111ll_opy_ = TestFramework.bstack1l111ll11ll_opy_(instance, name)
                bstack1lllll11lll_opy_.end(EVENTS.bstack1l11lll1l1_opy_.value, bstack1ll1ll111ll_opy_+bstack11111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᎍ"), bstack1ll1ll111ll_opy_+bstack11111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᎎ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᎏ").format(e))
    def bstack1l1lllll1ll_opy_(self):
        return self.bstack1l11ll1111l_opy_
    def __1l11ll11l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢ᎐"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1llll1ll1_opy_(rep, [bstack11111l_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤ᎑"), bstack11111l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨ᎒"), bstack11111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ᎓"), bstack11111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ᎔"), bstack11111l_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤ᎕"), bstack11111l_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣ᎖")])
        return None
    def __1l11ll1ll1l_opy_(self, instance: bstack1lll1ll1lll_opy_, *args):
        result = self.__1l11ll11l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll111l_opy_ = None
        if result.get(bstack11111l_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦ᎗"), None) == bstack11111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ᎘") and len(args) > 1 and getattr(args[1], bstack11111l_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨ᎙"), None) is not None:
            failure = [{bstack11111l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩ᎚"): [args[1].excinfo.exconly(), result.get(bstack11111l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨ᎛"), None)]}]
            bstack1111ll111l_opy_ = bstack11111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤ᎜") if bstack11111l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ᎝") in getattr(args[1].excinfo, bstack11111l_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧ᎞"), bstack11111l_opy_ (u"ࠦࠧ᎟")) else bstack11111l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᎠ")
        bstack1l111ll1lll_opy_ = result.get(bstack11111l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᎡ"), TestFramework.bstack1l11l11ll11_opy_)
        if bstack1l111ll1lll_opy_ != TestFramework.bstack1l11l11ll11_opy_:
            TestFramework.bstack1llllllll1l_opy_(instance, TestFramework.bstack1ll111111ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l1l1l11_opy_(instance, {
            TestFramework.bstack1l1l1ll1111_opy_: failure,
            TestFramework.bstack1l11l111111_opy_: bstack1111ll111l_opy_,
            TestFramework.bstack1l1l1l1llll_opy_: bstack1l111ll1lll_opy_,
        })
    def __1l111l1l1ll_opy_(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll11l1ll1_opy_,
        test_hook_state: bstack1ll1lll1lll_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll11l1ll1_opy_.SETUP_FIXTURE:
            instance = self.__1l11l1l1l1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11ll1llll_opy_ bstack1l111ll11l1_opy_ this to be bstack11111l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᎢ")
            if test_framework_state == bstack1lll11l1ll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11lll1ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11l1ll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11111l_opy_ (u"ࠣࡰࡲࡨࡪࠨᎣ"), None), bstack11111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᎤ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11111l_opy_ (u"ࠥࡲࡴࡪࡥࠣᎥ"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack11111l_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᎦ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack1llllllllll_opy_(target) if target else None
        return instance
    def __1l11l111l11_opy_(
        self,
        instance: bstack1lll1ll1lll_opy_,
        test_framework_state: bstack1lll11l1ll1_opy_,
        test_hook_state: bstack1ll1lll1lll_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l11lll1l11_opy_ = TestFramework.bstack1111111l11_opy_(instance, PytestBDDFramework.bstack1l11ll111ll_opy_, {})
        if not key in bstack1l11lll1l11_opy_:
            bstack1l11lll1l11_opy_[key] = []
        bstack1l11ll11111_opy_ = TestFramework.bstack1111111l11_opy_(instance, PytestBDDFramework.bstack1l11l111ll1_opy_, {})
        if not key in bstack1l11ll11111_opy_:
            bstack1l11ll11111_opy_[key] = []
        bstack1l111llll11_opy_ = {
            PytestBDDFramework.bstack1l11ll111ll_opy_: bstack1l11lll1l11_opy_,
            PytestBDDFramework.bstack1l11l111ll1_opy_: bstack1l11ll11111_opy_,
        }
        if test_hook_state == bstack1ll1lll1lll_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack11111l_opy_ (u"ࠧࡱࡥࡺࠤᎧ"): key,
                TestFramework.bstack1l11ll11ll1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1llll1_opy_: TestFramework.bstack1l11l11l1ll_opy_,
                TestFramework.bstack1l111ll111l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l1l1ll1_opy_: [],
                TestFramework.bstack1l111l1l11l_opy_: hook_name,
                TestFramework.bstack1l11ll1l1ll_opy_: bstack1lll1111l11_opy_.bstack1l11l1ll1ll_opy_()
            }
            bstack1l11lll1l11_opy_[key].append(hook)
            bstack1l111llll11_opy_[PytestBDDFramework.bstack1l111ll1111_opy_] = key
        elif test_hook_state == bstack1ll1lll1lll_opy_.POST:
            bstack1l111lll1l1_opy_ = bstack1l11lll1l11_opy_.get(key, [])
            hook = bstack1l111lll1l1_opy_.pop() if bstack1l111lll1l1_opy_ else None
            if hook:
                result = self.__1l11ll11l11_opy_(*args)
                if result:
                    bstack1l11lll11ll_opy_ = result.get(bstack11111l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᎨ"), TestFramework.bstack1l11l11l1ll_opy_)
                    if bstack1l11lll11ll_opy_ != TestFramework.bstack1l11l11l1ll_opy_:
                        hook[TestFramework.bstack1l11l1llll1_opy_] = bstack1l11lll11ll_opy_
                hook[TestFramework.bstack1l11l11lll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11ll1l1ll_opy_] = bstack1lll1111l11_opy_.bstack1l11l1ll1ll_opy_()
                self.bstack1l11ll111l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l1ll11_opy_, [])
                self.bstack1ll111lllll_opy_(instance, logs)
                bstack1l11ll11111_opy_[key].append(hook)
                bstack1l111llll11_opy_[PytestBDDFramework.bstack1l11ll1l111_opy_] = key
        TestFramework.bstack1l11l1l1l11_opy_(instance, bstack1l111llll11_opy_)
        self.logger.debug(bstack11111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᎩ") + str(bstack1l11ll11111_opy_) + bstack11111l_opy_ (u"ࠣࠤᎪ"))
    def __1l11l1l1l1l_opy_(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll11l1ll1_opy_,
        test_hook_state: bstack1ll1lll1lll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1llll1ll1_opy_(args[0], [bstack11111l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᎫ"), bstack11111l_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᎬ"), bstack11111l_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᎭ"), bstack11111l_opy_ (u"ࠧ࡯ࡤࡴࠤᎮ"), bstack11111l_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᎯ"), bstack11111l_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᎰ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack11111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᎱ")) else fixturedef.get(bstack11111l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᎲ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11111l_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᎳ")) else None
        node = request.node if hasattr(request, bstack11111l_opy_ (u"ࠦࡳࡵࡤࡦࠤᎴ")) else None
        target = request.node.nodeid if hasattr(node, bstack11111l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᎵ")) else None
        baseid = fixturedef.get(bstack11111l_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᎶ"), None) or bstack11111l_opy_ (u"ࠢࠣᎷ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11111l_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᎸ")):
            target = PytestBDDFramework.__1l111ll1l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11111l_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᎹ")) else None
            if target and not TestFramework.bstack1llllllllll_opy_(target):
                self.__1l11lll1ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᎺ") + str(test_hook_state) + bstack11111l_opy_ (u"ࠦࠧᎻ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᎼ") + str(target) + bstack11111l_opy_ (u"ࠨࠢᎽ"))
            return None
        instance = TestFramework.bstack1llllllllll_opy_(target)
        if not instance:
            self.logger.warning(bstack11111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᎾ") + str(target) + bstack11111l_opy_ (u"ࠣࠤᎿ"))
            return None
        bstack1l11l11111l_opy_ = TestFramework.bstack1111111l11_opy_(instance, PytestBDDFramework.bstack1l11l1ll1l1_opy_, {})
        if os.getenv(bstack11111l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᏀ"), bstack11111l_opy_ (u"ࠥ࠵ࠧᏁ")) == bstack11111l_opy_ (u"ࠦ࠶ࠨᏂ"):
            bstack1l11l1l1lll_opy_ = bstack11111l_opy_ (u"ࠧࡀࠢᏃ").join((scope, fixturename))
            bstack1l11ll1lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11l11ll1l_opy_ = {
                bstack11111l_opy_ (u"ࠨ࡫ࡦࡻࠥᏄ"): bstack1l11l1l1lll_opy_,
                bstack11111l_opy_ (u"ࠢࡵࡣࡪࡷࠧᏅ"): PytestBDDFramework.__1l11l1lll11_opy_(request.node, scenario),
                bstack11111l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᏆ"): fixturedef,
                bstack11111l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᏇ"): scope,
                bstack11111l_opy_ (u"ࠥࡸࡾࡶࡥࠣᏈ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lll1lll_opy_.POST and callable(getattr(args[-1], bstack11111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᏉ"), None)):
                    bstack1l11l11ll1l_opy_[bstack11111l_opy_ (u"ࠧࡺࡹࡱࡧࠥᏊ")] = TestFramework.bstack1ll1111lll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lll1lll_opy_.PRE:
                bstack1l11l11ll1l_opy_[bstack11111l_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᏋ")] = uuid4().__str__()
                bstack1l11l11ll1l_opy_[PytestBDDFramework.bstack1l111ll111l_opy_] = bstack1l11ll1lll1_opy_
            elif test_hook_state == bstack1ll1lll1lll_opy_.POST:
                bstack1l11l11ll1l_opy_[PytestBDDFramework.bstack1l11l11lll1_opy_] = bstack1l11ll1lll1_opy_
            if bstack1l11l1l1lll_opy_ in bstack1l11l11111l_opy_:
                bstack1l11l11111l_opy_[bstack1l11l1l1lll_opy_].update(bstack1l11l11ll1l_opy_)
                self.logger.debug(bstack11111l_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᏌ") + str(bstack1l11l11111l_opy_[bstack1l11l1l1lll_opy_]) + bstack11111l_opy_ (u"ࠣࠤᏍ"))
            else:
                bstack1l11l11111l_opy_[bstack1l11l1l1lll_opy_] = bstack1l11l11ll1l_opy_
                self.logger.debug(bstack11111l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᏎ") + str(len(bstack1l11l11111l_opy_)) + bstack11111l_opy_ (u"ࠥࠦᏏ"))
        TestFramework.bstack1llllllll1l_opy_(instance, PytestBDDFramework.bstack1l11l1ll1l1_opy_, bstack1l11l11111l_opy_)
        self.logger.debug(bstack11111l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᏐ") + str(instance.ref()) + bstack11111l_opy_ (u"ࠧࠨᏑ"))
        return instance
    def __1l11lll1ll1_opy_(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll11l1ll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack111111lll1_opy_.create_context(target)
        ob = bstack1lll1ll1lll_opy_(ctx, self.bstack1ll1ll11lll_opy_, self.bstack1l111l1ll1l_opy_, test_framework_state)
        TestFramework.bstack1l11l1l1l11_opy_(ob, {
            TestFramework.bstack1ll1l1ll1ll_opy_: context.test_framework_name,
            TestFramework.bstack1ll1111ll11_opy_: context.test_framework_version,
            TestFramework.bstack1l11l1l111l_opy_: [],
            PytestBDDFramework.bstack1l11l1ll1l1_opy_: {},
            PytestBDDFramework.bstack1l11l111ll1_opy_: {},
            PytestBDDFramework.bstack1l11ll111ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llllllll1l_opy_(ob, TestFramework.bstack1l111l11lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llllllll1l_opy_(ob, TestFramework.bstack1ll1l111l1l_opy_, context.platform_index)
        TestFramework.bstack1lllllllll1_opy_[ctx.id] = ob
        self.logger.debug(bstack11111l_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᏒ") + str(TestFramework.bstack1lllllllll1_opy_.keys()) + bstack11111l_opy_ (u"ࠢࠣᏓ"))
        return ob
    @staticmethod
    def __1l11l1lllll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11111l_opy_ (u"ࠨ࡫ࡧࠫᏔ"): id(step),
                bstack11111l_opy_ (u"ࠩࡷࡩࡽࡺࠧᏕ"): step.name,
                bstack11111l_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᏖ"): step.keyword,
            })
        meta = {
            bstack11111l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᏗ"): {
                bstack11111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᏘ"): feature.name,
                bstack11111l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᏙ"): feature.filename,
                bstack11111l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᏚ"): feature.description
            },
            bstack11111l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᏛ"): {
                bstack11111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᏜ"): scenario.name
            },
            bstack11111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᏝ"): steps,
            bstack11111l_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭Ꮮ"): PytestBDDFramework.__1l111lll1ll_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11lll1111_opy_: meta
            }
        )
    def bstack1l11ll111l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡨࡪࡵࠣࡱࡪࡺࡨࡰࡦ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠ࠮ࠢࡆ࡬ࡪࡩ࡫ࡴࠢࡷ࡬ࡪࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡯࡮ࡴ࡫ࡧࡩࠥࢄ࠯࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠯ࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡌ࡯ࡳࠢࡨࡥࡨ࡮ࠠࡧ࡫࡯ࡩࠥ࡯࡮ࠡࡪࡲࡳࡰࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠰ࠥࡸࡥࡱ࡮ࡤࡧࡪࡹࠠࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠢࠡ࡫ࡱࠤ࡮ࡺࡳࠡࡲࡤࡸ࡭࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡏࡦࠡࡣࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤࡹ࡮ࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡲࡧࡴࡤࡪࡨࡷࠥࡧࠠ࡮ࡱࡧ࡭࡫࡯ࡥࡥࠢ࡫ࡳࡴࡱ࠭࡭ࡧࡹࡩࡱࠦࡦࡪ࡮ࡨ࠰ࠥ࡯ࡴࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࠦࡷࡪࡶ࡫ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦࡨࡸࡦ࡯࡬ࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡕ࡬ࡱ࡮ࡲࡡࡳ࡮ࡼ࠰ࠥ࡯ࡴࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦ࡬ࡰࡥࡤࡸࡪࡪࠠࡪࡰࠣࡌࡴࡵ࡫ࡍࡧࡹࡩࡱ࠵ࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡨࡹࠡࡴࡨࡴࡱࡧࡣࡪࡰࡪࠤࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤࠣࡻ࡮ࡺࡨࠡࠤࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤ࡙࡮ࡥࠡࡥࡵࡩࡦࡺࡥࡥࠢࡏࡳ࡬ࡋ࡮ࡵࡴࡼࠤࡴࡨࡪࡦࡥࡷࡷࠥࡧࡲࡦࠢࡤࡨࡩ࡫ࡤࠡࡶࡲࠤࡹ࡮ࡥࠡࡪࡲࡳࡰ࠭ࡳࠡࠤ࡯ࡳ࡬ࡹࠢࠡ࡮࡬ࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡮࡯ࡰ࡭࠽ࠤ࡙࡮ࡥࠡࡧࡹࡩࡳࡺࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮ࡴࡧࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡰࡴ࡭ࡳࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥࡖࡡࡵࡪࠣࡳࡧࡰࡥࡤࡶࡶࠤ࡫ࡸ࡯࡮ࠢࡷ࡬ࡪࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠢࡰࡳࡳ࡯ࡴࡰࡴ࡬ࡲ࡬࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᏟ")
        global _1l1llllll11_opy_
        platform_index = os.environ[bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꮰ")]
        bstack1l1ll1lll11_opy_ = os.path.join(bstack1l1lll1ll1l_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), bstack1l11l111l1l_opy_)
        if not os.path.exists(bstack1l1ll1lll11_opy_) or not os.path.isdir(bstack1l1ll1lll11_opy_):
            return
        logs = hook.get(bstack11111l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᏡ"), [])
        with os.scandir(bstack1l1ll1lll11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1llllll11_opy_:
                    self.logger.info(bstack11111l_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᏢ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11111l_opy_ (u"ࠤࠥᏣ")
                    log_entry = bstack1ll1llll111_opy_(
                        kind=bstack11111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᏤ"),
                        message=bstack11111l_opy_ (u"ࠦࠧᏥ"),
                        level=bstack11111l_opy_ (u"ࠧࠨᏦ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll11ll1_opy_=entry.stat().st_size,
                        bstack1l1lllll11l_opy_=bstack11111l_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᏧ"),
                        bstack1lllllll_opy_=os.path.abspath(entry.path),
                        bstack1l11l1111ll_opy_=hook.get(TestFramework.bstack1l11ll11ll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1llllll11_opy_.add(abs_path)
        platform_index = os.environ[bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᏨ")]
        bstack1l111lllll1_opy_ = os.path.join(bstack1l1lll1ll1l_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), bstack1l11l111l1l_opy_, bstack1l111llllll_opy_)
        if not os.path.exists(bstack1l111lllll1_opy_) or not os.path.isdir(bstack1l111lllll1_opy_):
            self.logger.info(bstack11111l_opy_ (u"ࠣࡐࡲࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦࠣࡥࡹࡀࠠࡼࡿࠥᏩ").format(bstack1l111lllll1_opy_))
        else:
            self.logger.info(bstack11111l_opy_ (u"ࠤࡓࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࡋࡳࡴࡱࡅࡷࡧࡱࡸࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡪࡷࡵ࡭ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼ࠾ࠥࢁࡽࠣᏪ").format(bstack1l111lllll1_opy_))
            with os.scandir(bstack1l111lllll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1llllll11_opy_:
                        self.logger.info(bstack11111l_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᏫ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11111l_opy_ (u"ࠦࠧᏬ")
                        log_entry = bstack1ll1llll111_opy_(
                            kind=bstack11111l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᏭ"),
                            message=bstack11111l_opy_ (u"ࠨࠢᏮ"),
                            level=bstack11111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᏯ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll11ll1_opy_=entry.stat().st_size,
                            bstack1l1lllll11l_opy_=bstack11111l_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᏰ"),
                            bstack1lllllll_opy_=os.path.abspath(entry.path),
                            bstack1ll111ll1ll_opy_=hook.get(TestFramework.bstack1l11ll11ll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1llllll11_opy_.add(abs_path)
        hook[bstack11111l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᏱ")] = logs
    def bstack1ll111lllll_opy_(
        self,
        bstack1ll111ll11l_opy_: bstack1lll1ll1lll_opy_,
        entries: List[bstack1ll1llll111_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᏲ"))
        req.platform_index = TestFramework.bstack1111111l11_opy_(bstack1ll111ll11l_opy_, TestFramework.bstack1ll1l111l1l_opy_)
        req.execution_context.hash = str(bstack1ll111ll11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1ll111ll11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1ll111ll11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1111111l11_opy_(bstack1ll111ll11l_opy_, TestFramework.bstack1ll1l1ll1ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1111111l11_opy_(bstack1ll111ll11l_opy_, TestFramework.bstack1ll1111ll11_opy_)
            log_entry.uuid = entry.bstack1l11l1111ll_opy_
            log_entry.test_framework_state = bstack1ll111ll11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᏳ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11111l_opy_ (u"ࠧࠨᏴ")
            if entry.kind == bstack11111l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᏵ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll11ll1_opy_
                log_entry.file_path = entry.bstack1lllllll_opy_
        def bstack1ll111l1111_opy_():
            bstack1l1l1l1l_opy_ = datetime.now()
            try:
                self.bstack1lll11l11ll_opy_.LogCreatedEvent(req)
                bstack1ll111ll11l_opy_.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦ᏶"), datetime.now() - bstack1l1l1l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࢀࢃࠢ᏷").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1ll1l_opy_.enqueue(bstack1ll111l1111_opy_)
    def __1l111ll1ll1_opy_(self, instance) -> None:
        bstack11111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡌࡰࡣࡧࡷࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡵࡩࡦࡺࡥࡴࠢࡤࠤࡩ࡯ࡣࡵࠢࡦࡳࡳࡺࡡࡪࡰ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࡤࠡࡨࡵࡳࡲࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡷࡶࡸࡴࡳࡔࡢࡩࡐࡥࡳࡧࡧࡦࡴࠣࡥࡳࡪࠠࡶࡲࡧࡥࡹ࡫ࡳࠡࡶ࡫ࡩࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡴࡶࡤࡸࡪࠦࡵࡴ࡫ࡱ࡫ࠥࡹࡥࡵࡡࡶࡸࡦࡺࡥࡠࡧࡱࡸࡷ࡯ࡥࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᏸ")
        bstack1l111llll11_opy_ = {bstack11111l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠧᏹ"): bstack1lll1111l11_opy_.bstack1l11l1ll1ll_opy_()}
        TestFramework.bstack1l11l1l1l11_opy_(instance, bstack1l111llll11_opy_)
    @staticmethod
    def __1l111l1lll1_opy_(instance, args):
        request, bstack1l111lll111_opy_ = args
        bstack1l11llll111_opy_ = id(bstack1l111lll111_opy_)
        bstack1l111l1l111_opy_ = instance.data[TestFramework.bstack1l11lll1111_opy_]
        step = next(filter(lambda st: st[bstack11111l_opy_ (u"ࠫ࡮ࡪࠧᏺ")] == bstack1l11llll111_opy_, bstack1l111l1l111_opy_[bstack11111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᏻ")]), None)
        step.update({
            bstack11111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᏼ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l111l1l111_opy_[bstack11111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᏽ")]) if st[bstack11111l_opy_ (u"ࠨ࡫ࡧࠫ᏾")] == step[bstack11111l_opy_ (u"ࠩ࡬ࡨࠬ᏿")]), None)
        if index is not None:
            bstack1l111l1l111_opy_[bstack11111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩ᐀")][index] = step
        instance.data[TestFramework.bstack1l11lll1111_opy_] = bstack1l111l1l111_opy_
    @staticmethod
    def __1l11lll11l1_opy_(instance, args):
        bstack11111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡹ࡫ࡩࡳࠦ࡬ࡦࡰࠣࡥࡷ࡭ࡳࠡ࡫ࡶࠤ࠷࠲ࠠࡪࡶࠣࡷ࡮࡭࡮ࡪࡨ࡬ࡩࡸࠦࡴࡩࡧࡵࡩࠥ࡯ࡳࠡࡰࡲࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡲࡨࡵࠣࡥࡷ࡫ࠠ࠮ࠢ࡞ࡶࡪࡷࡵࡦࡵࡷ࠰ࠥࡹࡴࡦࡲࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࡣࡵ࡫ࡸࠦࡡࡳࡧࠣ࠷ࠥࡺࡨࡦࡰࠣࡸ࡭࡫ࠠ࡭ࡣࡶࡸࠥࡼࡡ࡭ࡷࡨࠤ࡮ࡹࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᐁ")
        bstack1l111l1llll_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l111lll111_opy_ = args[1]
        bstack1l11llll111_opy_ = id(bstack1l111lll111_opy_)
        bstack1l111l1l111_opy_ = instance.data[TestFramework.bstack1l11lll1111_opy_]
        step = None
        if bstack1l11llll111_opy_ is not None and bstack1l111l1l111_opy_.get(bstack11111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐂ")):
            step = next(filter(lambda st: st[bstack11111l_opy_ (u"࠭ࡩࡥࠩᐃ")] == bstack1l11llll111_opy_, bstack1l111l1l111_opy_[bstack11111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐄ")]), None)
            step.update({
                bstack11111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᐅ"): bstack1l111l1llll_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack11111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᐆ"): bstack11111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᐇ"),
                bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᐈ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack11111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᐉ"): bstack11111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᐊ"),
                })
        index = next((i for i, st in enumerate(bstack1l111l1l111_opy_[bstack11111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐋ")]) if st[bstack11111l_opy_ (u"ࠨ࡫ࡧࠫᐌ")] == step[bstack11111l_opy_ (u"ࠩ࡬ࡨࠬᐍ")]), None)
        if index is not None:
            bstack1l111l1l111_opy_[bstack11111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᐎ")][index] = step
        instance.data[TestFramework.bstack1l11lll1111_opy_] = bstack1l111l1l111_opy_
    @staticmethod
    def __1l111lll1ll_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack11111l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᐏ")):
                examples = list(node.callspec.params[bstack11111l_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᐐ")].values())
            return examples
        except:
            return []
    def bstack1ll1111111l_opy_(self, instance: bstack1lll1ll1lll_opy_, bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_]):
        bstack1l11l11l11l_opy_ = (
            PytestBDDFramework.bstack1l111ll1111_opy_
            if bstack1111111111_opy_[1] == bstack1ll1lll1lll_opy_.PRE
            else PytestBDDFramework.bstack1l11ll1l111_opy_
        )
        hook = PytestBDDFramework.bstack1l11l1l11ll_opy_(instance, bstack1l11l11l11l_opy_)
        entries = hook.get(TestFramework.bstack1l11l1l1ll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, []))
        return entries
    def bstack1l1lll1ll11_opy_(self, instance: bstack1lll1ll1lll_opy_, bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_]):
        bstack1l11l11l11l_opy_ = (
            PytestBDDFramework.bstack1l111ll1111_opy_
            if bstack1111111111_opy_[1] == bstack1ll1lll1lll_opy_.PRE
            else PytestBDDFramework.bstack1l11ll1l111_opy_
        )
        PytestBDDFramework.bstack1l11ll1l1l1_opy_(instance, bstack1l11l11l11l_opy_)
        TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, []).clear()
    @staticmethod
    def bstack1l11l1l11ll_opy_(instance: bstack1lll1ll1lll_opy_, bstack1l11l11l11l_opy_: str):
        bstack1l11l1l1111_opy_ = (
            PytestBDDFramework.bstack1l11l111ll1_opy_
            if bstack1l11l11l11l_opy_ == PytestBDDFramework.bstack1l11ll1l111_opy_
            else PytestBDDFramework.bstack1l11ll111ll_opy_
        )
        bstack1l111llll1l_opy_ = TestFramework.bstack1111111l11_opy_(instance, bstack1l11l11l11l_opy_, None)
        bstack1l11l11l111_opy_ = TestFramework.bstack1111111l11_opy_(instance, bstack1l11l1l1111_opy_, None) if bstack1l111llll1l_opy_ else None
        return (
            bstack1l11l11l111_opy_[bstack1l111llll1l_opy_][-1]
            if isinstance(bstack1l11l11l111_opy_, dict) and len(bstack1l11l11l111_opy_.get(bstack1l111llll1l_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l11ll1l1l1_opy_(instance: bstack1lll1ll1lll_opy_, bstack1l11l11l11l_opy_: str):
        hook = PytestBDDFramework.bstack1l11l1l11ll_opy_(instance, bstack1l11l11l11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l1l1ll1_opy_, []).clear()
    @staticmethod
    def __1l11l1ll111_opy_(instance: bstack1lll1ll1lll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11111l_opy_ (u"ࠨࡧࡦࡶࡢࡶࡪࡩ࡯ࡳࡦࡶࠦᐑ"), None)):
            return
        if os.getenv(bstack11111l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡌࡐࡉࡖࠦᐒ"), bstack11111l_opy_ (u"ࠣ࠳ࠥᐓ")) != bstack11111l_opy_ (u"ࠤ࠴ࠦᐔ"):
            PytestBDDFramework.logger.warning(bstack11111l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳ࡫ࡱ࡫ࠥࡩࡡࡱ࡮ࡲ࡫ࠧᐕ"))
            return
        bstack1l111ll1l1l_opy_ = {
            bstack11111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᐖ"): (PytestBDDFramework.bstack1l111ll1111_opy_, PytestBDDFramework.bstack1l11ll111ll_opy_),
            bstack11111l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᐗ"): (PytestBDDFramework.bstack1l11ll1l111_opy_, PytestBDDFramework.bstack1l11l111ll1_opy_),
        }
        for when in (bstack11111l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᐘ"), bstack11111l_opy_ (u"ࠢࡤࡣ࡯ࡰࠧᐙ"), bstack11111l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᐚ")):
            bstack1l11lll1lll_opy_ = args[1].get_records(when)
            if not bstack1l11lll1lll_opy_:
                continue
            records = [
                bstack1ll1llll111_opy_(
                    kind=TestFramework.bstack1ll11111ll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11111l_opy_ (u"ࠤ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩࠧᐛ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11111l_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠦᐜ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11lll1lll_opy_
                if isinstance(getattr(r, bstack11111l_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧᐝ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11ll1ll11_opy_, bstack1l11l1l1111_opy_ = bstack1l111ll1l1l_opy_.get(when, (None, None))
            bstack1l11l1111l1_opy_ = TestFramework.bstack1111111l11_opy_(instance, bstack1l11ll1ll11_opy_, None) if bstack1l11ll1ll11_opy_ else None
            bstack1l11l11l111_opy_ = TestFramework.bstack1111111l11_opy_(instance, bstack1l11l1l1111_opy_, None) if bstack1l11l1111l1_opy_ else None
            if isinstance(bstack1l11l11l111_opy_, dict) and len(bstack1l11l11l111_opy_.get(bstack1l11l1111l1_opy_, [])) > 0:
                hook = bstack1l11l11l111_opy_[bstack1l11l1111l1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11l1l1ll1_opy_ in hook:
                    hook[TestFramework.bstack1l11l1l1ll1_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11l1ll11l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack11lll1l1_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11l11l1l1_opy_(request.node, scenario)
        bstack1l11ll1l11l_opy_ = feature.filename
        if not bstack11lll1l1_opy_ or not test_name or not bstack1l11ll1l11l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1l1111l1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l1lll1l_opy_: bstack11lll1l1_opy_,
            TestFramework.bstack1ll1l1lll11_opy_: test_name,
            TestFramework.bstack1l1ll1ll1l1_opy_: bstack11lll1l1_opy_,
            TestFramework.bstack1l11ll11lll_opy_: bstack1l11ll1l11l_opy_,
            TestFramework.bstack1l11lll111l_opy_: PytestBDDFramework.__1l11l1lll11_opy_(feature, scenario),
            TestFramework.bstack1l11l11llll_opy_: code,
            TestFramework.bstack1l1l1l1llll_opy_: TestFramework.bstack1l11l11ll11_opy_,
            TestFramework.bstack1l1l111l1ll_opy_: test_name
        }
    @staticmethod
    def __1l11l11l1l1_opy_(node, scenario):
        if hasattr(node, bstack11111l_opy_ (u"ࠬࡩࡡ࡭࡮ࡶࡴࡪࡩࠧᐞ")):
            parts = node.nodeid.rsplit(bstack11111l_opy_ (u"ࠨ࡛ࠣᐟ"))
            params = parts[-1]
            return bstack11111l_opy_ (u"ࠢࡼࡿࠣ࡟ࢀࢃࠢᐠ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11l1lll11_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack11111l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᐡ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack11111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᐢ")) else [])
    @staticmethod
    def __1l111ll1l11_opy_(location):
        return bstack11111l_opy_ (u"ࠥ࠾࠿ࠨᐣ").join(filter(lambda x: isinstance(x, str), location))