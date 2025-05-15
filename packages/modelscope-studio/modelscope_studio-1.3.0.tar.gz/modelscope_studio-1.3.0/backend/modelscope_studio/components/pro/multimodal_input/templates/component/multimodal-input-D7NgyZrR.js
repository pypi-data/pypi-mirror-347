import { i as ni, a as qt, r as ri, b as ii, w as ot, g as oi, c as Z, d as si, e as ai, o as li } from "./Index-IYHbsoR5.js";
const R = window.ms_globals.React, f = window.ms_globals.React, Kr = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, Ie = window.ms_globals.React.useState, xe = window.ms_globals.React.useEffect, Yr = window.ms_globals.React.version, Zr = window.ms_globals.React.isValidElement, Qr = window.ms_globals.React.useLayoutEffect, Jr = window.ms_globals.React.useImperativeHandle, ei = window.ms_globals.React.memo, Gt = window.ms_globals.React.useMemo, ti = window.ms_globals.React.useCallback, mn = window.ms_globals.ReactDOM, dt = window.ms_globals.ReactDOM.createPortal, ci = window.ms_globals.internalContext.useContextPropsContext, ui = window.ms_globals.internalContext.useSuggestionOpenContext, di = window.ms_globals.antdIcons.FileTextFilled, fi = window.ms_globals.antdIcons.CloseCircleFilled, hi = window.ms_globals.antdIcons.FileExcelFilled, pi = window.ms_globals.antdIcons.FileImageFilled, mi = window.ms_globals.antdIcons.FileMarkdownFilled, gi = window.ms_globals.antdIcons.FilePdfFilled, vi = window.ms_globals.antdIcons.FilePptFilled, bi = window.ms_globals.antdIcons.FileWordFilled, yi = window.ms_globals.antdIcons.FileZipFilled, wi = window.ms_globals.antdIcons.PlusOutlined, Si = window.ms_globals.antdIcons.LeftOutlined, xi = window.ms_globals.antdIcons.RightOutlined, Ei = window.ms_globals.antdIcons.CloseOutlined, Ci = window.ms_globals.antdIcons.ClearOutlined, _i = window.ms_globals.antdIcons.ArrowUpOutlined, Ri = window.ms_globals.antdIcons.AudioMutedOutlined, Ti = window.ms_globals.antdIcons.AudioOutlined, Pi = window.ms_globals.antdIcons.CloudUploadOutlined, Mi = window.ms_globals.antdIcons.LinkOutlined, Oi = window.ms_globals.antd.ConfigProvider, sr = window.ms_globals.antd.Upload, ft = window.ms_globals.antd.theme, Li = window.ms_globals.antd.Progress, Ai = window.ms_globals.antd.Image, De = window.ms_globals.antd.Button, ar = window.ms_globals.antd.Flex, $t = window.ms_globals.antd.Typography, $i = window.ms_globals.antd.Input, Ii = window.ms_globals.antd.Tooltip, Di = window.ms_globals.antd.Badge, Kt = window.ms_globals.antdCssinjs.unit, It = window.ms_globals.antdCssinjs.token2CSSVar, gn = window.ms_globals.antdCssinjs.useStyleRegister, ki = window.ms_globals.antdCssinjs.useCSSVarRegister, Ni = window.ms_globals.antdCssinjs.createTheme, Fi = window.ms_globals.antdCssinjs.useCacheToken;
var ji = /\s/;
function Wi(n) {
  for (var e = n.length; e-- && ji.test(n.charAt(e)); )
    ;
  return e;
}
var Bi = /^\s+/;
function Hi(n) {
  return n && n.slice(0, Wi(n) + 1).replace(Bi, "");
}
var vn = NaN, zi = /^[-+]0x[0-9a-f]+$/i, Ui = /^0b[01]+$/i, Vi = /^0o[0-7]+$/i, Xi = parseInt;
function bn(n) {
  if (typeof n == "number")
    return n;
  if (ni(n))
    return vn;
  if (qt(n)) {
    var e = typeof n.valueOf == "function" ? n.valueOf() : n;
    n = qt(e) ? e + "" : e;
  }
  if (typeof n != "string")
    return n === 0 ? n : +n;
  n = Hi(n);
  var t = Ui.test(n);
  return t || Vi.test(n) ? Xi(n.slice(2), t ? 2 : 8) : zi.test(n) ? vn : +n;
}
function Gi() {
}
var Dt = function() {
  return ri.Date.now();
}, qi = "Expected a function", Ki = Math.max, Yi = Math.min;
function Zi(n, e, t) {
  var r, i, o, s, a, c, l = 0, u = !1, d = !1, h = !0;
  if (typeof n != "function")
    throw new TypeError(qi);
  e = bn(e) || 0, qt(t) && (u = !!t.leading, d = "maxWait" in t, o = d ? Ki(bn(t.maxWait) || 0, e) : o, h = "trailing" in t ? !!t.trailing : h);
  function p(S) {
    var T = r, E = i;
    return r = i = void 0, l = S, s = n.apply(E, T), s;
  }
  function b(S) {
    return l = S, a = setTimeout(m, e), u ? p(S) : s;
  }
  function v(S) {
    var T = S - c, E = S - l, P = e - T;
    return d ? Yi(P, o - E) : P;
  }
  function g(S) {
    var T = S - c, E = S - l;
    return c === void 0 || T >= e || T < 0 || d && E >= o;
  }
  function m() {
    var S = Dt();
    if (g(S))
      return x(S);
    a = setTimeout(m, v(S));
  }
  function x(S) {
    return a = void 0, h && r ? p(S) : (r = i = void 0, s);
  }
  function C() {
    a !== void 0 && clearTimeout(a), l = 0, r = c = i = a = void 0;
  }
  function y() {
    return a === void 0 ? s : x(Dt());
  }
  function _() {
    var S = Dt(), T = g(S);
    if (r = arguments, i = this, c = S, T) {
      if (a === void 0)
        return b(c);
      if (d)
        return clearTimeout(a), a = setTimeout(m, e), p(c);
    }
    return a === void 0 && (a = setTimeout(m, e)), s;
  }
  return _.cancel = C, _.flush = y, _;
}
function Qi(n, e) {
  return ii(n, e);
}
var lr = {
  exports: {}
}, gt = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ji = f, eo = Symbol.for("react.element"), to = Symbol.for("react.fragment"), no = Object.prototype.hasOwnProperty, ro = Ji.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, io = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function cr(n, e, t) {
  var r, i = {}, o = null, s = null;
  t !== void 0 && (o = "" + t), e.key !== void 0 && (o = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) no.call(e, r) && !io.hasOwnProperty(r) && (i[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) i[r] === void 0 && (i[r] = e[r]);
  return {
    $$typeof: eo,
    type: n,
    key: o,
    ref: s,
    props: i,
    _owner: ro.current
  };
}
gt.Fragment = to;
gt.jsx = cr;
gt.jsxs = cr;
lr.exports = gt;
var te = lr.exports;
const {
  SvelteComponent: oo,
  assign: yn,
  binding_callbacks: wn,
  check_outros: so,
  children: ur,
  claim_element: dr,
  claim_space: ao,
  component_subscribe: Sn,
  compute_slots: lo,
  create_slot: co,
  detach: Le,
  element: fr,
  empty: xn,
  exclude_internal_props: En,
  get_all_dirty_from_scope: uo,
  get_slot_changes: fo,
  group_outros: ho,
  init: po,
  insert_hydration: st,
  safe_not_equal: mo,
  set_custom_element_data: hr,
  space: go,
  transition_in: at,
  transition_out: Yt,
  update_slot_base: vo
} = window.__gradio__svelte__internal, {
  beforeUpdate: bo,
  getContext: yo,
  onDestroy: wo,
  setContext: So
} = window.__gradio__svelte__internal;
function Cn(n) {
  let e, t;
  const r = (
    /*#slots*/
    n[7].default
  ), i = co(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = fr("svelte-slot"), i && i.c(), this.h();
    },
    l(o) {
      e = dr(o, "SVELTE-SLOT", {
        class: !0
      });
      var s = ur(e);
      i && i.l(s), s.forEach(Le), this.h();
    },
    h() {
      hr(e, "class", "svelte-1rt0kpf");
    },
    m(o, s) {
      st(o, e, s), i && i.m(e, null), n[9](e), t = !0;
    },
    p(o, s) {
      i && i.p && (!t || s & /*$$scope*/
      64) && vo(
        i,
        r,
        o,
        /*$$scope*/
        o[6],
        t ? fo(
          r,
          /*$$scope*/
          o[6],
          s,
          null
        ) : uo(
          /*$$scope*/
          o[6]
        ),
        null
      );
    },
    i(o) {
      t || (at(i, o), t = !0);
    },
    o(o) {
      Yt(i, o), t = !1;
    },
    d(o) {
      o && Le(e), i && i.d(o), n[9](null);
    }
  };
}
function xo(n) {
  let e, t, r, i, o = (
    /*$$slots*/
    n[4].default && Cn(n)
  );
  return {
    c() {
      e = fr("react-portal-target"), t = go(), o && o.c(), r = xn(), this.h();
    },
    l(s) {
      e = dr(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), ur(e).forEach(Le), t = ao(s), o && o.l(s), r = xn(), this.h();
    },
    h() {
      hr(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      st(s, e, a), n[8](e), st(s, t, a), o && o.m(s, a), st(s, r, a), i = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? o ? (o.p(s, a), a & /*$$slots*/
      16 && at(o, 1)) : (o = Cn(s), o.c(), at(o, 1), o.m(r.parentNode, r)) : o && (ho(), Yt(o, 1, 1, () => {
        o = null;
      }), so());
    },
    i(s) {
      i || (at(o), i = !0);
    },
    o(s) {
      Yt(o), i = !1;
    },
    d(s) {
      s && (Le(e), Le(t), Le(r)), n[8](null), o && o.d(s);
    }
  };
}
function _n(n) {
  const {
    svelteInit: e,
    ...t
  } = n;
  return t;
}
function Eo(n, e, t) {
  let r, i, {
    $$slots: o = {},
    $$scope: s
  } = e;
  const a = lo(o);
  let {
    svelteInit: c
  } = e;
  const l = ot(_n(e)), u = ot();
  Sn(n, u, (y) => t(0, r = y));
  const d = ot();
  Sn(n, d, (y) => t(1, i = y));
  const h = [], p = yo("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: v,
    subSlotIndex: g
  } = oi() || {}, m = c({
    parent: p,
    props: l,
    target: u,
    slot: d,
    slotKey: b,
    slotIndex: v,
    subSlotIndex: g,
    onDestroy(y) {
      h.push(y);
    }
  });
  So("$$ms-gr-react-wrapper", m), bo(() => {
    l.set(_n(e));
  }), wo(() => {
    h.forEach((y) => y());
  });
  function x(y) {
    wn[y ? "unshift" : "push"](() => {
      r = y, u.set(r);
    });
  }
  function C(y) {
    wn[y ? "unshift" : "push"](() => {
      i = y, d.set(i);
    });
  }
  return n.$$set = (y) => {
    t(17, e = yn(yn({}, e), En(y))), "svelteInit" in y && t(5, c = y.svelteInit), "$$scope" in y && t(6, s = y.$$scope);
  }, e = En(e), [r, i, u, d, a, c, s, o, x, C];
}
class Co extends oo {
  constructor(e) {
    super(), po(this, e, Eo, xo, mo, {
      svelteInit: 5
    });
  }
}
const {
  SvelteComponent: cl
} = window.__gradio__svelte__internal, Rn = window.ms_globals.rerender, kt = window.ms_globals.tree;
function _o(n, e = {}) {
  function t(r) {
    const i = ot(), o = new Co({
      ...r,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: i,
            reactComponent: n,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? kt;
          return c.nodes = [...c.nodes, a], Rn({
            createPortal: dt,
            node: kt
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== i), Rn({
              createPortal: dt,
              node: kt
            });
          }), a;
        },
        ...r.props
      }
    });
    return i.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
const Ro = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function To(n) {
  return n ? Object.keys(n).reduce((e, t) => {
    const r = n[t];
    return e[t] = Po(t, r), e;
  }, {}) : {};
}
function Po(n, e) {
  return typeof e == "number" && !Ro.includes(n) ? e + "px" : e;
}
function Zt(n) {
  const e = [], t = n.cloneNode(!1);
  if (n._reactElement) {
    const i = f.Children.toArray(n._reactElement.props.children).map((o) => {
      if (f.isValidElement(o) && o.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Zt(o.props.el);
        return f.cloneElement(o, {
          ...o.props,
          el: a,
          children: [...f.Children.toArray(o.props.children), ...s]
        });
      }
      return null;
    });
    return i.originalChildren = n._reactElement.props.children, e.push(dt(f.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: i
    }), t)), {
      clonedElement: t,
      portals: e
    };
  }
  Object.keys(n.getEventListeners()).forEach((i) => {
    n.getEventListeners(i).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      t.addEventListener(a, s, c);
    });
  });
  const r = Array.from(n.childNodes);
  for (let i = 0; i < r.length; i++) {
    const o = r[i];
    if (o.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Zt(o);
      e.push(...a), t.appendChild(s);
    } else o.nodeType === 3 && t.appendChild(o.cloneNode());
  }
  return {
    clonedElement: t,
    portals: e
  };
}
function Mo(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const Ke = Kr(({
  slot: n,
  clone: e,
  className: t,
  style: r,
  observeAttributes: i
}, o) => {
  const s = he(), [a, c] = Ie([]), {
    forceClone: l
  } = ci(), u = l ? !0 : e;
  return xe(() => {
    var v;
    if (!s.current || !n)
      return;
    let d = n;
    function h() {
      let g = d;
      if (d.tagName.toLowerCase() === "svelte-slot" && d.children.length === 1 && d.children[0] && (g = d.children[0], g.tagName.toLowerCase() === "react-portal-target" && g.children[0] && (g = g.children[0])), Mo(o, g), t && g.classList.add(...t.split(" ")), r) {
        const m = To(r);
        Object.keys(m).forEach((x) => {
          g.style[x] = m[x];
        });
      }
    }
    let p = null, b = null;
    if (u && window.MutationObserver) {
      let g = function() {
        var y, _, S;
        (y = s.current) != null && y.contains(d) && ((_ = s.current) == null || _.removeChild(d));
        const {
          portals: x,
          clonedElement: C
        } = Zt(n);
        d = C, c(x), d.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          h();
        }, 50), (S = s.current) == null || S.appendChild(d);
      };
      g();
      const m = Zi(() => {
        g(), p == null || p.disconnect(), p == null || p.observe(n, {
          childList: !0,
          subtree: !0,
          attributes: i
        });
      }, 50);
      p = new window.MutationObserver(m), p.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      d.style.display = "contents", h(), (v = s.current) == null || v.appendChild(d);
    return () => {
      var g, m;
      d.style.display = "", (g = s.current) != null && g.contains(d) && ((m = s.current) == null || m.removeChild(d)), p == null || p.disconnect();
    };
  }, [n, u, t, r, o, i, l]), f.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Oo = "1.2.0", Lo = /* @__PURE__ */ f.createContext({}), Ao = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, pr = (n) => {
  const e = f.useContext(Lo);
  return f.useMemo(() => ({
    ...Ao,
    ...e[n]
  }), [e[n]]);
};
function ge() {
  return ge = Object.assign ? Object.assign.bind() : function(n) {
    for (var e = 1; e < arguments.length; e++) {
      var t = arguments[e];
      for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]);
    }
    return n;
  }, ge.apply(null, arguments);
}
function Ue() {
  const {
    getPrefixCls: n,
    direction: e,
    csp: t,
    iconPrefixCls: r,
    theme: i
  } = f.useContext(Oi.ConfigContext);
  return {
    theme: i,
    getPrefixCls: n,
    direction: e,
    csp: t,
    iconPrefixCls: r
  };
}
function _e(n) {
  var e = R.useRef();
  e.current = n;
  var t = R.useCallback(function() {
    for (var r, i = arguments.length, o = new Array(i), s = 0; s < i; s++)
      o[s] = arguments[s];
    return (r = e.current) === null || r === void 0 ? void 0 : r.call.apply(r, [e].concat(o));
  }, []);
  return t;
}
function $o(n) {
  if (Array.isArray(n)) return n;
}
function Io(n, e) {
  var t = n == null ? null : typeof Symbol < "u" && n[Symbol.iterator] || n["@@iterator"];
  if (t != null) {
    var r, i, o, s, a = [], c = !0, l = !1;
    try {
      if (o = (t = t.call(n)).next, e !== 0) for (; !(c = (r = o.call(t)).done) && (a.push(r.value), a.length !== e); c = !0) ;
    } catch (u) {
      l = !0, i = u;
    } finally {
      try {
        if (!c && t.return != null && (s = t.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw i;
      }
    }
    return a;
  }
}
function Tn(n, e) {
  (e == null || e > n.length) && (e = n.length);
  for (var t = 0, r = Array(e); t < e; t++) r[t] = n[t];
  return r;
}
function Do(n, e) {
  if (n) {
    if (typeof n == "string") return Tn(n, e);
    var t = {}.toString.call(n).slice(8, -1);
    return t === "Object" && n.constructor && (t = n.constructor.name), t === "Map" || t === "Set" ? Array.from(n) : t === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? Tn(n, e) : void 0;
  }
}
function ko() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ht(n, e) {
  return $o(n) || Io(n, e) || Do(n, e) || ko();
}
function vt() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var Pn = vt() ? R.useLayoutEffect : R.useEffect, No = function(e, t) {
  var r = R.useRef(!0);
  Pn(function() {
    return e(r.current);
  }, t), Pn(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, Mn = function(e, t) {
  No(function(r) {
    if (!r)
      return e();
  }, t);
};
function Ve(n) {
  var e = R.useRef(!1), t = R.useState(n), r = ht(t, 2), i = r[0], o = r[1];
  R.useEffect(function() {
    return e.current = !1, function() {
      e.current = !0;
    };
  }, []);
  function s(a, c) {
    c && e.current || o(a);
  }
  return [i, s];
}
function Nt(n) {
  return n !== void 0;
}
function cn(n, e) {
  var t = e || {}, r = t.defaultValue, i = t.value, o = t.onChange, s = t.postState, a = Ve(function() {
    return Nt(i) ? i : Nt(r) ? typeof r == "function" ? r() : r : typeof n == "function" ? n() : n;
  }), c = ht(a, 2), l = c[0], u = c[1], d = i !== void 0 ? i : l, h = s ? s(d) : d, p = _e(o), b = Ve([d]), v = ht(b, 2), g = v[0], m = v[1];
  Mn(function() {
    var C = g[0];
    l !== C && p(l, C);
  }, [g]), Mn(function() {
    Nt(i) || u(i);
  }, [i]);
  var x = _e(function(C, y) {
    u(C, y), m([d], y);
  });
  return [h, x];
}
function Re(n) {
  "@babel/helpers - typeof";
  return Re = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, Re(n);
}
var mr = {
  exports: {}
}, W = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var un = Symbol.for("react.element"), dn = Symbol.for("react.portal"), bt = Symbol.for("react.fragment"), yt = Symbol.for("react.strict_mode"), wt = Symbol.for("react.profiler"), St = Symbol.for("react.provider"), xt = Symbol.for("react.context"), Fo = Symbol.for("react.server_context"), Et = Symbol.for("react.forward_ref"), Ct = Symbol.for("react.suspense"), _t = Symbol.for("react.suspense_list"), Rt = Symbol.for("react.memo"), Tt = Symbol.for("react.lazy"), jo = Symbol.for("react.offscreen"), gr;
gr = Symbol.for("react.module.reference");
function ve(n) {
  if (typeof n == "object" && n !== null) {
    var e = n.$$typeof;
    switch (e) {
      case un:
        switch (n = n.type, n) {
          case bt:
          case wt:
          case yt:
          case Ct:
          case _t:
            return n;
          default:
            switch (n = n && n.$$typeof, n) {
              case Fo:
              case xt:
              case Et:
              case Tt:
              case Rt:
              case St:
                return n;
              default:
                return e;
            }
        }
      case dn:
        return e;
    }
  }
}
W.ContextConsumer = xt;
W.ContextProvider = St;
W.Element = un;
W.ForwardRef = Et;
W.Fragment = bt;
W.Lazy = Tt;
W.Memo = Rt;
W.Portal = dn;
W.Profiler = wt;
W.StrictMode = yt;
W.Suspense = Ct;
W.SuspenseList = _t;
W.isAsyncMode = function() {
  return !1;
};
W.isConcurrentMode = function() {
  return !1;
};
W.isContextConsumer = function(n) {
  return ve(n) === xt;
};
W.isContextProvider = function(n) {
  return ve(n) === St;
};
W.isElement = function(n) {
  return typeof n == "object" && n !== null && n.$$typeof === un;
};
W.isForwardRef = function(n) {
  return ve(n) === Et;
};
W.isFragment = function(n) {
  return ve(n) === bt;
};
W.isLazy = function(n) {
  return ve(n) === Tt;
};
W.isMemo = function(n) {
  return ve(n) === Rt;
};
W.isPortal = function(n) {
  return ve(n) === dn;
};
W.isProfiler = function(n) {
  return ve(n) === wt;
};
W.isStrictMode = function(n) {
  return ve(n) === yt;
};
W.isSuspense = function(n) {
  return ve(n) === Ct;
};
W.isSuspenseList = function(n) {
  return ve(n) === _t;
};
W.isValidElementType = function(n) {
  return typeof n == "string" || typeof n == "function" || n === bt || n === wt || n === yt || n === Ct || n === _t || n === jo || typeof n == "object" && n !== null && (n.$$typeof === Tt || n.$$typeof === Rt || n.$$typeof === St || n.$$typeof === xt || n.$$typeof === Et || n.$$typeof === gr || n.getModuleId !== void 0);
};
W.typeOf = ve;
mr.exports = W;
var Ft = mr.exports, Wo = Symbol.for("react.element"), Bo = Symbol.for("react.transitional.element"), Ho = Symbol.for("react.fragment");
function zo(n) {
  return (
    // Base object type
    n && Re(n) === "object" && // React Element type
    (n.$$typeof === Wo || n.$$typeof === Bo) && // React Fragment type
    n.type === Ho
  );
}
var Uo = Number(Yr.split(".")[0]), Vo = function(e, t) {
  typeof e == "function" ? e(t) : Re(e) === "object" && e && "current" in e && (e.current = t);
}, Xo = function(e) {
  var t, r;
  if (!e)
    return !1;
  if (vr(e) && Uo >= 19)
    return !0;
  var i = Ft.isMemo(e) ? e.type.type : e.type;
  return !(typeof i == "function" && !((t = i.prototype) !== null && t !== void 0 && t.render) && i.$$typeof !== Ft.ForwardRef || typeof e == "function" && !((r = e.prototype) !== null && r !== void 0 && r.render) && e.$$typeof !== Ft.ForwardRef);
};
function vr(n) {
  return /* @__PURE__ */ Zr(n) && !zo(n);
}
var Go = function(e) {
  if (e && vr(e)) {
    var t = e;
    return t.props.propertyIsEnumerable("ref") ? t.props.ref : t.ref;
  }
  return null;
};
function qo(n, e) {
  for (var t = n, r = 0; r < e.length; r += 1) {
    if (t == null)
      return;
    t = t[e[r]];
  }
  return t;
}
function Ko(n, e) {
  if (Re(n) != "object" || !n) return n;
  var t = n[Symbol.toPrimitive];
  if (t !== void 0) {
    var r = t.call(n, e);
    if (Re(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(n);
}
function Yo(n) {
  var e = Ko(n, "string");
  return Re(e) == "symbol" ? e : e + "";
}
function Zo(n, e, t) {
  return (e = Yo(e)) in n ? Object.defineProperty(n, e, {
    value: t,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : n[e] = t, n;
}
function On(n, e) {
  var t = Object.keys(n);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(n);
    e && (r = r.filter(function(i) {
      return Object.getOwnPropertyDescriptor(n, i).enumerable;
    })), t.push.apply(t, r);
  }
  return t;
}
function Qo(n) {
  for (var e = 1; e < arguments.length; e++) {
    var t = arguments[e] != null ? arguments[e] : {};
    e % 2 ? On(Object(t), !0).forEach(function(r) {
      Zo(n, r, t[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(n, Object.getOwnPropertyDescriptors(t)) : On(Object(t)).forEach(function(r) {
      Object.defineProperty(n, r, Object.getOwnPropertyDescriptor(t, r));
    });
  }
  return n;
}
const Xe = /* @__PURE__ */ f.createContext(null);
function Ln(n) {
  const {
    getDropContainer: e,
    className: t,
    prefixCls: r,
    children: i
  } = n, {
    disabled: o
  } = f.useContext(Xe), [s, a] = f.useState(), [c, l] = f.useState(null);
  if (f.useEffect(() => {
    const h = e == null ? void 0 : e();
    s !== h && a(h);
  }, [e]), f.useEffect(() => {
    if (s) {
      const h = () => {
        l(!0);
      }, p = (g) => {
        g.preventDefault();
      }, b = (g) => {
        g.relatedTarget || l(!1);
      }, v = (g) => {
        l(!1), g.preventDefault();
      };
      return document.addEventListener("dragenter", h), document.addEventListener("dragover", p), document.addEventListener("dragleave", b), document.addEventListener("drop", v), () => {
        document.removeEventListener("dragenter", h), document.removeEventListener("dragover", p), document.removeEventListener("dragleave", b), document.removeEventListener("drop", v);
      };
    }
  }, [!!s]), !(e && s && !o))
    return null;
  const d = `${r}-drop-area`;
  return /* @__PURE__ */ dt(/* @__PURE__ */ f.createElement("div", {
    className: Z(d, t, {
      [`${d}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: c ? "block" : "none"
    }
  }, i), s);
}
function ue(n) {
  "@babel/helpers - typeof";
  return ue = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, ue(n);
}
function Jo(n, e) {
  if (ue(n) != "object" || !n) return n;
  var t = n[Symbol.toPrimitive];
  if (t !== void 0) {
    var r = t.call(n, e);
    if (ue(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(n);
}
function br(n) {
  var e = Jo(n, "string");
  return ue(e) == "symbol" ? e : e + "";
}
function I(n, e, t) {
  return (e = br(e)) in n ? Object.defineProperty(n, e, {
    value: t,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : n[e] = t, n;
}
function An(n, e) {
  var t = Object.keys(n);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(n);
    e && (r = r.filter(function(i) {
      return Object.getOwnPropertyDescriptor(n, i).enumerable;
    })), t.push.apply(t, r);
  }
  return t;
}
function $(n) {
  for (var e = 1; e < arguments.length; e++) {
    var t = arguments[e] != null ? arguments[e] : {};
    e % 2 ? An(Object(t), !0).forEach(function(r) {
      I(n, r, t[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(n, Object.getOwnPropertyDescriptors(t)) : An(Object(t)).forEach(function(r) {
      Object.defineProperty(n, r, Object.getOwnPropertyDescriptor(t, r));
    });
  }
  return n;
}
function es(n) {
  if (Array.isArray(n)) return n;
}
function ts(n, e) {
  var t = n == null ? null : typeof Symbol < "u" && n[Symbol.iterator] || n["@@iterator"];
  if (t != null) {
    var r, i, o, s, a = [], c = !0, l = !1;
    try {
      if (o = (t = t.call(n)).next, e === 0) {
        if (Object(t) !== t) return;
        c = !1;
      } else for (; !(c = (r = o.call(t)).done) && (a.push(r.value), a.length !== e); c = !0) ;
    } catch (u) {
      l = !0, i = u;
    } finally {
      try {
        if (!c && t.return != null && (s = t.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw i;
      }
    }
    return a;
  }
}
function $n(n, e) {
  (e == null || e > n.length) && (e = n.length);
  for (var t = 0, r = Array(e); t < e; t++) r[t] = n[t];
  return r;
}
function ns(n, e) {
  if (n) {
    if (typeof n == "string") return $n(n, e);
    var t = {}.toString.call(n).slice(8, -1);
    return t === "Object" && n.constructor && (t = n.constructor.name), t === "Map" || t === "Set" ? Array.from(n) : t === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? $n(n, e) : void 0;
  }
}
function rs() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function me(n, e) {
  return es(n) || ts(n, e) || ns(n, e) || rs();
}
function In(n) {
  return n instanceof HTMLElement || n instanceof SVGElement;
}
function is(n) {
  return n && Re(n) === "object" && In(n.nativeElement) ? n.nativeElement : In(n) ? n : null;
}
function os(n) {
  var e = is(n);
  if (e)
    return e;
  if (n instanceof f.Component) {
    var t;
    return (t = mn.findDOMNode) === null || t === void 0 ? void 0 : t.call(mn, n);
  }
  return null;
}
function ss(n, e) {
  if (n == null) return {};
  var t = {};
  for (var r in n) if ({}.hasOwnProperty.call(n, r)) {
    if (e.indexOf(r) !== -1) continue;
    t[r] = n[r];
  }
  return t;
}
function Dn(n, e) {
  if (n == null) return {};
  var t, r, i = ss(n, e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(n);
    for (r = 0; r < o.length; r++) t = o[r], e.indexOf(t) === -1 && {}.propertyIsEnumerable.call(n, t) && (i[t] = n[t]);
  }
  return i;
}
var as = /* @__PURE__ */ R.createContext({});
function Ne(n, e) {
  if (!(n instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function kn(n, e) {
  for (var t = 0; t < e.length; t++) {
    var r = e[t];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(n, br(r.key), r);
  }
}
function Fe(n, e, t) {
  return e && kn(n.prototype, e), t && kn(n, t), Object.defineProperty(n, "prototype", {
    writable: !1
  }), n;
}
function Qt(n, e) {
  return Qt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(t, r) {
    return t.__proto__ = r, t;
  }, Qt(n, e);
}
function Pt(n, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  n.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: n,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(n, "prototype", {
    writable: !1
  }), e && Qt(n, e);
}
function pt(n) {
  return pt = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, pt(n);
}
function yr() {
  try {
    var n = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (yr = function() {
    return !!n;
  })();
}
function Pe(n) {
  if (n === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return n;
}
function ls(n, e) {
  if (e && (ue(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return Pe(n);
}
function Mt(n) {
  var e = yr();
  return function() {
    var t, r = pt(n);
    if (e) {
      var i = pt(this).constructor;
      t = Reflect.construct(r, arguments, i);
    } else t = r.apply(this, arguments);
    return ls(this, t);
  };
}
var cs = /* @__PURE__ */ function(n) {
  Pt(t, n);
  var e = Mt(t);
  function t() {
    return Ne(this, t), e.apply(this, arguments);
  }
  return Fe(t, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), t;
}(R.Component);
function us(n) {
  var e = R.useReducer(function(a) {
    return a + 1;
  }, 0), t = ht(e, 2), r = t[1], i = R.useRef(n), o = _e(function() {
    return i.current;
  }), s = _e(function(a) {
    i.current = typeof a == "function" ? a(i.current) : a, r();
  });
  return [o, s];
}
var Ce = "none", Ye = "appear", Ze = "enter", Qe = "leave", Nn = "none", ye = "prepare", Ae = "start", $e = "active", fn = "end", wr = "prepared";
function Fn(n, e) {
  var t = {};
  return t[n.toLowerCase()] = e.toLowerCase(), t["Webkit".concat(n)] = "webkit".concat(e), t["Moz".concat(n)] = "moz".concat(e), t["ms".concat(n)] = "MS".concat(e), t["O".concat(n)] = "o".concat(e.toLowerCase()), t;
}
function ds(n, e) {
  var t = {
    animationend: Fn("Animation", "AnimationEnd"),
    transitionend: Fn("Transition", "TransitionEnd")
  };
  return n && ("AnimationEvent" in e || delete t.animationend.animation, "TransitionEvent" in e || delete t.transitionend.transition), t;
}
var fs = ds(vt(), typeof window < "u" ? window : {}), Sr = {};
if (vt()) {
  var hs = document.createElement("div");
  Sr = hs.style;
}
var Je = {};
function xr(n) {
  if (Je[n])
    return Je[n];
  var e = fs[n];
  if (e)
    for (var t = Object.keys(e), r = t.length, i = 0; i < r; i += 1) {
      var o = t[i];
      if (Object.prototype.hasOwnProperty.call(e, o) && o in Sr)
        return Je[n] = e[o], Je[n];
    }
  return "";
}
var Er = xr("animationend"), Cr = xr("transitionend"), _r = !!(Er && Cr), jn = Er || "animationend", Wn = Cr || "transitionend";
function Bn(n, e) {
  if (!n) return null;
  if (ue(n) === "object") {
    var t = e.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return n[t];
  }
  return "".concat(n, "-").concat(e);
}
const ps = function(n) {
  var e = he();
  function t(i) {
    i && (i.removeEventListener(Wn, n), i.removeEventListener(jn, n));
  }
  function r(i) {
    e.current && e.current !== i && t(e.current), i && i !== e.current && (i.addEventListener(Wn, n), i.addEventListener(jn, n), e.current = i);
  }
  return R.useEffect(function() {
    return function() {
      t(e.current);
    };
  }, []), [r, t];
};
var Rr = vt() ? Qr : xe, Tr = function(e) {
  return +setTimeout(e, 16);
}, Pr = function(e) {
  return clearTimeout(e);
};
typeof window < "u" && "requestAnimationFrame" in window && (Tr = function(e) {
  return window.requestAnimationFrame(e);
}, Pr = function(e) {
  return window.cancelAnimationFrame(e);
});
var Hn = 0, hn = /* @__PURE__ */ new Map();
function Mr(n) {
  hn.delete(n);
}
var Jt = function(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  Hn += 1;
  var r = Hn;
  function i(o) {
    if (o === 0)
      Mr(r), e();
    else {
      var s = Tr(function() {
        i(o - 1);
      });
      hn.set(r, s);
    }
  }
  return i(t), r;
};
Jt.cancel = function(n) {
  var e = hn.get(n);
  return Mr(n), Pr(e);
};
const ms = function() {
  var n = R.useRef(null);
  function e() {
    Jt.cancel(n.current);
  }
  function t(r) {
    var i = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    e();
    var o = Jt(function() {
      i <= 1 ? r({
        isCanceled: function() {
          return o !== n.current;
        }
      }) : t(r, i - 1);
    });
    n.current = o;
  }
  return R.useEffect(function() {
    return function() {
      e();
    };
  }, []), [t, e];
};
var gs = [ye, Ae, $e, fn], vs = [ye, wr], Or = !1, bs = !0;
function Lr(n) {
  return n === $e || n === fn;
}
const ys = function(n, e, t) {
  var r = Ve(Nn), i = me(r, 2), o = i[0], s = i[1], a = ms(), c = me(a, 2), l = c[0], u = c[1];
  function d() {
    s(ye, !0);
  }
  var h = e ? vs : gs;
  return Rr(function() {
    if (o !== Nn && o !== fn) {
      var p = h.indexOf(o), b = h[p + 1], v = t(o);
      v === Or ? s(b, !0) : b && l(function(g) {
        function m() {
          g.isCanceled() || s(b, !0);
        }
        v === !0 ? m() : Promise.resolve(v).then(m);
      });
    }
  }, [n, o]), R.useEffect(function() {
    return function() {
      u();
    };
  }, []), [d, o];
};
function ws(n, e, t, r) {
  var i = r.motionEnter, o = i === void 0 ? !0 : i, s = r.motionAppear, a = s === void 0 ? !0 : s, c = r.motionLeave, l = c === void 0 ? !0 : c, u = r.motionDeadline, d = r.motionLeaveImmediately, h = r.onAppearPrepare, p = r.onEnterPrepare, b = r.onLeavePrepare, v = r.onAppearStart, g = r.onEnterStart, m = r.onLeaveStart, x = r.onAppearActive, C = r.onEnterActive, y = r.onLeaveActive, _ = r.onAppearEnd, S = r.onEnterEnd, T = r.onLeaveEnd, E = r.onVisibleChanged, P = Ve(), O = me(P, 2), D = O[0], k = O[1], N = us(Ce), F = me(N, 2), L = F[0], M = F[1], z = Ve(null), w = me(z, 2), ce = w[0], de = w[1], U = L(), B = he(!1), Q = he(null);
  function V() {
    return t();
  }
  var J = he(!1);
  function oe() {
    M(Ce), de(null, !0);
  }
  var j = _e(function(se) {
    var ee = L();
    if (ee !== Ce) {
      var ae = V();
      if (!(se && !se.deadline && se.target !== ae)) {
        var Me = J.current, Te;
        ee === Ye && Me ? Te = _ == null ? void 0 : _(ae, se) : ee === Ze && Me ? Te = S == null ? void 0 : S(ae, se) : ee === Qe && Me && (Te = T == null ? void 0 : T(ae, se)), Me && Te !== !1 && oe();
      }
    }
  }), A = ps(j), H = me(A, 1), re = H[0], q = function(ee) {
    switch (ee) {
      case Ye:
        return I(I(I({}, ye, h), Ae, v), $e, x);
      case Ze:
        return I(I(I({}, ye, p), Ae, g), $e, C);
      case Qe:
        return I(I(I({}, ye, b), Ae, m), $e, y);
      default:
        return {};
    }
  }, X = R.useMemo(function() {
    return q(U);
  }, [U]), pe = ys(U, !n, function(se) {
    if (se === ye) {
      var ee = X[ye];
      return ee ? ee(V()) : Or;
    }
    if (ie in X) {
      var ae;
      de(((ae = X[ie]) === null || ae === void 0 ? void 0 : ae.call(X, V(), null)) || null);
    }
    return ie === $e && U !== Ce && (re(V()), u > 0 && (clearTimeout(Q.current), Q.current = setTimeout(function() {
      j({
        deadline: !0
      });
    }, u))), ie === wr && oe(), bs;
  }), fe = me(pe, 2), G = fe[0], ie = fe[1], be = Lr(ie);
  J.current = be;
  var K = he(null);
  Rr(function() {
    if (!(B.current && K.current === e)) {
      k(e);
      var se = B.current;
      B.current = !0;
      var ee;
      !se && e && a && (ee = Ye), se && e && o && (ee = Ze), (se && !e && l || !se && d && !e && l) && (ee = Qe);
      var ae = q(ee);
      ee && (n || ae[ye]) ? (M(ee), G()) : M(Ce), K.current = e;
    }
  }, [e]), xe(function() {
    // Cancel appear
    (U === Ye && !a || // Cancel enter
    U === Ze && !o || // Cancel leave
    U === Qe && !l) && M(Ce);
  }, [a, o, l]), xe(function() {
    return function() {
      B.current = !1, clearTimeout(Q.current);
    };
  }, []);
  var we = R.useRef(!1);
  xe(function() {
    D && (we.current = !0), D !== void 0 && U === Ce && ((we.current || D) && (E == null || E(D)), we.current = !0);
  }, [D, U]);
  var Ee = ce;
  return X[ye] && ie === Ae && (Ee = $({
    transition: "none"
  }, Ee)), [U, ie, Ee, D ?? e];
}
function Ss(n) {
  var e = n;
  ue(n) === "object" && (e = n.transitionSupport);
  function t(i, o) {
    return !!(i.motionName && e && o !== !1);
  }
  var r = /* @__PURE__ */ R.forwardRef(function(i, o) {
    var s = i.visible, a = s === void 0 ? !0 : s, c = i.removeOnLeave, l = c === void 0 ? !0 : c, u = i.forceRender, d = i.children, h = i.motionName, p = i.leavedClassName, b = i.eventProps, v = R.useContext(as), g = v.motion, m = t(i, g), x = he(), C = he();
    function y() {
      try {
        return x.current instanceof HTMLElement ? x.current : os(C.current);
      } catch {
        return null;
      }
    }
    var _ = ws(m, a, y, i), S = me(_, 4), T = S[0], E = S[1], P = S[2], O = S[3], D = R.useRef(O);
    O && (D.current = !0);
    var k = R.useCallback(function(w) {
      x.current = w, Vo(o, w);
    }, [o]), N, F = $($({}, b), {}, {
      visible: a
    });
    if (!d)
      N = null;
    else if (T === Ce)
      O ? N = d($({}, F), k) : !l && D.current && p ? N = d($($({}, F), {}, {
        className: p
      }), k) : u || !l && !p ? N = d($($({}, F), {}, {
        style: {
          display: "none"
        }
      }), k) : N = null;
    else {
      var L;
      E === ye ? L = "prepare" : Lr(E) ? L = "active" : E === Ae && (L = "start");
      var M = Bn(h, "".concat(T, "-").concat(L));
      N = d($($({}, F), {}, {
        className: Z(Bn(h, T), I(I({}, M, M && L), h, typeof h == "string")),
        style: P
      }), k);
    }
    if (/* @__PURE__ */ R.isValidElement(N) && Xo(N)) {
      var z = Go(N);
      z || (N = /* @__PURE__ */ R.cloneElement(N, {
        ref: k
      }));
    }
    return /* @__PURE__ */ R.createElement(cs, {
      ref: C
    }, N);
  });
  return r.displayName = "CSSMotion", r;
}
const Ar = Ss(_r);
var en = "add", tn = "keep", nn = "remove", jt = "removed";
function xs(n) {
  var e;
  return n && ue(n) === "object" && "key" in n ? e = n : e = {
    key: n
  }, $($({}, e), {}, {
    key: String(e.key)
  });
}
function rn() {
  var n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return n.map(xs);
}
function Es() {
  var n = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], t = [], r = 0, i = e.length, o = rn(n), s = rn(e);
  o.forEach(function(l) {
    for (var u = !1, d = r; d < i; d += 1) {
      var h = s[d];
      if (h.key === l.key) {
        r < d && (t = t.concat(s.slice(r, d).map(function(p) {
          return $($({}, p), {}, {
            status: en
          });
        })), r = d), t.push($($({}, h), {}, {
          status: tn
        })), r += 1, u = !0;
        break;
      }
    }
    u || t.push($($({}, l), {}, {
      status: nn
    }));
  }), r < i && (t = t.concat(s.slice(r).map(function(l) {
    return $($({}, l), {}, {
      status: en
    });
  })));
  var a = {};
  t.forEach(function(l) {
    var u = l.key;
    a[u] = (a[u] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(l) {
    return a[l] > 1;
  });
  return c.forEach(function(l) {
    t = t.filter(function(u) {
      var d = u.key, h = u.status;
      return d !== l || h !== nn;
    }), t.forEach(function(u) {
      u.key === l && (u.status = tn);
    });
  }), t;
}
var Cs = ["component", "children", "onVisibleChanged", "onAllRemoved"], _s = ["status"], Rs = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function Ts(n) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Ar, t = /* @__PURE__ */ function(r) {
    Pt(o, r);
    var i = Mt(o);
    function o() {
      var s;
      Ne(this, o);
      for (var a = arguments.length, c = new Array(a), l = 0; l < a; l++)
        c[l] = arguments[l];
      return s = i.call.apply(i, [this].concat(c)), I(Pe(s), "state", {
        keyEntities: []
      }), I(Pe(s), "removeKey", function(u) {
        s.setState(function(d) {
          var h = d.keyEntities.map(function(p) {
            return p.key !== u ? p : $($({}, p), {}, {
              status: jt
            });
          });
          return {
            keyEntities: h
          };
        }, function() {
          var d = s.state.keyEntities, h = d.filter(function(p) {
            var b = p.status;
            return b !== jt;
          }).length;
          h === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Fe(o, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, l = this.props, u = l.component, d = l.children, h = l.onVisibleChanged;
        l.onAllRemoved;
        var p = Dn(l, Cs), b = u || R.Fragment, v = {};
        return Rs.forEach(function(g) {
          v[g] = p[g], delete p[g];
        }), delete p.keys, /* @__PURE__ */ R.createElement(b, p, c.map(function(g, m) {
          var x = g.status, C = Dn(g, _s), y = x === en || x === tn;
          return /* @__PURE__ */ R.createElement(e, ge({}, v, {
            key: C.key,
            visible: y,
            eventProps: C,
            onVisibleChanged: function(S) {
              h == null || h(S, {
                key: C.key
              }), S || a.removeKey(C.key);
            }
          }), function(_, S) {
            return d($($({}, _), {}, {
              index: m
            }), S);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var l = a.keys, u = c.keyEntities, d = rn(l), h = Es(u, d);
        return {
          keyEntities: h.filter(function(p) {
            var b = u.find(function(v) {
              var g = v.key;
              return p.key === g;
            });
            return !(b && b.status === jt && p.status === nn);
          })
        };
      }
    }]), o;
  }(R.Component);
  return I(t, "defaultProps", {
    component: "div"
  }), t;
}
const Ps = Ts(_r);
function Ms(n, e) {
  const {
    children: t,
    upload: r,
    rootClassName: i
  } = n, o = f.useRef(null);
  return f.useImperativeHandle(e, () => o.current), /* @__PURE__ */ f.createElement(sr, ge({}, r, {
    showUploadList: !1,
    rootClassName: i,
    ref: o
  }), t);
}
const $r = /* @__PURE__ */ f.forwardRef(Ms);
var Ir = /* @__PURE__ */ Fe(function n() {
  Ne(this, n);
}), Dr = "CALC_UNIT", Os = new RegExp(Dr, "g");
function Wt(n) {
  return typeof n == "number" ? "".concat(n).concat(Dr) : n;
}
var Ls = /* @__PURE__ */ function(n) {
  Pt(t, n);
  var e = Mt(t);
  function t(r, i) {
    var o;
    Ne(this, t), o = e.call(this), I(Pe(o), "result", ""), I(Pe(o), "unitlessCssVar", void 0), I(Pe(o), "lowPriority", void 0);
    var s = ue(r);
    return o.unitlessCssVar = i, r instanceof t ? o.result = "(".concat(r.result, ")") : s === "number" ? o.result = Wt(r) : s === "string" && (o.result = r), o;
  }
  return Fe(t, [{
    key: "add",
    value: function(i) {
      return i instanceof t ? this.result = "".concat(this.result, " + ").concat(i.getResult()) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " + ").concat(Wt(i))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(i) {
      return i instanceof t ? this.result = "".concat(this.result, " - ").concat(i.getResult()) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " - ").concat(Wt(i))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(i) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), i instanceof t ? this.result = "".concat(this.result, " * ").concat(i.getResult(!0)) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " * ").concat(i)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(i) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), i instanceof t ? this.result = "".concat(this.result, " / ").concat(i.getResult(!0)) : (typeof i == "number" || typeof i == "string") && (this.result = "".concat(this.result, " / ").concat(i)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(i) {
      return this.lowPriority || i ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(i) {
      var o = this, s = i || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(l) {
        return o.result.includes(l);
      }) && (c = !1), this.result = this.result.replace(Os, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), t;
}(Ir), As = /* @__PURE__ */ function(n) {
  Pt(t, n);
  var e = Mt(t);
  function t(r) {
    var i;
    return Ne(this, t), i = e.call(this), I(Pe(i), "result", 0), r instanceof t ? i.result = r.result : typeof r == "number" && (i.result = r), i;
  }
  return Fe(t, [{
    key: "add",
    value: function(i) {
      return i instanceof t ? this.result += i.result : typeof i == "number" && (this.result += i), this;
    }
  }, {
    key: "sub",
    value: function(i) {
      return i instanceof t ? this.result -= i.result : typeof i == "number" && (this.result -= i), this;
    }
  }, {
    key: "mul",
    value: function(i) {
      return i instanceof t ? this.result *= i.result : typeof i == "number" && (this.result *= i), this;
    }
  }, {
    key: "div",
    value: function(i) {
      return i instanceof t ? this.result /= i.result : typeof i == "number" && (this.result /= i), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), t;
}(Ir), $s = function(e, t) {
  var r = e === "css" ? Ls : As;
  return function(i) {
    return new r(i, t);
  };
}, zn = function(e, t) {
  return "".concat([t, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function Un(n, e, t, r) {
  var i = $({}, e[n]);
  if (r != null && r.deprecatedTokens) {
    var o = r.deprecatedTokens;
    o.forEach(function(a) {
      var c = me(a, 2), l = c[0], u = c[1];
      if (i != null && i[l] || i != null && i[u]) {
        var d;
        (d = i[u]) !== null && d !== void 0 || (i[u] = i == null ? void 0 : i[l]);
      }
    });
  }
  var s = $($({}, t), i);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var kr = typeof CSSINJS_STATISTIC < "u", on = !0;
function Ot() {
  for (var n = arguments.length, e = new Array(n), t = 0; t < n; t++)
    e[t] = arguments[t];
  if (!kr)
    return Object.assign.apply(Object, [{}].concat(e));
  on = !1;
  var r = {};
  return e.forEach(function(i) {
    if (ue(i) === "object") {
      var o = Object.keys(i);
      o.forEach(function(s) {
        Object.defineProperty(r, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return i[s];
          }
        });
      });
    }
  }), on = !0, r;
}
var Vn = {};
function Is() {
}
var Ds = function(e) {
  var t, r = e, i = Is;
  return kr && typeof Proxy < "u" && (t = /* @__PURE__ */ new Set(), r = new Proxy(e, {
    get: function(s, a) {
      if (on) {
        var c;
        (c = t) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), i = function(s, a) {
    var c;
    Vn[s] = {
      global: Array.from(t),
      component: $($({}, (c = Vn[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: r,
    keys: t,
    flush: i
  };
};
function Xn(n, e, t) {
  if (typeof t == "function") {
    var r;
    return t(Ot(e, (r = e[n]) !== null && r !== void 0 ? r : {}));
  }
  return t ?? {};
}
function ks(n) {
  return n === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var t = arguments.length, r = new Array(t), i = 0; i < t; i++)
        r[i] = arguments[i];
      return "max(".concat(r.map(function(o) {
        return Kt(o);
      }).join(","), ")");
    },
    min: function() {
      for (var t = arguments.length, r = new Array(t), i = 0; i < t; i++)
        r[i] = arguments[i];
      return "min(".concat(r.map(function(o) {
        return Kt(o);
      }).join(","), ")");
    }
  };
}
var Ns = 1e3 * 60 * 10, Fs = /* @__PURE__ */ function() {
  function n() {
    Ne(this, n), I(this, "map", /* @__PURE__ */ new Map()), I(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), I(this, "nextID", 0), I(this, "lastAccessBeat", /* @__PURE__ */ new Map()), I(this, "accessBeat", 0);
  }
  return Fe(n, [{
    key: "set",
    value: function(t, r) {
      this.clear();
      var i = this.getCompositeKey(t);
      this.map.set(i, r), this.lastAccessBeat.set(i, Date.now());
    }
  }, {
    key: "get",
    value: function(t) {
      var r = this.getCompositeKey(t), i = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, i;
    }
  }, {
    key: "getCompositeKey",
    value: function(t) {
      var r = this, i = t.map(function(o) {
        return o && ue(o) === "object" ? "obj_".concat(r.getObjectID(o)) : "".concat(ue(o), "_").concat(o);
      });
      return i.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(t) {
      if (this.objectIDMap.has(t))
        return this.objectIDMap.get(t);
      var r = this.nextID;
      return this.objectIDMap.set(t, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var t = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(i, o) {
          r - i > Ns && (t.map.delete(o), t.lastAccessBeat.delete(o));
        }), this.accessBeat = 0;
      }
    }
  }]), n;
}(), Gn = new Fs();
function js(n, e) {
  return f.useMemo(function() {
    var t = Gn.get(e);
    if (t)
      return t;
    var r = n();
    return Gn.set(e, r), r;
  }, e);
}
var Ws = function() {
  return {};
};
function Bs(n) {
  var e = n.useCSP, t = e === void 0 ? Ws : e, r = n.useToken, i = n.usePrefix, o = n.getResetStyles, s = n.getCommonStyle, a = n.getCompUnitless;
  function c(h, p, b, v) {
    var g = Array.isArray(h) ? h[0] : h;
    function m(E) {
      return "".concat(String(g)).concat(E.slice(0, 1).toUpperCase()).concat(E.slice(1));
    }
    var x = (v == null ? void 0 : v.unitless) || {}, C = typeof a == "function" ? a(h) : {}, y = $($({}, C), {}, I({}, m("zIndexPopup"), !0));
    Object.keys(x).forEach(function(E) {
      y[m(E)] = x[E];
    });
    var _ = $($({}, v), {}, {
      unitless: y,
      prefixToken: m
    }), S = u(h, p, b, _), T = l(g, b, _);
    return function(E) {
      var P = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : E, O = S(E, P), D = me(O, 2), k = D[1], N = T(P), F = me(N, 2), L = F[0], M = F[1];
      return [L, k, M];
    };
  }
  function l(h, p, b) {
    var v = b.unitless, g = b.injectStyle, m = g === void 0 ? !0 : g, x = b.prefixToken, C = b.ignore, y = function(T) {
      var E = T.rootCls, P = T.cssVar, O = P === void 0 ? {} : P, D = r(), k = D.realToken;
      return ki({
        path: [h],
        prefix: O.prefix,
        key: O.key,
        unitless: v,
        ignore: C,
        token: k,
        scope: E
      }, function() {
        var N = Xn(h, k, p), F = Un(h, k, N, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(N).forEach(function(L) {
          F[x(L)] = F[L], delete F[L];
        }), F;
      }), null;
    }, _ = function(T) {
      var E = r(), P = E.cssVar;
      return [function(O) {
        return m && P ? /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement(y, {
          rootCls: T,
          cssVar: P,
          component: h
        }), O) : O;
      }, P == null ? void 0 : P.key];
    };
    return _;
  }
  function u(h, p, b) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(h) ? h : [h, h], m = me(g, 1), x = m[0], C = g.join("-"), y = n.layer || {
      name: "antd"
    };
    return function(_) {
      var S = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : _, T = r(), E = T.theme, P = T.realToken, O = T.hashId, D = T.token, k = T.cssVar, N = i(), F = N.rootPrefixCls, L = N.iconPrefixCls, M = t(), z = k ? "css" : "js", w = js(function() {
        var V = /* @__PURE__ */ new Set();
        return k && Object.keys(v.unitless || {}).forEach(function(J) {
          V.add(It(J, k.prefix)), V.add(It(J, zn(x, k.prefix)));
        }), $s(z, V);
      }, [z, x, k == null ? void 0 : k.prefix]), ce = ks(z), de = ce.max, U = ce.min, B = {
        theme: E,
        token: D,
        hashId: O,
        nonce: function() {
          return M.nonce;
        },
        clientOnly: v.clientOnly,
        layer: y,
        // antd is always at top of styles
        order: v.order || -999
      };
      typeof o == "function" && gn($($({}, B), {}, {
        clientOnly: !1,
        path: ["Shared", F]
      }), function() {
        return o(D, {
          prefix: {
            rootPrefixCls: F,
            iconPrefixCls: L
          },
          csp: M
        });
      });
      var Q = gn($($({}, B), {}, {
        path: [C, _, L]
      }), function() {
        if (v.injectStyle === !1)
          return [];
        var V = Ds(D), J = V.token, oe = V.flush, j = Xn(x, P, b), A = ".".concat(_), H = Un(x, P, j, {
          deprecatedTokens: v.deprecatedTokens
        });
        k && j && ue(j) === "object" && Object.keys(j).forEach(function(pe) {
          j[pe] = "var(".concat(It(pe, zn(x, k.prefix)), ")");
        });
        var re = Ot(J, {
          componentCls: A,
          prefixCls: _,
          iconCls: ".".concat(L),
          antCls: ".".concat(F),
          calc: w,
          // @ts-ignore
          max: de,
          // @ts-ignore
          min: U
        }, k ? j : H), q = p(re, {
          hashId: O,
          prefixCls: _,
          rootPrefixCls: F,
          iconPrefixCls: L
        });
        oe(x, H);
        var X = typeof s == "function" ? s(re, _, S, v.resetFont) : null;
        return [v.resetStyle === !1 ? null : X, q];
      });
      return [Q, O];
    };
  }
  function d(h, p, b) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = u(h, p, b, $({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, v)), m = function(C) {
      var y = C.prefixCls, _ = C.rootCls, S = _ === void 0 ? y : _;
      return g(y, S), null;
    };
    return m;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: d,
    genComponentStyleHook: u
  };
}
const ne = Math.round;
function Bt(n, e) {
  const t = n.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = t.map((i) => parseFloat(i));
  for (let i = 0; i < 3; i += 1)
    r[i] = e(r[i] || 0, t[i] || "", i);
  return t[3] ? r[3] = t[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const qn = (n, e, t) => t === 0 ? n : n / 100;
function We(n, e) {
  const t = e || 255;
  return n > t ? t : n < 0 ? 0 : n;
}
class Se {
  constructor(e) {
    I(this, "isValid", !0), I(this, "r", 0), I(this, "g", 0), I(this, "b", 0), I(this, "a", 1), I(this, "_h", void 0), I(this, "_s", void 0), I(this, "_l", void 0), I(this, "_v", void 0), I(this, "_max", void 0), I(this, "_min", void 0), I(this, "_brightness", void 0);
    function t(r) {
      return r[0] in e && r[1] in e && r[2] in e;
    }
    if (e) if (typeof e == "string") {
      let i = function(o) {
        return r.startsWith(o);
      };
      const r = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : i("rgb") ? this.fromRgbString(r) : i("hsl") ? this.fromHslString(r) : (i("hsv") || i("hsb")) && this.fromHsvString(r);
    } else if (e instanceof Se)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (t("rgb"))
      this.r = We(e.r), this.g = We(e.g), this.b = We(e.b), this.a = typeof e.a == "number" ? We(e.a, 1) : 1;
    else if (t("hsl"))
      this.fromHsl(e);
    else if (t("hsv"))
      this.fromHsv(e);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(e));
  }
  // ======================= Setter =======================
  setR(e) {
    return this._sc("r", e);
  }
  setG(e) {
    return this._sc("g", e);
  }
  setB(e) {
    return this._sc("b", e);
  }
  setA(e) {
    return this._sc("a", e, 1);
  }
  setHue(e) {
    const t = this.toHsv();
    return t.h = e, this._c(t);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function e(o) {
      const s = o / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const t = e(this.r), r = e(this.g), i = e(this.b);
    return 0.2126 * t + 0.7152 * r + 0.0722 * i;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = ne(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._s = 0 : this._s = e / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(e = 10) {
    const t = this.getHue(), r = this.getSaturation();
    let i = this.getLightness() - e / 100;
    return i < 0 && (i = 0), this._c({
      h: t,
      s: r,
      l: i,
      a: this.a
    });
  }
  lighten(e = 10) {
    const t = this.getHue(), r = this.getSaturation();
    let i = this.getLightness() + e / 100;
    return i > 1 && (i = 1), this._c({
      h: t,
      s: r,
      l: i,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(e, t = 50) {
    const r = this._c(e), i = t / 100, o = (a) => (r[a] - this[a]) * i + this[a], s = {
      r: ne(o("r")),
      g: ne(o("g")),
      b: ne(o("b")),
      a: ne(o("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(e = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, e);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(e = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, e);
  }
  onBackground(e) {
    const t = this._c(e), r = this.a + t.a * (1 - this.a), i = (o) => ne((this[o] * this.a + t[o] * t.a * (1 - this.a)) / r);
    return this._c({
      r: i("r"),
      g: i("g"),
      b: i("b"),
      a: r
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(e) {
    return this.r === e.r && this.g === e.g && this.b === e.b && this.a === e.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let e = "#";
    const t = (this.r || 0).toString(16);
    e += t.length === 2 ? t : "0" + t;
    const r = (this.g || 0).toString(16);
    e += r.length === 2 ? r : "0" + r;
    const i = (this.b || 0).toString(16);
    if (e += i.length === 2 ? i : "0" + i, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const o = ne(this.a * 255).toString(16);
      e += o.length === 2 ? o : "0" + o;
    }
    return e;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const e = this.getHue(), t = ne(this.getSaturation() * 100), r = ne(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${e},${t}%,${r}%,${this.a})` : `hsl(${e},${t}%,${r}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(e, t, r) {
    const i = this.clone();
    return i[e] = We(t, r), i;
  }
  _c(e) {
    return new this.constructor(e);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(e) {
    const t = e.replace("#", "");
    function r(i, o) {
      return parseInt(t[i] + t[o || i], 16);
    }
    t.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = t[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = t[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: e,
    s: t,
    l: r,
    a: i
  }) {
    if (this._h = e % 360, this._s = t, this._l = r, this.a = typeof i == "number" ? i : 1, t <= 0) {
      const h = ne(r * 255);
      this.r = h, this.g = h, this.b = h;
    }
    let o = 0, s = 0, a = 0;
    const c = e / 60, l = (1 - Math.abs(2 * r - 1)) * t, u = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (o = l, s = u) : c >= 1 && c < 2 ? (o = u, s = l) : c >= 2 && c < 3 ? (s = l, a = u) : c >= 3 && c < 4 ? (s = u, a = l) : c >= 4 && c < 5 ? (o = u, a = l) : c >= 5 && c < 6 && (o = l, a = u);
    const d = r - l / 2;
    this.r = ne((o + d) * 255), this.g = ne((s + d) * 255), this.b = ne((a + d) * 255);
  }
  fromHsv({
    h: e,
    s: t,
    v: r,
    a: i
  }) {
    this._h = e % 360, this._s = t, this._v = r, this.a = typeof i == "number" ? i : 1;
    const o = ne(r * 255);
    if (this.r = o, this.g = o, this.b = o, t <= 0)
      return;
    const s = e / 60, a = Math.floor(s), c = s - a, l = ne(r * (1 - t) * 255), u = ne(r * (1 - t * c) * 255), d = ne(r * (1 - t * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = d, this.b = l;
        break;
      case 1:
        this.r = u, this.b = l;
        break;
      case 2:
        this.r = l, this.b = d;
        break;
      case 3:
        this.r = l, this.g = u;
        break;
      case 4:
        this.r = d, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = u;
        break;
    }
  }
  fromHsvString(e) {
    const t = Bt(e, qn);
    this.fromHsv({
      h: t[0],
      s: t[1],
      v: t[2],
      a: t[3]
    });
  }
  fromHslString(e) {
    const t = Bt(e, qn);
    this.fromHsl({
      h: t[0],
      s: t[1],
      l: t[2],
      a: t[3]
    });
  }
  fromRgbString(e) {
    const t = Bt(e, (r, i) => (
      // Convert percentage to number. e.g. 50% -> 128
      i.includes("%") ? ne(r / 100 * 255) : r
    ));
    this.r = t[0], this.g = t[1], this.b = t[2], this.a = t[3];
  }
}
const Hs = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, zs = Object.assign(Object.assign({}, Hs), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function Ht(n) {
  return n >= 0 && n <= 255;
}
function et(n, e) {
  const {
    r: t,
    g: r,
    b: i,
    a: o
  } = new Se(n).toRgb();
  if (o < 1)
    return n;
  const {
    r: s,
    g: a,
    b: c
  } = new Se(e).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const u = Math.round((t - s * (1 - l)) / l), d = Math.round((r - a * (1 - l)) / l), h = Math.round((i - c * (1 - l)) / l);
    if (Ht(u) && Ht(d) && Ht(h))
      return new Se({
        r: u,
        g: d,
        b: h,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new Se({
    r: t,
    g: r,
    b: i,
    a: 1
  }).toRgbString();
}
var Us = function(n, e) {
  var t = {};
  for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && e.indexOf(r) < 0 && (t[r] = n[r]);
  if (n != null && typeof Object.getOwnPropertySymbols == "function") for (var i = 0, r = Object.getOwnPropertySymbols(n); i < r.length; i++)
    e.indexOf(r[i]) < 0 && Object.prototype.propertyIsEnumerable.call(n, r[i]) && (t[r[i]] = n[r[i]]);
  return t;
};
function Vs(n) {
  const {
    override: e
  } = n, t = Us(n, ["override"]), r = Object.assign({}, e);
  Object.keys(zs).forEach((h) => {
    delete r[h];
  });
  const i = Object.assign(Object.assign({}, t), r), o = 480, s = 576, a = 768, c = 992, l = 1200, u = 1600;
  if (i.motion === !1) {
    const h = "0s";
    i.motionDurationFast = h, i.motionDurationMid = h, i.motionDurationSlow = h;
  }
  return Object.assign(Object.assign(Object.assign({}, i), {
    // ============== Background ============== //
    colorFillContent: i.colorFillSecondary,
    colorFillContentHover: i.colorFill,
    colorFillAlter: i.colorFillQuaternary,
    colorBgContainerDisabled: i.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: i.colorBgContainer,
    colorSplit: et(i.colorBorderSecondary, i.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: i.colorTextQuaternary,
    colorTextDisabled: i.colorTextQuaternary,
    colorTextHeading: i.colorText,
    colorTextLabel: i.colorTextSecondary,
    colorTextDescription: i.colorTextTertiary,
    colorTextLightSolid: i.colorWhite,
    colorHighlight: i.colorError,
    colorBgTextHover: i.colorFillSecondary,
    colorBgTextActive: i.colorFill,
    colorIcon: i.colorTextTertiary,
    colorIconHover: i.colorText,
    colorErrorOutline: et(i.colorErrorBg, i.colorBgContainer),
    colorWarningOutline: et(i.colorWarningBg, i.colorBgContainer),
    // Font
    fontSizeIcon: i.fontSizeSM,
    // Line
    lineWidthFocus: i.lineWidth * 3,
    // Control
    lineWidth: i.lineWidth,
    controlOutlineWidth: i.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: i.controlHeight / 2,
    controlItemBgHover: i.colorFillTertiary,
    controlItemBgActive: i.colorPrimaryBg,
    controlItemBgActiveHover: i.colorPrimaryBgHover,
    controlItemBgActiveDisabled: i.colorFill,
    controlTmpOutline: i.colorFillQuaternary,
    controlOutline: et(i.colorPrimaryBg, i.colorBgContainer),
    lineType: i.lineType,
    borderRadius: i.borderRadius,
    borderRadiusXS: i.borderRadiusXS,
    borderRadiusSM: i.borderRadiusSM,
    borderRadiusLG: i.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: i.sizeXXS,
    paddingXS: i.sizeXS,
    paddingSM: i.sizeSM,
    padding: i.size,
    paddingMD: i.sizeMD,
    paddingLG: i.sizeLG,
    paddingXL: i.sizeXL,
    paddingContentHorizontalLG: i.sizeLG,
    paddingContentVerticalLG: i.sizeMS,
    paddingContentHorizontal: i.sizeMS,
    paddingContentVertical: i.sizeSM,
    paddingContentHorizontalSM: i.size,
    paddingContentVerticalSM: i.sizeXS,
    marginXXS: i.sizeXXS,
    marginXS: i.sizeXS,
    marginSM: i.sizeSM,
    margin: i.size,
    marginMD: i.sizeMD,
    marginLG: i.sizeLG,
    marginXL: i.sizeXL,
    marginXXL: i.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: o,
    screenXSMin: o,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: l - 1,
    screenXL: l,
    screenXLMin: l,
    screenXLMax: u - 1,
    screenXXL: u,
    screenXXLMin: u,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new Se("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new Se("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new Se("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), r);
}
const Xs = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, Gs = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, qs = Ni(ft.defaultAlgorithm), Ks = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, Nr = (n, e, t) => {
  const r = t.getDerivativeToken(n), {
    override: i,
    ...o
  } = e;
  let s = {
    ...r,
    override: i
  };
  return s = Vs(s), o && Object.entries(o).forEach(([a, c]) => {
    const {
      theme: l,
      ...u
    } = c;
    let d = u;
    l && (d = Nr({
      ...s,
      ...u
    }, {
      override: u
    }, l)), s[a] = d;
  }), s;
};
function Ys() {
  const {
    token: n,
    hashed: e,
    theme: t = qs,
    override: r,
    cssVar: i
  } = f.useContext(ft._internalContext), [o, s, a] = Fi(t, [ft.defaultSeed, n], {
    salt: `${Oo}-${e || ""}`,
    override: r,
    getComputedToken: Nr,
    cssVar: i && {
      prefix: i.prefix,
      key: i.key,
      unitless: Xs,
      ignore: Gs,
      preserve: Ks
    }
  });
  return [t, a, e ? s : "", o, i];
}
const {
  genStyleHooks: Fr
} = Bs({
  usePrefix: () => {
    const {
      getPrefixCls: n,
      iconPrefixCls: e
    } = Ue();
    return {
      iconPrefixCls: e,
      rootPrefixCls: n()
    };
  },
  useToken: () => {
    const [n, e, t, r, i] = Ys();
    return {
      theme: n,
      realToken: e,
      hashId: t,
      token: r,
      cssVar: i
    };
  },
  useCSP: () => {
    const {
      csp: n
    } = Ue();
    return n ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), Zs = (n) => {
  const {
    componentCls: e,
    antCls: t,
    calc: r
  } = n, i = `${e}-list-card`, o = r(n.fontSize).mul(n.lineHeight).mul(2).add(n.paddingSM).add(n.paddingSM).equal();
  return {
    [i]: {
      borderRadius: n.borderRadius,
      position: "relative",
      background: n.colorFillContent,
      borderWidth: n.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${i}-name,${i}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${i}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${i}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: r(n.paddingSM).sub(n.lineWidth).equal(),
        paddingInlineStart: r(n.padding).add(n.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: n.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${i}-icon`]: {
          fontSize: r(n.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: r(n.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${i}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${i}-desc`]: {
          color: n.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: o,
        height: o,
        lineHeight: 1,
        display: "flex",
        alignItems: "center",
        [`&:not(${i}-status-error)`]: {
          border: 0
        },
        // Img
        [`${t}-image`]: {
          width: "100%",
          height: "100%",
          borderRadius: "inherit",
          img: {
            height: "100%",
            objectFit: "cover",
            borderRadius: "inherit"
          }
        },
        // Mask
        [`${i}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${n.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${i}-status-error`]: {
          [`img, ${i}-img-mask`]: {
            borderRadius: r(n.borderRadius).sub(n.lineWidth).equal()
          },
          [`${i}-desc`]: {
            paddingInline: n.paddingXXS
          }
        },
        // Progress
        [`${i}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${i}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: n.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: n.fontSize,
        cursor: "pointer",
        opacity: n.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: n.opacityLoading
        }
      },
      [`&:hover ${i}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: n.colorError,
        [`${i}-desc`]: {
          color: n.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((s) => `${s} ${n.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: r(n.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, sn = {
  "&, *": {
    boxSizing: "border-box"
  }
}, Qs = (n) => {
  const {
    componentCls: e,
    calc: t,
    antCls: r
  } = n, i = `${e}-drop-area`, o = `${e}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [i]: {
      position: "absolute",
      inset: 0,
      zIndex: n.zIndexPopupBase,
      ...sn,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${o}-inner`]: {
          display: "none"
        }
      },
      [o]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [o]: {
        height: "100%",
        borderRadius: n.borderRadius,
        borderWidth: n.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: n.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: n.colorBgPlaceholderHover,
        ...sn,
        [`${r}-upload-wrapper ${r}-upload${r}-upload-btn`]: {
          padding: 0
        },
        [`&${o}-drag-in`]: {
          borderColor: n.colorPrimaryHover
        },
        [`&${o}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${o}-inner`]: {
          gap: t(n.paddingXXS).div(2).equal()
        },
        [`${o}-icon`]: {
          fontSize: n.fontSizeHeading2,
          lineHeight: 1
        },
        [`${o}-title${o}-title`]: {
          margin: 0,
          fontSize: n.fontSize,
          lineHeight: n.lineHeight
        },
        [`${o}-description`]: {}
      }
    }
  };
}, Js = (n) => {
  const {
    componentCls: e,
    calc: t
  } = n, r = `${e}-list`, i = t(n.fontSize).mul(n.lineHeight).mul(2).add(n.paddingSM).add(n.paddingSM).equal();
  return {
    [e]: {
      position: "relative",
      width: "100%",
      ...sn,
      // =============================== File List ===============================
      [r]: {
        display: "flex",
        flexWrap: "wrap",
        gap: n.paddingSM,
        fontSize: n.fontSize,
        lineHeight: n.lineHeight,
        color: n.colorText,
        paddingBlock: n.paddingSM,
        paddingInline: n.padding,
        width: "100%",
        background: n.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${n.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: t(i).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: i,
          height: i,
          fontSize: n.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: n.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: n.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: n.padding
          }
        },
        "&:dir(ltr)": {
          [`&${r}-overflow-ping-start ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-end ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${r}-overflow-ping-end ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-start ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, ea = (n) => {
  const {
    colorBgContainer: e
  } = n;
  return {
    colorBgPlaceholderHover: new Se(e).setA(0.85).toRgbString()
  };
}, jr = Fr("Attachments", (n) => {
  const e = Ot(n, {});
  return [Qs(e), Js(e), Zs(e)];
}, ea), ta = (n) => n.indexOf("image/") === 0, tt = 200;
function na(n) {
  return new Promise((e) => {
    if (!n || !n.type || !ta(n.type)) {
      e("");
      return;
    }
    const t = new Image();
    if (t.onload = () => {
      const {
        width: r,
        height: i
      } = t, o = r / i, s = o > 1 ? tt : tt * o, a = o > 1 ? tt / o : tt, c = document.createElement("canvas");
      c.width = s, c.height = a, c.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(c), c.getContext("2d").drawImage(t, 0, 0, s, a);
      const u = c.toDataURL();
      document.body.removeChild(c), window.URL.revokeObjectURL(t.src), e(u);
    }, t.crossOrigin = "anonymous", n.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (t.src = r.result);
      }, r.readAsDataURL(n);
    } else if (n.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && e(r.result);
      }, r.readAsDataURL(n);
    } else
      t.src = window.URL.createObjectURL(n);
  });
}
function ra() {
  return /* @__PURE__ */ f.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    //xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ f.createElement("title", null, "audio"), /* @__PURE__ */ f.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ f.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function ia(n) {
  const {
    percent: e
  } = n, {
    token: t
  } = ft.useToken();
  return /* @__PURE__ */ f.createElement(Li, {
    type: "circle",
    percent: e,
    size: t.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ f.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function oa() {
  return /* @__PURE__ */ f.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg"
    // xmlnsXlink="http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ f.createElement("title", null, "video"), /* @__PURE__ */ f.createElement("g", {
    stroke: "none",
    strokeWidth: "1",
    fill: "none",
    fillRule: "evenodd"
  }, /* @__PURE__ */ f.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const zt = " ", an = "#8c8c8c", Wr = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], sa = [{
  icon: /* @__PURE__ */ f.createElement(hi, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ f.createElement(pi, null),
  color: an,
  ext: Wr
}, {
  icon: /* @__PURE__ */ f.createElement(mi, null),
  color: an,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ f.createElement(gi, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ f.createElement(vi, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ f.createElement(bi, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ f.createElement(yi, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ f.createElement(oa, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ f.createElement(ra, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Kn(n, e) {
  return e.some((t) => n.toLowerCase() === `.${t}`);
}
function aa(n) {
  let e = n;
  const t = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; e >= 1024 && r < t.length - 1; )
    e /= 1024, r++;
  return `${e.toFixed(0)} ${t[r]}`;
}
function la(n, e) {
  const {
    prefixCls: t,
    item: r,
    onRemove: i,
    className: o,
    style: s,
    imageProps: a
  } = n, c = f.useContext(Xe), {
    disabled: l
  } = c || {}, {
    name: u,
    size: d,
    percent: h,
    status: p = "done",
    description: b
  } = r, {
    getPrefixCls: v
  } = Ue(), g = v("attachment", t), m = `${g}-list-card`, [x, C, y] = jr(g), [_, S] = f.useMemo(() => {
    const M = u || "", z = M.match(/^(.*)\.[^.]+$/);
    return z ? [z[1], M.slice(z[1].length)] : [M, ""];
  }, [u]), T = f.useMemo(() => Kn(S, Wr), [S]), E = f.useMemo(() => b || (p === "uploading" ? `${h || 0}%` : p === "error" ? r.response || zt : d ? aa(d) : zt), [p, h]), [P, O] = f.useMemo(() => {
    for (const {
      ext: M,
      icon: z,
      color: w
    } of sa)
      if (Kn(S, M))
        return [z, w];
    return [/* @__PURE__ */ f.createElement(di, {
      key: "defaultIcon"
    }), an];
  }, [S]), [D, k] = f.useState();
  f.useEffect(() => {
    if (r.originFileObj) {
      let M = !0;
      return na(r.originFileObj).then((z) => {
        M && k(z);
      }), () => {
        M = !1;
      };
    }
    k(void 0);
  }, [r.originFileObj]);
  let N = null;
  const F = r.thumbUrl || r.url || D, L = T && (r.originFileObj || F);
  return L ? N = /* @__PURE__ */ f.createElement(f.Fragment, null, F && /* @__PURE__ */ f.createElement(Ai, ge({
    alt: "preview",
    src: F
  }, a)), p !== "done" && /* @__PURE__ */ f.createElement("div", {
    className: `${m}-img-mask`
  }, p === "uploading" && h !== void 0 && /* @__PURE__ */ f.createElement(ia, {
    percent: h,
    prefixCls: m
  }), p === "error" && /* @__PURE__ */ f.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, E)))) : N = /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-icon`,
    style: {
      color: O
    }
  }, P), /* @__PURE__ */ f.createElement("div", {
    className: `${m}-content`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-name`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, _ ?? zt), /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-suffix`
  }, S)), /* @__PURE__ */ f.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, E)))), x(/* @__PURE__ */ f.createElement("div", {
    className: Z(m, {
      [`${m}-status-${p}`]: p,
      [`${m}-type-preview`]: L,
      [`${m}-type-overview`]: !L
    }, o, C, y),
    style: s,
    ref: e
  }, N, !l && i && /* @__PURE__ */ f.createElement("button", {
    type: "button",
    className: `${m}-remove`,
    onClick: () => {
      i(r);
    }
  }, /* @__PURE__ */ f.createElement(fi, null))));
}
const Br = /* @__PURE__ */ f.forwardRef(la), Yn = 1;
function ca(n) {
  const {
    prefixCls: e,
    items: t,
    onRemove: r,
    overflow: i,
    upload: o,
    listClassName: s,
    listStyle: a,
    itemClassName: c,
    itemStyle: l,
    imageProps: u
  } = n, d = `${e}-list`, h = f.useRef(null), [p, b] = f.useState(!1), {
    disabled: v
  } = f.useContext(Xe);
  f.useEffect(() => (b(!0), () => {
    b(!1);
  }), []);
  const [g, m] = f.useState(!1), [x, C] = f.useState(!1), y = () => {
    const E = h.current;
    E && (i === "scrollX" ? (m(Math.abs(E.scrollLeft) >= Yn), C(E.scrollWidth - E.clientWidth - Math.abs(E.scrollLeft) >= Yn)) : i === "scrollY" && (m(E.scrollTop !== 0), C(E.scrollHeight - E.clientHeight !== E.scrollTop)));
  };
  f.useEffect(() => {
    y();
  }, [i, t.length]);
  const _ = (E) => {
    const P = h.current;
    P && P.scrollTo({
      left: P.scrollLeft + E * P.clientWidth,
      behavior: "smooth"
    });
  }, S = () => {
    _(-1);
  }, T = () => {
    _(1);
  };
  return /* @__PURE__ */ f.createElement("div", {
    className: Z(d, {
      [`${d}-overflow-${n.overflow}`]: i,
      [`${d}-overflow-ping-start`]: g,
      [`${d}-overflow-ping-end`]: x
    }, s),
    ref: h,
    onScroll: y,
    style: a
  }, /* @__PURE__ */ f.createElement(Ps, {
    keys: t.map((E) => ({
      key: E.uid,
      item: E
    })),
    motionName: `${d}-card-motion`,
    component: !1,
    motionAppear: p,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: E,
    item: P,
    className: O,
    style: D
  }) => /* @__PURE__ */ f.createElement(Br, {
    key: E,
    prefixCls: e,
    item: P,
    onRemove: r,
    className: Z(O, c),
    imageProps: u,
    style: {
      ...D,
      ...l
    }
  })), !v && /* @__PURE__ */ f.createElement($r, {
    upload: o
  }, /* @__PURE__ */ f.createElement(De, {
    className: `${d}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ f.createElement(wi, {
    className: `${d}-upload-btn-icon`
  }))), i === "scrollX" && /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement(De, {
    size: "small",
    shape: "circle",
    className: `${d}-prev-btn`,
    icon: /* @__PURE__ */ f.createElement(Si, null),
    onClick: S
  }), /* @__PURE__ */ f.createElement(De, {
    size: "small",
    shape: "circle",
    className: `${d}-next-btn`,
    icon: /* @__PURE__ */ f.createElement(xi, null),
    onClick: T
  })));
}
function ua(n, e) {
  const {
    prefixCls: t,
    placeholder: r = {},
    upload: i,
    className: o,
    style: s
  } = n, a = `${t}-placeholder`, c = r || {}, {
    disabled: l
  } = f.useContext(Xe), [u, d] = f.useState(!1), h = () => {
    d(!0);
  }, p = (g) => {
    g.currentTarget.contains(g.relatedTarget) || d(!1);
  }, b = () => {
    d(!1);
  }, v = /* @__PURE__ */ f.isValidElement(r) ? r : /* @__PURE__ */ f.createElement(ar, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ f.createElement($t.Text, {
    className: `${a}-icon`
  }, c.icon), /* @__PURE__ */ f.createElement($t.Title, {
    className: `${a}-title`,
    level: 5
  }, c.title), /* @__PURE__ */ f.createElement($t.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, c.description));
  return /* @__PURE__ */ f.createElement("div", {
    className: Z(a, {
      [`${a}-drag-in`]: u,
      [`${a}-disabled`]: l
    }, o),
    onDragEnter: h,
    onDragLeave: p,
    onDrop: b,
    "aria-hidden": l,
    style: s
  }, /* @__PURE__ */ f.createElement(sr.Dragger, ge({
    showUploadList: !1
  }, i, {
    ref: e,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), v));
}
const da = /* @__PURE__ */ f.forwardRef(ua);
function fa(n, e) {
  const {
    prefixCls: t,
    rootClassName: r,
    rootStyle: i,
    className: o,
    style: s,
    items: a,
    children: c,
    getDropContainer: l,
    placeholder: u,
    onChange: d,
    onRemove: h,
    overflow: p,
    imageProps: b,
    disabled: v,
    classNames: g = {},
    styles: m = {},
    ...x
  } = n, {
    getPrefixCls: C,
    direction: y
  } = Ue(), _ = C("attachment", t), S = pr("attachments"), {
    classNames: T,
    styles: E
  } = S, P = f.useRef(null), O = f.useRef(null);
  f.useImperativeHandle(e, () => ({
    nativeElement: P.current,
    upload: (B) => {
      var V, J;
      const Q = (J = (V = O.current) == null ? void 0 : V.nativeElement) == null ? void 0 : J.querySelector('input[type="file"]');
      if (Q) {
        const oe = new DataTransfer();
        oe.items.add(B), Q.files = oe.files, Q.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [D, k, N] = jr(_), F = Z(k, N), [L, M] = cn([], {
    value: a
  }), z = _e((B) => {
    M(B.fileList), d == null || d(B);
  }), w = {
    ...x,
    fileList: L,
    onChange: z
  }, ce = (B) => Promise.resolve(typeof h == "function" ? h(B) : h).then((Q) => {
    if (Q === !1)
      return;
    const V = L.filter((J) => J.uid !== B.uid);
    z({
      file: {
        ...B,
        status: "removed"
      },
      fileList: V
    });
  });
  let de;
  const U = (B, Q, V) => {
    const J = typeof u == "function" ? u(B) : u;
    return /* @__PURE__ */ f.createElement(da, {
      placeholder: J,
      upload: w,
      prefixCls: _,
      className: Z(T.placeholder, g.placeholder),
      style: {
        ...E.placeholder,
        ...m.placeholder,
        ...Q == null ? void 0 : Q.style
      },
      ref: V
    });
  };
  if (c)
    de = /* @__PURE__ */ f.createElement(f.Fragment, null, /* @__PURE__ */ f.createElement($r, {
      upload: w,
      rootClassName: r,
      ref: O
    }, c), /* @__PURE__ */ f.createElement(Ln, {
      getDropContainer: l,
      prefixCls: _,
      className: Z(F, r)
    }, U("drop")));
  else {
    const B = L.length > 0;
    de = /* @__PURE__ */ f.createElement("div", {
      className: Z(_, F, {
        [`${_}-rtl`]: y === "rtl"
      }, o, r),
      style: {
        ...i,
        ...s
      },
      dir: y || "ltr",
      ref: P
    }, /* @__PURE__ */ f.createElement(ca, {
      prefixCls: _,
      items: L,
      onRemove: ce,
      overflow: p,
      upload: w,
      listClassName: Z(T.list, g.list),
      listStyle: {
        ...E.list,
        ...m.list,
        ...!B && {
          display: "none"
        }
      },
      itemClassName: Z(T.item, g.item),
      itemStyle: {
        ...E.item,
        ...m.item
      },
      imageProps: b
    }), U("inline", B ? {
      style: {
        display: "none"
      }
    } : {}, O), /* @__PURE__ */ f.createElement(Ln, {
      getDropContainer: l || (() => P.current),
      prefixCls: _,
      className: F
    }, U("drop")));
  }
  return D(/* @__PURE__ */ f.createElement(Xe.Provider, {
    value: {
      disabled: v
    }
  }, de));
}
const Hr = /* @__PURE__ */ f.forwardRef(fa);
Hr.FileCard = Br;
var ha = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, pa = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, ma = "".concat(ha, " ").concat(pa).split(/[\s\n]+/), ga = "aria-", va = "data-";
function Zn(n, e) {
  return n.indexOf(e) === 0;
}
function ba(n) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, t;
  e === !1 ? t = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? t = {
    aria: !0
  } : t = Qo({}, e);
  var r = {};
  return Object.keys(n).forEach(function(i) {
    // Aria
    (t.aria && (i === "role" || Zn(i, ga)) || // Data
    t.data && Zn(i, va) || // Attr
    t.attr && ma.includes(i)) && (r[i] = n[i]);
  }), r;
}
function ya(n, e) {
  return Jr(n, () => {
    const t = e(), {
      nativeElement: r
    } = t;
    return new Proxy(r, {
      get(i, o) {
        return t[o] ? t[o] : Reflect.get(i, o);
      }
    });
  });
}
const zr = /* @__PURE__ */ R.createContext({}), Qn = () => ({
  height: 0
}), Jn = (n) => ({
  height: n.scrollHeight
});
function wa(n) {
  const {
    title: e,
    onOpenChange: t,
    open: r,
    children: i,
    className: o,
    style: s,
    classNames: a = {},
    styles: c = {},
    closable: l,
    forceRender: u
  } = n, {
    prefixCls: d
  } = R.useContext(zr), h = `${d}-header`;
  return /* @__PURE__ */ R.createElement(Ar, {
    motionEnter: !0,
    motionLeave: !0,
    motionName: `${h}-motion`,
    leavedClassName: `${h}-motion-hidden`,
    onEnterStart: Qn,
    onEnterActive: Jn,
    onLeaveStart: Jn,
    onLeaveActive: Qn,
    visible: r,
    forceRender: u
  }, ({
    className: p,
    style: b
  }) => /* @__PURE__ */ R.createElement("div", {
    className: Z(h, p, o),
    style: {
      ...b,
      ...s
    }
  }, (l !== !1 || e) && /* @__PURE__ */ R.createElement("div", {
    className: (
      // We follow antd naming standard here.
      // So the header part is use `-header` suffix.
      // Though its little bit weird for double `-header`.
      Z(`${h}-header`, a.header)
    ),
    style: {
      ...c.header
    }
  }, /* @__PURE__ */ R.createElement("div", {
    className: `${h}-title`
  }, e), l !== !1 && /* @__PURE__ */ R.createElement("div", {
    className: `${h}-close`
  }, /* @__PURE__ */ R.createElement(De, {
    type: "text",
    icon: /* @__PURE__ */ R.createElement(Ei, null),
    size: "small",
    onClick: () => {
      t == null || t(!r);
    }
  }))), i && /* @__PURE__ */ R.createElement("div", {
    className: Z(`${h}-content`, a.content),
    style: {
      ...c.content
    }
  }, i)));
}
const Lt = /* @__PURE__ */ R.createContext(null);
function Sa(n, e) {
  const {
    className: t,
    action: r,
    onClick: i,
    ...o
  } = n, s = R.useContext(Lt), {
    prefixCls: a,
    disabled: c
  } = s, l = o.disabled ?? c ?? s[`${r}Disabled`];
  return /* @__PURE__ */ R.createElement(De, ge({
    type: "text"
  }, o, {
    ref: e,
    onClick: (u) => {
      var d;
      l || ((d = s[r]) == null || d.call(s), i == null || i(u));
    },
    className: Z(a, t, {
      [`${a}-disabled`]: l
    })
  }));
}
const At = /* @__PURE__ */ R.forwardRef(Sa);
function xa(n, e) {
  return /* @__PURE__ */ R.createElement(At, ge({
    icon: /* @__PURE__ */ R.createElement(Ci, null)
  }, n, {
    action: "onClear",
    ref: e
  }));
}
const Ea = /* @__PURE__ */ R.forwardRef(xa), Ca = /* @__PURE__ */ ei((n) => {
  const {
    className: e
  } = n;
  return /* @__PURE__ */ f.createElement("svg", {
    color: "currentColor",
    viewBox: "0 0 1000 1000",
    xmlns: "http://www.w3.org/2000/svg",
    className: e
  }, /* @__PURE__ */ f.createElement("title", null, "Stop Loading"), /* @__PURE__ */ f.createElement("rect", {
    fill: "currentColor",
    height: "250",
    rx: "24",
    ry: "24",
    width: "250",
    x: "375",
    y: "375"
  }), /* @__PURE__ */ f.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    opacity: "0.45"
  }), /* @__PURE__ */ f.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    strokeDasharray: "600 9999999"
  }, /* @__PURE__ */ f.createElement("animateTransform", {
    attributeName: "transform",
    dur: "1s",
    from: "0 500 500",
    repeatCount: "indefinite",
    to: "360 500 500",
    type: "rotate"
  })));
});
function _a(n, e) {
  const {
    prefixCls: t
  } = R.useContext(Lt), {
    className: r
  } = n;
  return /* @__PURE__ */ R.createElement(At, ge({
    icon: null,
    color: "primary",
    variant: "text",
    shape: "circle"
  }, n, {
    className: Z(r, `${t}-loading-button`),
    action: "onCancel",
    ref: e
  }), /* @__PURE__ */ R.createElement(Ca, {
    className: `${t}-loading-icon`
  }));
}
const Ur = /* @__PURE__ */ R.forwardRef(_a);
function Ra(n, e) {
  return /* @__PURE__ */ R.createElement(At, ge({
    icon: /* @__PURE__ */ R.createElement(_i, null),
    type: "primary",
    shape: "circle"
  }, n, {
    action: "onSend",
    ref: e
  }));
}
const Vr = /* @__PURE__ */ R.forwardRef(Ra), Be = 1e3, He = 4, lt = 140, er = lt / 2, nt = 250, tr = 500, rt = 0.8;
function Ta({
  className: n
}) {
  return /* @__PURE__ */ f.createElement("svg", {
    color: "currentColor",
    viewBox: `0 0 ${Be} ${Be}`,
    xmlns: "http://www.w3.org/2000/svg",
    className: n
  }, /* @__PURE__ */ f.createElement("title", null, "Speech Recording"), Array.from({
    length: He
  }).map((e, t) => {
    const r = (Be - lt * He) / (He - 1), i = t * (r + lt), o = Be / 2 - nt / 2, s = Be / 2 - tr / 2;
    return /* @__PURE__ */ f.createElement("rect", {
      fill: "currentColor",
      rx: er,
      ry: er,
      height: nt,
      width: lt,
      x: i,
      y: o,
      key: t
    }, /* @__PURE__ */ f.createElement("animate", {
      attributeName: "height",
      values: `${nt}; ${tr}; ${nt}`,
      keyTimes: "0; 0.5; 1",
      dur: `${rt}s`,
      begin: `${rt / He * t}s`,
      repeatCount: "indefinite"
    }), /* @__PURE__ */ f.createElement("animate", {
      attributeName: "y",
      values: `${o}; ${s}; ${o}`,
      keyTimes: "0; 0.5; 1",
      dur: `${rt}s`,
      begin: `${rt / He * t}s`,
      repeatCount: "indefinite"
    }));
  }));
}
function Pa(n, e) {
  const {
    speechRecording: t,
    onSpeechDisabled: r,
    prefixCls: i
  } = R.useContext(Lt);
  let o = null;
  return t ? o = /* @__PURE__ */ R.createElement(Ta, {
    className: `${i}-recording-icon`
  }) : r ? o = /* @__PURE__ */ R.createElement(Ri, null) : o = /* @__PURE__ */ R.createElement(Ti, null), /* @__PURE__ */ R.createElement(At, ge({
    icon: o,
    color: "primary",
    variant: "text"
  }, n, {
    action: "onSpeech",
    ref: e
  }));
}
const Xr = /* @__PURE__ */ R.forwardRef(Pa), Ma = (n) => {
  const {
    componentCls: e,
    calc: t
  } = n, r = `${e}-header`;
  return {
    [e]: {
      [r]: {
        borderBottomWidth: n.lineWidth,
        borderBottomStyle: "solid",
        borderBottomColor: n.colorBorder,
        // ======================== Header ========================
        "&-header": {
          background: n.colorFillAlter,
          fontSize: n.fontSize,
          lineHeight: n.lineHeight,
          paddingBlock: t(n.paddingSM).sub(n.lineWidthBold).equal(),
          paddingInlineStart: n.padding,
          paddingInlineEnd: n.paddingXS,
          display: "flex",
          borderRadius: {
            _skip_check_: !0,
            value: t(n.borderRadius).mul(2).equal()
          },
          borderEndStartRadius: 0,
          borderEndEndRadius: 0,
          [`${r}-title`]: {
            flex: "auto"
          }
        },
        // ======================= Content ========================
        "&-content": {
          padding: n.padding
        },
        // ======================== Motion ========================
        "&-motion": {
          transition: ["height", "border"].map((i) => `${i} ${n.motionDurationSlow}`).join(","),
          overflow: "hidden",
          "&-enter-start, &-leave-active": {
            borderBottomColor: "transparent"
          },
          "&-hidden": {
            display: "none"
          }
        }
      }
    }
  };
}, Oa = (n) => {
  const {
    componentCls: e,
    padding: t,
    paddingSM: r,
    paddingXS: i,
    paddingXXS: o,
    lineWidth: s,
    lineWidthBold: a,
    calc: c
  } = n;
  return {
    [e]: {
      position: "relative",
      width: "100%",
      boxSizing: "border-box",
      boxShadow: `${n.boxShadowTertiary}`,
      transition: `background ${n.motionDurationSlow}`,
      // Border
      borderRadius: {
        _skip_check_: !0,
        value: c(n.borderRadius).mul(2).equal()
      },
      borderColor: n.colorBorder,
      borderWidth: 0,
      borderStyle: "solid",
      // Border
      "&:after": {
        content: '""',
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        transition: `border-color ${n.motionDurationSlow}`,
        borderRadius: {
          _skip_check_: !0,
          value: "inherit"
        },
        borderStyle: "inherit",
        borderColor: "inherit",
        borderWidth: s
      },
      // Focus
      "&:focus-within": {
        boxShadow: `${n.boxShadowSecondary}`,
        borderColor: n.colorPrimary,
        "&:after": {
          borderWidth: a
        }
      },
      "&-disabled": {
        background: n.colorBgContainerDisabled
      },
      // ============================== RTL ==============================
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      // ============================ Content ============================
      [`${e}-content`]: {
        display: "flex",
        gap: i,
        width: "100%",
        paddingBlock: r,
        paddingInlineStart: t,
        paddingInlineEnd: r,
        boxSizing: "border-box",
        alignItems: "flex-end"
      },
      // ============================ Prefix =============================
      [`${e}-prefix`]: {
        flex: "none"
      },
      // ============================= Input =============================
      [`${e}-input`]: {
        padding: 0,
        borderRadius: 0,
        flex: "auto",
        alignSelf: "center",
        minHeight: "auto"
      },
      // ============================ Actions ============================
      [`${e}-actions-list`]: {
        flex: "none",
        display: "flex",
        "&-presets": {
          gap: n.paddingXS
        }
      },
      [`${e}-actions-btn`]: {
        "&-disabled": {
          opacity: 0.45
        },
        "&-loading-button": {
          padding: 0,
          border: 0
        },
        "&-loading-icon": {
          height: n.controlHeight,
          width: n.controlHeight,
          verticalAlign: "top"
        },
        "&-recording-icon": {
          height: "1.2em",
          width: "1.2em",
          verticalAlign: "top"
        }
      },
      // ============================ Footer =============================
      [`${e}-footer`]: {
        paddingInlineStart: t,
        paddingInlineEnd: r,
        paddingBlockEnd: r,
        paddingBlockStart: o,
        boxSizing: "border-box"
      }
    }
  };
}, La = () => ({}), Aa = Fr("Sender", (n) => {
  const {
    paddingXS: e,
    calc: t
  } = n, r = Ot(n, {
    SenderContentMaxWidth: `calc(100% - ${Kt(t(e).add(32).equal())})`
  });
  return [Oa(r), Ma(r)];
}, La);
let mt;
!mt && typeof window < "u" && (mt = window.SpeechRecognition || window.webkitSpeechRecognition);
function $a(n, e) {
  const t = _e(n), [r, i, o] = f.useMemo(() => typeof e == "object" ? [e.recording, e.onRecordingChange, typeof e.recording == "boolean"] : [void 0, void 0, !1], [e]), [s, a] = f.useState(null);
  f.useEffect(() => {
    if (typeof navigator < "u" && "permissions" in navigator) {
      let v = null;
      return navigator.permissions.query({
        name: "microphone"
      }).then((g) => {
        a(g.state), g.onchange = function() {
          a(this.state);
        }, v = g;
      }), () => {
        v && (v.onchange = null);
      };
    }
  }, []);
  const c = mt && s !== "denied", l = f.useRef(null), [u, d] = cn(!1, {
    value: r
  }), h = f.useRef(!1), p = () => {
    if (c && !l.current) {
      const v = new mt();
      v.onstart = () => {
        d(!0);
      }, v.onend = () => {
        d(!1);
      }, v.onresult = (g) => {
        var m, x, C;
        if (!h.current) {
          const y = (C = (x = (m = g.results) == null ? void 0 : m[0]) == null ? void 0 : x[0]) == null ? void 0 : C.transcript;
          t(y);
        }
        h.current = !1;
      }, l.current = v;
    }
  }, b = _e((v) => {
    v && !u || (h.current = v, o ? i == null || i(!u) : (p(), l.current && (u ? (l.current.stop(), i == null || i(!1)) : (l.current.start(), i == null || i(!0)))));
  });
  return [c, b, u];
}
function Ia(n, e, t) {
  return qo(n, e) || t;
}
const nr = {
  SendButton: Vr,
  ClearButton: Ea,
  LoadingButton: Ur,
  SpeechButton: Xr
}, Da = /* @__PURE__ */ f.forwardRef((n, e) => {
  const {
    prefixCls: t,
    styles: r = {},
    classNames: i = {},
    className: o,
    rootClassName: s,
    style: a,
    defaultValue: c,
    value: l,
    readOnly: u,
    submitType: d = "enter",
    onSubmit: h,
    loading: p,
    components: b,
    onCancel: v,
    onChange: g,
    actions: m,
    onKeyPress: x,
    onKeyDown: C,
    disabled: y,
    allowSpeech: _,
    prefix: S,
    footer: T,
    header: E,
    onPaste: P,
    onPasteFile: O,
    autoSize: D = {
      maxRows: 8
    },
    ...k
  } = n, {
    direction: N,
    getPrefixCls: F
  } = Ue(), L = F("sender", t), M = f.useRef(null), z = f.useRef(null);
  ya(e, () => {
    var Y, le;
    return {
      nativeElement: M.current,
      focus: (Y = z.current) == null ? void 0 : Y.focus,
      blur: (le = z.current) == null ? void 0 : le.blur
    };
  });
  const w = pr("sender"), ce = `${L}-input`, [de, U, B] = Aa(L), Q = Z(L, w.className, o, s, U, B, {
    [`${L}-rtl`]: N === "rtl",
    [`${L}-disabled`]: y
  }), V = `${L}-actions-btn`, J = `${L}-actions-list`, [oe, j] = cn(c || "", {
    value: l
  }), A = (Y, le) => {
    j(Y), g && g(Y, le);
  }, [H, re, q] = $a((Y) => {
    A(`${oe} ${Y}`);
  }, _), X = Ia(b, ["input"], $i.TextArea), fe = {
    ...ba(k, {
      attr: !0,
      aria: !0,
      data: !0
    }),
    ref: z
  }, G = () => {
    oe && h && !p && h(oe);
  }, ie = () => {
    A("");
  }, be = f.useRef(!1), K = () => {
    be.current = !0;
  }, we = () => {
    be.current = !1;
  }, Ee = (Y) => {
    const le = Y.key === "Enter" && !be.current;
    switch (d) {
      case "enter":
        le && !Y.shiftKey && (Y.preventDefault(), G());
        break;
      case "shiftEnter":
        le && Y.shiftKey && (Y.preventDefault(), G());
        break;
    }
    x == null || x(Y);
  }, se = (Y) => {
    var je;
    const le = (je = Y.clipboardData) == null ? void 0 : je.files;
    le != null && le.length && O && (O(le[0], le), Y.preventDefault()), P == null || P(Y);
  }, ee = (Y) => {
    var le, je;
    Y.target !== ((le = M.current) == null ? void 0 : le.querySelector(`.${ce}`)) && Y.preventDefault(), (je = z.current) == null || je.focus();
  };
  let ae = /* @__PURE__ */ f.createElement(ar, {
    className: `${J}-presets`
  }, _ && /* @__PURE__ */ f.createElement(Xr, null), p ? /* @__PURE__ */ f.createElement(Ur, null) : /* @__PURE__ */ f.createElement(Vr, null));
  typeof m == "function" ? ae = m(ae, {
    components: nr
  }) : (m || m === !1) && (ae = m);
  const Me = {
    prefixCls: V,
    onSend: G,
    onSendDisabled: !oe,
    onClear: ie,
    onClearDisabled: !oe,
    onCancel: v,
    onCancelDisabled: !p,
    onSpeech: () => re(!1),
    onSpeechDisabled: !H,
    speechRecording: q,
    disabled: y
  }, Te = typeof T == "function" ? T({
    components: nr
  }) : T || null;
  return de(/* @__PURE__ */ f.createElement("div", {
    ref: M,
    className: Q,
    style: {
      ...w.style,
      ...a
    }
  }, E && /* @__PURE__ */ f.createElement(zr.Provider, {
    value: {
      prefixCls: L
    }
  }, E), /* @__PURE__ */ f.createElement(Lt.Provider, {
    value: Me
  }, /* @__PURE__ */ f.createElement("div", {
    className: `${L}-content`,
    onMouseDown: ee
  }, S && /* @__PURE__ */ f.createElement("div", {
    className: Z(`${L}-prefix`, w.classNames.prefix, i.prefix),
    style: {
      ...w.styles.prefix,
      ...r.prefix
    }
  }, S), /* @__PURE__ */ f.createElement(X, ge({}, fe, {
    disabled: y,
    style: {
      ...w.styles.input,
      ...r.input
    },
    className: Z(ce, w.classNames.input, i.input),
    autoSize: D,
    value: oe,
    onChange: (Y) => {
      A(Y.target.value, Y), re(!0);
    },
    onPressEnter: Ee,
    onCompositionStart: K,
    onCompositionEnd: we,
    onKeyDown: C,
    onPaste: se,
    variant: "borderless",
    readOnly: u
  })), ae && /* @__PURE__ */ f.createElement("div", {
    className: Z(J, w.classNames.actions, i.actions),
    style: {
      ...w.styles.actions,
      ...r.actions
    }
  }, ae)), Te && /* @__PURE__ */ f.createElement("div", {
    className: Z(`${L}-footer`, w.classNames.footer, i.footer),
    style: {
      ...w.styles.footer,
      ...r.footer
    }
  }, Te))));
}), ln = Da;
ln.Header = wa;
function ka(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Na(n, e = !1) {
  try {
    if (si(n))
      return n;
    if (e && !ka(n))
      return;
    if (typeof n == "string") {
      let t = n.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function rr(n, e) {
  return Gt(() => Na(n, e), [n, e]);
}
function ct(n) {
  const e = he(n);
  return e.current = n, ti((...t) => {
    var r;
    return (r = e.current) == null ? void 0 : r.call(e, ...t);
  }, []);
}
function Fa({
  value: n,
  onValueChange: e
}) {
  const [t, r] = Ie(n), i = he(e);
  i.current = e;
  const o = he(t);
  return o.current = t, xe(() => {
    i.current(t);
  }, [t]), xe(() => {
    Qi(n, o.current) || r(n);
  }, [n]), [t, r];
}
function ja(n, e) {
  return Object.keys(n).reduce((t, r) => (n[r] !== void 0 && n[r] !== null && (t[r] = n[r]), t), {});
}
function Ut(n, e, t, r) {
  return new (t || (t = Promise))(function(i, o) {
    function s(l) {
      try {
        c(r.next(l));
      } catch (u) {
        o(u);
      }
    }
    function a(l) {
      try {
        c(r.throw(l));
      } catch (u) {
        o(u);
      }
    }
    function c(l) {
      var u;
      l.done ? i(l.value) : (u = l.value, u instanceof t ? u : new t(function(d) {
        d(u);
      })).then(s, a);
    }
    c((r = r.apply(n, [])).next());
  });
}
class Gr {
  constructor() {
    this.listeners = {};
  }
  on(e, t, r) {
    if (this.listeners[e] || (this.listeners[e] = /* @__PURE__ */ new Set()), this.listeners[e].add(t), r == null ? void 0 : r.once) {
      const i = () => {
        this.un(e, i), this.un(e, t);
      };
      return this.on(e, i), i;
    }
    return () => this.un(e, t);
  }
  un(e, t) {
    var r;
    (r = this.listeners[e]) === null || r === void 0 || r.delete(t);
  }
  once(e, t) {
    return this.on(e, t, {
      once: !0
    });
  }
  unAll() {
    this.listeners = {};
  }
  emit(e, ...t) {
    this.listeners[e] && this.listeners[e].forEach((r) => r(...t));
  }
}
class Wa extends Gr {
  constructor(e) {
    super(), this.subscriptions = [], this.options = e;
  }
  onInit() {
  }
  _init(e) {
    this.wavesurfer = e, this.onInit();
  }
  destroy() {
    this.emit("destroy"), this.subscriptions.forEach((e) => e());
  }
}
class Ba extends Gr {
  constructor() {
    super(...arguments), this.unsubscribe = () => {
    };
  }
  start() {
    this.unsubscribe = this.on("tick", () => {
      requestAnimationFrame(() => {
        this.emit("tick");
      });
    }), this.emit("tick");
  }
  stop() {
    this.unsubscribe();
  }
  destroy() {
    this.unsubscribe();
  }
}
const Ha = ["audio/webm", "audio/wav", "audio/mpeg", "audio/mp4", "audio/mp3"];
class pn extends Wa {
  constructor(e) {
    var t, r, i, o, s, a;
    super(Object.assign(Object.assign({}, e), {
      audioBitsPerSecond: (t = e.audioBitsPerSecond) !== null && t !== void 0 ? t : 128e3,
      scrollingWaveform: (r = e.scrollingWaveform) !== null && r !== void 0 && r,
      scrollingWaveformWindow: (i = e.scrollingWaveformWindow) !== null && i !== void 0 ? i : 5,
      continuousWaveform: (o = e.continuousWaveform) !== null && o !== void 0 && o,
      renderRecordedAudio: (s = e.renderRecordedAudio) === null || s === void 0 || s,
      mediaRecorderTimeslice: (a = e.mediaRecorderTimeslice) !== null && a !== void 0 ? a : void 0
    })), this.stream = null, this.mediaRecorder = null, this.dataWindow = null, this.isWaveformPaused = !1, this.lastStartTime = 0, this.lastDuration = 0, this.duration = 0, this.timer = new Ba(), this.subscriptions.push(this.timer.on("tick", () => {
      const c = performance.now() - this.lastStartTime;
      this.duration = this.isPaused() ? this.duration : this.lastDuration + c, this.emit("record-progress", this.duration);
    }));
  }
  static create(e) {
    return new pn(e || {});
  }
  renderMicStream(e) {
    var t;
    const r = new AudioContext(), i = r.createMediaStreamSource(e), o = r.createAnalyser();
    i.connect(o), this.options.continuousWaveform && (o.fftSize = 32);
    const s = o.frequencyBinCount, a = new Float32Array(s);
    let c = 0;
    this.wavesurfer && ((t = this.originalOptions) !== null && t !== void 0 || (this.originalOptions = Object.assign({}, this.wavesurfer.options)), this.wavesurfer.options.interact = !1, this.options.scrollingWaveform && (this.wavesurfer.options.cursorWidth = 0));
    const l = setInterval(() => {
      var u, d, h, p;
      if (!this.isWaveformPaused) {
        if (o.getFloatTimeDomainData(a), this.options.scrollingWaveform) {
          const b = Math.floor((this.options.scrollingWaveformWindow || 0) * r.sampleRate), v = Math.min(b, this.dataWindow ? this.dataWindow.length + s : s), g = new Float32Array(b);
          if (this.dataWindow) {
            const m = Math.max(0, b - this.dataWindow.length);
            g.set(this.dataWindow.slice(-v + s), m);
          }
          g.set(a, b - s), this.dataWindow = g;
        } else if (this.options.continuousWaveform) {
          if (!this.dataWindow) {
            const v = this.options.continuousWaveformDuration ? Math.round(100 * this.options.continuousWaveformDuration) : ((d = (u = this.wavesurfer) === null || u === void 0 ? void 0 : u.getWidth()) !== null && d !== void 0 ? d : 0) * window.devicePixelRatio;
            this.dataWindow = new Float32Array(v);
          }
          let b = 0;
          for (let v = 0; v < s; v++) {
            const g = Math.abs(a[v]);
            g > b && (b = g);
          }
          if (c + 1 > this.dataWindow.length) {
            const v = new Float32Array(2 * this.dataWindow.length);
            v.set(this.dataWindow, 0), this.dataWindow = v;
          }
          this.dataWindow[c] = b, c++;
        } else this.dataWindow = a;
        if (this.wavesurfer) {
          const b = ((p = (h = this.dataWindow) === null || h === void 0 ? void 0 : h.length) !== null && p !== void 0 ? p : 0) / 100;
          this.wavesurfer.load("", [this.dataWindow], this.options.scrollingWaveform ? this.options.scrollingWaveformWindow : b).then(() => {
            this.wavesurfer && this.options.continuousWaveform && (this.wavesurfer.setTime(this.getDuration() / 1e3), this.wavesurfer.options.minPxPerSec || this.wavesurfer.setOptions({
              minPxPerSec: this.wavesurfer.getWidth() / this.wavesurfer.getDuration()
            }));
          }).catch((v) => {
            console.error("Error rendering real-time recording data:", v);
          });
        }
      }
    }, 10);
    return {
      onDestroy: () => {
        clearInterval(l), i == null || i.disconnect(), r == null || r.close();
      },
      onEnd: () => {
        this.isWaveformPaused = !0, clearInterval(l), this.stopMic();
      }
    };
  }
  startMic(e) {
    return Ut(this, void 0, void 0, function* () {
      let t;
      try {
        t = yield navigator.mediaDevices.getUserMedia({
          audio: e == null || e
        });
      } catch (o) {
        throw new Error("Error accessing the microphone: " + o.message);
      }
      const {
        onDestroy: r,
        onEnd: i
      } = this.renderMicStream(t);
      return this.subscriptions.push(this.once("destroy", r)), this.subscriptions.push(this.once("record-end", i)), this.stream = t, t;
    });
  }
  stopMic() {
    this.stream && (this.stream.getTracks().forEach((e) => e.stop()), this.stream = null, this.mediaRecorder = null);
  }
  startRecording(e) {
    return Ut(this, void 0, void 0, function* () {
      const t = this.stream || (yield this.startMic(e));
      this.dataWindow = null;
      const r = this.mediaRecorder || new MediaRecorder(t, {
        mimeType: this.options.mimeType || Ha.find((s) => MediaRecorder.isTypeSupported(s)),
        audioBitsPerSecond: this.options.audioBitsPerSecond
      });
      this.mediaRecorder = r, this.stopRecording();
      const i = [];
      r.ondataavailable = (s) => {
        s.data.size > 0 && i.push(s.data), this.emit("record-data-available", s.data);
      };
      const o = (s) => {
        var a;
        const c = new Blob(i, {
          type: r.mimeType
        });
        this.emit(s, c), this.options.renderRecordedAudio && (this.applyOriginalOptionsIfNeeded(), (a = this.wavesurfer) === null || a === void 0 || a.load(URL.createObjectURL(c)));
      };
      r.onpause = () => o("record-pause"), r.onstop = () => o("record-end"), r.start(this.options.mediaRecorderTimeslice), this.lastStartTime = performance.now(), this.lastDuration = 0, this.duration = 0, this.isWaveformPaused = !1, this.timer.start(), this.emit("record-start");
    });
  }
  getDuration() {
    return this.duration;
  }
  isRecording() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) === "recording";
  }
  isPaused() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) === "paused";
  }
  isActive() {
    var e;
    return ((e = this.mediaRecorder) === null || e === void 0 ? void 0 : e.state) !== "inactive";
  }
  stopRecording() {
    var e;
    this.isActive() && ((e = this.mediaRecorder) === null || e === void 0 || e.stop(), this.timer.stop());
  }
  pauseRecording() {
    var e, t;
    this.isRecording() && (this.isWaveformPaused = !0, (e = this.mediaRecorder) === null || e === void 0 || e.requestData(), (t = this.mediaRecorder) === null || t === void 0 || t.pause(), this.timer.stop(), this.lastDuration = this.duration);
  }
  resumeRecording() {
    var e;
    this.isPaused() && (this.isWaveformPaused = !1, (e = this.mediaRecorder) === null || e === void 0 || e.resume(), this.timer.start(), this.lastStartTime = performance.now(), this.emit("record-resume"));
  }
  static getAvailableAudioDevices() {
    return Ut(this, void 0, void 0, function* () {
      return navigator.mediaDevices.enumerateDevices().then((e) => e.filter((t) => t.kind === "audioinput"));
    });
  }
  destroy() {
    this.applyOriginalOptionsIfNeeded(), super.destroy(), this.stopRecording(), this.stopMic();
  }
  applyOriginalOptionsIfNeeded() {
    this.wavesurfer && this.originalOptions && (this.wavesurfer.setOptions(this.originalOptions), delete this.originalOptions);
  }
}
class Ge {
  constructor() {
    this.listeners = {};
  }
  /** Subscribe to an event. Returns an unsubscribe function. */
  on(e, t, r) {
    if (this.listeners[e] || (this.listeners[e] = /* @__PURE__ */ new Set()), this.listeners[e].add(t), r != null && r.once) {
      const i = () => {
        this.un(e, i), this.un(e, t);
      };
      return this.on(e, i), i;
    }
    return () => this.un(e, t);
  }
  /** Unsubscribe from an event */
  un(e, t) {
    var r;
    (r = this.listeners[e]) === null || r === void 0 || r.delete(t);
  }
  /** Subscribe to an event only once */
  once(e, t) {
    return this.on(e, t, {
      once: !0
    });
  }
  /** Clear all events */
  unAll() {
    this.listeners = {};
  }
  /** Emit an event */
  emit(e, ...t) {
    this.listeners[e] && this.listeners[e].forEach((r) => r(...t));
  }
}
class za extends Ge {
  /** Create a plugin instance */
  constructor(e) {
    super(), this.subscriptions = [], this.options = e;
  }
  /** Called after this.wavesurfer is available */
  onInit() {
  }
  /** Do not call directly, only called by WavesSurfer internally */
  _init(e) {
    this.wavesurfer = e, this.onInit();
  }
  /** Destroy the plugin and unsubscribe from all events */
  destroy() {
    this.emit("destroy"), this.subscriptions.forEach((e) => e());
  }
}
var Ua = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
function Va(n, e) {
  return Ua(this, void 0, void 0, function* () {
    const t = new AudioContext({
      sampleRate: e
    });
    return t.decodeAudioData(n).finally(() => t.close());
  });
}
function Xa(n) {
  const e = n[0];
  if (e.some((t) => t > 1 || t < -1)) {
    const t = e.length;
    let r = 0;
    for (let i = 0; i < t; i++) {
      const o = Math.abs(e[i]);
      o > r && (r = o);
    }
    for (const i of n)
      for (let o = 0; o < t; o++)
        i[o] /= r;
  }
  return n;
}
function Ga(n, e) {
  return typeof n[0] == "number" && (n = [n]), Xa(n), {
    duration: e,
    length: n[0].length,
    sampleRate: n[0].length / e,
    numberOfChannels: n.length,
    getChannelData: (t) => n == null ? void 0 : n[t],
    copyFromChannel: AudioBuffer.prototype.copyFromChannel,
    copyToChannel: AudioBuffer.prototype.copyToChannel
  };
}
const it = {
  decode: Va,
  createBuffer: Ga
};
function qr(n, e) {
  const t = e.xmlns ? document.createElementNS(e.xmlns, n) : document.createElement(n);
  for (const [r, i] of Object.entries(e))
    if (r === "children")
      for (const [o, s] of Object.entries(e))
        typeof s == "string" ? t.appendChild(document.createTextNode(s)) : t.appendChild(qr(o, s));
    else r === "style" ? Object.assign(t.style, i) : r === "textContent" ? t.textContent = i : t.setAttribute(r, i.toString());
  return t;
}
function ir(n, e, t) {
  const r = qr(n, e || {});
  return t == null || t.appendChild(r), r;
}
const qa = /* @__PURE__ */ Object.freeze(/* @__PURE__ */ Object.defineProperty({
  __proto__: null,
  createElement: ir,
  default: ir
}, Symbol.toStringTag, {
  value: "Module"
}));
var ut = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
function Ka(n, e) {
  return ut(this, void 0, void 0, function* () {
    if (!n.body || !n.headers) return;
    const t = n.body.getReader(), r = Number(n.headers.get("Content-Length")) || 0;
    let i = 0;
    const o = (a) => ut(this, void 0, void 0, function* () {
      i += (a == null ? void 0 : a.length) || 0;
      const c = Math.round(i / r * 100);
      e(c);
    }), s = () => ut(this, void 0, void 0, function* () {
      let a;
      try {
        a = yield t.read();
      } catch {
        return;
      }
      a.done || (o(a.value), yield s());
    });
    s();
  });
}
function Ya(n, e, t) {
  return ut(this, void 0, void 0, function* () {
    const r = yield fetch(n, t);
    if (r.status >= 400)
      throw new Error(`Failed to fetch ${n}: ${r.status} (${r.statusText})`);
    return Ka(r.clone(), e), r.blob();
  });
}
const Za = {
  fetchBlob: Ya
};
var Qa = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
class Ja extends Ge {
  constructor(e) {
    super(), this.isExternalMedia = !1, e.media ? (this.media = e.media, this.isExternalMedia = !0) : this.media = document.createElement("audio"), e.mediaControls && (this.media.controls = !0), e.autoplay && (this.media.autoplay = !0), e.playbackRate != null && this.onMediaEvent("canplay", () => {
      e.playbackRate != null && (this.media.playbackRate = e.playbackRate);
    }, {
      once: !0
    });
  }
  onMediaEvent(e, t, r) {
    return this.media.addEventListener(e, t, r), () => this.media.removeEventListener(e, t, r);
  }
  getSrc() {
    return this.media.currentSrc || this.media.src || "";
  }
  revokeSrc() {
    const e = this.getSrc();
    e.startsWith("blob:") && URL.revokeObjectURL(e);
  }
  canPlayType(e) {
    return this.media.canPlayType(e) !== "";
  }
  setSrc(e, t) {
    const r = this.getSrc();
    if (e && r === e) return;
    this.revokeSrc();
    const i = t instanceof Blob && (this.canPlayType(t.type) || !e) ? URL.createObjectURL(t) : e;
    r && (this.media.src = "");
    try {
      this.media.src = i;
    } catch {
      this.media.src = e;
    }
  }
  destroy() {
    this.isExternalMedia || (this.media.pause(), this.media.remove(), this.revokeSrc(), this.media.src = "", this.media.load());
  }
  setMediaElement(e) {
    this.media = e;
  }
  /** Start playing the audio */
  play() {
    return Qa(this, void 0, void 0, function* () {
      return this.media.play();
    });
  }
  /** Pause the audio */
  pause() {
    this.media.pause();
  }
  /** Check if the audio is playing */
  isPlaying() {
    return !this.media.paused && !this.media.ended;
  }
  /** Jump to a specific time in the audio (in seconds) */
  setTime(e) {
    this.media.currentTime = Math.max(0, Math.min(e, this.getDuration()));
  }
  /** Get the duration of the audio in seconds */
  getDuration() {
    return this.media.duration;
  }
  /** Get the current audio position in seconds */
  getCurrentTime() {
    return this.media.currentTime;
  }
  /** Get the audio volume */
  getVolume() {
    return this.media.volume;
  }
  /** Set the audio volume */
  setVolume(e) {
    this.media.volume = e;
  }
  /** Get the audio muted state */
  getMuted() {
    return this.media.muted;
  }
  /** Mute or unmute the audio */
  setMuted(e) {
    this.media.muted = e;
  }
  /** Get the playback speed */
  getPlaybackRate() {
    return this.media.playbackRate;
  }
  /** Check if the audio is seeking */
  isSeeking() {
    return this.media.seeking;
  }
  /** Set the playback speed, pass an optional false to NOT preserve the pitch */
  setPlaybackRate(e, t) {
    t != null && (this.media.preservesPitch = t), this.media.playbackRate = e;
  }
  /** Get the HTML media element */
  getMediaElement() {
    return this.media;
  }
  /** Set a sink id to change the audio output device */
  setSinkId(e) {
    return this.media.setSinkId(e);
  }
}
function el(n, e, t, r, i = 3, o = 0, s = 100) {
  if (!n) return () => {
  };
  const a = matchMedia("(pointer: coarse)").matches;
  let c = () => {
  };
  const l = (u) => {
    if (u.button !== o) return;
    u.preventDefault(), u.stopPropagation();
    let d = u.clientX, h = u.clientY, p = !1;
    const b = Date.now(), v = (y) => {
      if (y.preventDefault(), y.stopPropagation(), a && Date.now() - b < s) return;
      const _ = y.clientX, S = y.clientY, T = _ - d, E = S - h;
      if (p || Math.abs(T) > i || Math.abs(E) > i) {
        const P = n.getBoundingClientRect(), {
          left: O,
          top: D
        } = P;
        p || (t == null || t(d - O, h - D), p = !0), e(T, E, _ - O, S - D), d = _, h = S;
      }
    }, g = (y) => {
      if (p) {
        const _ = y.clientX, S = y.clientY, T = n.getBoundingClientRect(), {
          left: E,
          top: P
        } = T;
        r == null || r(_ - E, S - P);
      }
      c();
    }, m = (y) => {
      (!y.relatedTarget || y.relatedTarget === document.documentElement) && g(y);
    }, x = (y) => {
      p && (y.stopPropagation(), y.preventDefault());
    }, C = (y) => {
      p && y.preventDefault();
    };
    document.addEventListener("pointermove", v), document.addEventListener("pointerup", g), document.addEventListener("pointerout", m), document.addEventListener("pointercancel", m), document.addEventListener("touchmove", C, {
      passive: !1
    }), document.addEventListener("click", x, {
      capture: !0
    }), c = () => {
      document.removeEventListener("pointermove", v), document.removeEventListener("pointerup", g), document.removeEventListener("pointerout", m), document.removeEventListener("pointercancel", m), document.removeEventListener("touchmove", C), setTimeout(() => {
        document.removeEventListener("click", x, {
          capture: !0
        });
      }, 10);
    };
  };
  return n.addEventListener("pointerdown", l), () => {
    c(), n.removeEventListener("pointerdown", l);
  };
}
var or = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
}, tl = function(n, e) {
  var t = {};
  for (var r in n) Object.prototype.hasOwnProperty.call(n, r) && e.indexOf(r) < 0 && (t[r] = n[r]);
  if (n != null && typeof Object.getOwnPropertySymbols == "function") for (var i = 0, r = Object.getOwnPropertySymbols(n); i < r.length; i++)
    e.indexOf(r[i]) < 0 && Object.prototype.propertyIsEnumerable.call(n, r[i]) && (t[r[i]] = n[r[i]]);
  return t;
};
class ke extends Ge {
  constructor(e, t) {
    super(), this.timeouts = [], this.isScrollable = !1, this.audioData = null, this.resizeObserver = null, this.lastContainerWidth = 0, this.isDragging = !1, this.subscriptions = [], this.unsubscribeOnScroll = [], this.subscriptions = [], this.options = e;
    const r = this.parentFromOptionsContainer(e.container);
    this.parent = r;
    const [i, o] = this.initHtml();
    r.appendChild(i), this.container = i, this.scrollContainer = o.querySelector(".scroll"), this.wrapper = o.querySelector(".wrapper"), this.canvasWrapper = o.querySelector(".canvases"), this.progressWrapper = o.querySelector(".progress"), this.cursor = o.querySelector(".cursor"), t && o.appendChild(t), this.initEvents();
  }
  parentFromOptionsContainer(e) {
    let t;
    if (typeof e == "string" ? t = document.querySelector(e) : e instanceof HTMLElement && (t = e), !t)
      throw new Error("Container not found");
    return t;
  }
  initEvents() {
    const e = (t) => {
      const r = this.wrapper.getBoundingClientRect(), i = t.clientX - r.left, o = t.clientY - r.top, s = i / r.width, a = o / r.height;
      return [s, a];
    };
    if (this.wrapper.addEventListener("click", (t) => {
      const [r, i] = e(t);
      this.emit("click", r, i);
    }), this.wrapper.addEventListener("dblclick", (t) => {
      const [r, i] = e(t);
      this.emit("dblclick", r, i);
    }), (this.options.dragToSeek === !0 || typeof this.options.dragToSeek == "object") && this.initDrag(), this.scrollContainer.addEventListener("scroll", () => {
      const {
        scrollLeft: t,
        scrollWidth: r,
        clientWidth: i
      } = this.scrollContainer, o = t / r, s = (t + i) / r;
      this.emit("scroll", o, s, t, t + i);
    }), typeof ResizeObserver == "function") {
      const t = this.createDelay(100);
      this.resizeObserver = new ResizeObserver(() => {
        t().then(() => this.onContainerResize()).catch(() => {
        });
      }), this.resizeObserver.observe(this.scrollContainer);
    }
  }
  onContainerResize() {
    const e = this.parent.clientWidth;
    e === this.lastContainerWidth && this.options.height !== "auto" || (this.lastContainerWidth = e, this.reRender());
  }
  initDrag() {
    this.subscriptions.push(el(
      this.wrapper,
      // On drag
      (e, t, r) => {
        this.emit("drag", Math.max(0, Math.min(1, r / this.wrapper.getBoundingClientRect().width)));
      },
      // On start drag
      (e) => {
        this.isDragging = !0, this.emit("dragstart", Math.max(0, Math.min(1, e / this.wrapper.getBoundingClientRect().width)));
      },
      // On end drag
      (e) => {
        this.isDragging = !1, this.emit("dragend", Math.max(0, Math.min(1, e / this.wrapper.getBoundingClientRect().width)));
      }
    ));
  }
  getHeight(e, t) {
    var r;
    const o = ((r = this.audioData) === null || r === void 0 ? void 0 : r.numberOfChannels) || 1;
    if (e == null) return 128;
    if (!isNaN(Number(e))) return Number(e);
    if (e === "auto") {
      const s = this.parent.clientHeight || 128;
      return t != null && t.every((a) => !a.overlay) ? s / o : s;
    }
    return 128;
  }
  initHtml() {
    const e = document.createElement("div"), t = e.attachShadow({
      mode: "open"
    }), r = this.options.cspNonce && typeof this.options.cspNonce == "string" ? this.options.cspNonce.replace(/"/g, "") : "";
    return t.innerHTML = `
      <style${r ? ` nonce="${r}"` : ""}>
        :host {
          user-select: none;
          min-width: 1px;
        }
        :host audio {
          display: block;
          width: 100%;
        }
        :host .scroll {
          overflow-x: auto;
          overflow-y: hidden;
          width: 100%;
          position: relative;
        }
        :host .noScrollbar {
          scrollbar-color: transparent;
          scrollbar-width: none;
        }
        :host .noScrollbar::-webkit-scrollbar {
          display: none;
          -webkit-appearance: none;
        }
        :host .wrapper {
          position: relative;
          overflow: visible;
          z-index: 2;
        }
        :host .canvases {
          min-height: ${this.getHeight(this.options.height, this.options.splitChannels)}px;
        }
        :host .canvases > div {
          position: relative;
        }
        :host canvas {
          display: block;
          position: absolute;
          top: 0;
          image-rendering: pixelated;
        }
        :host .progress {
          pointer-events: none;
          position: absolute;
          z-index: 2;
          top: 0;
          left: 0;
          width: 0;
          height: 100%;
          overflow: hidden;
        }
        :host .progress > div {
          position: relative;
        }
        :host .cursor {
          pointer-events: none;
          position: absolute;
          z-index: 5;
          top: 0;
          left: 0;
          height: 100%;
          border-radius: 2px;
        }
      </style>

      <div class="scroll" part="scroll">
        <div class="wrapper" part="wrapper">
          <div class="canvases" part="canvases"></div>
          <div class="progress" part="progress"></div>
          <div class="cursor" part="cursor"></div>
        </div>
      </div>
    `, [e, t];
  }
  /** Wavesurfer itself calls this method. Do not call it manually. */
  setOptions(e) {
    if (this.options.container !== e.container) {
      const t = this.parentFromOptionsContainer(e.container);
      t.appendChild(this.container), this.parent = t;
    }
    (e.dragToSeek === !0 || typeof this.options.dragToSeek == "object") && this.initDrag(), this.options = e, this.reRender();
  }
  getWrapper() {
    return this.wrapper;
  }
  getWidth() {
    return this.scrollContainer.clientWidth;
  }
  getScroll() {
    return this.scrollContainer.scrollLeft;
  }
  setScroll(e) {
    this.scrollContainer.scrollLeft = e;
  }
  setScrollPercentage(e) {
    const {
      scrollWidth: t
    } = this.scrollContainer, r = t * e;
    this.setScroll(r);
  }
  destroy() {
    var e, t;
    this.subscriptions.forEach((r) => r()), this.container.remove(), (e = this.resizeObserver) === null || e === void 0 || e.disconnect(), (t = this.unsubscribeOnScroll) === null || t === void 0 || t.forEach((r) => r()), this.unsubscribeOnScroll = [];
  }
  createDelay(e = 10) {
    let t, r;
    const i = () => {
      t && clearTimeout(t), r && r();
    };
    return this.timeouts.push(i), () => new Promise((o, s) => {
      i(), r = s, t = setTimeout(() => {
        t = void 0, r = void 0, o();
      }, e);
    });
  }
  // Convert array of color values to linear gradient
  convertColorValues(e) {
    if (!Array.isArray(e)) return e || "";
    if (e.length < 2) return e[0] || "";
    const t = document.createElement("canvas"), r = t.getContext("2d"), i = t.height * (window.devicePixelRatio || 1), o = r.createLinearGradient(0, 0, 0, i), s = 1 / (e.length - 1);
    return e.forEach((a, c) => {
      const l = c * s;
      o.addColorStop(l, a);
    }), o;
  }
  getPixelRatio() {
    return Math.max(1, window.devicePixelRatio || 1);
  }
  renderBarWaveform(e, t, r, i) {
    const o = e[0], s = e[1] || e[0], a = o.length, {
      width: c,
      height: l
    } = r.canvas, u = l / 2, d = this.getPixelRatio(), h = t.barWidth ? t.barWidth * d : 1, p = t.barGap ? t.barGap * d : t.barWidth ? h / 2 : 0, b = t.barRadius || 0, v = c / (h + p) / a, g = b && "roundRect" in r ? "roundRect" : "rect";
    r.beginPath();
    let m = 0, x = 0, C = 0;
    for (let y = 0; y <= a; y++) {
      const _ = Math.round(y * v);
      if (_ > m) {
        const E = Math.round(x * u * i), P = Math.round(C * u * i), O = E + P || 1;
        let D = u - E;
        t.barAlign === "top" ? D = 0 : t.barAlign === "bottom" && (D = l - O), r[g](m * (h + p), D, h, O, b), m = _, x = 0, C = 0;
      }
      const S = Math.abs(o[y] || 0), T = Math.abs(s[y] || 0);
      S > x && (x = S), T > C && (C = T);
    }
    r.fill(), r.closePath();
  }
  renderLineWaveform(e, t, r, i) {
    const o = (s) => {
      const a = e[s] || e[0], c = a.length, {
        height: l
      } = r.canvas, u = l / 2, d = r.canvas.width / c;
      r.moveTo(0, u);
      let h = 0, p = 0;
      for (let b = 0; b <= c; b++) {
        const v = Math.round(b * d);
        if (v > h) {
          const m = Math.round(p * u * i) || 1, x = u + m * (s === 0 ? -1 : 1);
          r.lineTo(h, x), h = v, p = 0;
        }
        const g = Math.abs(a[b] || 0);
        g > p && (p = g);
      }
      r.lineTo(h, u);
    };
    r.beginPath(), o(0), o(1), r.fill(), r.closePath();
  }
  renderWaveform(e, t, r) {
    if (r.fillStyle = this.convertColorValues(t.waveColor), t.renderFunction) {
      t.renderFunction(e, r);
      return;
    }
    let i = t.barHeight || 1;
    if (t.normalize) {
      const o = Array.from(e[0]).reduce((s, a) => Math.max(s, Math.abs(a)), 0);
      i = o ? 1 / o : 1;
    }
    if (t.barWidth || t.barGap || t.barAlign) {
      this.renderBarWaveform(e, t, r, i);
      return;
    }
    this.renderLineWaveform(e, t, r, i);
  }
  renderSingleCanvas(e, t, r, i, o, s, a) {
    const c = this.getPixelRatio(), l = document.createElement("canvas");
    l.width = Math.round(r * c), l.height = Math.round(i * c), l.style.width = `${r}px`, l.style.height = `${i}px`, l.style.left = `${Math.round(o)}px`, s.appendChild(l);
    const u = l.getContext("2d");
    if (this.renderWaveform(e, t, u), l.width > 0 && l.height > 0) {
      const d = l.cloneNode(), h = d.getContext("2d");
      h.drawImage(l, 0, 0), h.globalCompositeOperation = "source-in", h.fillStyle = this.convertColorValues(t.progressColor), h.fillRect(0, 0, l.width, l.height), a.appendChild(d);
    }
  }
  renderMultiCanvas(e, t, r, i, o, s) {
    const a = this.getPixelRatio(), {
      clientWidth: c
    } = this.scrollContainer, l = r / a;
    let u = Math.min(ke.MAX_CANVAS_WIDTH, c, l), d = {};
    if (u === 0) return;
    if (t.barWidth || t.barGap) {
      const m = t.barWidth || 0.5, x = t.barGap || m / 2, C = m + x;
      u % C !== 0 && (u = Math.floor(u / C) * C);
    }
    const h = (m) => {
      if (m < 0 || m >= b || d[m]) return;
      d[m] = !0;
      const x = m * u, C = Math.min(l - x, u);
      if (C <= 0) return;
      const y = e.map((_) => {
        const S = Math.floor(x / l * _.length), T = Math.floor((x + C) / l * _.length);
        return _.slice(S, T);
      });
      this.renderSingleCanvas(y, t, C, i, x, o, s);
    }, p = () => {
      Object.keys(d).length > ke.MAX_NODES && (o.innerHTML = "", s.innerHTML = "", d = {});
    }, b = Math.ceil(l / u);
    if (!this.isScrollable) {
      for (let m = 0; m < b; m++)
        h(m);
      return;
    }
    const v = this.scrollContainer.scrollLeft / l, g = Math.floor(v * b);
    if (h(g - 1), h(g), h(g + 1), b > 1) {
      const m = this.on("scroll", () => {
        const {
          scrollLeft: x
        } = this.scrollContainer, C = Math.floor(x / l * b);
        p(), h(C - 1), h(C), h(C + 1);
      });
      this.unsubscribeOnScroll.push(m);
    }
  }
  renderChannel(e, t, r, i) {
    var {
      overlay: o
    } = t, s = tl(t, ["overlay"]);
    const a = document.createElement("div"), c = this.getHeight(s.height, s.splitChannels);
    a.style.height = `${c}px`, o && i > 0 && (a.style.marginTop = `-${c}px`), this.canvasWrapper.style.minHeight = `${c}px`, this.canvasWrapper.appendChild(a);
    const l = a.cloneNode();
    this.progressWrapper.appendChild(l), this.renderMultiCanvas(e, s, r, c, a, l);
  }
  render(e) {
    return or(this, void 0, void 0, function* () {
      var t;
      this.timeouts.forEach((c) => c()), this.timeouts = [], this.canvasWrapper.innerHTML = "", this.progressWrapper.innerHTML = "", this.options.width != null && (this.scrollContainer.style.width = typeof this.options.width == "number" ? `${this.options.width}px` : this.options.width);
      const r = this.getPixelRatio(), i = this.scrollContainer.clientWidth, o = Math.ceil(e.duration * (this.options.minPxPerSec || 0));
      this.isScrollable = o > i;
      const s = this.options.fillParent && !this.isScrollable, a = (s ? i : o) * r;
      if (this.wrapper.style.width = s ? "100%" : `${o}px`, this.scrollContainer.style.overflowX = this.isScrollable ? "auto" : "hidden", this.scrollContainer.classList.toggle("noScrollbar", !!this.options.hideScrollbar), this.cursor.style.backgroundColor = `${this.options.cursorColor || this.options.progressColor}`, this.cursor.style.width = `${this.options.cursorWidth}px`, this.audioData = e, this.emit("render"), this.options.splitChannels)
        for (let c = 0; c < e.numberOfChannels; c++) {
          const l = Object.assign(Object.assign({}, this.options), (t = this.options.splitChannels) === null || t === void 0 ? void 0 : t[c]);
          this.renderChannel([e.getChannelData(c)], l, a, c);
        }
      else {
        const c = [e.getChannelData(0)];
        e.numberOfChannels > 1 && c.push(e.getChannelData(1)), this.renderChannel(c, this.options, a, 0);
      }
      Promise.resolve().then(() => this.emit("rendered"));
    });
  }
  reRender() {
    if (this.unsubscribeOnScroll.forEach((r) => r()), this.unsubscribeOnScroll = [], !this.audioData) return;
    const {
      scrollWidth: e
    } = this.scrollContainer, {
      right: t
    } = this.progressWrapper.getBoundingClientRect();
    if (this.render(this.audioData), this.isScrollable && e !== this.scrollContainer.scrollWidth) {
      const {
        right: r
      } = this.progressWrapper.getBoundingClientRect();
      let i = r - t;
      i *= 2, i = i < 0 ? Math.floor(i) : Math.ceil(i), i /= 2, this.scrollContainer.scrollLeft += i;
    }
  }
  zoom(e) {
    this.options.minPxPerSec = e, this.reRender();
  }
  scrollIntoView(e, t = !1) {
    const {
      scrollLeft: r,
      scrollWidth: i,
      clientWidth: o
    } = this.scrollContainer, s = e * i, a = r, c = r + o, l = o / 2;
    if (this.isDragging)
      s + 30 > c ? this.scrollContainer.scrollLeft += 30 : s - 30 < a && (this.scrollContainer.scrollLeft -= 30);
    else {
      (s < a || s > c) && (this.scrollContainer.scrollLeft = s - (this.options.autoCenter ? l : 0));
      const u = s - r - l;
      t && this.options.autoCenter && u > 0 && (this.scrollContainer.scrollLeft += Math.min(u, 10));
    }
    {
      const u = this.scrollContainer.scrollLeft, d = u / i, h = (u + o) / i;
      this.emit("scroll", d, h, u, u + o);
    }
  }
  renderProgress(e, t) {
    if (isNaN(e)) return;
    const r = e * 100;
    this.canvasWrapper.style.clipPath = `polygon(${r}% 0, 100% 0, 100% 100%, ${r}% 100%)`, this.progressWrapper.style.width = `${r}%`, this.cursor.style.left = `${r}%`, this.cursor.style.transform = `translateX(-${Math.round(r) === 100 ? this.options.cursorWidth : 0}px)`, this.isScrollable && this.options.autoScroll && this.scrollIntoView(e, t);
  }
  exportImage(e, t, r) {
    return or(this, void 0, void 0, function* () {
      const i = this.canvasWrapper.querySelectorAll("canvas");
      if (!i.length)
        throw new Error("No waveform data");
      if (r === "dataURL") {
        const o = Array.from(i).map((s) => s.toDataURL(e, t));
        return Promise.resolve(o);
      }
      return Promise.all(Array.from(i).map((o) => new Promise((s, a) => {
        o.toBlob((c) => {
          c ? s(c) : a(new Error("Could not export image"));
        }, e, t);
      })));
    });
  }
}
ke.MAX_CANVAS_WIDTH = 8e3;
ke.MAX_NODES = 10;
class nl extends Ge {
  constructor() {
    super(...arguments), this.unsubscribe = () => {
    };
  }
  start() {
    this.unsubscribe = this.on("tick", () => {
      requestAnimationFrame(() => {
        this.emit("tick");
      });
    }), this.emit("tick");
  }
  stop() {
    this.unsubscribe();
  }
  destroy() {
    this.unsubscribe();
  }
}
var Vt = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
class Xt extends Ge {
  constructor(e = new AudioContext()) {
    super(), this.bufferNode = null, this.playStartTime = 0, this.playedDuration = 0, this._muted = !1, this._playbackRate = 1, this._duration = void 0, this.buffer = null, this.currentSrc = "", this.paused = !0, this.crossOrigin = null, this.seeking = !1, this.autoplay = !1, this.addEventListener = this.on, this.removeEventListener = this.un, this.audioContext = e, this.gainNode = this.audioContext.createGain(), this.gainNode.connect(this.audioContext.destination);
  }
  load() {
    return Vt(this, void 0, void 0, function* () {
    });
  }
  get src() {
    return this.currentSrc;
  }
  set src(e) {
    if (this.currentSrc = e, this._duration = void 0, !e) {
      this.buffer = null, this.emit("emptied");
      return;
    }
    fetch(e).then((t) => {
      if (t.status >= 400)
        throw new Error(`Failed to fetch ${e}: ${t.status} (${t.statusText})`);
      return t.arrayBuffer();
    }).then((t) => this.currentSrc !== e ? null : this.audioContext.decodeAudioData(t)).then((t) => {
      this.currentSrc === e && (this.buffer = t, this.emit("loadedmetadata"), this.emit("canplay"), this.autoplay && this.play());
    });
  }
  _play() {
    var e;
    if (!this.paused) return;
    this.paused = !1, (e = this.bufferNode) === null || e === void 0 || e.disconnect(), this.bufferNode = this.audioContext.createBufferSource(), this.buffer && (this.bufferNode.buffer = this.buffer), this.bufferNode.playbackRate.value = this._playbackRate, this.bufferNode.connect(this.gainNode);
    let t = this.playedDuration * this._playbackRate;
    (t >= this.duration || t < 0) && (t = 0, this.playedDuration = 0), this.bufferNode.start(this.audioContext.currentTime, t), this.playStartTime = this.audioContext.currentTime, this.bufferNode.onended = () => {
      this.currentTime >= this.duration && (this.pause(), this.emit("ended"));
    };
  }
  _pause() {
    var e;
    this.paused = !0, (e = this.bufferNode) === null || e === void 0 || e.stop(), this.playedDuration += this.audioContext.currentTime - this.playStartTime;
  }
  play() {
    return Vt(this, void 0, void 0, function* () {
      this.paused && (this._play(), this.emit("play"));
    });
  }
  pause() {
    this.paused || (this._pause(), this.emit("pause"));
  }
  stopAt(e) {
    const t = e - this.currentTime, r = this.bufferNode;
    r == null || r.stop(this.audioContext.currentTime + t), r == null || r.addEventListener("ended", () => {
      r === this.bufferNode && (this.bufferNode = null, this.pause());
    }, {
      once: !0
    });
  }
  setSinkId(e) {
    return Vt(this, void 0, void 0, function* () {
      return this.audioContext.setSinkId(e);
    });
  }
  get playbackRate() {
    return this._playbackRate;
  }
  set playbackRate(e) {
    this._playbackRate = e, this.bufferNode && (this.bufferNode.playbackRate.value = e);
  }
  get currentTime() {
    return (this.paused ? this.playedDuration : this.playedDuration + (this.audioContext.currentTime - this.playStartTime)) * this._playbackRate;
  }
  set currentTime(e) {
    const t = !this.paused;
    t && this._pause(), this.playedDuration = e / this._playbackRate, t && this._play(), this.emit("seeking"), this.emit("timeupdate");
  }
  get duration() {
    var e, t;
    return (e = this._duration) !== null && e !== void 0 ? e : ((t = this.buffer) === null || t === void 0 ? void 0 : t.duration) || 0;
  }
  set duration(e) {
    this._duration = e;
  }
  get volume() {
    return this.gainNode.gain.value;
  }
  set volume(e) {
    this.gainNode.gain.value = e, this.emit("volumechange");
  }
  get muted() {
    return this._muted;
  }
  set muted(e) {
    this._muted !== e && (this._muted = e, this._muted ? this.gainNode.disconnect() : this.gainNode.connect(this.audioContext.destination));
  }
  canPlayType(e) {
    return /^(audio|video)\//.test(e);
  }
  /** Get the GainNode used to play the audio. Can be used to attach filters. */
  getGainNode() {
    return this.gainNode;
  }
  /** Get decoded audio */
  getChannelData() {
    const e = [];
    if (!this.buffer) return e;
    const t = this.buffer.numberOfChannels;
    for (let r = 0; r < t; r++)
      e.push(this.buffer.getChannelData(r));
    return e;
  }
}
var Oe = function(n, e, t, r) {
  function i(o) {
    return o instanceof t ? o : new t(function(s) {
      s(o);
    });
  }
  return new (t || (t = Promise))(function(o, s) {
    function a(u) {
      try {
        l(r.next(u));
      } catch (d) {
        s(d);
      }
    }
    function c(u) {
      try {
        l(r.throw(u));
      } catch (d) {
        s(d);
      }
    }
    function l(u) {
      u.done ? o(u.value) : i(u.value).then(a, c);
    }
    l((r = r.apply(n, e || [])).next());
  });
};
const rl = {
  waveColor: "#999",
  progressColor: "#555",
  cursorWidth: 1,
  minPxPerSec: 0,
  fillParent: !0,
  interact: !0,
  dragToSeek: !1,
  autoScroll: !0,
  autoCenter: !0,
  sampleRate: 8e3
};
class qe extends Ja {
  /** Create a new WaveSurfer instance */
  static create(e) {
    return new qe(e);
  }
  /** Create a new WaveSurfer instance */
  constructor(e) {
    const t = e.media || (e.backend === "WebAudio" ? new Xt() : void 0);
    super({
      media: t,
      mediaControls: e.mediaControls,
      autoplay: e.autoplay,
      playbackRate: e.audioRate
    }), this.plugins = [], this.decodedData = null, this.stopAtPosition = null, this.subscriptions = [], this.mediaSubscriptions = [], this.abortController = null, this.options = Object.assign({}, rl, e), this.timer = new nl();
    const r = t ? void 0 : this.getMediaElement();
    this.renderer = new ke(this.options, r), this.initPlayerEvents(), this.initRendererEvents(), this.initTimerEvents(), this.initPlugins();
    const i = this.options.url || this.getSrc() || "";
    Promise.resolve().then(() => {
      this.emit("init");
      const {
        peaks: o,
        duration: s
      } = this.options;
      (i || o && s) && this.load(i, o, s).catch(() => null);
    });
  }
  updateProgress(e = this.getCurrentTime()) {
    return this.renderer.renderProgress(e / this.getDuration(), this.isPlaying()), e;
  }
  initTimerEvents() {
    this.subscriptions.push(this.timer.on("tick", () => {
      if (!this.isSeeking()) {
        const e = this.updateProgress();
        this.emit("timeupdate", e), this.emit("audioprocess", e), this.stopAtPosition != null && this.isPlaying() && e >= this.stopAtPosition && this.pause();
      }
    }));
  }
  initPlayerEvents() {
    this.isPlaying() && (this.emit("play"), this.timer.start()), this.mediaSubscriptions.push(this.onMediaEvent("timeupdate", () => {
      const e = this.updateProgress();
      this.emit("timeupdate", e);
    }), this.onMediaEvent("play", () => {
      this.emit("play"), this.timer.start();
    }), this.onMediaEvent("pause", () => {
      this.emit("pause"), this.timer.stop(), this.stopAtPosition = null;
    }), this.onMediaEvent("emptied", () => {
      this.timer.stop(), this.stopAtPosition = null;
    }), this.onMediaEvent("ended", () => {
      this.emit("timeupdate", this.getDuration()), this.emit("finish"), this.stopAtPosition = null;
    }), this.onMediaEvent("seeking", () => {
      this.emit("seeking", this.getCurrentTime());
    }), this.onMediaEvent("error", () => {
      var e;
      this.emit("error", (e = this.getMediaElement().error) !== null && e !== void 0 ? e : new Error("Media error")), this.stopAtPosition = null;
    }));
  }
  initRendererEvents() {
    this.subscriptions.push(
      // Seek on click
      this.renderer.on("click", (e, t) => {
        this.options.interact && (this.seekTo(e), this.emit("interaction", e * this.getDuration()), this.emit("click", e, t));
      }),
      // Double click
      this.renderer.on("dblclick", (e, t) => {
        this.emit("dblclick", e, t);
      }),
      // Scroll
      this.renderer.on("scroll", (e, t, r, i) => {
        const o = this.getDuration();
        this.emit("scroll", e * o, t * o, r, i);
      }),
      // Redraw
      this.renderer.on("render", () => {
        this.emit("redraw");
      }),
      // RedrawComplete
      this.renderer.on("rendered", () => {
        this.emit("redrawcomplete");
      }),
      // DragStart
      this.renderer.on("dragstart", (e) => {
        this.emit("dragstart", e);
      }),
      // DragEnd
      this.renderer.on("dragend", (e) => {
        this.emit("dragend", e);
      })
    );
    {
      let e;
      this.subscriptions.push(this.renderer.on("drag", (t) => {
        if (!this.options.interact) return;
        this.renderer.renderProgress(t), clearTimeout(e);
        let r;
        this.isPlaying() ? r = 0 : this.options.dragToSeek === !0 ? r = 200 : typeof this.options.dragToSeek == "object" && this.options.dragToSeek !== void 0 && (r = this.options.dragToSeek.debounceTime), e = setTimeout(() => {
          this.seekTo(t);
        }, r), this.emit("interaction", t * this.getDuration()), this.emit("drag", t);
      }));
    }
  }
  initPlugins() {
    var e;
    !((e = this.options.plugins) === null || e === void 0) && e.length && this.options.plugins.forEach((t) => {
      this.registerPlugin(t);
    });
  }
  unsubscribePlayerEvents() {
    this.mediaSubscriptions.forEach((e) => e()), this.mediaSubscriptions = [];
  }
  /** Set new wavesurfer options and re-render it */
  setOptions(e) {
    this.options = Object.assign({}, this.options, e), e.duration && !e.peaks && (this.decodedData = it.createBuffer(this.exportPeaks(), e.duration)), e.peaks && e.duration && (this.decodedData = it.createBuffer(e.peaks, e.duration)), this.renderer.setOptions(this.options), e.audioRate && this.setPlaybackRate(e.audioRate), e.mediaControls != null && (this.getMediaElement().controls = e.mediaControls);
  }
  /** Register a wavesurfer.js plugin */
  registerPlugin(e) {
    return e._init(this), this.plugins.push(e), this.subscriptions.push(e.once("destroy", () => {
      this.plugins = this.plugins.filter((t) => t !== e);
    })), e;
  }
  /** For plugins only: get the waveform wrapper div */
  getWrapper() {
    return this.renderer.getWrapper();
  }
  /** For plugins only: get the scroll container client width */
  getWidth() {
    return this.renderer.getWidth();
  }
  /** Get the current scroll position in pixels */
  getScroll() {
    return this.renderer.getScroll();
  }
  /** Set the current scroll position in pixels */
  setScroll(e) {
    return this.renderer.setScroll(e);
  }
  /** Move the start of the viewing window to a specific time in the audio (in seconds) */
  setScrollTime(e) {
    const t = e / this.getDuration();
    this.renderer.setScrollPercentage(t);
  }
  /** Get all registered plugins */
  getActivePlugins() {
    return this.plugins;
  }
  loadAudio(e, t, r, i) {
    return Oe(this, void 0, void 0, function* () {
      var o;
      if (this.emit("load", e), !this.options.media && this.isPlaying() && this.pause(), this.decodedData = null, this.stopAtPosition = null, !t && !r) {
        const a = this.options.fetchParams || {};
        window.AbortController && !a.signal && (this.abortController = new AbortController(), a.signal = (o = this.abortController) === null || o === void 0 ? void 0 : o.signal);
        const c = (u) => this.emit("loading", u);
        t = yield Za.fetchBlob(e, c, a);
        const l = this.options.blobMimeType;
        l && (t = new Blob([t], {
          type: l
        }));
      }
      this.setSrc(e, t);
      const s = yield new Promise((a) => {
        const c = i || this.getDuration();
        c ? a(c) : this.mediaSubscriptions.push(this.onMediaEvent("loadedmetadata", () => a(this.getDuration()), {
          once: !0
        }));
      });
      if (!e && !t) {
        const a = this.getMediaElement();
        a instanceof Xt && (a.duration = s);
      }
      if (r)
        this.decodedData = it.createBuffer(r, s || 0);
      else if (t) {
        const a = yield t.arrayBuffer();
        this.decodedData = yield it.decode(a, this.options.sampleRate);
      }
      this.decodedData && (this.emit("decode", this.getDuration()), this.renderer.render(this.decodedData)), this.emit("ready", this.getDuration());
    });
  }
  /** Load an audio file by URL, with optional pre-decoded audio data */
  load(e, t, r) {
    return Oe(this, void 0, void 0, function* () {
      try {
        return yield this.loadAudio(e, void 0, t, r);
      } catch (i) {
        throw this.emit("error", i), i;
      }
    });
  }
  /** Load an audio blob */
  loadBlob(e, t, r) {
    return Oe(this, void 0, void 0, function* () {
      try {
        return yield this.loadAudio("", e, t, r);
      } catch (i) {
        throw this.emit("error", i), i;
      }
    });
  }
  /** Zoom the waveform by a given pixels-per-second factor */
  zoom(e) {
    if (!this.decodedData)
      throw new Error("No audio loaded");
    this.renderer.zoom(e), this.emit("zoom", e);
  }
  /** Get the decoded audio data */
  getDecodedData() {
    return this.decodedData;
  }
  /** Get decoded peaks */
  exportPeaks({
    channels: e = 2,
    maxLength: t = 8e3,
    precision: r = 1e4
  } = {}) {
    if (!this.decodedData)
      throw new Error("The audio has not been decoded yet");
    const i = Math.min(e, this.decodedData.numberOfChannels), o = [];
    for (let s = 0; s < i; s++) {
      const a = this.decodedData.getChannelData(s), c = [], l = a.length / t;
      for (let u = 0; u < t; u++) {
        const d = a.slice(Math.floor(u * l), Math.ceil((u + 1) * l));
        let h = 0;
        for (let p = 0; p < d.length; p++) {
          const b = d[p];
          Math.abs(b) > Math.abs(h) && (h = b);
        }
        c.push(Math.round(h * r) / r);
      }
      o.push(c);
    }
    return o;
  }
  /** Get the duration of the audio in seconds */
  getDuration() {
    let e = super.getDuration() || 0;
    return (e === 0 || e === 1 / 0) && this.decodedData && (e = this.decodedData.duration), e;
  }
  /** Toggle if the waveform should react to clicks */
  toggleInteraction(e) {
    this.options.interact = e;
  }
  /** Jump to a specific time in the audio (in seconds) */
  setTime(e) {
    this.stopAtPosition = null, super.setTime(e), this.updateProgress(e), this.emit("timeupdate", e);
  }
  /** Seek to a percentage of audio as [0..1] (0 = beginning, 1 = end) */
  seekTo(e) {
    const t = this.getDuration() * e;
    this.setTime(t);
  }
  /** Start playing the audio */
  play(e, t) {
    const r = Object.create(null, {
      play: {
        get: () => super.play
      }
    });
    return Oe(this, void 0, void 0, function* () {
      e != null && this.setTime(e);
      const i = yield r.play.call(this);
      return t != null && (this.media instanceof Xt ? this.media.stopAt(t) : this.stopAtPosition = t), i;
    });
  }
  /** Play or pause the audio */
  playPause() {
    return Oe(this, void 0, void 0, function* () {
      return this.isPlaying() ? this.pause() : this.play();
    });
  }
  /** Stop the audio and go to the beginning */
  stop() {
    this.pause(), this.setTime(0);
  }
  /** Skip N or -N seconds from the current position */
  skip(e) {
    this.setTime(this.getCurrentTime() + e);
  }
  /** Empty the waveform */
  empty() {
    this.load("", [[0]], 1e-3);
  }
  /** Set HTML media element */
  setMediaElement(e) {
    this.unsubscribePlayerEvents(), super.setMediaElement(e), this.initPlayerEvents();
  }
  exportImage() {
    return Oe(this, arguments, void 0, function* (e = "image/png", t = 1, r = "dataURL") {
      return this.renderer.exportImage(e, t, r);
    });
  }
  /** Unmount wavesurfer */
  destroy() {
    var e;
    this.emit("destroy"), (e = this.abortController) === null || e === void 0 || e.abort(), this.plugins.forEach((t) => t.destroy()), this.subscriptions.forEach((t) => t()), this.unsubscribePlayerEvents(), this.timer.destroy(), this.renderer.destroy(), super.destroy();
  }
}
qe.BasePlugin = za;
qe.dom = qa;
function il({
  container: n,
  onStop: e
}) {
  const t = he(null), [r, i] = Ie(!1), o = ct(() => {
    var c;
    (c = t.current) == null || c.startRecording();
  }), s = ct(() => {
    var c;
    (c = t.current) == null || c.stopRecording();
  }), a = ct(e);
  return xe(() => {
    if (n) {
      const l = qe.create({
        normalize: !1,
        container: n
      }).registerPlugin(pn.create());
      t.current = l, l.on("record-start", () => {
        i(!0);
      }), l.on("record-end", (u) => {
        a(u), i(!1);
      });
    }
  }, [n, a]), {
    recording: r,
    start: o,
    stop: s
  };
}
function ol(n) {
  const e = function(a, c, l) {
    for (let u = 0; u < l.length; u++)
      a.setUint8(c + u, l.charCodeAt(u));
  }, t = n.numberOfChannels, r = n.length * t * 2 + 44, i = new ArrayBuffer(r), o = new DataView(i);
  let s = 0;
  e(o, s, "RIFF"), s += 4, o.setUint32(s, r - 8, !0), s += 4, e(o, s, "WAVE"), s += 4, e(o, s, "fmt "), s += 4, o.setUint32(s, 16, !0), s += 4, o.setUint16(s, 1, !0), s += 2, o.setUint16(s, t, !0), s += 2, o.setUint32(s, n.sampleRate, !0), s += 4, o.setUint32(s, n.sampleRate * 2 * t, !0), s += 4, o.setUint16(s, t * 2, !0), s += 2, o.setUint16(s, 16, !0), s += 2, e(o, s, "data"), s += 4, o.setUint32(s, n.length * t * 2, !0), s += 4;
  for (let a = 0; a < n.numberOfChannels; a++) {
    const c = n.getChannelData(a);
    for (let l = 0; l < c.length; l++)
      o.setInt16(s, c[l] * 65535, !0), s += 2;
  }
  return new Uint8Array(i);
}
async function sl(n, e, t) {
  const r = await n.arrayBuffer(), o = await new AudioContext().decodeAudioData(r), s = new AudioContext(), a = o.numberOfChannels, c = o.sampleRate;
  let l = o.length, u = 0;
  const d = s.createBuffer(a, l, c);
  for (let h = 0; h < a; h++) {
    const p = o.getChannelData(h), b = d.getChannelData(h);
    for (let v = 0; v < l; v++)
      b[v] = p[u + v];
  }
  return Promise.resolve(ol(d));
}
const al = (n) => !!n.name, ze = (n) => {
  var e;
  return {
    text: (n == null ? void 0 : n.text) || "",
    files: ((e = n == null ? void 0 : n.files) == null ? void 0 : e.map((t) => t.path)) || []
  };
}, ul = _o(({
  onValueChange: n,
  onChange: e,
  onPasteFile: t,
  onUpload: r,
  onSubmit: i,
  onRemove: o,
  onDownload: s,
  onDrop: a,
  onPreview: c,
  upload: l,
  onCancel: u,
  children: d,
  readOnly: h,
  loading: p,
  disabled: b,
  placeholder: v,
  elRef: g,
  slots: m,
  // setSlotParams,
  uploadConfig: x,
  value: C,
  ...y
}) => {
  const [_, S] = Ie(!1), T = ui(), E = he(null), [P, O] = Ie(!1), D = rr(y.actions, !0), k = rr(y.footer, !0), {
    start: N,
    stop: F,
    recording: L
  } = il({
    container: E.current,
    async onStop(j) {
      const A = new File([await sl(j)], `${Date.now()}_recording_result.wav`, {
        type: "audio/wav"
      });
      de(A);
    }
  }), [M, z] = Fa({
    onValueChange: n,
    value: C
  }), w = Gt(() => ai(x), [x]), ce = b || (w == null ? void 0 : w.disabled) || p || h || P, de = ct(async (j) => {
    try {
      if (ce)
        return;
      O(!0);
      const A = w == null ? void 0 : w.maxCount;
      if (typeof A == "number" && A > 0 && U.length >= A)
        return;
      let H = Array.isArray(j) ? j : [j];
      if (A === 1)
        H = H.slice(0, 1);
      else if (H.length === 0) {
        O(!1);
        return;
      } else if (typeof A == "number") {
        const G = A - U.length;
        H = H.slice(0, G < 0 ? 0 : G);
      }
      const re = U, q = H.map((G) => ({
        ...G,
        size: G.size,
        uid: `${G.name}-${Date.now()}`,
        name: G.name,
        status: "uploading"
      }));
      B((G) => [...A === 1 ? [] : G, ...q]);
      const X = (await l(H)).filter(Boolean).map((G, ie) => ({
        ...G,
        uid: q[ie].uid
      })), pe = A === 1 ? X : [...re, ...X];
      r == null || r(X.map((G) => G.path)), O(!1);
      const fe = {
        ...M,
        files: pe
      };
      return e == null || e(ze(fe)), z(fe), X;
    } catch {
      return O(!1), [];
    }
  }), [U, B] = Ie(() => (M == null ? void 0 : M.files) || []);
  xe(() => {
    B((M == null ? void 0 : M.files) || []);
  }, [M == null ? void 0 : M.files]);
  const Q = Gt(() => {
    const j = {};
    return U.map((A) => {
      if (!al(A)) {
        const H = A.uid || A.url || A.path;
        return j[H] || (j[H] = 0), j[H]++, {
          ...A,
          name: A.orig_name || A.path,
          uid: A.uid || H + "-" + j[H],
          status: "done"
        };
      }
      return A;
    }) || [];
  }, [U]), V = (w == null ? void 0 : w.allowUpload) ?? !0, J = V ? w == null ? void 0 : w.allowSpeech : !1, oe = V ? w == null ? void 0 : w.allowPasteFile : !1;
  return /* @__PURE__ */ te.jsxs(te.Fragment, {
    children: [/* @__PURE__ */ te.jsx("div", {
      style: {
        display: "none"
      },
      ref: E
    }), /* @__PURE__ */ te.jsx("div", {
      style: {
        display: "none"
      },
      children: d
    }), /* @__PURE__ */ te.jsx(ln, {
      ...y,
      value: M == null ? void 0 : M.text,
      ref: g,
      disabled: b,
      readOnly: h,
      allowSpeech: J ? {
        recording: L,
        onRecordingChange(j) {
          ce || (j ? N() : F());
        }
      } : !1,
      placeholder: v,
      loading: p,
      onSubmit: () => {
        T || i == null || i(ze(M));
      },
      onCancel: () => {
        u == null || u();
      },
      onChange: (j) => {
        const A = {
          ...M,
          text: j
        };
        e == null || e(ze(A)), z(A);
      },
      onPasteFile: async (j, A) => {
        if (!(oe ?? !0))
          return;
        const H = await de(Array.from(A));
        H && (t == null || t(H.map((re) => re.path)));
      },
      prefix: /* @__PURE__ */ te.jsxs(te.Fragment, {
        children: [V ? /* @__PURE__ */ te.jsx(Ii, {
          title: w == null ? void 0 : w.uploadButtonTooltip,
          children: /* @__PURE__ */ te.jsx(Di, {
            count: ((w == null ? void 0 : w.showCount) ?? !0) && !_ ? Q.length : 0,
            children: /* @__PURE__ */ te.jsx(De, {
              onClick: () => {
                S(!_);
              },
              color: "default",
              variant: "text",
              icon: /* @__PURE__ */ te.jsx(Mi, {})
            })
          })
        }) : null, m.prefix ? /* @__PURE__ */ te.jsx(Ke, {
          slot: m.prefix
        }) : null]
      }),
      actions: m.actions ? /* @__PURE__ */ te.jsx(Ke, {
        slot: m.actions
      }) : D || y.actions,
      footer: m.footer ? /* @__PURE__ */ te.jsx(Ke, {
        slot: m.footer
      }) : k || y.footer,
      header: V ? /* @__PURE__ */ te.jsx(ln.Header, {
        title: (w == null ? void 0 : w.title) || "Attachments",
        open: _,
        onOpenChange: S,
        children: /* @__PURE__ */ te.jsx(Hr, {
          ...ja(li(w, ["title", "placeholder", "showCount", "buttonTooltip", "allowPasteFile"])),
          imageProps: {
            ...w == null ? void 0 : w.imageProps
          },
          disabled: ce,
          getDropContainer: () => w != null && w.fullscreenDrop ? document.body : null,
          items: Q,
          placeholder: (j) => {
            var H, re, q, X, pe, fe, G, ie, be, K, we, Ee;
            const A = j === "drop";
            return {
              title: A ? ((re = (H = w == null ? void 0 : w.placeholder) == null ? void 0 : H.drop) == null ? void 0 : re.title) ?? "Drop file here" : ((X = (q = w == null ? void 0 : w.placeholder) == null ? void 0 : q.inline) == null ? void 0 : X.title) ?? "Upload files",
              description: A ? ((fe = (pe = w == null ? void 0 : w.placeholder) == null ? void 0 : pe.drop) == null ? void 0 : fe.description) ?? void 0 : ((ie = (G = w == null ? void 0 : w.placeholder) == null ? void 0 : G.inline) == null ? void 0 : ie.description) ?? "Click or drag files to this area to upload",
              icon: A ? ((K = (be = w == null ? void 0 : w.placeholder) == null ? void 0 : be.drop) == null ? void 0 : K.icon) ?? void 0 : ((Ee = (we = w == null ? void 0 : w.placeholder) == null ? void 0 : we.inline) == null ? void 0 : Ee.icon) ?? /* @__PURE__ */ te.jsx(Pi, {})
            };
          },
          onDownload: s,
          onPreview: c,
          onDrop: a,
          onChange: async (j) => {
            try {
              const A = j.file, H = j.fileList, re = Q.findIndex((q) => q.uid === A.uid);
              if (re !== -1) {
                if (ce)
                  return;
                o == null || o(A);
                const q = U.slice();
                q.splice(re, 1);
                const X = {
                  ...M,
                  files: q
                };
                z(X), e == null || e(ze(X));
              } else {
                if (ce)
                  return;
                O(!0);
                let q = H.filter((K) => K.status !== "done");
                const X = w == null ? void 0 : w.maxCount;
                if (X === 1)
                  q = q.slice(0, 1);
                else if (q.length === 0) {
                  O(!1);
                  return;
                } else if (typeof X == "number") {
                  const K = X - U.length;
                  q = q.slice(0, K < 0 ? 0 : K);
                }
                const pe = U, fe = q.map((K) => ({
                  ...K,
                  size: K.size,
                  uid: K.uid,
                  name: K.name,
                  status: "uploading"
                }));
                B((K) => [...X === 1 ? [] : K, ...fe]);
                const G = (await l(q.map((K) => K.originFileObj))).filter(Boolean).map((K, we) => ({
                  ...K,
                  uid: fe[we].uid
                })), ie = X === 1 ? G : [...pe, ...G];
                r == null || r(G.map((K) => K.path)), O(!1);
                const be = {
                  ...M,
                  files: ie
                };
                B(ie), n == null || n(be), e == null || e(ze(be));
              }
            } catch (A) {
              O(!1), console.error(A);
            }
          },
          customRequest: Gi
        })
      }) : m.header ? /* @__PURE__ */ te.jsx(Ke, {
        slot: m.header
      }) : y.header
    })]
  });
});
export {
  ul as MultimodalInput,
  ul as default
};
