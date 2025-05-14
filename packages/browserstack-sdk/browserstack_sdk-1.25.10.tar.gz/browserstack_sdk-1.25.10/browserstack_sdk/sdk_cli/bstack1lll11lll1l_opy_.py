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
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll11l1ll1_opy_,
    bstack1lll1ll1lll_opy_,
    bstack1ll1lll1lll_opy_,
    bstack1l11l1l11l1_opy_,
    bstack1ll1llll111_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1lllll1l1_opy_
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lllll11lll_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l1ll1l_opy_ import bstack1111l1l11l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llll11l111_opy_ import bstack1lll1111l11_opy_
from bstack_utils.bstack11l111llll_opy_ import bstack1l1ll11l1l_opy_
bstack1l1lll1ll1l_opy_ = bstack1l1lllll1l1_opy_()
bstack1l11lll1l1l_opy_ = 1.0
bstack1l1llll111l_opy_ = bstack11111l_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᐤ")
bstack1l111l11ll1_opy_ = bstack11111l_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᐥ")
bstack1l111l111l1_opy_ = bstack11111l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᐦ")
bstack1l111l11l11_opy_ = bstack11111l_opy_ (u"ࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥᐧ")
bstack1l111l11l1l_opy_ = bstack11111l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢᐨ")
_1l1llllll11_opy_ = set()
class bstack1lll1l1lll1_opy_(TestFramework):
    bstack1l11l1ll1l1_opy_ = bstack11111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᐩ")
    bstack1l11ll111ll_opy_ = bstack11111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠣᐪ")
    bstack1l11l111ll1_opy_ = bstack11111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠥᐫ")
    bstack1l111ll1111_opy_ = bstack11111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪࠢᐬ")
    bstack1l11ll1l111_opy_ = bstack11111l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᐭ")
    bstack1l11ll1111l_opy_: bool
    bstack1111l1ll1l_opy_: bstack1111l1l11l_opy_  = None
    bstack1lll11l11ll_opy_ = None
    bstack1l111l1l1l1_opy_ = [
        bstack1lll11l1ll1_opy_.BEFORE_ALL,
        bstack1lll11l1ll1_opy_.AFTER_ALL,
        bstack1lll11l1ll1_opy_.BEFORE_EACH,
        bstack1lll11l1ll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111l1ll1l_opy_: Dict[str, str],
        bstack1ll1ll11lll_opy_: List[str]=[bstack11111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᐮ")],
        bstack1111l1ll1l_opy_: bstack1111l1l11l_opy_=None,
        bstack1lll11l11ll_opy_=None
    ):
        super().__init__(bstack1ll1ll11lll_opy_, bstack1l111l1ll1l_opy_, bstack1111l1ll1l_opy_)
        self.bstack1l11ll1111l_opy_ = any(bstack11111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴࠣᐯ") in item.lower() for item in bstack1ll1ll11lll_opy_)
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
        if test_framework_state == bstack1lll11l1ll1_opy_.TEST or test_framework_state in bstack1lll1l1lll1_opy_.bstack1l111l1l1l1_opy_:
            bstack1l11ll11l1l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll11l1ll1_opy_.NONE:
            self.logger.warning(bstack11111l_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦࡦࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦ࠿ࠥᐰ") + str(test_hook_state) + bstack11111l_opy_ (u"ࠥࠦᐱ"))
            return
        if not self.bstack1l11ll1111l_opy_:
            self.logger.warning(bstack11111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡹࡳࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡁࠧᐲ") + str(str(self.bstack1ll1ll11lll_opy_)) + bstack11111l_opy_ (u"ࠧࠨᐳ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack11111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᐴ") + str(kwargs) + bstack11111l_opy_ (u"ࠢࠣᐵ"))
            return
        instance = self.__1l111l1l1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack11111l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡣࡵ࡫ࡸࡃࠢᐶ") + str(args) + bstack11111l_opy_ (u"ࠤࠥᐷ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll1l1lll1_opy_.bstack1l111l1l1l1_opy_ and test_hook_state == bstack1ll1lll1lll_opy_.PRE:
                bstack1ll1ll111ll_opy_ = bstack1lllll11lll_opy_.bstack1ll1l11l111_opy_(EVENTS.bstack1l11lll1l1_opy_.value)
                name = str(EVENTS.bstack1l11lll1l1_opy_.name)+bstack11111l_opy_ (u"ࠥ࠾ࠧᐸ")+str(test_framework_state.name)
                TestFramework.bstack1l11l111lll_opy_(instance, name, bstack1ll1ll111ll_opy_)
        except Exception as e:
            self.logger.debug(bstack11111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡴࡵ࡫ࠡࡧࡵࡶࡴࡸࠠࡱࡴࡨ࠾ࠥࢁࡽࠣᐹ").format(e))
        try:
            if not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l11l1lll1l_opy_) and test_hook_state == bstack1ll1lll1lll_opy_.PRE:
                test = bstack1lll1l1lll1_opy_.__1l11l1ll11l_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack11111l_opy_ (u"ࠧࡲ࡯ࡢࡦࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᐺ") + str(test_hook_state) + bstack11111l_opy_ (u"ࠨࠢᐻ"))
            if test_framework_state == bstack1lll11l1ll1_opy_.TEST:
                if test_hook_state == bstack1ll1lll1lll_opy_.PRE and not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll1111l1ll_opy_):
                    TestFramework.bstack1llllllll1l_opy_(instance, TestFramework.bstack1ll1111l1ll_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11111l_opy_ (u"ࠢࡴࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᐼ") + str(test_hook_state) + bstack11111l_opy_ (u"ࠣࠤᐽ"))
                elif test_hook_state == bstack1ll1lll1lll_opy_.POST and not TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1lll111l1_opy_):
                    TestFramework.bstack1llllllll1l_opy_(instance, TestFramework.bstack1l1lll111l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack11111l_opy_ (u"ࠤࡶࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᐾ") + str(test_hook_state) + bstack11111l_opy_ (u"ࠥࠦᐿ"))
            elif test_framework_state == bstack1lll11l1ll1_opy_.LOG and test_hook_state == bstack1ll1lll1lll_opy_.POST:
                bstack1lll1l1lll1_opy_.__1l11l1ll111_opy_(instance, *args)
            elif test_framework_state == bstack1lll11l1ll1_opy_.LOG_REPORT and test_hook_state == bstack1ll1lll1lll_opy_.POST:
                self.__1l11ll1ll1l_opy_(instance, *args)
                self.__1l111ll1ll1_opy_(instance)
            elif test_framework_state in bstack1lll1l1lll1_opy_.bstack1l111l1l1l1_opy_:
                self.__1l11l111l11_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack11111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧᑀ") + str(instance.ref()) + bstack11111l_opy_ (u"ࠧࠨᑁ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l111lll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll1l1lll1_opy_.bstack1l111l1l1l1_opy_ and test_hook_state == bstack1ll1lll1lll_opy_.POST:
                name = str(EVENTS.bstack1l11lll1l1_opy_.name)+bstack11111l_opy_ (u"ࠨ࠺ࠣᑂ")+str(test_framework_state.name)
                bstack1ll1ll111ll_opy_ = TestFramework.bstack1l111ll11ll_opy_(instance, name)
                bstack1lllll11lll_opy_.end(EVENTS.bstack1l11lll1l1_opy_.value, bstack1ll1ll111ll_opy_+bstack11111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᑃ"), bstack1ll1ll111ll_opy_+bstack11111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᑄ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack11111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᑅ").format(e))
    def bstack1l1lllll1ll_opy_(self):
        return self.bstack1l11ll1111l_opy_
    def __1l11ll11l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack11111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᑆ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1llll1ll1_opy_(rep, [bstack11111l_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᑇ"), bstack11111l_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑈ"), bstack11111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨᑉ"), bstack11111l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᑊ"), bstack11111l_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤᑋ"), bstack11111l_opy_ (u"ࠤ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠣᑌ")])
        return None
    def __1l11ll1ll1l_opy_(self, instance: bstack1lll1ll1lll_opy_, *args):
        result = self.__1l11ll11l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll111l_opy_ = None
        if result.get(bstack11111l_opy_ (u"ࠥࡳࡺࡺࡣࡰ࡯ࡨࠦᑍ"), None) == bstack11111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᑎ") and len(args) > 1 and getattr(args[1], bstack11111l_opy_ (u"ࠧ࡫ࡸࡤ࡫ࡱࡪࡴࠨᑏ"), None) is not None:
            failure = [{bstack11111l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᑐ"): [args[1].excinfo.exconly(), result.get(bstack11111l_opy_ (u"ࠢ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹࠨᑑ"), None)]}]
            bstack1111ll111l_opy_ = bstack11111l_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤᑒ") if bstack11111l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᑓ") in getattr(args[1].excinfo, bstack11111l_opy_ (u"ࠥࡸࡾࡶࡥ࡯ࡣࡰࡩࠧᑔ"), bstack11111l_opy_ (u"ࠦࠧᑕ")) else bstack11111l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᑖ")
        bstack1l111ll1lll_opy_ = result.get(bstack11111l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑗ"), TestFramework.bstack1l11l11ll11_opy_)
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
            target = None # bstack1l11ll1llll_opy_ bstack1l111ll11l1_opy_ this to be bstack11111l_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᑘ")
            if test_framework_state == bstack1lll11l1ll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11lll1ll1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11l1ll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack11111l_opy_ (u"ࠣࡰࡲࡨࡪࠨᑙ"), None), bstack11111l_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᑚ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack11111l_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥᑛ"), None):
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
        bstack1l11lll1l11_opy_ = TestFramework.bstack1111111l11_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11ll111ll_opy_, {})
        if not key in bstack1l11lll1l11_opy_:
            bstack1l11lll1l11_opy_[key] = []
        bstack1l11ll11111_opy_ = TestFramework.bstack1111111l11_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11l111ll1_opy_, {})
        if not key in bstack1l11ll11111_opy_:
            bstack1l11ll11111_opy_[key] = []
        bstack1l111llll11_opy_ = {
            bstack1lll1l1lll1_opy_.bstack1l11ll111ll_opy_: bstack1l11lll1l11_opy_,
            bstack1lll1l1lll1_opy_.bstack1l11l111ll1_opy_: bstack1l11ll11111_opy_,
        }
        if test_hook_state == bstack1ll1lll1lll_opy_.PRE:
            hook = {
                bstack11111l_opy_ (u"ࠦࡰ࡫ࡹࠣᑜ"): key,
                TestFramework.bstack1l11ll11ll1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1llll1_opy_: TestFramework.bstack1l11l11l1ll_opy_,
                TestFramework.bstack1l111ll111l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11l1l1ll1_opy_: [],
                TestFramework.bstack1l111l1l11l_opy_: args[1] if len(args) > 1 else bstack11111l_opy_ (u"ࠬ࠭ᑝ"),
                TestFramework.bstack1l11ll1l1ll_opy_: bstack1lll1111l11_opy_.bstack1l11l1ll1ll_opy_()
            }
            bstack1l11lll1l11_opy_[key].append(hook)
            bstack1l111llll11_opy_[bstack1lll1l1lll1_opy_.bstack1l111ll1111_opy_] = key
        elif test_hook_state == bstack1ll1lll1lll_opy_.POST:
            bstack1l111lll1l1_opy_ = bstack1l11lll1l11_opy_.get(key, [])
            hook = bstack1l111lll1l1_opy_.pop() if bstack1l111lll1l1_opy_ else None
            if hook:
                result = self.__1l11ll11l11_opy_(*args)
                if result:
                    bstack1l11lll11ll_opy_ = result.get(bstack11111l_opy_ (u"ࠨ࡯ࡶࡶࡦࡳࡲ࡫ࠢᑞ"), TestFramework.bstack1l11l11l1ll_opy_)
                    if bstack1l11lll11ll_opy_ != TestFramework.bstack1l11l11l1ll_opy_:
                        hook[TestFramework.bstack1l11l1llll1_opy_] = bstack1l11lll11ll_opy_
                hook[TestFramework.bstack1l11l11lll1_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11ll1l1ll_opy_]= bstack1lll1111l11_opy_.bstack1l11l1ll1ll_opy_()
                self.bstack1l11ll111l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111l1ll11_opy_, [])
                if logs: self.bstack1ll111lllll_opy_(instance, logs)
                bstack1l11ll11111_opy_[key].append(hook)
                bstack1l111llll11_opy_[bstack1lll1l1lll1_opy_.bstack1l11ll1l111_opy_] = key
        TestFramework.bstack1l11l1l1l11_opy_(instance, bstack1l111llll11_opy_)
        self.logger.debug(bstack11111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࡃࡻ࡬ࡧࡼࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥ࠿ࡾ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࢀࠤ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࡂࠨᑟ") + str(bstack1l11ll11111_opy_) + bstack11111l_opy_ (u"ࠣࠤᑠ"))
    def __1l11l1l1l1l_opy_(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll11l1ll1_opy_,
        test_hook_state: bstack1ll1lll1lll_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1llll1ll1_opy_(args[0], [bstack11111l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑡ"), bstack11111l_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᑢ"), bstack11111l_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᑣ"), bstack11111l_opy_ (u"ࠧ࡯ࡤࡴࠤᑤ"), bstack11111l_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣᑥ"), bstack11111l_opy_ (u"ࠢࡣࡣࡶࡩ࡮ࡪࠢᑦ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack11111l_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᑧ")) else fixturedef.get(bstack11111l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑨ"), None)
        fixturename = request.fixturename if hasattr(request, bstack11111l_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᑩ")) else None
        node = request.node if hasattr(request, bstack11111l_opy_ (u"ࠦࡳࡵࡤࡦࠤᑪ")) else None
        target = request.node.nodeid if hasattr(node, bstack11111l_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᑫ")) else None
        baseid = fixturedef.get(bstack11111l_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᑬ"), None) or bstack11111l_opy_ (u"ࠢࠣᑭ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack11111l_opy_ (u"ࠣࡡࡳࡽ࡫ࡻ࡮ࡤ࡫ࡷࡩࡲࠨᑮ")):
            target = bstack1lll1l1lll1_opy_.__1l111ll1l11_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack11111l_opy_ (u"ࠤ࡯ࡳࡨࡧࡴࡪࡱࡱࠦᑯ")) else None
            if target and not TestFramework.bstack1llllllllll_opy_(target):
                self.__1l11lll1ll1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack11111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡩ࡭ࡽࡺࡵࡳࡧࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡪࡦࡲ࡬ࡣࡣࡦ࡯ࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡴ࡯ࡥࡧࡀࡿࡳࡵࡤࡦࡿࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᑰ") + str(test_hook_state) + bstack11111l_opy_ (u"ࠦࠧᑱ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack11111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࠡࡧࡹࡩࡳࡺ࠽ࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫ࡤࡦࡨࡀࡿ࡫࡯ࡸࡵࡷࡵࡩࡩ࡫ࡦࡾࠢࡶࡧࡴࡶࡥ࠾ࡽࡶࡧࡴࡶࡥࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥᑲ") + str(target) + bstack11111l_opy_ (u"ࠨࠢᑳ"))
            return None
        instance = TestFramework.bstack1llllllllll_opy_(target)
        if not instance:
            self.logger.warning(bstack11111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡢࡢࡵࡨ࡭ࡩࡃࡻࡣࡣࡶࡩ࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᑴ") + str(target) + bstack11111l_opy_ (u"ࠣࠤᑵ"))
            return None
        bstack1l11l11111l_opy_ = TestFramework.bstack1111111l11_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11l1ll1l1_opy_, {})
        if os.getenv(bstack11111l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡈࡌ࡜࡙࡛ࡒࡆࡕࠥᑶ"), bstack11111l_opy_ (u"ࠥ࠵ࠧᑷ")) == bstack11111l_opy_ (u"ࠦ࠶ࠨᑸ"):
            bstack1l11l1l1lll_opy_ = bstack11111l_opy_ (u"ࠧࡀࠢᑹ").join((scope, fixturename))
            bstack1l11ll1lll1_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11l11ll1l_opy_ = {
                bstack11111l_opy_ (u"ࠨ࡫ࡦࡻࠥᑺ"): bstack1l11l1l1lll_opy_,
                bstack11111l_opy_ (u"ࠢࡵࡣࡪࡷࠧᑻ"): bstack1lll1l1lll1_opy_.__1l11l1lll11_opy_(request.node),
                bstack11111l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࠤᑼ"): fixturedef,
                bstack11111l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣᑽ"): scope,
                bstack11111l_opy_ (u"ࠥࡸࡾࡶࡥࠣᑾ"): None,
            }
            try:
                if test_hook_state == bstack1ll1lll1lll_opy_.POST and callable(getattr(args[-1], bstack11111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡴࡨࡷࡺࡲࡴࠣᑿ"), None)):
                    bstack1l11l11ll1l_opy_[bstack11111l_opy_ (u"ࠧࡺࡹࡱࡧࠥᒀ")] = TestFramework.bstack1ll1111lll1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1ll1lll1lll_opy_.PRE:
                bstack1l11l11ll1l_opy_[bstack11111l_opy_ (u"ࠨࡵࡶ࡫ࡧࠦᒁ")] = uuid4().__str__()
                bstack1l11l11ll1l_opy_[bstack1lll1l1lll1_opy_.bstack1l111ll111l_opy_] = bstack1l11ll1lll1_opy_
            elif test_hook_state == bstack1ll1lll1lll_opy_.POST:
                bstack1l11l11ll1l_opy_[bstack1lll1l1lll1_opy_.bstack1l11l11lll1_opy_] = bstack1l11ll1lll1_opy_
            if bstack1l11l1l1lll_opy_ in bstack1l11l11111l_opy_:
                bstack1l11l11111l_opy_[bstack1l11l1l1lll_opy_].update(bstack1l11l11ll1l_opy_)
                self.logger.debug(bstack11111l_opy_ (u"ࠢࡶࡲࡧࡥࡹ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࠣᒂ") + str(bstack1l11l11111l_opy_[bstack1l11l1l1lll_opy_]) + bstack11111l_opy_ (u"ࠣࠤᒃ"))
            else:
                bstack1l11l11111l_opy_[bstack1l11l1l1lll_opy_] = bstack1l11l11ll1l_opy_
                self.logger.debug(bstack11111l_opy_ (u"ࠤࡶࡥࡻ࡫ࡤࠡࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࡃࡻࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࢂࠦࡳࡤࡱࡳࡩࡂࢁࡳࡤࡱࡳࡩࢂࠦࡦࡪࡺࡷࡹࡷ࡫࠽ࡼࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡽࠡࡶࡵࡥࡨࡱࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࠧᒄ") + str(len(bstack1l11l11111l_opy_)) + bstack11111l_opy_ (u"ࠥࠦᒅ"))
        TestFramework.bstack1llllllll1l_opy_(instance, bstack1lll1l1lll1_opy_.bstack1l11l1ll1l1_opy_, bstack1l11l11111l_opy_)
        self.logger.debug(bstack11111l_opy_ (u"ࠦࡸࡧࡶࡦࡦࠣࡪ࡮ࡾࡴࡶࡴࡨࡷࡂࢁ࡬ࡦࡰࠫࡸࡷࡧࡣ࡬ࡧࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࡸ࠯ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᒆ") + str(instance.ref()) + bstack11111l_opy_ (u"ࠧࠨᒇ"))
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
            bstack1lll1l1lll1_opy_.bstack1l11l1ll1l1_opy_: {},
            bstack1lll1l1lll1_opy_.bstack1l11l111ll1_opy_: {},
            bstack1lll1l1lll1_opy_.bstack1l11ll111ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack1llllllll1l_opy_(ob, TestFramework.bstack1l111l11lll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack1llllllll1l_opy_(ob, TestFramework.bstack1ll1l111l1l_opy_, context.platform_index)
        TestFramework.bstack1lllllllll1_opy_[ctx.id] = ob
        self.logger.debug(bstack11111l_opy_ (u"ࠨࡳࡢࡸࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡤࡶࡻ࠲࡮ࡪ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᒈ") + str(TestFramework.bstack1lllllllll1_opy_.keys()) + bstack11111l_opy_ (u"ࠢࠣᒉ"))
        return ob
    def bstack1ll1111111l_opy_(self, instance: bstack1lll1ll1lll_opy_, bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_]):
        bstack1l11l11l11l_opy_ = (
            bstack1lll1l1lll1_opy_.bstack1l111ll1111_opy_
            if bstack1111111111_opy_[1] == bstack1ll1lll1lll_opy_.PRE
            else bstack1lll1l1lll1_opy_.bstack1l11ll1l111_opy_
        )
        hook = bstack1lll1l1lll1_opy_.bstack1l11l1l11ll_opy_(instance, bstack1l11l11l11l_opy_)
        entries = hook.get(TestFramework.bstack1l11l1l1ll1_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, []))
        return entries
    def bstack1l1lll1ll11_opy_(self, instance: bstack1lll1ll1lll_opy_, bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_]):
        bstack1l11l11l11l_opy_ = (
            bstack1lll1l1lll1_opy_.bstack1l111ll1111_opy_
            if bstack1111111111_opy_[1] == bstack1ll1lll1lll_opy_.PRE
            else bstack1lll1l1lll1_opy_.bstack1l11ll1l111_opy_
        )
        bstack1lll1l1lll1_opy_.bstack1l11ll1l1l1_opy_(instance, bstack1l11l11l11l_opy_)
        TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1l11l1l111l_opy_, []).clear()
    def bstack1l11ll111l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack11111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖ࡫࡭ࡸࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠱ࠥࡉࡨࡦࡥ࡮ࡷࠥࡺࡨࡦࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡ࡫ࡱࡷ࡮ࡪࡥࠡࢀ࠲࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠲࡙ࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡈࡲࡶࠥ࡫ࡡࡤࡪࠣࡪ࡮ࡲࡥࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡡ࡯ࡩࡻ࡫࡬ࡠࡨ࡬ࡰࡪࡹࠬࠡࡴࡨࡴࡱࡧࡣࡦࡵ࡙ࠣࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢࠡࡹ࡬ࡸ࡭ࠦࠢࡉࡱࡲ࡯ࡑ࡫ࡶࡦ࡮ࠥࠤ࡮ࡴࠠࡪࡶࡶࠤࡵࡧࡴࡩ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡋࡩࠤࡦࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡵࡪࡨࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡮ࡣࡷࡧ࡭࡫ࡳࠡࡣࠣࡱࡴࡪࡩࡧ࡫ࡨࡨࠥ࡮࡯ࡰ࡭࠰ࡰࡪࡼࡥ࡭ࠢࡩ࡭ࡱ࡫ࠬࠡ࡫ࡷࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠࡍࡱࡪࡉࡳࡺࡲࡺࠢࡲࡦ࡯࡫ࡣࡵࠢࡺ࡭ࡹ࡮ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡘ࡯࡭ࡪ࡮ࡤࡶࡱࡿࠬࠡ࡫ࡷࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢ࡯ࡳࡨࡧࡴࡦࡦࠣ࡭ࡳࠦࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭࠱ࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡤࡼࠤࡷ࡫ࡰ࡭ࡣࡦ࡭ࡳ࡭ࠠࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧࠦࡷࡪࡶ࡫ࠤࠧࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠢ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡕࡪࡨࠤࡨࡸࡥࡢࡶࡨࡨࠥࡒ࡯ࡨࡇࡱࡸࡷࡿࠠࡰࡤ࡭ࡩࡨࡺࡳࠡࡣࡵࡩࠥࡧࡤࡥࡧࡧࠤࡹࡵࠠࡵࡪࡨࠤ࡭ࡵ࡯࡬ࠩࡶࠤࠧࡲ࡯ࡨࡵࠥࠤࡱ࡯ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡳࡰࡀࠠࡕࡪࡨࠤࡪࡼࡥ࡯ࡶࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠠࡤࡱࡱࡸࡦ࡯࡮ࡪࡰࡪࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸࡀࠠࡍ࡫ࡶࡸࠥࡵࡦࠡࡒࡤࡸ࡭ࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡧࡴࡲࡱࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡸ࡭ࡱࡪ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠥࡳ࡯࡯࡫ࡷࡳࡷ࡯࡮ࡨ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᒊ")
        global _1l1llllll11_opy_
        platform_index = os.environ[bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒋ")]
        bstack1l1ll1lll11_opy_ = os.path.join(bstack1l1lll1ll1l_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), bstack1l111l11l11_opy_)
        if not os.path.exists(bstack1l1ll1lll11_opy_) or not os.path.isdir(bstack1l1ll1lll11_opy_):
            self.logger.info(bstack11111l_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦࡤࡰࡧࡶࠤࡳࡵࡴࠡࡧࡻ࡭ࡸࡺࡳࠡࡶࡲࠤࡵࡸ࡯ࡤࡧࡶࡷࠥࢁࡽࠣᒌ").format(bstack1l1ll1lll11_opy_))
            return
        logs = hook.get(bstack11111l_opy_ (u"ࠦࡱࡵࡧࡴࠤᒍ"), [])
        with os.scandir(bstack1l1ll1lll11_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1l1llllll11_opy_:
                    self.logger.info(bstack11111l_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᒎ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack11111l_opy_ (u"ࠨࠢᒏ")
                    log_entry = bstack1ll1llll111_opy_(
                        kind=bstack11111l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᒐ"),
                        message=bstack11111l_opy_ (u"ࠣࠤᒑ"),
                        level=bstack11111l_opy_ (u"ࠤࠥᒒ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1lll11ll1_opy_=entry.stat().st_size,
                        bstack1l1lllll11l_opy_=bstack11111l_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᒓ"),
                        bstack1lllllll_opy_=os.path.abspath(entry.path),
                        bstack1l11l1111ll_opy_=hook.get(TestFramework.bstack1l11ll11ll1_opy_)
                    )
                    logs.append(log_entry)
                    _1l1llllll11_opy_.add(abs_path)
        platform_index = os.environ[bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᒔ")]
        bstack1l111lllll1_opy_ = os.path.join(bstack1l1lll1ll1l_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), bstack1l111l11l11_opy_, bstack1l111l11l1l_opy_)
        if not os.path.exists(bstack1l111lllll1_opy_) or not os.path.isdir(bstack1l111lllll1_opy_):
            self.logger.info(bstack11111l_opy_ (u"ࠧࡔ࡯ࠡࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡨࡲࡹࡳࡪࠠࡢࡶ࠽ࠤࢀࢃࠢᒕ").format(bstack1l111lllll1_opy_))
        else:
            self.logger.info(bstack11111l_opy_ (u"ࠨࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡧࡴࡲࡱࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹ࠻ࠢࡾࢁࠧᒖ").format(bstack1l111lllll1_opy_))
            with os.scandir(bstack1l111lllll1_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1l1llllll11_opy_:
                        self.logger.info(bstack11111l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᒗ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack11111l_opy_ (u"ࠣࠤᒘ")
                        log_entry = bstack1ll1llll111_opy_(
                            kind=bstack11111l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᒙ"),
                            message=bstack11111l_opy_ (u"ࠥࠦᒚ"),
                            level=bstack11111l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᒛ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1lll11ll1_opy_=entry.stat().st_size,
                            bstack1l1lllll11l_opy_=bstack11111l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᒜ"),
                            bstack1lllllll_opy_=os.path.abspath(entry.path),
                            bstack1ll111ll1ll_opy_=hook.get(TestFramework.bstack1l11ll11ll1_opy_)
                        )
                        logs.append(log_entry)
                        _1l1llllll11_opy_.add(abs_path)
        hook[bstack11111l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᒝ")] = logs
    def bstack1ll111lllll_opy_(
        self,
        bstack1ll111ll11l_opy_: bstack1lll1ll1lll_opy_,
        entries: List[bstack1ll1llll111_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack11111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᒞ"))
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
            log_entry.message = entry.message.encode(bstack11111l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᒟ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack11111l_opy_ (u"ࠤࠥᒠ")
            if entry.kind == bstack11111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᒡ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll11ll1_opy_
                log_entry.file_path = entry.bstack1lllllll_opy_
        def bstack1ll111l1111_opy_():
            bstack1l1l1l1l_opy_ = datetime.now()
            try:
                self.bstack1lll11l11ll_opy_.LogCreatedEvent(req)
                bstack1ll111ll11l_opy_.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣᒢ"), datetime.now() - bstack1l1l1l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11111l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࢀࠦᒣ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1ll1l_opy_.enqueue(bstack1ll111l1111_opy_)
    def __1l111ll1ll1_opy_(self, instance) -> None:
        bstack11111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᒤ")
        bstack1l111llll11_opy_ = {bstack11111l_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᒥ"): bstack1lll1111l11_opy_.bstack1l11l1ll1ll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11l1l1l11_opy_(instance, bstack1l111llll11_opy_)
    @staticmethod
    def bstack1l11l1l11ll_opy_(instance: bstack1lll1ll1lll_opy_, bstack1l11l11l11l_opy_: str):
        bstack1l11l1l1111_opy_ = (
            bstack1lll1l1lll1_opy_.bstack1l11l111ll1_opy_
            if bstack1l11l11l11l_opy_ == bstack1lll1l1lll1_opy_.bstack1l11ll1l111_opy_
            else bstack1lll1l1lll1_opy_.bstack1l11ll111ll_opy_
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
        hook = bstack1lll1l1lll1_opy_.bstack1l11l1l11ll_opy_(instance, bstack1l11l11l11l_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11l1l1ll1_opy_, []).clear()
    @staticmethod
    def __1l11l1ll111_opy_(instance: bstack1lll1ll1lll_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack11111l_opy_ (u"ࠣࡩࡨࡸࡤࡸࡥࡤࡱࡵࡨࡸࠨᒦ"), None)):
            return
        if os.getenv(bstack11111l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡎࡒࡋࡘࠨᒧ"), bstack11111l_opy_ (u"ࠥ࠵ࠧᒨ")) != bstack11111l_opy_ (u"ࠦ࠶ࠨᒩ"):
            bstack1lll1l1lll1_opy_.logger.warning(bstack11111l_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵ࡭ࡳ࡭ࠠࡤࡣࡳࡰࡴ࡭ࠢᒪ"))
            return
        bstack1l111ll1l1l_opy_ = {
            bstack11111l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᒫ"): (bstack1lll1l1lll1_opy_.bstack1l111ll1111_opy_, bstack1lll1l1lll1_opy_.bstack1l11ll111ll_opy_),
            bstack11111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᒬ"): (bstack1lll1l1lll1_opy_.bstack1l11ll1l111_opy_, bstack1lll1l1lll1_opy_.bstack1l11l111ll1_opy_),
        }
        for when in (bstack11111l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᒭ"), bstack11111l_opy_ (u"ࠤࡦࡥࡱࡲࠢᒮ"), bstack11111l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᒯ")):
            bstack1l11lll1lll_opy_ = args[1].get_records(when)
            if not bstack1l11lll1lll_opy_:
                continue
            records = [
                bstack1ll1llll111_opy_(
                    kind=TestFramework.bstack1ll11111ll1_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack11111l_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠢᒰ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack11111l_opy_ (u"ࠧࡩࡲࡦࡣࡷࡩࡩࠨᒱ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11lll1lll_opy_
                if isinstance(getattr(r, bstack11111l_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢᒲ"), None), str) and r.message.strip()
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
    def __1l11l1ll11l_opy_(test) -> Dict[str, Any]:
        bstack11lll1l1_opy_ = bstack1lll1l1lll1_opy_.__1l111ll1l11_opy_(test.location) if hasattr(test, bstack11111l_opy_ (u"ࠢ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠤᒳ")) else getattr(test, bstack11111l_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᒴ"), None)
        test_name = test.name if hasattr(test, bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᒵ")) else None
        bstack1l11ll1l11l_opy_ = test.fspath.strpath if hasattr(test, bstack11111l_opy_ (u"ࠥࡪࡸࡶࡡࡵࡪࠥᒶ")) and test.fspath else None
        if not bstack11lll1l1_opy_ or not test_name or not bstack1l11ll1l11l_opy_:
            return None
        code = None
        if hasattr(test, bstack11111l_opy_ (u"ࠦࡴࡨࡪࠣᒷ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l111l111ll_opy_ = []
        try:
            bstack1l111l111ll_opy_ = bstack1l1ll11l1l_opy_.bstack111ll1l1l1_opy_(test)
        except:
            bstack1lll1l1lll1_opy_.logger.warning(bstack11111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡦࡵࡷࠤࡸࡩ࡯ࡱࡧࡶ࠰ࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡷ࡫ࡳࡰ࡮ࡹࡩࡩࠦࡩ࡯ࠢࡆࡐࡎࠨᒸ"))
        return {
            TestFramework.bstack1ll1l1111l1_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l1lll1l_opy_: bstack11lll1l1_opy_,
            TestFramework.bstack1ll1l1lll11_opy_: test_name,
            TestFramework.bstack1l1ll1ll1l1_opy_: getattr(test, bstack11111l_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᒹ"), None),
            TestFramework.bstack1l11ll11lll_opy_: bstack1l11ll1l11l_opy_,
            TestFramework.bstack1l11lll111l_opy_: bstack1lll1l1lll1_opy_.__1l11l1lll11_opy_(test),
            TestFramework.bstack1l11l11llll_opy_: code,
            TestFramework.bstack1l1l1l1llll_opy_: TestFramework.bstack1l11l11ll11_opy_,
            TestFramework.bstack1l1l111l1ll_opy_: bstack11lll1l1_opy_,
            TestFramework.bstack1l111l1111l_opy_: bstack1l111l111ll_opy_
        }
    @staticmethod
    def __1l11l1lll11_opy_(test) -> List[str]:
        markers = []
        current = test
        while current:
            own_markers = getattr(current, bstack11111l_opy_ (u"ࠢࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠧᒺ"), [])
            markers.extend([getattr(m, bstack11111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᒻ"), None) for m in own_markers if getattr(m, bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᒼ"), None)])
            current = getattr(current, bstack11111l_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᒽ"), None)
        return markers
    @staticmethod
    def __1l111ll1l11_opy_(location):
        return bstack11111l_opy_ (u"ࠦ࠿ࡀࠢᒾ").join(filter(lambda x: isinstance(x, str), location))