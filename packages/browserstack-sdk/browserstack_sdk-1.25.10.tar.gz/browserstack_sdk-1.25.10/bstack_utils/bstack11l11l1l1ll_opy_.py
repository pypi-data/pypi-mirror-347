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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1l1l111l_opy_
from browserstack_sdk.bstack1l11l1ll1_opy_ import bstack1llllll11_opy_
def _11l11l1llll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11l11l11_opy_:
    def __init__(self, handler):
        self._11l11l1l11l_opy_ = {}
        self._11l11l1l111_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1llllll11_opy_.version()
        if bstack11l1l1l111l_opy_(pytest_version, bstack11111l_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨᯖ")) >= 0:
            self._11l11l1l11l_opy_[bstack11111l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯗ")] = Module._register_setup_function_fixture
            self._11l11l1l11l_opy_[bstack11111l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯘ")] = Module._register_setup_module_fixture
            self._11l11l1l11l_opy_[bstack11111l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᯙ")] = Class._register_setup_class_fixture
            self._11l11l1l11l_opy_[bstack11111l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯚ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11l11l1l_opy_(bstack11111l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯛ"))
            Module._register_setup_module_fixture = self.bstack11l11l11l1l_opy_(bstack11111l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯜ"))
            Class._register_setup_class_fixture = self.bstack11l11l11l1l_opy_(bstack11111l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᯝ"))
            Class._register_setup_method_fixture = self.bstack11l11l11l1l_opy_(bstack11111l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯞ"))
        else:
            self._11l11l1l11l_opy_[bstack11111l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᯟ")] = Module._inject_setup_function_fixture
            self._11l11l1l11l_opy_[bstack11111l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯠ")] = Module._inject_setup_module_fixture
            self._11l11l1l11l_opy_[bstack11111l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᯡ")] = Class._inject_setup_class_fixture
            self._11l11l1l11l_opy_[bstack11111l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᯢ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11l11l1l_opy_(bstack11111l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᯣ"))
            Module._inject_setup_module_fixture = self.bstack11l11l11l1l_opy_(bstack11111l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯤ"))
            Class._inject_setup_class_fixture = self.bstack11l11l11l1l_opy_(bstack11111l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᯥ"))
            Class._inject_setup_method_fixture = self.bstack11l11l11l1l_opy_(bstack11111l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ᯦ࠪ"))
    def bstack11l11l11lll_opy_(self, bstack11l11l11ll1_opy_, hook_type):
        bstack11l11l1ll1l_opy_ = id(bstack11l11l11ll1_opy_.__class__)
        if (bstack11l11l1ll1l_opy_, hook_type) in self._11l11l1l111_opy_:
            return
        meth = getattr(bstack11l11l11ll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11l1l111_opy_[(bstack11l11l1ll1l_opy_, hook_type)] = meth
            setattr(bstack11l11l11ll1_opy_, hook_type, self.bstack11l11ll11l1_opy_(hook_type, bstack11l11l1ll1l_opy_))
    def bstack11l11l1lll1_opy_(self, instance, bstack11l11ll111l_opy_):
        if bstack11l11ll111l_opy_ == bstack11111l_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᯧ"):
            self.bstack11l11l11lll_opy_(instance.obj, bstack11111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᯨ"))
            self.bstack11l11l11lll_opy_(instance.obj, bstack11111l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᯩ"))
        if bstack11l11ll111l_opy_ == bstack11111l_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᯪ"):
            self.bstack11l11l11lll_opy_(instance.obj, bstack11111l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨᯫ"))
            self.bstack11l11l11lll_opy_(instance.obj, bstack11111l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥᯬ"))
        if bstack11l11ll111l_opy_ == bstack11111l_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᯭ"):
            self.bstack11l11l11lll_opy_(instance.obj, bstack11111l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣᯮ"))
            self.bstack11l11l11lll_opy_(instance.obj, bstack11111l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᯯ"))
        if bstack11l11ll111l_opy_ == bstack11111l_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᯰ"):
            self.bstack11l11l11lll_opy_(instance.obj, bstack11111l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᯱ"))
            self.bstack11l11l11lll_opy_(instance.obj, bstack11111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤ᯲"))
    @staticmethod
    def bstack11l11ll1111_opy_(hook_type, func, args):
        if hook_type in [bstack11111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪ᯳ࠧ"), bstack11111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫ᯴")]:
            _11l11l1llll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11ll11l1_opy_(self, hook_type, bstack11l11l1ll1l_opy_):
        def bstack11l11l1ll11_opy_(arg=None):
            self.handler(hook_type, bstack11111l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪ᯵"))
            result = None
            try:
                bstack11111ll111_opy_ = self._11l11l1l111_opy_[(bstack11l11l1ll1l_opy_, hook_type)]
                self.bstack11l11ll1111_opy_(hook_type, bstack11111ll111_opy_, (arg,))
                result = Result(result=bstack11111l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ᯶"))
            except Exception as e:
                result = Result(result=bstack11111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᯷"), exception=e)
                self.handler(hook_type, bstack11111l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬ᯸"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11111l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭᯹"), result)
        def bstack11l11l1l1l1_opy_(this, arg=None):
            self.handler(hook_type, bstack11111l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ᯺"))
            result = None
            exception = None
            try:
                self.bstack11l11ll1111_opy_(hook_type, self._11l11l1l111_opy_[hook_type], (this, arg))
                result = Result(result=bstack11111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᯻"))
            except Exception as e:
                result = Result(result=bstack11111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ᯼"), exception=e)
                self.handler(hook_type, bstack11111l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ᯽"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ᯾"), result)
        if hook_type in [bstack11111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬ᯿"), bstack11111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᰀ")]:
            return bstack11l11l1l1l1_opy_
        return bstack11l11l1ll11_opy_
    def bstack11l11l11l1l_opy_(self, bstack11l11ll111l_opy_):
        def bstack11l11l111ll_opy_(this, *args, **kwargs):
            self.bstack11l11l1lll1_opy_(this, bstack11l11ll111l_opy_)
            self._11l11l1l11l_opy_[bstack11l11ll111l_opy_](this, *args, **kwargs)
        return bstack11l11l111ll_opy_