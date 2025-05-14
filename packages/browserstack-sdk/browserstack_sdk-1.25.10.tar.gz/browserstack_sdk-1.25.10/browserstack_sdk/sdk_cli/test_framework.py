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
import logging
from enum import Enum
import os
import threading
import traceback
from typing import Dict, List, Any, Callable, Tuple, Union
import abc
from datetime import datetime, timezone
from dataclasses import dataclass
from browserstack_sdk.sdk_cli.bstack1111l1ll1l_opy_ import bstack1111l1l11l_opy_
from browserstack_sdk.sdk_cli.bstack11111lllll_opy_ import bstack111111lll1_opy_, bstack11111l11l1_opy_
class bstack1ll1lll1lll_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11111l_opy_ (u"ࠨࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡻࡾࠤᓸ").format(self.name)
class bstack1lll11l1ll1_opy_(Enum):
    NONE = 0
    BEFORE_ALL = 1
    LOG = 2
    SETUP_FIXTURE = 3
    INIT_TEST = 4
    BEFORE_EACH = 5
    AFTER_EACH = 6
    TEST = 7
    STEP = 8
    LOG_REPORT = 9
    AFTER_ALL = 10
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack11111l_opy_ (u"ࠢࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᓹ").format(self.name)
class bstack1lll1ll1lll_opy_(bstack111111lll1_opy_):
    bstack1ll1ll11lll_opy_: List[str]
    bstack1l111l1ll1l_opy_: Dict[str, str]
    state: bstack1lll11l1ll1_opy_
    bstack111111l11l_opy_: datetime
    bstack111111111l_opy_: datetime
    def __init__(
        self,
        context: bstack11111l11l1_opy_,
        bstack1ll1ll11lll_opy_: List[str],
        bstack1l111l1ll1l_opy_: Dict[str, str],
        state=bstack1lll11l1ll1_opy_.NONE,
    ):
        super().__init__(context)
        self.bstack1ll1ll11lll_opy_ = bstack1ll1ll11lll_opy_
        self.bstack1l111l1ll1l_opy_ = bstack1l111l1ll1l_opy_
        self.state = state
        self.bstack111111l11l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack111111111l_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llllllll1l_opy_(self, bstack11111l111l_opy_: bstack1lll11l1ll1_opy_):
        bstack11111ll1ll_opy_ = bstack1lll11l1ll1_opy_(bstack11111l111l_opy_).name
        if not bstack11111ll1ll_opy_:
            return False
        if bstack11111l111l_opy_ == self.state:
            return False
        self.state = bstack11111l111l_opy_
        self.bstack111111111l_opy_ = datetime.now(tz=timezone.utc)
        return True
@dataclass
class bstack1l11l1l11l1_opy_:
    test_framework_name: str
    test_framework_version: str
    platform_index: int
@dataclass
class bstack1ll1llll111_opy_:
    kind: str
    message: str
    level: Union[None, str] = None
    timestamp: Union[None, datetime] = datetime.now(tz=timezone.utc)
    fileName: str = None
    bstack1l1lll11ll1_opy_: int = None
    bstack1l1lllll11l_opy_: str = None
    bstack1lllllll_opy_: str = None
    bstack1llll1llll_opy_: str = None
    bstack1ll111ll1ll_opy_: str = None
    bstack1l11l1111ll_opy_: str = None
class TestFramework(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1ll1l1111l1_opy_ = bstack11111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠦᓺ")
    bstack1l11l1lll1l_opy_ = bstack11111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡪࡦࠥᓻ")
    bstack1ll1l1lll11_opy_ = bstack11111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡰࡤࡱࡪࠨᓼ")
    bstack1l11ll11lll_opy_ = bstack11111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠧᓽ")
    bstack1l11lll111l_opy_ = bstack11111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡸࡦ࡭ࡳࠣᓾ")
    bstack1l1l1l1llll_opy_ = bstack11111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷ࡫ࡳࡶ࡮ࡷࠦᓿ")
    bstack1ll111111ll_opy_ = bstack11111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡴࡷ࡯ࡸࡤࡧࡴࠣᔀ")
    bstack1ll1111l1ll_opy_ = bstack11111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᔁ")
    bstack1l1lll111l1_opy_ = bstack11111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡦࡰࡧࡩࡩࡥࡡࡵࠤᔂ")
    bstack1l111l11lll_opy_ = bstack11111l_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᔃ")
    bstack1ll1l1ll1ll_opy_ = bstack11111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠥᔄ")
    bstack1ll1111ll11_opy_ = bstack11111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠢᔅ")
    bstack1l11l11llll_opy_ = bstack11111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡨࡵࡤࡦࠤᔆ")
    bstack1l1ll1ll1l1_opy_ = bstack11111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠤᔇ")
    bstack1ll1l111l1l_opy_ = bstack11111l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࠤᔈ")
    bstack1l1l1ll1111_opy_ = bstack11111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧࡣ࡬ࡰࡺࡸࡥࠣᔉ")
    bstack1l11l111111_opy_ = bstack11111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠢᔊ")
    bstack1l11l1l111l_opy_ = bstack11111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡯ࡳ࡬ࡹࠢᔋ")
    bstack1l11lll1111_opy_ = bstack11111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡱࡪࡺࡡࠣᔌ")
    bstack1l111l1111l_opy_ = bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡸࡩ࡯ࡱࡧࡶࠫᔍ")
    bstack1l1l111l1ll_opy_ = bstack11111l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡦࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᔎ")
    bstack1l111ll111l_opy_ = bstack11111l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᔏ")
    bstack1l11l11lll1_opy_ = bstack11111l_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡧࡱࡨࡪࡪ࡟ࡢࡶࠥᔐ")
    bstack1l11ll11ll1_opy_ = bstack11111l_opy_ (u"ࠥ࡬ࡴࡵ࡫ࡠ࡫ࡧࠦᔑ")
    bstack1l11l1llll1_opy_ = bstack11111l_opy_ (u"ࠦ࡭ࡵ࡯࡬ࡡࡵࡩࡸࡻ࡬ࡵࠤᔒ")
    bstack1l11l1l1ll1_opy_ = bstack11111l_opy_ (u"ࠧ࡮࡯ࡰ࡭ࡢࡰࡴ࡭ࡳࠣᔓ")
    bstack1l111l1l11l_opy_ = bstack11111l_opy_ (u"ࠨࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠤᔔ")
    bstack1l111l1ll11_opy_ = bstack11111l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᔕ")
    bstack1l11ll1l1ll_opy_ = bstack11111l_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠥᔖ")
    bstack1l11l11ll11_opy_ = bstack11111l_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥᔗ")
    bstack1l11l11l1ll_opy_ = bstack11111l_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦᔘ")
    bstack1l1llll1lll_opy_ = bstack11111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙ࠨᔙ")
    bstack1ll11111ll1_opy_ = bstack11111l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡐࡔࡍࠢᔚ")
    bstack1l1llll11ll_opy_ = bstack11111l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᔛ")
    bstack1lllllllll1_opy_: Dict[str, bstack1lll1ll1lll_opy_] = dict()
    bstack1l1111l1lll_opy_: Dict[str, List[Callable]] = dict()
    bstack1ll1ll11lll_opy_: List[str]
    bstack1l111l1ll1l_opy_: Dict[str, str]
    def __init__(
        self,
        bstack1ll1ll11lll_opy_: List[str],
        bstack1l111l1ll1l_opy_: Dict[str, str],
        bstack1111l1ll1l_opy_: bstack1111l1l11l_opy_
    ):
        self.bstack1ll1ll11lll_opy_ = bstack1ll1ll11lll_opy_
        self.bstack1l111l1ll1l_opy_ = bstack1l111l1ll1l_opy_
        self.bstack1111l1ll1l_opy_ = bstack1111l1ll1l_opy_
    def track_event(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll11l1ll1_opy_,
        test_hook_state: bstack1ll1lll1lll_opy_,
        *args,
        **kwargs,
    ):
        self.logger.debug(bstack11111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡾࠢࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࢃࠠࡢࡴࡪࡷࡂࢁࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࡽࢀࠦᔜ").format(test_framework_state,test_hook_state,args,kwargs))
    def bstack1l111lll11l_opy_(
        self,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l11llll1l1_opy_ = TestFramework.bstack1l11llllll1_opy_(bstack1111111111_opy_)
        if not bstack1l11llll1l1_opy_ in TestFramework.bstack1l1111l1lll_opy_:
            return
        self.logger.debug(bstack11111l_opy_ (u"ࠣ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡿࢂࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠤᔝ").format(len(TestFramework.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_])))
        for callback in TestFramework.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_]:
            try:
                callback(self, instance, bstack1111111111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡ࡫ࡱࡺࡴࡱࡩ࡯ࡩࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯࠿ࠦࡻࡾࠤᔞ").format(e))
                traceback.print_exc()
    @abc.abstractmethod
    def bstack1l1lllll1ll_opy_(self):
        return
    @abc.abstractmethod
    def bstack1ll1111111l_opy_(self, instance, bstack1111111111_opy_):
        return
    @abc.abstractmethod
    def bstack1l1lll1ll11_opy_(self, instance, bstack1111111111_opy_):
        return
    @staticmethod
    def bstack1llllllllll_opy_(target: object, strict=True):
        if target is None:
            return None
        ctx = bstack111111lll1_opy_.create_context(target)
        instance = TestFramework.bstack1lllllllll1_opy_.get(ctx.id, None)
        if instance and instance.bstack11111l1ll1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll111111l1_opy_(reverse=True) -> List[bstack1lll1ll1lll_opy_]:
        thread_id = threading.get_ident()
        process_id = os.getpid()
        return sorted(
            filter(
                lambda t: t.context.thread_id == thread_id
                and t.context.process_id == process_id,
                TestFramework.bstack1lllllllll1_opy_.values(),
            ),
            key=lambda t: t.bstack111111l11l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack111111l1l1_opy_(ctx: bstack11111l11l1_opy_, reverse=True) -> List[bstack1lll1ll1lll_opy_]:
        return sorted(
            filter(
                lambda t: t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                TestFramework.bstack1lllllllll1_opy_.values(),
            ),
            key=lambda t: t.bstack111111l11l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack11111111ll_opy_(instance: bstack1lll1ll1lll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1111111l11_opy_(instance: bstack1lll1ll1lll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llllllll1l_opy_(instance: bstack1lll1ll1lll_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11111l_opy_ (u"ࠥࡷࡪࡺ࡟ࡴࡶࡤࡸࡪࡀࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࡾࢁࠥࡱࡥࡺ࠿ࡾࢁࠥࡼࡡ࡭ࡷࡨࡁࢀࢃࠢᔟ").format(instance.ref(),key,value))
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l1l1l11_opy_(instance: bstack1lll1ll1lll_opy_, entries: Dict[str, Any]):
        TestFramework.logger.debug(bstack11111l_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀࢃࠠࡦࡰࡷࡶ࡮࡫ࡳ࠾ࡽࢀࠦᔠ").format(instance.ref(),entries,))
        instance.data.update(entries)
        return True
    @staticmethod
    def bstack1l1111l1ll1_opy_(instance: bstack1lll11l1ll1_opy_, key: str, value: Any):
        TestFramework.logger.debug(bstack11111l_opy_ (u"ࠧࡻࡰࡥࡣࡷࡩࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼࡿࠣ࡯ࡪࡿ࠽ࡼࡿࠣࡺࡦࡲࡵࡦ࠿ࡾࢁࠧᔡ").format(instance.ref(),key,value))
        instance.data.update(key, value)
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = TestFramework.bstack1llllllllll_opy_(target, strict)
        return TestFramework.bstack1111111l11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = TestFramework.bstack1llllllllll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    @staticmethod
    def bstack1l11l111lll_opy_(instance: bstack1lll1ll1lll_opy_, key: str, value: object):
        if instance == None:
            return
        instance.data[key] = value
    @staticmethod
    def bstack1l111ll11ll_opy_(instance: bstack1lll1ll1lll_opy_, key: str):
        return instance.data[key]
    @staticmethod
    def bstack1l11llllll1_opy_(bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_]):
        return bstack11111l_opy_ (u"ࠨ࠺ࠣᔢ").join((bstack1lll11l1ll1_opy_(bstack1111111111_opy_[0]).name, bstack1ll1lll1lll_opy_(bstack1111111111_opy_[1]).name))
    @staticmethod
    def bstack1ll1l111111_opy_(bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_], callback: Callable):
        bstack1l11llll1l1_opy_ = TestFramework.bstack1l11llllll1_opy_(bstack1111111111_opy_)
        TestFramework.logger.debug(bstack11111l_opy_ (u"ࠢࡴࡧࡷࡣ࡭ࡵ࡯࡬ࡡࡦࡥࡱࡲࡢࡢࡥ࡮࠾ࠥ࡮࡯ࡰ࡭ࡢࡶࡪ࡭ࡩࡴࡶࡵࡽࡤࡱࡥࡺ࠿ࡾࢁࠧᔣ").format(bstack1l11llll1l1_opy_))
        if not bstack1l11llll1l1_opy_ in TestFramework.bstack1l1111l1lll_opy_:
            TestFramework.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_] = []
        TestFramework.bstack1l1111l1lll_opy_[bstack1l11llll1l1_opy_].append(callback)
    @staticmethod
    def bstack1ll1111lll1_opy_(o):
        klass = o.__class__
        module = klass.__module__
        if module == bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡺࡩ࡯ࡵࠥᔤ"):
            return klass.__qualname__
        return module + bstack11111l_opy_ (u"ࠤ࠱ࠦᔥ") + klass.__qualname__
    @staticmethod
    def bstack1l1llll1ll1_opy_(obj, keys, default_value=None):
        return {k: getattr(obj, k, default_value) for k in keys}