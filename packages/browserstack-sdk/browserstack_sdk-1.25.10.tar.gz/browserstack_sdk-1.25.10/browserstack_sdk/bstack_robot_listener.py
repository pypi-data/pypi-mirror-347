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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l11l111_opy_ import RobotHandler
from bstack_utils.capture import bstack11l111l111_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack111ll1ll1l_opy_, bstack11l1111lll_opy_, bstack11l111lll1_opy_
from bstack_utils.bstack11l111llll_opy_ import bstack1l1ll11l1l_opy_
from bstack_utils.bstack111lll1lll_opy_ import bstack1111lll11_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l11llll1_opy_, bstack1l11l1lll_opy_, Result, \
    bstack111l1lllll_opy_, bstack111l11llll_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ༜"): [],
        bstack11111l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫ༝"): [],
        bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ༞"): []
    }
    bstack111lll11ll_opy_ = []
    bstack111l1l1ll1_opy_ = []
    @staticmethod
    def bstack111lllll11_opy_(log):
        if not ((isinstance(log[bstack11111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༟")], list) or (isinstance(log[bstack11111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༠")], dict)) and len(log[bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༡")])>0) or (isinstance(log[bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༢")], str) and log[bstack11111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༣")].strip())):
            return
        active = bstack1l1ll11l1l_opy_.bstack111llll1ll_opy_()
        log = {
            bstack11111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ༤"): log[bstack11111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ༥")],
            bstack11111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ༦"): bstack111l11llll_opy_().isoformat() + bstack11111l_opy_ (u"ࠨ࡜ࠪ༧"),
            bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༨"): log[bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༩")],
        }
        if active:
            if active[bstack11111l_opy_ (u"ࠫࡹࡿࡰࡦࠩ༪")] == bstack11111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ༫"):
                log[bstack11111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭༬")] = active[bstack11111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ༭")]
            elif active[bstack11111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭༮")] == bstack11111l_opy_ (u"ࠩࡷࡩࡸࡺࠧ༯"):
                log[bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ༰")] = active[bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ༱")]
        bstack1111lll11_opy_.bstack1l1lll1111_opy_([log])
    def __init__(self):
        self.messages = bstack111l11ll11_opy_()
        self._111ll11l11_opy_ = None
        self._111ll11111_opy_ = None
        self._111l11l11l_opy_ = OrderedDict()
        self.bstack11l11111l1_opy_ = bstack11l111l111_opy_(self.bstack111lllll11_opy_)
    @bstack111l1lllll_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l111lll_opy_()
        if not self._111l11l11l_opy_.get(attrs.get(bstack11111l_opy_ (u"ࠬ࡯ࡤࠨ༲")), None):
            self._111l11l11l_opy_[attrs.get(bstack11111l_opy_ (u"࠭ࡩࡥࠩ༳"))] = {}
        bstack111ll1111l_opy_ = bstack11l111lll1_opy_(
                bstack111lll111l_opy_=attrs.get(bstack11111l_opy_ (u"ࠧࡪࡦࠪ༴")),
                name=name,
                started_at=bstack1l11l1lll_opy_(),
                file_path=os.path.relpath(attrs[bstack11111l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ༵")], start=os.getcwd()) if attrs.get(bstack11111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ༶")) != bstack11111l_opy_ (u"༷ࠪࠫ") else bstack11111l_opy_ (u"ࠫࠬ༸"),
                framework=bstack11111l_opy_ (u"ࠬࡘ࡯ࡣࡱࡷ༹ࠫ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11111l_opy_ (u"࠭ࡩࡥࠩ༺"), None)
        self._111l11l11l_opy_[attrs.get(bstack11111l_opy_ (u"ࠧࡪࡦࠪ༻"))][bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ༼")] = bstack111ll1111l_opy_
    @bstack111l1lllll_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l1l1lll_opy_()
        self._111l11lll1_opy_(messages)
        for bstack111l1l11l1_opy_ in self.bstack111lll11ll_opy_:
            bstack111l1l11l1_opy_[bstack11111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ༽")][bstack11111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ༾")].extend(self.store[bstack11111l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ༿")])
            bstack1111lll11_opy_.bstack1l1l1l1l1_opy_(bstack111l1l11l1_opy_)
        self.bstack111lll11ll_opy_ = []
        self.store[bstack11111l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫཀ")] = []
    @bstack111l1lllll_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l11111l1_opy_.start()
        if not self._111l11l11l_opy_.get(attrs.get(bstack11111l_opy_ (u"࠭ࡩࡥࠩཁ")), None):
            self._111l11l11l_opy_[attrs.get(bstack11111l_opy_ (u"ࠧࡪࡦࠪག"))] = {}
        driver = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧགྷ"), None)
        bstack111lllllll_opy_ = bstack11l111lll1_opy_(
            bstack111lll111l_opy_=attrs.get(bstack11111l_opy_ (u"ࠩ࡬ࡨࠬང")),
            name=name,
            started_at=bstack1l11l1lll_opy_(),
            file_path=os.path.relpath(attrs[bstack11111l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪཅ")], start=os.getcwd()),
            scope=RobotHandler.bstack111ll1l1l1_opy_(attrs.get(bstack11111l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫཆ"), None)),
            framework=bstack11111l_opy_ (u"ࠬࡘ࡯ࡣࡱࡷࠫཇ"),
            tags=attrs[bstack11111l_opy_ (u"࠭ࡴࡢࡩࡶࠫ཈")],
            hooks=self.store[bstack11111l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ཉ")],
            bstack11l11111ll_opy_=bstack1111lll11_opy_.bstack111llllll1_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11111l_opy_ (u"ࠣࡽࢀࠤࡡࡴࠠࡼࡿࠥཊ").format(bstack11111l_opy_ (u"ࠤࠣࠦཋ").join(attrs[bstack11111l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨཌ")]), name) if attrs[bstack11111l_opy_ (u"ࠫࡹࡧࡧࡴࠩཌྷ")] else name
        )
        self._111l11l11l_opy_[attrs.get(bstack11111l_opy_ (u"ࠬ࡯ࡤࠨཎ"))][bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཏ")] = bstack111lllllll_opy_
        threading.current_thread().current_test_uuid = bstack111lllllll_opy_.bstack111l1ll1ll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11111l_opy_ (u"ࠧࡪࡦࠪཐ"), None)
        self.bstack111lllll1l_opy_(bstack11111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩད"), bstack111lllllll_opy_)
    @bstack111l1lllll_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l11111l1_opy_.reset()
        bstack111l11ll1l_opy_ = bstack111ll1llll_opy_.get(attrs.get(bstack11111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩདྷ")), bstack11111l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫན"))
        self._111l11l11l_opy_[attrs.get(bstack11111l_opy_ (u"ࠫ࡮ࡪࠧཔ"))][bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཕ")].stop(time=bstack1l11l1lll_opy_(), duration=int(attrs.get(bstack11111l_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫབ"), bstack11111l_opy_ (u"ࠧ࠱ࠩབྷ"))), result=Result(result=bstack111l11ll1l_opy_, exception=attrs.get(bstack11111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩམ")), bstack111lll1ll1_opy_=[attrs.get(bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪཙ"))]))
        self.bstack111lllll1l_opy_(bstack11111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬཚ"), self._111l11l11l_opy_[attrs.get(bstack11111l_opy_ (u"ࠫ࡮ࡪࠧཛ"))][bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཛྷ")], True)
        self.store[bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪཝ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111l1lllll_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l111lll_opy_()
        current_test_id = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩཞ"), None)
        bstack111ll1l11l_opy_ = current_test_id if bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪཟ"), None) else bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡺ࡯ࡴࡦࡡ࡬ࡨࠬའ"), None)
        if attrs.get(bstack11111l_opy_ (u"ࠪࡸࡾࡶࡥࠨཡ"), bstack11111l_opy_ (u"ࠫࠬར")).lower() in [bstack11111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫལ"), bstack11111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨཤ")]:
            hook_type = bstack111l1l11ll_opy_(attrs.get(bstack11111l_opy_ (u"ࠧࡵࡻࡳࡩࠬཥ")), bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬས"), None))
            hook_name = bstack11111l_opy_ (u"ࠩࡾࢁࠬཧ").format(attrs.get(bstack11111l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪཨ"), bstack11111l_opy_ (u"ࠫࠬཀྵ")))
            if hook_type in [bstack11111l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍࠩཪ"), bstack11111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩཫ")]:
                hook_name = bstack11111l_opy_ (u"ࠧ࡜ࡽࢀࡡࠥࢁࡽࠨཬ").format(bstack111l1lll1l_opy_.get(hook_type), attrs.get(bstack11111l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨ཭"), bstack11111l_opy_ (u"ࠩࠪ཮")))
            bstack111lll1l11_opy_ = bstack11l1111lll_opy_(
                bstack111lll111l_opy_=bstack111ll1l11l_opy_ + bstack11111l_opy_ (u"ࠪ࠱ࠬ཯") + attrs.get(bstack11111l_opy_ (u"ࠫࡹࡿࡰࡦࠩ཰"), bstack11111l_opy_ (u"ཱࠬ࠭")).lower(),
                name=hook_name,
                started_at=bstack1l11l1lll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪི࠭")), start=os.getcwd()),
                framework=bstack11111l_opy_ (u"ࠧࡓࡱࡥࡳࡹཱི࠭"),
                tags=attrs[bstack11111l_opy_ (u"ࠨࡶࡤ࡫ࡸུ࠭")],
                scope=RobotHandler.bstack111ll1l1l1_opy_(attrs.get(bstack11111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦཱུࠩ"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111lll1l11_opy_.bstack111l1ll1ll_opy_()
            threading.current_thread().current_hook_id = bstack111ll1l11l_opy_ + bstack11111l_opy_ (u"ࠪ࠱ࠬྲྀ") + attrs.get(bstack11111l_opy_ (u"ࠫࡹࡿࡰࡦࠩཷ"), bstack11111l_opy_ (u"ࠬ࠭ླྀ")).lower()
            self.store[bstack11111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪཹ")] = [bstack111lll1l11_opy_.bstack111l1ll1ll_opy_()]
            if bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧེࠫ"), None):
                self.store[bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷཻࠬ")].append(bstack111lll1l11_opy_.bstack111l1ll1ll_opy_())
            else:
                self.store[bstack11111l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭ࡡ࡫ࡳࡴࡱࡳࠨོ")].append(bstack111lll1l11_opy_.bstack111l1ll1ll_opy_())
            if bstack111ll1l11l_opy_:
                self._111l11l11l_opy_[bstack111ll1l11l_opy_ + bstack11111l_opy_ (u"ࠪ࠱ཽࠬ") + attrs.get(bstack11111l_opy_ (u"ࠫࡹࡿࡰࡦࠩཾ"), bstack11111l_opy_ (u"ࠬ࠭ཿ")).lower()] = { bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢྀࠩ"): bstack111lll1l11_opy_ }
            bstack1111lll11_opy_.bstack111lllll1l_opy_(bstack11111l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨཱྀ"), bstack111lll1l11_opy_)
        else:
            bstack11l1111l1l_opy_ = {
                bstack11111l_opy_ (u"ࠨ࡫ࡧࠫྂ"): uuid4().__str__(),
                bstack11111l_opy_ (u"ࠩࡷࡩࡽࡺࠧྃ"): bstack11111l_opy_ (u"ࠪࡿࢂࠦࡻࡾ྄ࠩ").format(attrs.get(bstack11111l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ྅")), attrs.get(bstack11111l_opy_ (u"ࠬࡧࡲࡨࡵࠪ྆"), bstack11111l_opy_ (u"࠭ࠧ྇"))) if attrs.get(bstack11111l_opy_ (u"ࠧࡢࡴࡪࡷࠬྈ"), []) else attrs.get(bstack11111l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨྉ")),
                bstack11111l_opy_ (u"ࠩࡶࡸࡪࡶ࡟ࡢࡴࡪࡹࡲ࡫࡮ࡵࠩྊ"): attrs.get(bstack11111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨྋ"), []),
                bstack11111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨྌ"): bstack1l11l1lll_opy_(),
                bstack11111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬྍ"): bstack11111l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧྎ"),
                bstack11111l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬྏ"): attrs.get(bstack11111l_opy_ (u"ࠨࡦࡲࡧࠬྐ"), bstack11111l_opy_ (u"ࠩࠪྑ"))
            }
            if attrs.get(bstack11111l_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫྒ"), bstack11111l_opy_ (u"ࠫࠬྒྷ")) != bstack11111l_opy_ (u"ࠬ࠭ྔ"):
                bstack11l1111l1l_opy_[bstack11111l_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧྕ")] = attrs.get(bstack11111l_opy_ (u"ࠧ࡭࡫ࡥࡲࡦࡳࡥࠨྖ"))
            if not self.bstack111l1l1ll1_opy_:
                self._111l11l11l_opy_[self._111l1l1111_opy_()][bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྗ")].add_step(bstack11l1111l1l_opy_)
                threading.current_thread().current_step_uuid = bstack11l1111l1l_opy_[bstack11111l_opy_ (u"ࠩ࡬ࡨࠬ྘")]
            self.bstack111l1l1ll1_opy_.append(bstack11l1111l1l_opy_)
    @bstack111l1lllll_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l1l1lll_opy_()
        self._111l11lll1_opy_(messages)
        current_test_id = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬྙ"), None)
        bstack111ll1l11l_opy_ = current_test_id if current_test_id else bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡵࡪࡶࡨࡣ࡮ࡪࠧྚ"), None)
        bstack111l1l1l11_opy_ = bstack111ll1llll_opy_.get(attrs.get(bstack11111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬྛ")), bstack11111l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧྜ"))
        bstack111ll1lll1_opy_ = attrs.get(bstack11111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྜྷ"))
        if bstack111l1l1l11_opy_ != bstack11111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩྞ") and not attrs.get(bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྟ")) and self._111ll11l11_opy_:
            bstack111ll1lll1_opy_ = self._111ll11l11_opy_
        bstack11l111l1l1_opy_ = Result(result=bstack111l1l1l11_opy_, exception=bstack111ll1lll1_opy_, bstack111lll1ll1_opy_=[bstack111ll1lll1_opy_])
        if attrs.get(bstack11111l_opy_ (u"ࠪࡸࡾࡶࡥࠨྠ"), bstack11111l_opy_ (u"ࠫࠬྡ")).lower() in [bstack11111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫྡྷ"), bstack11111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨྣ")]:
            bstack111ll1l11l_opy_ = current_test_id if current_test_id else bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪྤ"), None)
            if bstack111ll1l11l_opy_:
                bstack111llll111_opy_ = bstack111ll1l11l_opy_ + bstack11111l_opy_ (u"ࠣ࠯ࠥྥ") + attrs.get(bstack11111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧྦ"), bstack11111l_opy_ (u"ࠪࠫྦྷ")).lower()
                self._111l11l11l_opy_[bstack111llll111_opy_][bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧྨ")].stop(time=bstack1l11l1lll_opy_(), duration=int(attrs.get(bstack11111l_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪྩ"), bstack11111l_opy_ (u"࠭࠰ࠨྪ"))), result=bstack11l111l1l1_opy_)
                bstack1111lll11_opy_.bstack111lllll1l_opy_(bstack11111l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩྫ"), self._111l11l11l_opy_[bstack111llll111_opy_][bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫྫྷ")])
        else:
            bstack111ll1l11l_opy_ = current_test_id if current_test_id else bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠ࡫ࡧࠫྭ"), None)
            if bstack111ll1l11l_opy_ and len(self.bstack111l1l1ll1_opy_) == 1:
                current_step_uuid = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡺࡥࡱࡡࡸࡹ࡮ࡪࠧྮ"), None)
                self._111l11l11l_opy_[bstack111ll1l11l_opy_][bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧྯ")].bstack111llll1l1_opy_(current_step_uuid, duration=int(attrs.get(bstack11111l_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪྰ"), bstack11111l_opy_ (u"࠭࠰ࠨྱ"))), result=bstack11l111l1l1_opy_)
            else:
                self.bstack111ll111ll_opy_(attrs)
            self.bstack111l1l1ll1_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11111l_opy_ (u"ࠧࡩࡶࡰࡰࠬྲ"), bstack11111l_opy_ (u"ࠨࡰࡲࠫླ")) == bstack11111l_opy_ (u"ࠩࡼࡩࡸ࠭ྴ"):
                return
            self.messages.push(message)
            logs = []
            if bstack1l1ll11l1l_opy_.bstack111llll1ll_opy_():
                logs.append({
                    bstack11111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ྵ"): bstack1l11l1lll_opy_(),
                    bstack11111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྶ"): message.get(bstack11111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ྷ")),
                    bstack11111l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬྸ"): message.get(bstack11111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ྐྵ")),
                    **bstack1l1ll11l1l_opy_.bstack111llll1ll_opy_()
                })
                if len(logs) > 0:
                    bstack1111lll11_opy_.bstack1l1lll1111_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1111lll11_opy_.bstack111l1llll1_opy_()
    def bstack111ll111ll_opy_(self, bstack111l1ll11l_opy_):
        if not bstack1l1ll11l1l_opy_.bstack111llll1ll_opy_():
            return
        kwname = bstack11111l_opy_ (u"ࠨࡽࢀࠤࢀࢃࠧྺ").format(bstack111l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩྻ")), bstack111l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨྼ"), bstack11111l_opy_ (u"ࠫࠬ྽"))) if bstack111l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠬࡧࡲࡨࡵࠪ྾"), []) else bstack111l1ll11l_opy_.get(bstack11111l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭྿"))
        error_message = bstack11111l_opy_ (u"ࠢ࡬ࡹࡱࡥࡲ࡫࠺ࠡ࡞ࠥࡿ࠵ࢃ࡜ࠣࠢࡿࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࡢࠢࡼ࠳ࢀࡠࠧࠦࡼࠡࡧࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࡢࠢࡼ࠴ࢀࡠࠧࠨ࿀").format(kwname, bstack111l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ࿁")), str(bstack111l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿂"))))
        bstack111l11l1l1_opy_ = bstack11111l_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠤ࿃").format(kwname, bstack111l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ࿄")))
        bstack111lll11l1_opy_ = error_message if bstack111l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭࿅")) else bstack111l11l1l1_opy_
        bstack111l1lll11_opy_ = {
            bstack11111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱ࿆ࠩ"): self.bstack111l1l1ll1_opy_[-1].get(bstack11111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ࿇"), bstack1l11l1lll_opy_()),
            bstack11111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ࿈"): bstack111lll11l1_opy_,
            bstack11111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ࿉"): bstack11111l_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩ࿊") if bstack111l1ll11l_opy_.get(bstack11111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ࿋")) == bstack11111l_opy_ (u"ࠬࡌࡁࡊࡎࠪ࿌") else bstack11111l_opy_ (u"࠭ࡉࡏࡈࡒࠫ࿍"),
            **bstack1l1ll11l1l_opy_.bstack111llll1ll_opy_()
        }
        bstack1111lll11_opy_.bstack1l1lll1111_opy_([bstack111l1lll11_opy_])
    def _111l1l1111_opy_(self):
        for bstack111lll111l_opy_ in reversed(self._111l11l11l_opy_):
            bstack111l1ll111_opy_ = bstack111lll111l_opy_
            data = self._111l11l11l_opy_[bstack111lll111l_opy_][bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ࿎")]
            if isinstance(data, bstack11l1111lll_opy_):
                if not bstack11111l_opy_ (u"ࠨࡇࡄࡇࡍ࠭࿏") in data.bstack111ll1l1ll_opy_():
                    return bstack111l1ll111_opy_
            else:
                return bstack111l1ll111_opy_
    def _111l11lll1_opy_(self, messages):
        try:
            bstack111lll1111_opy_ = BuiltIn().get_variable_value(bstack11111l_opy_ (u"ࠤࠧࡿࡑࡕࡇࠡࡎࡈ࡚ࡊࡒࡽࠣ࿐")) in (bstack111ll11lll_opy_.DEBUG, bstack111ll11lll_opy_.TRACE)
            for message, bstack111l11l1ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿑"))
                level = message.get(bstack11111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ࿒"))
                if level == bstack111ll11lll_opy_.FAIL:
                    self._111ll11l11_opy_ = name or self._111ll11l11_opy_
                    self._111ll11111_opy_ = bstack111l11l1ll_opy_.get(bstack11111l_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨ࿓")) if bstack111lll1111_opy_ and bstack111l11l1ll_opy_ else self._111ll11111_opy_
        except:
            pass
    @classmethod
    def bstack111lllll1l_opy_(self, event: str, bstack111lll1l1l_opy_: bstack111ll1ll1l_opy_, bstack111ll111l1_opy_=False):
        if event == bstack11111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ࿔"):
            bstack111lll1l1l_opy_.set(hooks=self.store[bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ࿕")])
        if event == bstack11111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ࿖"):
            event = bstack11111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ࿗")
        if bstack111ll111l1_opy_:
            bstack111ll1ll11_opy_ = {
                bstack11111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ࿘"): event,
                bstack111lll1l1l_opy_.bstack111ll11l1l_opy_(): bstack111lll1l1l_opy_.bstack111l1l1l1l_opy_(event)
            }
            self.bstack111lll11ll_opy_.append(bstack111ll1ll11_opy_)
        else:
            bstack1111lll11_opy_.bstack111lllll1l_opy_(event, bstack111lll1l1l_opy_)
class bstack111l11ll11_opy_:
    def __init__(self):
        self._111l1l111l_opy_ = []
    def bstack111l111lll_opy_(self):
        self._111l1l111l_opy_.append([])
    def bstack111l1l1lll_opy_(self):
        return self._111l1l111l_opy_.pop() if self._111l1l111l_opy_ else list()
    def push(self, message):
        self._111l1l111l_opy_[-1].append(message) if self._111l1l111l_opy_ else self._111l1l111l_opy_.append([message])
class bstack111ll11lll_opy_:
    FAIL = bstack11111l_opy_ (u"ࠫࡋࡇࡉࡍࠩ࿙")
    ERROR = bstack11111l_opy_ (u"ࠬࡋࡒࡓࡑࡕࠫ࿚")
    WARNING = bstack11111l_opy_ (u"࠭ࡗࡂࡔࡑࠫ࿛")
    bstack111ll11ll1_opy_ = bstack11111l_opy_ (u"ࠧࡊࡐࡉࡓࠬ࿜")
    DEBUG = bstack11111l_opy_ (u"ࠨࡆࡈࡆ࡚ࡍࠧ࿝")
    TRACE = bstack11111l_opy_ (u"ࠩࡗࡖࡆࡉࡅࠨ࿞")
    bstack111ll1l111_opy_ = [FAIL, ERROR]
def bstack111l1ll1l1_opy_(bstack111l111ll1_opy_):
    if not bstack111l111ll1_opy_:
        return None
    if bstack111l111ll1_opy_.get(bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿟"), None):
        return getattr(bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿠")], bstack11111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ࿡"), None)
    return bstack111l111ll1_opy_.get(bstack11111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ࿢"), None)
def bstack111l1l11ll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭࿣"), bstack11111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ࿤")]:
        return
    if hook_type.lower() == bstack11111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ࿥"):
        if current_test_uuid is None:
            return bstack11111l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧ࿦")
        else:
            return bstack11111l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩ࿧")
    elif hook_type.lower() == bstack11111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧ࿨"):
        if current_test_uuid is None:
            return bstack11111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩ࿩")
        else:
            return bstack11111l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫ࿪")