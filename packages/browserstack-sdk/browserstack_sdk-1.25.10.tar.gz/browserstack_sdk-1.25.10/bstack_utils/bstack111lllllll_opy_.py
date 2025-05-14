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
from uuid import uuid4
from bstack_utils.helper import bstack1l11l1lll_opy_, bstack11l1lllllll_opy_
from bstack_utils.bstack1ll1l1l1_opy_ import bstack111l1l111l1_opy_
class bstack111ll1ll1l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack1111lllll11_opy_=None, bstack111l1111l1l_opy_=True, bstack1l111l1llll_opy_=None, bstack1111111l_opy_=None, result=None, duration=None, bstack111lll111l_opy_=None, meta={}):
        self.bstack111lll111l_opy_ = bstack111lll111l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111l1111l1l_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1111lllll11_opy_ = bstack1111lllll11_opy_
        self.bstack1l111l1llll_opy_ = bstack1l111l1llll_opy_
        self.bstack1111111l_opy_ = bstack1111111l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1ll1ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l111ll11_opy_(self, meta):
        self.meta = meta
    def bstack11l111111l_opy_(self, hooks):
        self.hooks = hooks
    def bstack111l11111ll_opy_(self):
        bstack1111lllllll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack11111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧ᷎ࠪ"): bstack1111lllllll_opy_,
            bstack11111l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰ᷏ࠪ"): bstack1111lllllll_opy_,
            bstack11111l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮᷐ࠧ"): bstack1111lllllll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack11111l_opy_ (u"࡙ࠥࡳ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࡢࡴࡪࡹࡲ࡫࡮ࡵ࠼ࠣࠦ᷑") + key)
            setattr(self, key, val)
    def bstack111l1111l11_opy_(self):
        return {
            bstack11111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᷒"): self.name,
            bstack11111l_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᷓ"): {
                bstack11111l_opy_ (u"࠭࡬ࡢࡰࡪࠫᷔ"): bstack11111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᷕ"),
                bstack11111l_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᷖ"): self.code
            },
            bstack11111l_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᷗ"): self.scope,
            bstack11111l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᷘ"): self.tags,
            bstack11111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᷙ"): self.framework,
            bstack11111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᷚ"): self.started_at
        }
    def bstack111l1111111_opy_(self):
        return {
         bstack11111l_opy_ (u"࠭࡭ࡦࡶࡤࠫᷛ"): self.meta
        }
    def bstack1111llll11l_opy_(self):
        return {
            bstack11111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᷜ"): {
                bstack11111l_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᷝ"): self.bstack1111lllll11_opy_
            }
        }
    def bstack111l1111ll1_opy_(self, bstack1111lllll1l_opy_, details):
        step = next(filter(lambda st: st[bstack11111l_opy_ (u"ࠩ࡬ࡨࠬᷞ")] == bstack1111lllll1l_opy_, self.meta[bstack11111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᷟ")]), None)
        step.update(details)
    def bstack1ll1l1ll11_opy_(self, bstack1111lllll1l_opy_):
        step = next(filter(lambda st: st[bstack11111l_opy_ (u"ࠫ࡮ࡪࠧᷠ")] == bstack1111lllll1l_opy_, self.meta[bstack11111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᷡ")]), None)
        step.update({
            bstack11111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᷢ"): bstack1l11l1lll_opy_()
        })
    def bstack111llll1l1_opy_(self, bstack1111lllll1l_opy_, result, duration=None):
        bstack1l111l1llll_opy_ = bstack1l11l1lll_opy_()
        if bstack1111lllll1l_opy_ is not None and self.meta.get(bstack11111l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᷣ")):
            step = next(filter(lambda st: st[bstack11111l_opy_ (u"ࠨ࡫ࡧࠫᷤ")] == bstack1111lllll1l_opy_, self.meta[bstack11111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᷥ")]), None)
            step.update({
                bstack11111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᷦ"): bstack1l111l1llll_opy_,
                bstack11111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᷧ"): duration if duration else bstack11l1lllllll_opy_(step[bstack11111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᷨ")], bstack1l111l1llll_opy_),
                bstack11111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᷩ"): result.result,
                bstack11111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᷪ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1111llllll1_opy_):
        if self.meta.get(bstack11111l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᷫ")):
            self.meta[bstack11111l_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᷬ")].append(bstack1111llllll1_opy_)
        else:
            self.meta[bstack11111l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᷭ")] = [ bstack1111llllll1_opy_ ]
    def bstack1111llll111_opy_(self):
        return {
            bstack11111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᷮ"): self.bstack111l1ll1ll_opy_(),
            **self.bstack111l1111l11_opy_(),
            **self.bstack111l11111ll_opy_(),
            **self.bstack111l1111111_opy_()
        }
    def bstack1111llll1l1_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack11111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᷯ"): self.bstack1l111l1llll_opy_,
            bstack11111l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᷰ"): self.duration,
            bstack11111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᷱ"): self.result.result
        }
        if data[bstack11111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᷲ")] == bstack11111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᷳ"):
            data[bstack11111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᷴ")] = self.result.bstack1111ll111l_opy_()
            data[bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ᷵")] = [{bstack11111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ᷶"): self.result.bstack11l1l11lll1_opy_()}]
        return data
    def bstack1111lll1lll_opy_(self):
        return {
            bstack11111l_opy_ (u"࠭ࡵࡶ࡫ࡧ᷷ࠫ"): self.bstack111l1ll1ll_opy_(),
            **self.bstack111l1111l11_opy_(),
            **self.bstack111l11111ll_opy_(),
            **self.bstack1111llll1l1_opy_(),
            **self.bstack111l1111111_opy_()
        }
    def bstack111l1l1l1l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack11111l_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡫ࡤࠨ᷸") in event:
            return self.bstack1111llll111_opy_()
        elif bstack11111l_opy_ (u"ࠨࡈ࡬ࡲ࡮ࡹࡨࡦࡦ᷹ࠪ") in event:
            return self.bstack1111lll1lll_opy_()
    def bstack111ll11l1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111l1llll_opy_ = time if time else bstack1l11l1lll_opy_()
        self.duration = duration if duration else bstack11l1lllllll_opy_(self.started_at, self.bstack1l111l1llll_opy_)
        if result:
            self.result = result
class bstack11l111lll1_opy_(bstack111ll1ll1l_opy_):
    def __init__(self, hooks=[], bstack11l11111ll_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l11111ll_opy_ = bstack11l11111ll_opy_
        super().__init__(*args, **kwargs, bstack1111111l_opy_=bstack11111l_opy_ (u"ࠩࡷࡩࡸࡺ᷺ࠧ"))
    @classmethod
    def bstack111l111111l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack11111l_opy_ (u"ࠪ࡭ࡩ࠭᷻"): id(step),
                bstack11111l_opy_ (u"ࠫࡹ࡫ࡸࡵࠩ᷼"): step.name,
                bstack11111l_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ᷽࠭"): step.keyword,
            })
        return bstack11l111lll1_opy_(
            **kwargs,
            meta={
                bstack11111l_opy_ (u"࠭ࡦࡦࡣࡷࡹࡷ࡫ࠧ᷾"): {
                    bstack11111l_opy_ (u"ࠧ࡯ࡣࡰࡩ᷿ࠬ"): feature.name,
                    bstack11111l_opy_ (u"ࠨࡲࡤࡸ࡭࠭Ḁ"): feature.filename,
                    bstack11111l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧḁ"): feature.description
                },
                bstack11111l_opy_ (u"ࠪࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬḂ"): {
                    bstack11111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩḃ"): scenario.name
                },
                bstack11111l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫḄ"): steps,
                bstack11111l_opy_ (u"࠭ࡥࡹࡣࡰࡴࡱ࡫ࡳࠨḅ"): bstack111l1l111l1_opy_(test)
            }
        )
    def bstack1111llll1ll_opy_(self):
        return {
            bstack11111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭Ḇ"): self.hooks
        }
    def bstack111l11111l1_opy_(self):
        if self.bstack11l11111ll_opy_:
            return {
                bstack11111l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧḇ"): self.bstack11l11111ll_opy_
            }
        return {}
    def bstack1111lll1lll_opy_(self):
        return {
            **super().bstack1111lll1lll_opy_(),
            **self.bstack1111llll1ll_opy_()
        }
    def bstack1111llll111_opy_(self):
        return {
            **super().bstack1111llll111_opy_(),
            **self.bstack111l11111l1_opy_()
        }
    def bstack111ll11l1l_opy_(self):
        return bstack11111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫḈ")
class bstack11l1111lll_opy_(bstack111ll1ll1l_opy_):
    def __init__(self, hook_type, *args,bstack11l11111ll_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111lll1ll1_opy_ = None
        self.bstack11l11111ll_opy_ = bstack11l11111ll_opy_
        super().__init__(*args, **kwargs, bstack1111111l_opy_=bstack11111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨḉ"))
    def bstack111ll1l1ll_opy_(self):
        return self.hook_type
    def bstack1111lll1l1l_opy_(self):
        return {
            bstack11111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧḊ"): self.hook_type
        }
    def bstack1111lll1lll_opy_(self):
        return {
            **super().bstack1111lll1lll_opy_(),
            **self.bstack1111lll1l1l_opy_()
        }
    def bstack1111llll111_opy_(self):
        return {
            **super().bstack1111llll111_opy_(),
            bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪḋ"): self.bstack1111lll1ll1_opy_,
            **self.bstack1111lll1l1l_opy_()
        }
    def bstack111ll11l1l_opy_(self):
        return bstack11111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨḌ")
    def bstack11l111l11l_opy_(self, bstack1111lll1ll1_opy_):
        self.bstack1111lll1ll1_opy_ = bstack1111lll1ll1_opy_