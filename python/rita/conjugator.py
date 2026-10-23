"""
rita/conjugator.py — Conjugator for RiTa
Python port of ritajs/src/conjugator.js
"""
import re
import json
import os

# ── RiTa constants ──────────────────────────────────────────────────────────
FIRST = 1; SECOND = 2; THIRD = 3
PAST = 4; PRESENT = 5; FUTURE = 6
SINGULAR = 7; PLURAL = 8; NORMAL = 9
INFINITIVE = 1; GERUND = 2

# ── Internal helpers ────────────────────────────────────────────────────────
_CONS = "[bcdfghjklmnpqrstvwxyz]"
_MODALS = ["shall", "would", "may", "might", "ought", "should"]
_VP = r"((be|with|pre|un|over|re|mis|under|out|up|fore|for|counter|co|sub)(-?))"
_ANY = r"^((\w+)(-\w+)*)(\s((\w+)(-\w+)*))*$"
_TO_BE = ["am", "are", "is", "was", "were"]

_dict_cache = None
_all_verbs_cache = None
_verbs_in_e_cache = None
_verbs_dbl_cache = None


def _get_dict():
    global _dict_cache
    if _dict_cache is None:
        p = os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'rita_dict.json')
        with open(p) as f:
            _dict_cache = json.load(f)
    return _dict_cache


def _pos_arr(word):
    e = _get_dict().get(word)
    if e is None:
        return None
    return e[1].split() if len(e) > 1 else None


def _has_tag(word, tag):
    p = _pos_arr(word)
    return p is not None and tag in p


def _all_verbs():
    global _all_verbs_cache
    if _all_verbs_cache is None:
        d = _get_dict()
        _all_verbs_cache = [w for w, e in d.items()
                            if len(e) > 1 and 'vb' in e[1].split()]
    return _all_verbs_cache


def _verbs_ending_in_e():
    global _verbs_in_e_cache
    if _verbs_in_e_cache is None:
        _verbs_in_e_cache = [v for v in _all_verbs() if v.endswith('e')]
    return _verbs_in_e_cache


def _verbs_ending_in_double():
    global _verbs_dbl_cache
    if _verbs_dbl_cache is None:
        _verbs_dbl_cache = [v for v in _all_verbs() if re.search(r'(.)\1$', v)]
    return _verbs_dbl_cache


# ── Rule class ───────────────────────────────────────────────────────────────
class _Rule:
    __slots__ = ("regex", "offset", "suffix")

    def __init__(self, pattern, offset=0, suffix=""):
        self.regex = re.compile(pattern)
        self.offset = offset if offset is not None else 0
        self.suffix = suffix if suffix is not None else ""

    def applies(self, word):
        return bool(self.regex.search(word))

    def fire(self, word):
        if self.offset == 0 and self.suffix == "":
            return word  # null / identity form
        trimmed = word if self.offset == 0 else word[:-self.offset]
        return trimmed + self.suffix


def _RE(p, o=None, s=None, _=None):
    return _Rule(p, o if o is not None else 0, s if s is not None else "")


# ── Rule data ────────────────────────────────────────────────────────────────
_ING_FORM_RULES = [
    _RE(_CONS + r"ie$", 2, "ying"),
    _RE(r"^be$", 0, "ing"),
    _RE(r"[^oie]e$", 1, "ing"),
    _RE(r"^trek$", 1, "cking"),
    _RE(r"^bring$", 0, "ing"),
    _RE(r"^age$", 1, "ing"),
    _RE(r"(ibe)$", 1, "ing"),
]

_PAST_PART_RULES = [
    _RE(_CONS + r"y$", 1, "ied"),
    _RE(r"^" + _VP + r"?(bring)$", 3, "ought"),
    _RE(r"^" + _VP + r"?(take|rise|strew|blow|draw|drive|know|give|"
        r"arise|gnaw|grave|grow|hew|know|mow|see|sew|throw|prove|saw|quartersaw|"
        r"partake|sake|shake|shew|show|shrive|sightsee|strew|strive)$", 0, "n"),
    _RE(r"^" + _VP + r"?[gd]o$", 0, "ne"),
    _RE(r"^(beat|eat|be|fall)$", 0, "en"),
    _RE(r"^(have)$", 2, "d"),
    _RE(r"^" + _VP + r"?bid$", 0, "den"),
    _RE(r"^" + _VP + r"?[lps]ay$", 1, "id"),
    _RE(r"^behave$", 0, "d"),
    _RE(r"^" + _VP + r"?have$", 2, "d"),
    _RE(r"(sink|slink|drink|shrink|stink)$", 3, "unk"),
    _RE(r"(([sfc][twlp]?r?|w?r)ing|hang)$", 3, "ung"),
    _RE(r"^" + _VP + r"?(shear|swear|wear|tear)$", 3, "orn"),
    _RE(r"^" + _VP + r"?(bend|spend|send|lend)$", 1, "t"),
    _RE(r"^" + _VP + r"?(weep|sleep|sweep|creep|keep$)$", 2, "pt"),
    _RE(r"^" + _VP + r"?(sell|tell)$", 3, "old"),
    _RE(r"^(outfight|beseech)$", 4, "ought"),
    _RE(r"^bear$", 3, "orne"),
    _RE(r"^bethink$", 3, "ought"),
    _RE(r"^buy$", 2, "ought"),
    _RE(r"^aby$", 1, "ought"),
    _RE(r"^tarmac", 0, "ked"),
    _RE(r"^abide$", 3, "ode"),
    _RE(r"^" + _VP + r"?(speak|(a?)wake|break)$", 3, "oken"),
    _RE(r"^backbite$", 1, "ten"),
    _RE(r"^backslide$", 1, "den"),
    _RE(r"^become$", 3, "ame"),
    _RE(r"^begird$", 3, "irt"),
    _RE(r"^outlie$", 2, "ay"),
    _RE(r"^rebind$", 3, "ound"),
    _RE(r"^relay$", 2, "aid"),
    _RE(r"^shit$", 3, "hat"),
    _RE(r"^bereave$", 4, "eft"),
    _RE(r"^foreswear$", 3, "ore"),
    _RE(r"^overfly$", 1, "own"),
    _RE(r"^beget$", 2, "otten"),
    _RE(r"^begin$", 3, "gun"),
    _RE(r"^bestride$", 1, "den"),
    _RE(r"^bite$", 1, "ten"),
    _RE(r"^bleed$", 4, "led"),
    _RE(r"^bog-down$", 5, "ged-down"),
    _RE(r"^bind$", 3, "ound"),
    _RE(r"^(.*)feed$", 4, "fed"),
    _RE(r"^breed$", 4, "red"),
    _RE(r"^brei", 0, "d"),
    _RE(r"^bring$", 3, "ought"),
    _RE(r"^build$", 1, "t"),
    _RE(r"^come", 0, ""),
    _RE(r"^catch$", 3, "ught"),
    _RE(r"^chivy$", 1, "vied"),
    _RE(r"^choose$", 3, "sen"),
    _RE(r"^cleave$", 4, "oven"),
    _RE(r"^crossbreed$", 4, "red"),
    _RE(r"^deal", 0, "t"),
    _RE(r"^dow$", 1, "ught"),
    _RE(r"^dream", 0, "t"),
    _RE(r"^dig$", 3, "dug"),
    _RE(r"^dwell$", 2, "lt"),
    _RE(r"^enwind$", 3, "ound"),
    _RE(r"^feel$", 3, "elt"),
    _RE(r"^flee$", 2, "ed"),
    _RE(r"^floodlight$", 5, "lit"),
    _RE(r"^fly$", 1, "own"),
    _RE(r"^forbear$", 3, "orne"),
    _RE(r"^forerun$", 3, "ran"),
    _RE(r"^forget$", 2, "otten"),
    _RE(r"^fight$", 4, "ought"),
    _RE(r"^find$", 3, "ound"),
    _RE(r"^freeze$", 4, "ozen"),
    _RE(r"^gainsay$", 2, "aid"),
    _RE(r"^gin$", 3, "gan"),
    _RE(r"^gen-up$", 3, "ned-up"),
    _RE(r"^ghostwrite$", 1, "ten"),
    _RE(r"^get$", 2, "otten"),
    _RE(r"^grind$", 3, "ound"),
    _RE(r"^hacksaw", 0, "n"),
    _RE(r"^hear$", 0, "d"),
    _RE(r"^hold$", 3, "eld"),
    _RE(r"^hide$", 1, "den"),
    _RE(r"^honey$", 2, "ied"),
    _RE(r"^inbreed$", 4, "red"),
    _RE(r"^indwell$", 3, "elt"),
    _RE(r"^interbreed$", 4, "red"),
    _RE(r"^interweave$", 4, "oven"),
    _RE(r"^inweave$", 4, "oven"),
    _RE(r"^ken$", 2, "ent"),
    _RE(r"^kneel$", 3, "elt"),
    _RE(r"^lie$", 2, "ain"),
    _RE(r"^leap$", 0, "t"),
    _RE(r"^learn$", 0, "t"),
    _RE(r"^lead$", 4, "led"),
    _RE(r"^leave$", 4, "eft"),
    _RE(r"^light$", 5, "lit"),
    _RE(r"^lose$", 3, "ost"),
    _RE(r"^make$", 3, "ade"),
    _RE(r"^mean", 0, "t"),
    _RE(r"^meet$", 4, "met"),
    _RE(r"^misbecome$", 3, "ame"),
    _RE(r"^misdeal$", 2, "alt"),
    _RE(r"^mishear$", 1, "d"),
    _RE(r"^mislead$", 4, "led"),
    _RE(r"^misunderstand$", 3, "ood"),
    _RE(r"^outbreed$", 4, "red"),
    _RE(r"^outrun$", 3, "ran"),
    _RE(r"^outride$", 1, "den"),
    _RE(r"^outshine$", 3, "one"),
    _RE(r"^outshoot$", 4, "hot"),
    _RE(r"^outstand$", 3, "ood"),
    _RE(r"^outthink$", 3, "ought"),
    _RE(r"^outgo$", 2, "went"),
    _RE(r"^overbear$", 3, "orne"),
    _RE(r"^overbuild$", 3, "ilt"),
    _RE(r"^overcome$", 3, "ame"),
    _RE(r"^overfly$", 2, "lew"),
    _RE(r"^overhear$", 2, "ard"),
    _RE(r"^overlie$", 2, "ain"),
    _RE(r"^overrun$", 3, "ran"),
    _RE(r"^override$", 1, "den"),
    _RE(r"^overshoot$", 4, "hot"),
    _RE(r"^overwind$", 3, "ound"),
    _RE(r"^overwrite$", 1, "ten"),
    _RE(r"^plead$", 2, "d"),
    _RE(r"^rebuild$", 3, "ilt"),
    _RE(r"^red$", 3, "red"),
    _RE(r"^redo$", 1, "one"),
    _RE(r"^remake$", 3, "ade"),
    _RE(r"^resit$", 3, "sat"),
    _RE(r"^rethink$", 3, "ought"),
    _RE(r"^rewind$", 3, "ound"),
    _RE(r"^rewrite$", 1, "ten"),
    _RE(r"^ride$", 1, "den"),
    _RE(r"^reeve$", 4, "ove"),
    _RE(r"^sit$", 3, "sat"),
    _RE(r"^shoe$", 3, "hod"),
    _RE(r"^shine$", 3, "one"),
    _RE(r"^shoot$", 4, "hot"),
    _RE(r"^ski$", 1, "i'd"),
    _RE(r"^slide$", 1, "den"),
    _RE(r"^smite$", 1, "ten"),
    _RE(r"^seek$", 3, "ought"),
    _RE(r"^spit$", 3, "pat"),
    _RE(r"^speed$", 4, "ped"),
    _RE(r"^spellbind$", 3, "ound"),
    _RE(r"^spoil$", 2, "ilt"),
    _RE(r"^spotlight$", 5, "lit"),
    _RE(r"^spin$", 3, "pun"),
    _RE(r"^steal$", 3, "olen"),
    _RE(r"^stand$", 3, "ood"),
    _RE(r"^stave$", 3, "ove"),
    _RE(r"^stride$", 1, "den"),
    _RE(r"^strike$", 3, "uck"),
    _RE(r"^stick$", 3, "uck"),
    _RE(r"^swell$", 3, "ollen"),
    _RE(r"^swim$", 3, "wum"),
    _RE(r"^teach$", 4, "aught"),
    _RE(r"^think$", 3, "ought"),
    _RE(r"^tread$", 3, "odden"),
    _RE(r"^typewrite$", 1, "ten"),
    _RE(r"^unbind$", 3, "ound"),
    _RE(r"^underbuy$", 2, "ought"),
    _RE(r"^undergird$", 3, "irt"),
    _RE(r"^undergo$", 1, "one"),
    _RE(r"^underlie$", 2, "ain"),
    _RE(r"^undershoot$", 4, "hot"),
    _RE(r"^understand$", 3, "ood"),
    _RE(r"^unfreeze$", 4, "ozen"),
    _RE(r"^unlearn", 0, "t"),
    _RE(r"^unmake$", 3, "ade"),
    _RE(r"^unreeve$", 4, "ove"),
    _RE(r"^unstick$", 3, "uck"),
    _RE(r"^unteach$", 4, "aught"),
    _RE(r"^unthink$", 3, "ought"),
    _RE(r"^untread$", 3, "odden"),
    _RE(r"^unwind$", 3, "ound"),
    _RE(r"^upbuild$", 1, "t"),
    _RE(r"^uphold$", 3, "eld"),
    _RE(r"^upheave$", 4, "ove"),
    _RE(r"^waylay$", 2, "ain"),
    _RE(r"^whipsaw$", 2, "awn"),
    _RE(r"^withhold$", 3, "eld"),
    _RE(r"^withstand$", 3, "ood"),
    _RE(r"^win$", 3, "won"),
    _RE(r"^wind$", 3, "ound"),
    _RE(r"^weave$", 4, "oven"),
    _RE(r"^write$", 1, "ten"),
    _RE(r"^trek$", 1, "cked"),
    _RE(r"^ko$", 1, "o'd"),
    _RE(r"^win$", 2, "on"),
    _RE(r"e$", 0, "d"),
    # null past forms
    _RE(r"^" + _VP + r"?(cast|thrust|typeset|cut|bid|upset|wet|bet|cut|hit|"
        r"hurt|inset|let|cost|burst|beat|beset|set|upset|hit|offset|put|quit|"
        r"wed|typeset|wed|spread|split|slit|read|run|rerun|shut|shed)$", 0),
]

_PAST_RULES = [
    _RE(r"^(reduce)$", 0, "d"),
    _RE(r"^" + _VP + r"?[pls]ay$", 1, "id"),
    _RE(_CONS + r"y$", 1, "ied"),
    _RE(r"^(fling|cling|hang)$", 3, "ung"),
    _RE(r"(([sfc][twlp]?r?|w?r)ing)$", 3, "ang"),
    _RE(r"^" + _VP + r"?(bend|spend|send|lend|spend)$", 1, "t"),
    _RE(r"^" + _VP + r"?lie$", 2, "ay"),
    _RE(r"^" + _VP + r"?(weep|sleep|sweep|creep|keep)$", 2, "pt"),
    _RE(r"^" + _VP + r"?(sell|tell)$", 3, "old"),
    _RE(r"^" + _VP + r"?do$", 1, "id"),
    _RE(r"^" + _VP + r"?dig$", 2, "ug"),
    _RE(r"^behave$", 0, "d"),
    _RE(r"^(have)$", 2, "d"),
    _RE(r"(sink|drink)$", 3, "ank"),
    _RE(r"^swing$", 3, "ung"),
    _RE(r"^be$", 2, "was"),
    _RE(r"^outfight$", 4, "ought"),
    _RE(r"^tarmac", 0, "ked"),
    _RE(r"^abide$", 3, "ode"),
    _RE(r"^aby$", 1, "ought"),
    _RE(r"^become$", 3, "ame"),
    _RE(r"^begird$", 3, "irt"),
    _RE(r"^outlie$", 2, "ay"),
    _RE(r"^rebind$", 3, "ound"),
    _RE(r"^shit$", 3, "hat"),
    _RE(r"^bereave$", 4, "eft"),
    _RE(r"^foreswear$", 3, "ore"),
    _RE(r"^bename$", 3, "empt"),
    _RE(r"^beseech$", 4, "ought"),
    _RE(r"^bethink$", 3, "ought"),
    _RE(r"^bleed$", 4, "led"),
    _RE(r"^bog-down$", 5, "ged-down"),
    _RE(r"^buy$", 2, "ought"),
    _RE(r"^bind$", 3, "ound"),
    _RE(r"^(.*)feed$", 4, "fed"),
    _RE(r"^breed$", 4, "red"),
    _RE(r"^brei$", 2, "eid"),
    _RE(r"^bring$", 3, "ought"),
    _RE(r"^build$", 3, "ilt"),
    _RE(r"^come$", 3, "ame"),
    _RE(r"^catch$", 3, "ught"),
    _RE(r"^clothe$", 5, "lad"),
    _RE(r"^crossbreed$", 4, "red"),
    _RE(r"^deal$", 2, "alt"),
    _RE(r"^dow$", 1, "ught"),
    _RE(r"^dream$", 2, "amt"),
    _RE(r"^dwell$", 3, "elt"),
    _RE(r"^enwind$", 3, "ound"),
    _RE(r"^feel$", 3, "elt"),
    _RE(r"^flee$", 3, "led"),
    _RE(r"^floodlight$", 5, "lit"),
    _RE(r"^arise$", 3, "ose"),
    _RE(r"^eat$", 3, "ate"),
    _RE(r"^backbite$", 4, "bit"),
    _RE(r"^backslide$", 4, "lid"),
    _RE(r"^befall$", 3, "ell"),
    _RE(r"^begin$", 3, "gan"),
    _RE(r"^beget$", 3, "got"),
    _RE(r"^behold$", 3, "eld"),
    _RE(r"^bespeak$", 3, "oke"),
    _RE(r"^bestride$", 3, "ode"),
    _RE(r"^betake$", 3, "ook"),
    _RE(r"^bite$", 4, "bit"),
    _RE(r"^blow$", 3, "lew"),
    _RE(r"^bear$", 3, "ore"),
    _RE(r"^break$", 3, "oke"),
    _RE(r"^choose$", 4, "ose"),
    _RE(r"^cleave$", 4, "ove"),
    _RE(r"^countersink$", 3, "ank"),
    _RE(r"^drink$", 3, "ank"),
    _RE(r"^draw$", 3, "rew"),
    _RE(r"^drive$", 3, "ove"),
    _RE(r"^fall$", 3, "ell"),
    _RE(r"^fly$", 2, "lew"),
    _RE(r"^flyblow$", 3, "lew"),
    _RE(r"^forbid$", 2, "ade"),
    _RE(r"^forbear$", 3, "ore"),
    _RE(r"^foreknow$", 3, "new"),
    _RE(r"^foresee$", 3, "saw"),
    _RE(r"^forespeak$", 3, "oke"),
    _RE(r"^forego$", 2, "went"),
    _RE(r"^forgive$", 3, "ave"),
    _RE(r"^forget$", 3, "got"),
    _RE(r"^forsake$", 3, "ook"),
    _RE(r"^forspeak$", 3, "oke"),
    _RE(r"^forswear$", 3, "ore"),
    _RE(r"^forgo$", 2, "went"),
    _RE(r"^fight$", 4, "ought"),
    _RE(r"^find$", 3, "ound"),
    _RE(r"^freeze$", 4, "oze"),
    _RE(r"^give$", 3, "ave"),
    _RE(r"^geld$", 3, "elt"),
    _RE(r"^gen-up$", 3, "ned-up"),
    _RE(r"^ghostwrite$", 3, "ote"),
    _RE(r"^get$", 3, "got"),
    _RE(r"^grow$", 3, "rew"),
    _RE(r"^grind$", 3, "ound"),
    _RE(r"^hear$", 2, "ard"),
    _RE(r"^hold$", 3, "eld"),
    _RE(r"^hide$", 4, "hid"),
    _RE(r"^honey$", 2, "ied"),
    _RE(r"^inbreed$", 4, "red"),
    _RE(r"^indwell$", 3, "elt"),
    _RE(r"^interbreed$", 4, "red"),
    _RE(r"^interweave$", 4, "ove"),
    _RE(r"^inweave$", 4, "ove"),
    _RE(r"^ken$", 2, "ent"),
    _RE(r"^kneel$", 3, "elt"),
    _RE(r"^^know$$", 3, "new"),
    _RE(r"^leap$", 2, "apt"),
    _RE(r"^learn$", 2, "rnt"),
    _RE(r"^lead$", 4, "led"),
    _RE(r"^leave$", 4, "eft"),
    _RE(r"^light$", 5, "lit"),
    _RE(r"^lose$", 3, "ost"),
    _RE(r"^make$", 3, "ade"),
    _RE(r"^mean$", 2, "ant"),
    _RE(r"^meet$", 4, "met"),
    _RE(r"^misbecome$", 3, "ame"),
    _RE(r"^misdeal$", 2, "alt"),
    _RE(r"^misgive$", 3, "ave"),
    _RE(r"^mishear$", 2, "ard"),
    _RE(r"^mislead$", 4, "led"),
    _RE(r"^mistake$", 3, "ook"),
    _RE(r"^misunderstand$", 3, "ood"),
    _RE(r"^outbreed$", 4, "red"),
    _RE(r"^outgrow$", 3, "rew"),
    _RE(r"^outride$", 3, "ode"),
    _RE(r"^outshine$", 3, "one"),
    _RE(r"^outshoot$", 4, "hot"),
    _RE(r"^outstand$", 3, "ood"),
    _RE(r"^outthink$", 3, "ought"),
    _RE(r"^outgo$", 2, "went"),
    _RE(r"^outwear$", 3, "ore"),
    _RE(r"^overblow$", 3, "lew"),
    _RE(r"^overbear$", 3, "ore"),
    _RE(r"^overbuild$", 3, "ilt"),
    _RE(r"^overcome$", 3, "ame"),
    _RE(r"^overdraw$", 3, "rew"),
    _RE(r"^overdrive$", 3, "ove"),
    _RE(r"^overfly$", 2, "lew"),
    _RE(r"^overgrow$", 3, "rew"),
    _RE(r"^overhear$", 2, "ard"),
    _RE(r"^overpass$", 3, "ast"),
    _RE(r"^override$", 3, "ode"),
    _RE(r"^oversee$", 3, "saw"),
    _RE(r"^overshoot$", 4, "hot"),
    _RE(r"^overthrow$", 3, "rew"),
    _RE(r"^overtake$", 3, "ook"),
    _RE(r"^overwind$", 3, "ound"),
    _RE(r"^overwrite$", 3, "ote"),
    _RE(r"^partake$", 3, "ook"),
    _RE(r"^" + _VP + r"?run$", 2, "an"),
    _RE(r"^ring$", 3, "ang"),
    _RE(r"^rebuild$", 3, "ilt"),
    _RE(r"^red$"),
    _RE(r"^reave$", 4, "eft"),
    _RE(r"^remake$", 3, "ade"),
    _RE(r"^resit$", 3, "sat"),
    _RE(r"^rethink$", 3, "ought"),
    _RE(r"^retake$", 3, "ook"),
    _RE(r"^rewind$", 3, "ound"),
    _RE(r"^rewrite$", 3, "ote"),
    _RE(r"^ride$", 3, "ode"),
    _RE(r"^rise$", 3, "ose"),
    _RE(r"^reeve$", 4, "ove"),
    _RE(r"^sing$", 3, "ang"),
    _RE(r"^sink$", 3, "ank"),
    _RE(r"^sit$", 3, "sat"),
    _RE(r"^see$", 3, "saw"),
    _RE(r"^shoe$", 3, "hod"),
    _RE(r"^shine$", 3, "one"),
    _RE(r"^shake$", 3, "ook"),
    _RE(r"^shoot$", 4, "hot"),
    _RE(r"^shrink$", 3, "ank"),
    _RE(r"^shrive$", 3, "ove"),
    _RE(r"^sightsee$", 3, "saw"),
    _RE(r"^ski$", 1, "i'd"),
    _RE(r"^skydive$", 3, "ove"),
    _RE(r"^slay$", 3, "lew"),
    _RE(r"^slide$", 4, "lid"),
    _RE(r"^slink$", 3, "unk"),
    _RE(r"^smite$", 4, "mit"),
    _RE(r"^seek$", 3, "ought"),
    _RE(r"^spit$", 3, "pat"),
    _RE(r"^speed$", 4, "ped"),
    _RE(r"^spellbind$", 3, "ound"),
    _RE(r"^spoil$", 2, "ilt"),
    _RE(r"^speak$", 3, "oke"),
    _RE(r"^spotlight$", 5, "lit"),
    _RE(r"^spring$", 3, "ang"),
    _RE(r"^spin$", 3, "pun"),
    _RE(r"^stink$", 3, "ank"),
    _RE(r"^steal$", 3, "ole"),
    _RE(r"^stand$", 3, "ood"),
    _RE(r"^stave$", 3, "ove"),
    _RE(r"^stride$", 3, "ode"),
    _RE(r"^strive$", 3, "ove"),
    _RE(r"^strike$", 3, "uck"),
    _RE(r"^stick$", 3, "uck"),
    _RE(r"^swim$", 3, "wam"),
    _RE(r"^swear$", 3, "ore"),
    _RE(r"^teach$", 4, "aught"),
    _RE(r"^think$", 3, "ought"),
    _RE(r"^throw$", 3, "rew"),
    _RE(r"^take$", 3, "ook"),
    _RE(r"^tear$", 3, "ore"),
    _RE(r"^transship$", 4, "hip"),
    _RE(r"^tread$", 4, "rod"),
    _RE(r"^typewrite$", 3, "ote"),
    _RE(r"^unbind$", 3, "ound"),
    _RE(r"^unclothe$", 5, "lad"),
    _RE(r"^underbuy$", 2, "ought"),
    _RE(r"^undergird$", 3, "irt"),
    _RE(r"^undershoot$", 4, "hot"),
    _RE(r"^understand$", 3, "ood"),
    _RE(r"^undertake$", 3, "ook"),
    _RE(r"^undergo$", 2, "went"),
    _RE(r"^underwrite$", 3, "ote"),
    _RE(r"^unfreeze$", 4, "oze"),
    _RE(r"^unlearn$", 2, "rnt"),
    _RE(r"^unmake$", 3, "ade"),
    _RE(r"^unreeve$", 4, "ove"),
    _RE(r"^unspeak$", 3, "oke"),
    _RE(r"^unstick$", 3, "uck"),
    _RE(r"^unswear$", 3, "ore"),
    _RE(r"^unteach$", 4, "aught"),
    _RE(r"^unthink$", 3, "ought"),
    _RE(r"^untread$", 4, "rod"),
    _RE(r"^unwind$", 3, "ound"),
    _RE(r"^upbuild$", 3, "ilt"),
    _RE(r"^uphold$", 3, "eld"),
    _RE(r"^upheave$", 4, "ove"),
    _RE(r"^uprise$", 3, "ose"),
    _RE(r"^upspring$", 3, "ang"),
    _RE(r"^go$", 2, "went"),
    _RE(r"^wiredraw$", 3, "rew"),
    _RE(r"^withdraw$", 3, "rew"),
    _RE(r"^withhold$", 3, "eld"),
    _RE(r"^withstand$", 3, "ood"),
    _RE(r"^wake$", 3, "oke"),
    _RE(r"^win$", 3, "won"),
    _RE(r"^wear$", 3, "ore"),
    _RE(r"^wind$", 3, "ound"),
    _RE(r"^weave$", 4, "ove"),
    _RE(r"^write$", 3, "ote"),
    _RE(r"^trek$", 1, "cked"),
    _RE(r"^ko$", 1, "o'd"),
    _RE(r"^bid", 2, "ade"),
    _RE(r"^win$", 2, "on"),
    _RE(r"^swim", 2, "am"),
    _RE(r"e$", 0, "d"),
    # null past forms
    _RE(r"^" + _VP + r"?(cast|thrust|typeset|cut|bid|upset|wet|bet|cut|hit|"
        r"hurt|inset|let|cost|burst|beat|beset|set|upset|offset|put|quit|wed|"
        r"typeset|wed|spread|split|slit|read|run|shut|shed|lay)$", 0),
]

_PRESENT_RULES = [
    _RE(r"^aby$", 0, "es"),
    _RE(r"^bog-down$", 5, "s-down"),
    _RE(r"^chivy$", 1, "vies"),
    _RE(r"^gen-up$", 3, "s-up"),
    _RE(r"^prologue$", 3, "gs"),
    _RE(r"^picknic$", 0, "ks"),
    _RE(r"^ko$", 0, "'s"),
    _RE(r"[osz]$", 0, "es"),
    _RE(r"^have$", 2, "s"),
    _RE(_CONS + r"y$", 1, "ies"),
    _RE(r"^be$", 2, "is"),
    _RE(r"([zsx]|ch|sh)$", 0, "es"),
]

_VERB_CONS_DOUBLING = frozenset([
    "abat", "abet", "abhor", "abut", "accur", "acquit", "adlib",
    "admit", "aerobat", "aerosol", "allot", "alot", "anagram",
    "annul", "appal", "apparel", "armbar", "aver", "babysit", "airdrop", "appal",
    "blackleg", "bobsled", "bur", "chum", "confab", "counterplot", "dib",
    "backdrop", "backfil", "backflip", "backlog", "backpedal", "backslap",
    "backstab", "bag", "balfun", "ballot", "ban", "bar", "barbel", "bareleg",
    "barrel", "bat", "bayonet", "becom", "bed", "bedevil", "bedwet",
    "befit", "befog", "beg", "beget", "begin", "bejewel", "benefit",
    "beset", "besot", "bet", "bevel", "bewig",
    "bib", "bid", "billet", "bin", "bip", "bit", "bitmap", "blab", "blag", "blam",
    "blan", "blat", "bles", "blim", "blip", "blob", "bloodlet", "blot", "blub",
    "blur", "bob", "bog", "booby-trap", "boobytrap", "booksel",
    "bootleg", "bop", "bot", "bowel", "bracket", "brag", "brig", "brim", "bud",
    "buffet", "bug", "bullshit", "bum", "bun", "bus", "but", "cab", "cabal", "cam",
    "can", "cancel", "cap", "caravan", "carburet", "carnap", "carol",
    "carpetbag", "castanet", "cat", "catcal", "catnap", "chanel",
    "channel", "chap", "char", "chat", "chin", "chip", "chir",
    "chirrup", "chisel", "chop", "chug", "chur", "clam", "clap", "clearcut",
    "clip", "clodhop", "clog", "clop", "clot", "club", "co-star", "cob", "cobweb",
    "cod", "coif",
    "com", "combat", "comit", "commit", "compel", "con", "concur", "confer",
    "confiscat", "control", "cop", "coquet", "coral", "corral", "cosset",
    "cotransmit", "councel", "council", "counsel", "court-martial", "crab", "cram",
    "crap", "crib", "crop", "crossleg", "cub", "cudgel", "cum", "cun", "cup",
    "cut", "dab", "dag", "dam", "dan", "dap", "daysit", "deadpan",
    "debag", "debar", "log", "decommit", "decontrol", "defer", "defog", "deg",
    "degas", "deinstal", "demur", "den", "denet", "depig",
    "depip", "depit", "der", "deskil", "deter", "devil", "diagram", "dial", "dig",
    "dim", "din", "dip", "disbar", "disbud", "discomfit", "disembed", "disembowel",
    "dishevel", "disinter", "dispel", "distil", "dog", "dognap",
    "don", "doorstep", "dot", "dowel", "drag", "drat", "driftnet", "distil",
    "egotrip", "enrol", "enthral", "extol", "fulfil", "gaffe", "idyl",
    "inspan", "drip", "drivel", "drop", "drub", "drug", "drum", "dub", "duel",
    "dun", "earwig", "eavesdrop", "ecolabel",
    "embed", "emit", "enamel", "endlabel", "endtrim",
    "enrol", "enthral", "entrap", "enwrap", "equal", "equip",
    "exaggerat", "excel", "expel", "extol", "fag", "fan", "farewel", "fat",
    "featherbed", "feget", "fet", "fib", "fig", "fin", "fingerspel", "fingertip",
    "fit", "flab", "flag", "flap", "flip", "flit", "flog", "flop", "fob", "focus",
    "fog", "footbal", "footslog", "fop", "forbid", "forget", "format",
    "fortunetel", "fot", "foxtrot", "frag", "freefal", "fret", "frig", "frip",
    "frog", "frug", "fuel", "fufil", "fulfil", "fullyfit", "fun", "funnel", "fur",
    "furpul", "gab", "gad", "gag", "gam", "gambol", "gap", "garot", "garrot",
    "gas", "gat", "gel", "gen", "get", "giftwrap", "gig", "gimbal", "gin", "glam",
    "glenden", "glendin", "globetrot", "glug", "glut", "gob", "goldpan", "goostep",
    "gossip", "grab", "gravel", "grid", "grin", "grip", "grit",
    "grovel", "grub", "gum", "gun", "gunrun", "gut", "gyp", "haircut", "ham",
    "han", "handbag", "handicap", "handknit", "handset", "hap", "hareleg", "hat",
    "headbut", "hedgehop", "hem", "hen", "hiccup", "highwal", "hip", "hit",
    "hobnob", "hog", "hop", "horsewhip", "hostel", "hot", "hotdog", "hovel", "hug",
    "hum", "humbug", "hup", "hut", "illfit", "imbed",
    "impel", "imperil", "incur", "infer", "infil",
    "inflam", "initial", "input", "inset", "instil", "inter", "interbed",
    "intercrop", "intercut", "interfer", "instal", "instil", "intermit",
    "jug", "mousse", "mud", "jab", "jag",
    "jam", "jar", "jawdrop", "jet", "jetlag", "jewel", "jib", "jig", "jitterbug",
    "job", "jog", "jot", "jut", "ken", "kennel", "kid", "kidnap",
    "kip", "kit", "knap", "kneecap", "knit", "knob", "knot",
    "label", "lag", "lam", "lap", "lavel", "leafcut", "leapfrog", "leg", "lem",
    "lep", "let", "level", "libel", "lid", "lig", "lip", "lob", "log", "lok",
    "lollop", "longleg", "lop", "lowbal", "lug", "mackerel", "mahom", "man", "map",
    "mar", "marshal", "marvel", "mat", "matchwin", "metal", "micro-program",
    "microplan", "microprogram", "milksop", "mis-cal", "mis-club", "mis-spel",
    "miscal", "mishit", "mislabel", "mit", "mob", "mod", "model", "mohmam",
    "monogram", "mop", "mothbal", "mug", "multilevel", "mum", "nab", "nag", "nan",
    "nap", "net", "nightclub", "nightsit", "nip", "nod", "nonplus", "norkop",
    "nostril", "not", "nut", "nutmeg", "occur", "ocur", "offput", "offset", "omit",
    "ommit", "onlap", "out-general", "outbid", "outcrop", "outfit",
    "outgas", "outgun", "outhit", "outjab", "outpol", "output", "outrun",
    "outship", "outshop", "outstrip", "outswel", "outspan", "overcrop",
    "pettifog", "photostat", "pouf", "preset", "prim", "pug", "ret", "rosin",
    "outwit", "overbid", "overcal", "overcommit", "overcontrol",
    "overcrap", "overdub", "overfil", "overhat", "overhit", "overlap", "overman",
    "overplot", "overrun", "overshop", "overstep", "overtip", "overtop", "overwet",
    "overwil", "pad", "paintbal", "pan", "panel", "paperclip", "par", "parallel",
    "parcel", "pat", "patrol", "pedal", "peg", "pen",
    "pencil", "pep", "permit", "pet", "petal", "photoset",
    "picket", "pig", "pilot", "pin", "pinbal", "pip", "pipefit", "pipet", "pit",
    "plan", "plit", "plod", "plop", "plot", "plug", "plumet", "plummet", "pod",
    "policyset", "polyfil", "pop", "pot", "pram", "prebag",
    "predistil", "predril", "prefer", "prefil", "preinstal", "prep", "preplan",
    "preprogram", "prizewin", "prod", "profer", "prog", "program", "prop",
    "propel", "pub", "pummel", "pun", "pup", "pushfit", "put", "quarel", "quarrel",
    "quickskim", "quickstep", "quickwit", "quip", "quit", "quivertip", "quiz",
    "rabbit", "rabit", "radiolabel", "rag", "ram", "ramrod", "rap", "rat",
    "ratecap", "ravel", "readmit", "reallot", "rebel", "rebid", "rebin", "rebut",
    "recap", "rechannel", "recommit", "recrop", "recur", "recut", "red", "redril",
    "refer", "refit", "reformat", "refret", "refuel", "reget", "regret", "reinter",
    "rejig", "rekit", "reknot", "relabel", "relet", "rem", "remap", "remetal",
    "remit", "remodel", "reoccur", "rep", "repel", "repin", "replan", "replot",
    "repol", "repot", "reprogram", "rerun", "reset", "resignal", "resit", "reskil",
    "resubmit", "retransfer", "retransmit", "retro-fit", "retrofit", "rev",
    "revel", "revet", "rewrap", "rib", "richochet", "ricochet", "rid", "rig",
    "rim", "ringlet", "rip", "rit", "rival", "rivet", "roadrun", "rob", "rocket",
    "rod", "roset", "rot", "rowel", "rub", "run", "runnel", "rut", "sab", "sad",
    "sag", "sandbag", "sap", "scab", "scalpel", "scam", "scan", "scar", "scat",
    "schlep", "scrag", "scram", "shall", "sled", "smut", "stet",
    "trepan", "unrip", "unstop", "whir", "whop", "wig", "scrap", "scrat", "scrub",
    "scrum", "scud", "scum", "scur", "sentinel", "set", "shag", "sham", "shed",
    "shim", "shin", "ship", "shir", "shit", "shlap", "shop", "shopfit", "shortfal",
    "shot", "shovel",
    "shred", "shrinkwrap", "shrivel", "shrug", "shun", "shut", "side-step",
    "sideslip", "sidestep", "signal", "sin", "sinbin", "sip", "sit", "skid",
    "skim", "skin", "skip", "skir", "skrag", "slab", "slag", "slam", "slap",
    "slim", "slip", "slit", "slob", "slog", "slop", "slot", "slowclap", "slug",
    "slum", "slur", "smit", "snag", "snap", "snip", "snivel", "snog", "snorkel",
    "snowcem", "snub", "snug", "sob", "sod", "softpedal", "son", "sop", "spam",
    "span", "spar", "spat", "spin", "spiral", "spit", "splat",
    "split", "spot", "sprig", "springtip", "spud", "spur",
    "squat", "squirrel", "stab", "stag", "star", "stem", "sten", "stencil", "step",
    "stir", "stop", "storytel", "strap", "strim", "strip", "strop", "strug",
    "strum", "strut", "stub", "stud", "stun", "sub", "subcrop", "sublet", "submit",
    "subset", "sum", "summit", "sun", "suntan", "sup", "super-chil",
    "superad", "swab", "swag", "swan", "swap", "swat", "swig", "swim", "swivel",
    "swot", "tab", "tag", "tan", "tansfer", "tap", "tar", "tassel", "tat", "tefer",
    "teleshop", "tendril", "thermal", "thermostat", "thin",
    "throb", "thrum", "thud", "thug", "tightlip", "tin", "tinsel", "tip", "tittup",
    "toecap", "tog", "tom", "tomorrow", "top", "tot", "total", "towel", "traget",
    "trainspot", "tram", "trammel", "transfer", "tranship", "transit", "transmit",
    "trap", "travel", "trek", "trendset", "trim", "trip", "tripod",
    "trod", "trot", "trowel", "tub", "tug",
    "tunnel", "tup", "tut", "twat", "twig", "twin", "twit", "typeset", "tyset",
    "un-man", "unban", "unbar", "unbob", "uncap", "unclip", "uncompel", "undam",
    "underbid", "undercut", "underlet", "underman", "underpin", "unfit", "unfulfil",
    "unknot",
    "unlip", "unlywil", "unman", "unpad", "unpeg", "unpin", "unplug", "unravel",
    "unrol", "unscrol", "unsnap", "unstal", "unstep", "unstir", "untap", "unwrap",
    "unzip", "up", "upset", "upskil", "upwel", "ven", "verbal", "vet",
    "vignet", "wad", "wag", "wainscot", "wan", "war", "waterfal",
    "waterfil", "waterlog", "weasel", "web", "wed", "wet", "wham", "whet", "whip",
    "whir", "whiz", "whup", "wildcat", "win", "windmil", "wit",
    "woodchop", "woodcut", "worship", "wrap", "wiretap", "yen", "yak",
    "yap", "yip", "yodel", "zag", "zap", "zig", "zigzag",
    "zip", "hocus",
])

_IRREG_PAST_PART = frozenset([
    "done", "gone", "been", "begun", "bent", "bid", "bidden", "bled", "born",
    "bought", "brought", "built", "caught", "clad", "could", "crept", "dove",
    "drunk", "dug", "dwelt", "fed", "felt", "fled", "flung", "fought", "found",
    "ground", "had", "held", "hung", "hurt", "kept", "knelt", "laid", "lain",
    "led", "left", "lent", "lit", "lost", "made", "met", "mown", "paid", "pled",
    "relaid", "rung", "said", "sat", "sent", "shot", "slain", "slept", "slid",
    "sold", "sought", "spat", "sped", "spelt", "spent", "split", "sprung", "spun",
    "stood", "stuck", "struck", "stung", "stunk", "sung", "sunk", "swept",
    "sworn", "swum", "swung", "thought", "told", "torn", "undergone",
    "understood", "wept", "woken", "won", "worn", "wound", "wrung",
])

IRREG_VERBS_LEX = {
    "abetted": "abet", "abetting": "abet", "abhorred": "abhor", "abhorring": "abhor",
    "abode": "abide", "accompanied": "accompany", "acidified": "acidify",
    "acquitted": "acquit", "acquitting": "acquit", "addrest": "address",
    "admitted": "admit", "admitting": "admit", "allotted": "allot", "allotting": "allot",
    "am": "be", "amplified": "amplify", "annulled": "annul", "annulling": "annul",
    "applied": "apply", "arcked": "arc", "arcking": "arc", "are": "be",
    "arisen": "arise", "arose": "arise", "ate": "eat", "atrophied": "atrophy",
    "awoke": "awake", "awoken": "awake", "bade": "bid", "bagged": "bag",
    "bagging": "bag", "bandied": "bandy", "banned": "ban", "banning": "ban",
    "barred": "bar", "barrelled": "barrel", "barrelling": "barrel", "barring": "bar",
    "batted": "bat", "batting": "bat", "beaten": "beat", "beautified": "beautify",
    "became": "become", "bed": "bed", "bedded": "bed", "bedding": "bed",
    "bedevilled": "bedevil", "bedevilling": "bedevil", "been": "be",
    "befallen": "befall", "befell": "befall", "befitted": "befit", "befitting": "befit",
    "began": "begin", "begat": "beget", "begetting": "beget", "begged": "beg",
    "begging": "beg", "beginning": "begin", "begot": "beget", "begotten": "beget",
    "begun": "begin", "beheld": "behold", "beholden": "behold", "belying": "belie",
    "benefitted": "benefit", "benefitting": "benefit", "bent": "bend",
    "bespoke": "bespeak", "bespoken": "bespeak", "betted": "bet", "betting": "bet",
    "bevelled": "bevel", "bevelling": "bevel", "biassed": "bias", "biassing": "bias",
    "bidden": "bid", "bidding": "bid", "bit": "bite", "bitted": "bit",
    "bitten": "bite", "bitting": "bit", "bled": "bleed", "blest": "bless",
    "blew": "blow", "blipped": "blip", "blipping": "blip", "blotted": "blot",
    "blotting": "blot", "blown": "blow", "blurred": "blur", "blurring": "blur",
    "bore": "bear", "born": "bear", "bought": "buy", "bound": "bind",
    "bragged": "brag", "bragging": "brag", "bred": "breed", "broke": "break",
    "broken": "break", "brought": "bring", "browbeaten": "browbeat",
    "budded": "bud", "budding": "bud", "bugged": "bug", "bugging": "bug",
    "built": "build", "bullied": "bully", "bummed": "bum", "bumming": "bum",
    "buried": "bury", "burnt": "burn", "bypast": "bypass", "calcified": "calcify",
    "came": "come", "cancelled": "cancel", "cancelling": "cancel", "canned": "can",
    "canning": "can", "capped": "cap", "capping": "cap", "carried": "carry",
    "caught": "catch", "certified": "certify", "channelled": "channel",
    "channelling": "channel", "charred": "char", "charring": "char",
    "chatted": "chat", "chatting": "chat", "chid": "chide", "chidden": "chide",
    "chinned": "chin", "chinning": "chin", "chiselled": "chisel",
    "chiselling": "chisel", "chopped": "chop", "chopping": "chop",
    "chose": "choose", "chosen": "choose", "chugged": "chug", "chugging": "chug",
    "clad": "clothe", "clarified": "clarify", "classified": "classify",
    "clipped": "clip", "clipping": "clip", "clogged": "clog", "clogging": "clog",
    "clung": "cling", "co-ordinate": "coordinate", "co-ordinated": "coordinate",
    "co-ordinates": "coordinate", "co-ordinating": "coordinate",
    "codified": "codify", "combatted": "combat", "combatting": "combat",
    "committed": "commit", "committing": "commit", "compelled": "compel",
    "compelling": "compel", "complied": "comply", "concurred": "concur",
    "concurring": "concur", "conferred": "confer", "conferring": "confer",
    "controlled": "control", "controlling": "control", "copied": "copy",
    "corralled": "corral", "corralling": "corral", "counselled": "counsel",
    "counselling": "counsel", "crammed": "cram", "cramming": "cram",
    "crept": "creep", "cried": "cry", "cropped": "crop", "cropping": "crop",
    "crucified": "crucify", "cupped": "cup", "cupping": "cup",
    "curried": "curry", "curst": "curse", "cutting": "cut", "dallied": "dally",
    "dealt": "deal", "decried": "decry", "deferred": "defer", "deferring": "defer",
    "defied": "defy", "demurred": "demur", "demurring": "demur", "denied": "deny",
    "deterred": "deter", "deterring": "deter", "detoxified": "detoxify",
    "dialled": "dial", "dialling": "dial", "did": "do", "digging": "dig",
    "dignified": "dignify", "dimmed": "dim", "dimming": "dim", "dipped": "dip",
    "dipping": "dip", "dirtied": "dirty", "dispelled": "dispel",
    "dispelling": "dispel", "disqualified": "disqualify",
    "dissatisfied": "dissatisfy", "diversified": "diversify", "divvied": "divvy",
    "dizzied": "dizzy", "done": "do", "donned": "don", "donning": "don",
    "dotted": "dot", "dotting": "dot", "dove": "dive", "dragged": "drag",
    "dragging": "drag", "drank": "drink", "drawn": "draw", "dreamt": "dream",
    "drew": "draw", "dried": "dry", "dripped": "drip", "dripping": "drip",
    "driven": "drive", "dropped": "drop", "dropping": "drop", "drove": "drive",
    "drubbed": "drub", "drubbing": "drub", "drummed": "drum", "drumming": "drum",
    "drunk": "drink", "dubbed": "dub", "dubbing": "dub", "duelled": "duel",
    "duelling": "duel", "dug": "dig", "dwelt": "dwell", "dying": "die",
    "eaten": "eat", "eavesdropped": "eavesdrop", "eavesdropping": "eavesdrop",
    "electrified": "electrify", "embedded": "embed", "embedding": "embed",
    "embodied": "embody", "emitted": "emit", "emitting": "emit",
    "emptied": "empty", "enthralled": "enthral", "enthralling": "enthral",
    "envied": "envy", "equalled": "equal", "equalling": "equal",
    "equipped": "equip", "equipping": "equip", "excelled": "excel",
    "excelling": "excel", "exemplified": "exemplify", "expelled": "expel",
    "expelling": "expel", "extolled": "extol", "extolling": "extol",
    "fallen": "fall", "falsified": "falsify", "fancied": "fancy", "fanned": "fan",
    "fanning": "fan", "fed": "feed", "feed": "feed", "fell": "fall",
    "felt": "feel", "ferried": "ferry", "fitted": "fit", "fitting": "fit",
    "flagged": "flag", "flagging": "flag", "fled": "flee", "flew": "fly",
    "flipped": "flip", "flipping": "flip", "flitted": "flit", "flitting": "flit",
    "flopped": "flop", "flopping": "flop", "flown": "fly", "flung": "fling",
    "fogged": "fog", "fogging": "fog", "forbad": "forbid", "forbade": "forbid",
    "forbidden": "forbid", "forbidding": "forbid", "foregone": "forego",
    "foresaw": "foresee", "foreseen": "foresee", "foretold": "foretell",
    "forewent": "forego", "forgave": "forgive", "forgetting": "forget",
    "forgiven": "forgive", "forgone": "forgo", "forgot": "forget",
    "forgotten": "forget", "forsaken": "forsake", "forsook": "forsake",
    "fortified": "fortify", "forwent": "forgo", "fought": "fight",
    "found": "find", "fretted": "fret", "fretting": "fret", "fried": "fry",
    "frolicked": "frolic", "frolicking": "frolic", "froze": "freeze",
    "frozen": "freeze", "fuelled": "fuel", "fuelling": "fuel",
    "funnelled": "funnel", "funnelling": "funnel", "gapped": "gap",
    "gapping": "gap", "gassed": "gas", "gasses": "gas", "gassing": "gas",
    "gave": "give", "gelled": "gel", "gelling": "gel", "getting": "get",
    "girt": "gird", "given": "give", "glorified": "glorify", "glutted": "glut",
    "glutting": "glut", "gnawn": "gnaw", "gone": "go", "got": "get",
    "gotten": "get", "grabbed": "grab", "grabbing": "grab",
    "gratified": "gratify", "grew": "grow", "grinned": "grin", "grinning": "grin",
    "gripped": "grip", "gripping": "grip", "gript": "grip", "gritted": "grit",
    "gritting": "grit", "ground": "grind", "grovelled": "grovel",
    "grovelling": "grovel", "grown": "grow", "gummed": "gum", "gumming": "gum",
    "gunned": "gun", "gunning": "gun", "had": "have", "handicapped": "handicap",
    "handicapping": "handicap", "harried": "harry", "has": "have",
    "heard": "hear", "held": "hold", "hewn": "hew", "hid": "hide",
    "hidden": "hide", "hitting": "hit", "hobnobbed": "hobnob",
    "hobnobbing": "hobnob", "honied": "honey", "hopped": "hop", "hopping": "hop",
    "horrified": "horrify", "hove": "heave", "hugged": "hug", "hugging": "hug",
    "hummed": "hum", "humming": "hum", "hung": "hang", "hurried": "hurry",
    "identified": "identify", "impelled": "impel", "impelling": "impel",
    "implied": "imply", "incurred": "incur", "incurring": "incur",
    "indemnified": "indemnify", "inferred": "infer", "inferring": "infer",
    "initialled": "initial", "initialling": "initial", "intensified": "intensify",
    "interred": "inter", "interring": "inter", "interwove": "interweave",
    "interwoven": "interweave", "is": "be", "jagged": "jag", "jagging": "jag",
    "jammed": "jam", "jamming": "jam", "jetted": "jet", "jetting": "jet",
    "jimmied": "jimmy", "jogged": "jog", "jogging": "jog", "justified": "justify",
    "kept": "keep", "kidded": "kid", "kidding": "kid", "kidnapped": "kidnap",
    "kidnapping": "kidnap", "knelt": "kneel", "knew": "know", "knitted": "knit",
    "knitting": "knit", "knotted": "knot", "knotting": "knot", "known": "know",
    "labelled": "label", "labelling": "label", "laden": "lade", "lagged": "lag",
    "lagging": "lag", "laid": "lay", "lain": "lie", "lay": "lie",
    "leant": "lean", "leapfrogged": "leapfrog", "leapfrogging": "leapfrog",
    "leapt": "leap", "learnt": "learn", "led": "lead", "left": "leave",
    "lent": "lend", "letting": "let", "levelled": "level", "levelling": "level",
    "levied": "levy", "libelled": "libel", "libelling": "libel",
    "liquefied": "liquefy", "lit": "light", "lobbed": "lob", "lobbied": "lobby",
    "lobbing": "lob", "logged": "log", "logging": "log", "lost": "lose",
    "lugged": "lug", "lugging": "lug", "lying": "lie", "made": "make",
    "magnified": "magnify", "manned": "man", "manning": "man", "mapped": "map",
    "mapping": "map", "marred": "mar", "married": "marry", "marring": "mar",
    "marshalled": "marshal", "marshalling": "marshal", "marvelled": "marvel",
    "marvelling": "marvel", "meant": "mean", "met": "meet", "mimicked": "mimic",
    "mimicking": "mimic", "misapplied": "misapply", "misled": "mislead",
    "misspelt": "misspell", "mistaken": "mistake", "mistook": "mistake",
    "misunderstood": "misunderstand", "modelled": "model", "modelling": "model",
    "modified": "modify", "mollified": "mollify", "molten": "melt",
    "mopped": "mop", "mopping": "mop", "mown": "mow", "multiplied": "multiply",
    "mummified": "mummify", "mystified": "mystify", "nabbed": "nab",
    "nabbing": "nab", "nagged": "nag", "nagging": "nag", "napped": "nap",
    "napping": "nap", "netted": "net", "netting": "net", "nipped": "nip",
    "nipping": "nip", "nodded": "nod", "nodding": "nod", "notified": "notify",
    "nullified": "nullify", "occupied": "occupy", "occurred": "occur",
    "occurring": "occur", "offsetting": "offset", "omitted": "omit",
    "omitting": "omit", "ossified": "ossify", "outbidden": "outbid",
    "outbidding": "outbid", "outdid": "outdo", "outdone": "outdo",
    "outfitted": "outfit", "outfitting": "outfit", "outgrew": "outgrow",
    "outgrown": "outgrow", "outputted": "output", "outputting": "output",
    "outran": "outrun", "outrunning": "outrun", "outshone": "outshine",
    "outsold": "outsell", "outstripped": "outstrip", "outstripping": "outstrip",
    "outwitted": "outwit", "outwitting": "outwit", "overcame": "overcome",
    "overdid": "overdo", "overdone": "overdo", "overdrawn": "overdraw",
    "overdrew": "overdraw", "overflown": "overflow", "overheard": "overhear",
    "overhung": "overhang", "overlaid": "overlay", "overlapped": "overlap",
    "overlapping": "overlap", "overpaid": "overpay", "overridden": "override",
    "overrode": "override", "oversaw": "oversee", "overseen": "oversee",
    "oversimplified": "oversimplify", "overspent": "overspend",
    "overstepped": "overstep", "overstepping": "overstep",
    "overtaken": "overtake", "overthrew": "overthrow", "overthrown": "overthrow",
    "overtook": "overtake", "pacified": "pacify", "padded": "pad",
    "padding": "pad", "paid": "pay", "panicked": "panic", "panicking": "panic",
    "panned": "pan", "panning": "pan", "parallelled": "parallel",
    "parallelling": "parallel", "parcelled": "parcel", "parcelling": "parcel",
    "parodied": "parody", "parried": "parry", "partaken": "partake",
    "partook": "partake", "patrolled": "patrol", "patrolling": "patrol",
    "patted": "pat", "patting": "pat", "pedalled": "pedal", "pedalling": "pedal",
    "pegged": "peg", "pegging": "peg", "pencilled": "pencil",
    "pencilling": "pencil", "penned": "pen", "penning": "pen", "pent": "pen",
    "permitted": "permit", "permitting": "permit", "personified": "personify",
    "petrified": "petrify", "petted": "pet", "petting": "pet",
    "photocopied": "photocopy", "pilloried": "pillory", "pinned": "pin",
    "pinning": "pin", "pitied": "pity", "pitted": "pit", "pitting": "pit",
    "planned": "plan", "planning": "plan", "pled": "plead", "plied": "ply",
    "plodded": "plod", "plodding": "plod", "plopped": "plop", "plopping": "plop",
    "plotted": "plot", "plotting": "plot", "plugged": "plug", "plugging": "plug",
    "popped": "pop", "popping": "pop", "potted": "pot", "potting": "pot",
    "preferred": "prefer", "preferring": "prefer", "preoccupied": "preoccupy",
    "prepaid": "prepay", "pried": "pry", "prodded": "prod", "prodding": "prod",
    "programmed": "program", "programmes": "program", "programming": "program",
    "propelled": "propel", "propelling": "propel", "prophesied": "prophesy",
    "propped": "prop", "propping": "prop", "proven": "prove",
    "pummelled": "pummel", "pummelling": "pummel", "purified": "purify",
    "putting": "put", "qualified": "qualify", "quantified": "quantify",
    "quarrelled": "quarrel", "quarrelling": "quarrel", "quitted": "quit",
    "quitting": "quit", "quizzed": "quiz", "quizzes": "quiz", "quizzing": "quiz",
    "rallied": "rally", "rammed": "ram", "ramming": "ram", "ran": "run",
    "rang": "ring", "rapped": "rap", "rapping": "rap", "rarefied": "rarefy",
    "ratified": "ratify", "ratted": "rat", "ratting": "rat",
    "rebelled": "rebel", "rebelling": "rebel", "rebuilt": "rebuild",
    "rebutted": "rebut", "rebutting": "rebut", "reclassified": "reclassify",
    "rectified": "rectify", "recurred": "recur", "recurring": "recur",
    "redid": "redo", "redone": "redo", "referred": "refer", "referring": "refer",
    "refitted": "refit", "refitting": "refit", "refuelled": "refuel",
    "refuelling": "refuel", "regretted": "regret", "regretting": "regret",
    "reheard": "rehear", "relied": "rely", "remade": "remake",
    "remarried": "remarry", "remitted": "remit", "remitting": "remit",
    "repaid": "repay", "repelled": "repel", "repelling": "repel",
    "replied": "reply", "resetting": "reset", "retaken": "retake",
    "rethought": "rethink", "retook": "retake", "retried": "retry",
    "retrofitted": "retrofit", "retrofitting": "retrofit", "revelled": "revel",
    "revelling": "revel", "revved": "rev", "revving": "rev",
    "rewritten": "rewrite", "rewrote": "rewrite", "ricochetted": "ricochet",
    "ricochetting": "ricochet", "ridded": "rid", "ridden": "ride",
    "ridding": "rid", "rigged": "rig", "rigging": "rig", "ripped": "rip",
    "ripping": "rip", "risen": "rise", "rivalled": "rival", "rivalling": "rival",
    "resold": "resell", "robbed": "rob", "robbing": "rob", "rode": "ride",
    "rose": "rise", "rotted": "rot", "rotting": "rot", "rubbed": "rub",
    "rubbing": "rub", "rung": "ring", "running": "run", "sagged": "sag",
    "sagging": "sag", "said": "say", "sallied": "sally", "sang": "sing",
    "sank": "sink", "sapped": "sap", "sapping": "sap", "sat": "sit",
    "satisfied": "satisfy", "savvied": "savvy", "saw": "see",
    "scanned": "scan", "scanning": "scan", "scrapped": "scrap",
    "scrapping": "scrap", "scrubbed": "scrub", "scrubbing": "scrub",
    "scurried": "scurry", "seed": "seed", "seen": "see", "sent": "send",
    "setting": "set", "sewn": "sew", "shaken": "shake", "shaven": "shave",
    "shed": "shed", "shedding": "shed", "shied": "shy", "shimmed": "shim",
    "shimmied": "shimmy", "shimming": "shim", "shipped": "ship",
    "shipping": "ship", "shone": "shine", "shook": "shake", "shopped": "shop",
    "shopping": "shop", "shot": "shoot", "shovelled": "shovel",
    "shovelling": "shovel", "shown": "show", "shrank": "shrink",
    "shredded": "shred", "shredding": "shred", "shrivelled": "shrivel",
    "shrivelling": "shrivel", "shrugged": "shrug", "shrugging": "shrug",
    "shrunk": "shrink", "shrunken": "shrink", "shunned": "shun",
    "shunning": "shun", "shutting": "shut", "sicked": "sic", "sicking": "sic",
    "sidestepped": "sidestep", "sidestepping": "sidestep",
    "signalled": "signal", "signalling": "signal", "signified": "signify",
    "simplified": "simplify", "singing": "sing", "sinned": "sin",
    "sinning": "sin", "sitting": "sit", "ski'd": "ski", "skidded": "skid",
    "skidding": "skid", "skimmed": "skim", "skimming": "skim",
    "skipped": "skip", "skipping": "skip", "slain": "slay",
    "slammed": "slam", "slamming": "slam", "slapped": "slap",
    "slapping": "slap", "sledding": "sled", "slept": "sleep", "slew": "slay",
    "slid": "slide", "slidden": "slide", "slipped": "slip", "slipping": "slip",
    "slitting": "slit", "slogged": "slog", "slogging": "slog",
    "slopped": "slop", "slopping": "slop", "slugged": "slug", "slugging": "slug",
    "slung": "sling", "slurred": "slur", "slurring": "slur", "smelt": "smell",
    "snagged": "snag", "snagging": "snag", "snapped": "snap", "snapping": "snap",
    "snipped": "snip", "snipping": "snip", "snubbed": "snub", "snubbing": "snub",
    "snuck": "sneak", "sobbed": "sob", "sobbing": "sob", "sold": "sell",
    "solidified": "solidify", "sought": "seek", "sown": "sow",
    "spanned": "span", "spanning": "span", "spat": "spit",
    "specified": "specify", "sped": "speed", "spelt": "spell",
    "spent": "spend", "spied": "spy", "spilt": "spill", "spinning": "spin",
    "spiralled": "spiral", "spiralling": "spiral", "spitted": "spit",
    "spitting": "spit", "splitting": "split", "spoilt": "spoil",
    "spoke": "speak", "spoken": "speak", "spotlit": "spotlight",
    "spotted": "spot", "spotting": "spot", "sprang": "spring",
    "sprung": "spring", "spun": "spin", "spurred": "spur", "spurring": "spur",
    "squatted": "squat", "squatting": "squat", "stank": "stink",
    "starred": "star", "starring": "star", "stemmed": "stem",
    "stemming": "stem", "stepped": "step", "stepping": "step",
    "stirred": "stir", "stirring": "stir", "stole": "steal", "stolen": "steal",
    "stood": "stand", "stopped": "stop", "stopping": "stop", "stove": "stave",
    "strapped": "strap", "strapping": "strap", "stratified": "stratify",
    "stridden": "stride", "stripped": "strip", "stripping": "strip",
    "striven": "strive", "strode": "stride", "strove": "strive",
    "struck": "strike", "strung": "string", "stubbed": "stub", "stubbing": "stub",
    "stuck": "stick", "studied": "study", "stung": "sting", "stunk": "stink",
    "stunned": "stun", "stunning": "stun", "stymying": "stymie",
    "subletting": "sublet", "submitted": "submit", "submitting": "submit",
    "summed": "sum", "summing": "sum", "sung": "sing", "sunk": "sink",
    "sunken": "sink", "sunned": "sun", "sunning": "sun", "supplied": "supply",
    "swabbed": "swab", "swabbing": "swab", "swam": "swim", "swapped": "swap",
    "swapping": "swap", "swept": "sweep", "swimming": "swim",
    "swivelled": "swivel", "swivelling": "swivel", "swollen": "swell",
    "swopped": "swap", "swopping": "swap", "swops": "swap", "swore": "swear",
    "sworn": "swear", "swum": "swim", "swung": "swing", "tagged": "tag",
    "tagging": "tag", "taken": "take", "tallied": "tally", "tapped": "tap",
    "tapping": "tap", "tarried": "tarry", "taught": "teach", "taxying": "taxi",
    "terrified": "terrify", "testified": "testify", "thinned": "thin",
    "thinning": "thin", "thought": "think", "threw": "throw",
    "thriven": "thrive", "throbbed": "throb", "throbbing": "throb",
    "throve": "thrive", "thrown": "throw", "thudded": "thud", "thudding": "thud",
    "tipped": "tip", "tipping": "tip", "told": "tell", "took": "take",
    "topped": "top", "topping": "top", "tore": "tear", "torn": "tear",
    "totalled": "total", "totalling": "total", "trafficked": "traffic",
    "trafficking": "traffic", "trameled": "trammel", "trameling": "trammel",
    "tramelled": "trammel", "tramelling": "trammel", "tramels": "trammel",
    "transferred": "transfer", "transferring": "transfer",
    "transmitted": "transmit", "transmitting": "transmit", "trapped": "trap",
    "trapping": "trap", "travelled": "travel", "travelling": "travel",
    "trekked": "trek", "trekking": "trek", "tried": "try", "trimmed": "trim",
    "trimming": "trim", "tripped": "trip", "tripping": "trip", "trod": "tread",
    "trodden": "tread", "trotted": "trot", "trotting": "trot", "tugged": "tug",
    "tugging": "tug", "tunnelled": "tunnel", "tunnelling": "tunnel",
    "tying": "tie", "typified": "typify", "undercutting": "undercut",
    "undergone": "undergo", "underlain": "underlie", "underlay": "underlie",
    "underlying": "underlie", "underpinned": "underpin",
    "underpinning": "underpin", "understood": "understand",
    "undertaken": "undertake", "undertook": "undertake", "underwent": "undergo",
    "underwritten": "underwrite", "underwrote": "underwrite", "undid": "undo",
    "undone": "undo", "unified": "unify", "unravelled": "unravel",
    "unravelling": "unravel", "unsteadied": "unsteady", "untying": "untie",
    "unwound": "unwind", "upheld": "uphold", "upsetting": "upset",
    "varied": "vary", "verified": "verify", "vilified": "vilify",
    "wadded": "wad", "wadding": "wad", "wagged": "wag", "wagging": "wag",
    "was": "be", "wearied": "weary", "wedded": "wed", "wedding": "wed",
    "weed": "weed", "went": "go", "wept": "weep", "were": "be",
    "wetted": "wet", "wetting": "wet", "whetted": "whet", "whetting": "whet",
    "whipped": "whip", "whipping": "whip", "whizzed": "whiz",
    "whizzes": "whiz", "whizzing": "whiz", "winning": "win",
    "withdrawn": "withdraw", "withdrew": "withdraw", "withheld": "withhold",
    "withstood": "withstand", "woke": "wake", "woken": "wake", "won": "win",
    "wore": "wear", "worn": "wear", "worried": "worry",
    "worshipped": "worship", "worshipping": "worship", "wound": "wind",
    "wove": "weave", "woven": "weave", "wrapped": "wrap", "wrapping": "wrap",
    "written": "write", "wrote": "write", "wrought": "work", "wrung": "wring",
    "yodelled": "yodel", "yodelling": "yodel", "zapped": "zap", "zapping": "zap",
    "zigzagged": "zigzag", "zigzagging": "zigzag", "zipped": "zip",
    "zipping": "zip",
}

IRREG_VERBS_NOLEX = {
    "abutted": "abut", "abutting": "abut", "ad-libbed": "ad-lib",
    "ad-libbing": "ad-lib", "aerified": "aerify", "air-dried": "air-dry",
    "airdropped": "airdrop", "airdropping": "airdrop", "appalled": "appal",
    "appalling": "appal", "averred": "aver", "averring": "aver",
    "baby-sat": "baby-sit", "baby-sitting": "baby-sit",
    "back-pedalled": "back-pedal", "back-pedalling": "back-pedal",
    "backslid": "backslide", "backslidden": "backslide", "befogged": "befog",
    "befogging": "befog", "begirt": "begird", "bejewelled": "bejewel",
    "bejewelling": "bejewel", "belly-flopped": "belly-flop",
    "belly-flopping": "belly-flop", "blabbed": "blab", "blabbing": "blab",
    "bobbed": "bob", "bobbing": "bob", "bogged-down": "bog-down",
    "bogged_down": "bog_down", "bogging-down": "bog-down",
    "bogging_down": "bog_down", "bogs-down": "bog-down", "bogs_down": "bog_down",
    "booby-trapped": "booby-trap", "booby-trapping": "booby-trap",
    "bottle-fed": "bottle-feed", "breast-fed": "breast-feed",
    "brutified": "brutify", "bullshitted": "bullshit", "bullshitting": "bullshit",
    "bullwhipped": "bullwhip", "bullwhipping": "bullwhip", "caddies": "caddie",
    "caddying": "caddie", "carolled": "carol", "carolling": "carol",
    "catnapped": "catnap", "catnapping": "catnap", "citified": "citify",
    "cleft": "cleave", "clopped": "clop", "clopping": "clop", "clove": "cleave",
    "cloven": "cleave", "co-opted": "coopt", "co-opting": "coopt",
    "co-opts": "coopts", "co-starred": "co-star", "co-starring": "co-star",
    "coiffed": "coif", "coiffing": "coif", "court-martialled": "court-martial",
    "court-martialling": "court-martial", "crossbred": "crossbreed",
    "crosscutting": "crosscut", "curtsied": "curtsy", "dabbed": "dab",
    "dabbing": "dab", "dandified": "dandify", "debarred": "debar",
    "debarring": "debar", "debugged": "debug", "debugging": "debug",
    "decalcified": "decalcify", "declassified": "declassify",
    "decontrolled": "decontrol", "deep-fried": "deep-fry",
    "dehumidified": "dehumidify", "deified": "deify", "demystified": "demystify",
    "disbarred": "disbar", "disbarring": "disbar", "disembodied": "disembody",
    "disembowelled": "disembowel", "disembowelling": "disembowel",
    "disenthralled": "disenthral", "disenthralling": "disenthral",
    "disenthralls": "disenthral", "disenthrals": "disenthrall",
    "disinterred": "disinter", "disinterring": "disinter", "distilled": "distil",
    "distilling": "distil", "eddied": "eddy", "edified": "edify",
    "ego-tripped": "ego-trip", "ego-tripping": "ego-trip",
    "empanelled": "empanel", "empanelling": "empanel",
    "emulsified": "emulsify", "entrapped": "entrap", "entrapping": "entrap",
    "fibbed": "fib", "fibbing": "fib", "filled_up": "fill_up",
    "flip-flopped": "flip-flop", "flip-flopping": "flip-flop", "flogged": "flog",
    "flogging": "flog", "foreran": "forerun", "forerunning": "forerun",
    "foxtrotted": "foxtrot", "foxtrotting": "foxtrot",
    "freeze-dried": "freeze-dry", "frigged": "frig", "frigging": "frig",
    "fritted": "frit", "fritting": "frit", "fulfilled": "fulfil",
    "fulfilling": "fulfil", "gambolled": "gambol", "gambolling": "gambol",
    "gasified": "gasify", "gelt": "geld", "ghostwritten": "ghostwrite",
    "ghostwrote": "ghostwrite", "giftwrapped": "giftwrap",
    "giftwrapping": "giftwrap", "gilt": "gild", "gipped": "gip",
    "gipping": "gip", "glommed": "glom", "glomming": "glom",
    "goose-stepped": "goose-step", "goose-stepping": "goose-step",
    "gypped": "gyp", "gypping": "gyp",
    "hand-knitted": "hand-knit", "hand-knitting": "hand-knit",
    "handfed": "handfeed", "high-hatted": "high-hat", "high-hatting": "high-hat",
    "hogtying": "hogtie", "horsewhipped": "horsewhip",
    "horsewhipping": "horsewhip", "humidified": "humidify",
    "hypertrophied": "hypertrophy", "inbred": "inbreed", "installed": "instal",
    "installing": "instal", "interbred": "interbreed",
    "intercutting": "intercut", "interlaid": "interlay",
    "interlapped": "interlap", "intermarried": "intermarry",
    "jellified": "jellify", "jibbed": "jib", "jibbing": "jib",
    "jitterbugged": "jitterbug", "jitterbugging": "jitterbug",
    "joy-ridden": "joy-ride", "joy-rode": "joy-ride", "jutted": "jut",
    "jutting": "jut", "knapped": "knap", "knapping": "knap", "ko'd": "ko",
    "ko'ing": "ko", "ko's": "ko", "lallygagged": "lallygag",
    "lallygagging": "lallygag", "lignified": "lignify", "liquified": "liquify",
    "machine-gunned": "machine-gun", "machine-gunning": "machine-gun",
    "minified": "minify", "miscarried": "miscarry", "misdealt": "misdeal",
    "misgave": "misgive", "misgiven": "misgive", "mislaid": "mislay",
    "mispled": "misplead", "misspent": "misspend", "mortified": "mortify",
    "objectified": "objectify", "outfought": "outfight",
    "outridden": "outride", "outrode": "outride", "outshot": "outshoot",
    "outthought": "outthink", "overbidden": "overbid", "overbidding": "overbid",
    "overblew": "overblow", "overblown": "overblow", "overflew": "overfly",
    "overgrew": "overgrow", "overgrown": "overgrow", "overshot": "overshoot",
    "overslept": "oversleep", "overwritten": "overwrite",
    "overwrote": "overwrite", "pinch-hitting": "pinch-hit",
    "pistol-whipped": "pistol-whip", "pistol-whipping": "pistol-whip",
    "pommelled": "pommel", "pommelling": "pommel", "prettified": "prettify",
    "putrefied": "putrefy", "quickstepped": "quickstep",
    "quickstepping": "quickstep", "rappelled": "rappel", "rappelling": "rappel",
    "recapped": "recap", "recapping": "recap", "recommitted": "recommit",
    "recommitting": "recommit", "reified": "reify", "rent": "rend",
    "repotted": "repot", "repotting": "repot",
    "retransmitted": "retransmit", "retransmitting": "retransmit",
    "reunified": "reunify", "rewound": "rewind", "sanctified": "sanctify",
    "sandbagged": "sandbag", "sandbagging": "sandbag", "scarified": "scarify",
    "scatted": "scat", "scrammed": "scram", "scramming": "scram",
    "scrummed": "scrum", "scrumming": "scrum", "shagged": "shag",
    "shagging": "shag", "sharecropped": "sharecrop",
    "sharecropping": "sharecrop", "shellacked": "shellac",
    "shellacking": "shellac", "shrink-wrapped": "shrink-wrap",
    "shrink-wrapping": "shrink-wrap", "sideslipped": "sideslip",
    "sideslipping": "sideslip", "sightsaw": "sightsee", "sightseen": "sightsee",
    "skinny-dipped": "skinny-dip", "skinny-dipping": "skinny-dip",
    "skydove": "skydive", "slunk": "slink", "smit": "smite",
    "smitten": "smite", "smote": "smite", "snivelled": "snivel",
    "snivelling": "snivel", "snogged": "snog", "snogging": "snog",
    "soft-pedalled": "soft-pedal", "soft-pedalling": "soft-pedal",
    "sparred": "spar", "sparring": "spar", "speechified": "speechify",
    "spellbound": "spellbind", "spin-dried": "spin-dry",
    "spoon-fed": "spoon-feed", "stencilled": "stencil", "stencilling": "stencil",
    "strewn": "strew", "strummed": "strum", "strumming": "strum",
    "stultified": "stultify", "stupefied": "stupefy",
    "subjectified": "subjectify", "subtotalled": "subtotal",
    "subtotalling": "subtotal", "sullied": "sully", "supped": "sup",
    "supping": "sup", "syllabified": "syllabify",
    "talcked": "talc", "talcking": "talc",
    "thrummed": "thrum", "thrumming": "thrum",
    "trammed": "tram", "tramming": "tram", "transfixt": "transfix",
    "transmogrified": "transmogrify", "trepanned": "trepan",
    "trepanning": "trepan", "typesetting": "typeset",
    "typewritten": "typewrite", "typewrote": "typewrite",
    "uglified": "uglify", "unbound": "unbind", "unclad": "unclothe",
    "underbidding": "underbid", "underfed": "underfeed",
    "underpaid": "underpay", "undersold": "undersell",
    "understudied": "understudy", "unfroze": "unfreeze",
    "unfrozen": "unfreeze", "unlearnt": "unlearn", "unmade": "unmake",
    "unmanned": "unman", "unmanning": "unman", "unpinned": "unpin",
    "unpinning": "unpin", "unplugged": "unplug", "unplugging": "unplug",
    "unslung": "unsling", "unstrung": "unstring", "unstuck": "unstick",
    "unwrapped": "unwrap", "unwrapping": "unwrap", "unzipped": "unzip",
    "unzipping": "unzip", "uppercutting": "uppercut", "verbified": "verbify",
    "versified": "versify", "vivified": "vivify", "vying": "vie",
    "waylaid": "waylay", "whinnied": "whinny", "whirred": "whir",
    "whirring": "whir", "window-shopped": "window-shop",
    "window-shopping": "window-shop", "yakked": "yak", "yakking": "yak",
    "yapped": "yap", "yapping": "yap",
}

_IRREG_VERBS_LEX_VALUES = frozenset(IRREG_VERBS_LEX.values())
_IRREG_VERBS_NOLEX_VALUES = frozenset(IRREG_VERBS_NOLEX.values())

_PAST_PART_RULESET = {
    "name": "PAST_PARTICIPLE",
    "default": _RE(_ANY, 0, "ed"),
    "rules": _PAST_PART_RULES,
    "doubling": True,
}
_PRESENT_PART_RULESET = {
    "name": "ING_FORM",
    "default": _RE(_ANY, 0, "ing"),
    "rules": _ING_FORM_RULES,
    "doubling": True,
}
_PAST_RULESET = {
    "name": "PAST",
    "default": _RE(_ANY, 0, "ed"),
    "rules": _PAST_RULES,
    "doubling": True,
}
_PRESENT_RULESET = {
    "name": "PRESENT",
    "default": _RE(_ANY, 0, "s"),
    "rules": _PRESENT_RULES,
    "doubling": False,
}


# ── Conjugator class ─────────────────────────────────────────────────────────
class Conjugator:
    """English verb conjugator."""

    def __init__(self):
        self._reset()

    # ── Public API ───────────────────────────────────────────────────────────
    def conjugate(self, verb, args=None):
        if not verb:
            raise ValueError("No verb")
        if args is None:
            return verb

        verb = verb.lower()

        # ensure base form
        if not _has_tag(verb, "vb"):
            verb = self.unconjugate(verb) or verb

        self._parse_args(args)

        front_vg = "be" if verb in _TO_BE else self._handle_stem(verb)
        actual_modal = None
        conjs = []

        if self.form == INFINITIVE:
            actual_modal = "to"
        if self.tense == FUTURE:
            actual_modal = "will"
        if self.passive:
            conjs.append(self.past_part(front_vg))
            front_vg = "be"
        if self.progressive:
            conjs.append(self.present_part(front_vg))
            front_vg = "be"
        if self.perfect:
            conjs.append(self.past_part(front_vg))
            front_vg = "have"
        if actual_modal:
            conjs.append(front_vg)
            front_vg = None

        if front_vg:
            if self.form == GERUND:
                conjs.append(self.present_part(front_vg))
            elif self.interrogative and front_vg != "be" and len(conjs) < 1:
                conjs.append(front_vg)
            else:
                conjs.append(self._verb_form(front_vg, self.tense, self.person, self.number))

        if actual_modal:
            conjs.append(actual_modal)

        # JS reduce: (acc, cur) => cur + ' ' + acc  →  reverse join
        result = conjs[0]
        for i in range(1, len(conjs)):
            result = conjs[i] + " " + result
        return result.strip()

    def past_part(self, verb):
        if not verb:
            return ""
        if self._is_past_participle(verb):
            return verb
        return self._check_rules(_PAST_PART_RULESET, verb)

    def present_part(self, verb):
        if not verb:
            return ""
        return self._check_rules(_PRESENT_PART_RULESET, verb)

    def unconjugate(self, word, dbug=False):
        if not isinstance(word, str):
            return None

        if word in IRREG_VERBS_LEX:
            return IRREG_VERBS_LEX[word]
        if word in _IRREG_VERBS_LEX_VALUES:
            return word

        if word in IRREG_VERBS_NOLEX:
            return IRREG_VERBS_NOLEX[word]
        if word in _IRREG_VERBS_NOLEX_VALUES:
            return word

        tags = _pos_arr(word) or []

        # already base form verb
        if "vb" in tags:
            return word

        # 1) 3rd person present (-s)
        if word.endswith("s"):
            if word.endswith("ies"):
                return word[:-3] + "y"
            elif re.search(r"(ch|s|sh|x|z|o)es$", word):
                return word[:-2]
            return word[:-1]

        # 2) past forms (-ed)
        elif word.endswith("ed"):
            if word.endswith("ied"):
                return word[:-3] + "y"
            elif re.search(r"([a-z])\1ed$", word):
                if word[:-2] in _verbs_ending_in_double():
                    return word[:-2]
                return word[:-3]
            else:
                base_e = word[:-1]  # strip just d → might end in 'e'
                if base_e in _verbs_ending_in_e():
                    return base_e
                return word[:-2]

        # 3) ends with -ing
        elif word.endswith("ing"):
            if re.search(r"([a-z])\1ing$", word):
                stem = word[:-3]
                if stem in _verbs_ending_in_double():
                    return stem
                return word[:-4]

            if word.endswith("ying"):
                ie_form = word[:-4] + "ie"
                if ie_form in _verbs_ending_in_e():
                    return ie_form

            e_form = word[:-3] + "e"
            if e_form in _verbs_ending_in_e():
                return e_form

            return word[:-3]

        else:
            if not any(t.startswith("vb") for t in tags):
                return word

        return word

    def __str__(self):
        return (
            "  ---------------------\n"
            f"  Passive = {str(self.passive).lower()}\n"
            f"  Perfect = {str(self.perfect).lower()}\n"
            f"  Progressive = {str(self.progressive).lower()}\n"
            "  ---------------------\n"
            f"  Number = {self.number}\n"
            f"  Person = {self.person}\n"
            f"  Tense = {self.tense}\n"
            "  ---------------------\n"
        )

    # ── Private ──────────────────────────────────────────────────────────────
    def _reset(self):
        self.passive = self.perfect = self.progressive = self.interrogative = False
        self.tense = PRESENT
        self.person = FIRST
        self.number = SINGULAR
        self.form = NORMAL

    def _parse_args(self, args):
        self._reset()
        if isinstance(args, str):
            m = re.match(r"^([123])([SP])(Pr|Pa|Fu)$", args)
            if not m:
                raise ValueError(f"Invalid args: {args}")
            self.person = int(m.group(1))
            self.number = SINGULAR if m.group(2) == "S" else PLURAL
            t = m.group(3)
            self.tense = PRESENT if t == "Pr" else (PAST if t == "Pa" else FUTURE)
            return
        if not isinstance(args, dict):
            raise ValueError(f"Invalid args: {args}")
        if "number" in args:
            self.number = args["number"]
        if "person" in args:
            self.person = args["person"]
        if "tense" in args:
            self.tense = args["tense"]
        if "form" in args:
            self.form = args["form"]
        if "passive" in args:
            self.passive = args["passive"]
        if "progressive" in args:
            self.progressive = args["progressive"]
        if "interrogative" in args:
            self.interrogative = args["interrogative"]
        if "perfect" in args:
            self.perfect = args["perfect"]

    def _check_rules(self, ruleset, verb):
        if not verb:
            return ""
        verb = verb.strip()
        if verb in _MODALS:
            return verb
        for rule in ruleset["rules"]:
            if rule.applies(verb):
                return rule.fire(verb)
        if ruleset["doubling"] and verb in _VERB_CONS_DOUBLING:
            verb = verb + verb[-1]
        return ruleset["default"].fire(verb)

    def _is_past_participle(self, word):
        w = word.lower()
        pa = _pos_arr(w)
        if pa and "vbn" in pa:
            return True
        if w in _IRREG_PAST_PART:
            return True
        if w.endswith("ed"):
            p = (_pos_arr(w[:-1]) or _pos_arr(w[:-2]))
            if not p and len(w) >= 5 and w[-3] == w[-4]:
                p = _pos_arr(w[:-3])
            if not p and w.endswith("ied"):
                p = _pos_arr(w[:-3] + "y")
            if p and "vb" in p:
                return True
        if w.endswith("en"):
            p = (_pos_arr(w[:-1]) or _pos_arr(w[:-2]))
            if not p and len(w) >= 4 and w[-3] == w[-4]:
                p = _pos_arr(w[:-3])
            if p and ("vb" in p or "vbd" in p):
                return True
            stem = w[:-2]
            if re.match(r"^(writt|ridd|chidd|swoll)$", stem):
                return True
        if re.search(r"[ndt]$", w) and w in IRREG_VERBS_LEX:
            p = _pos_arr(w[:-1])
            if p and "vb" in p:
                return True
        return False

    def _past_tense(self, verb, person, number):
        if verb.lower() == "be":
            if number == SINGULAR:
                if person == FIRST:
                    pass  # fall through to checkRules → "was"
                elif person == THIRD:
                    return "was"
                elif person == SECOND:
                    return "were"
            else:
                return "were"
        return self._check_rules(_PAST_RULESET, verb)

    def _present_tense(self, verb, person=None, number=None):
        person = person or self.person
        number = number or self.number
        if person == THIRD and number == SINGULAR:
            return self._check_rules(_PRESENT_RULESET, verb)
        if verb == "be":
            if number == SINGULAR:
                if person == FIRST:
                    return "am"
                elif person == SECOND:
                    return "are"
                elif person == THIRD:
                    return "is"
            else:
                return "are"
        return verb

    def _verb_form(self, verb, tense, person, number):
        if tense == PRESENT:
            return self._present_tense(verb, person, number)
        elif tense == PAST:
            return self._past_tense(verb, person, number)
        return verb

    def _handle_stem(self, word):
        """Port of JS _handleStem: find the best matching verb base form for a stem."""
        # already a base-form verb in the lexicon
        if _has_tag(word, "vb"):
            return word

        verbs = _all_verbs()
        w = word
        while len(w) > 1:
            candidates = [v for v in verbs if v.startswith(w)]
            if candidates:
                # prefer shorter words first (same as JS sort)
                candidates.sort(key=len)
                for c in candidates:
                    if word == c:
                        return word
                    # import lazily to avoid circular import
                    from rita.stemmer import Stemmer
                    if Stemmer.stem(c) == word:
                        return c
                    unc = self.unconjugate(Stemmer.stem(c))
                    if unc and unc == word:
                        return c
            w = w[:-1]

        # can't find anything — return original
        return word
