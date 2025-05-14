# D:\SIMHousing4DG\SIMHousing4DG\__main__.py

import os
import copy
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rcParams

# ---------- Matplotlib 字体缓存重建 ----------
font_manager.fontManager = font_manager.FontManager()

# ---------- 字体加载 ----------
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
FONT_DIR  = os.path.join(BASE_DIR, "fonts")
FONT_FILE = "NotoSerifCJKsc-Black.otf"
font_path = os.path.join(FONT_DIR, FONT_FILE)

if os.path.isfile(font_path):
    font_manager.fontManager.addfont(font_path)
    font_prop = font_manager.FontProperties(fname=font_path)
    font_name = font_prop.get_name()
else:
    font_name = "sans-serif"

def apply_font():
    matplotlib.rcParams["font.family"] = font_name
    matplotlib.rcParams["axes.unicode_minus"] = False
    rcParams["legend.fontsize"] = 12
    rcParams["axes.titlesize"] = 14
    rcParams["axes.labelsize"] = 12

# ---------- Streamlit 页面配置 ----------
st.set_page_config(page_title="双梯度政策模拟器", layout="wide")
sns.set_style("whitegrid")

# ---------- 预设参数定义 ----------
PRESETS = {
    "保守": {"elasticity": 1.0, "MA_weight": 0.2, "alpha": 5.0,  "beta": 2.0},
    "中性": {"elasticity": 3.0, "MA_weight": 0.5, "alpha":10.0,  "beta": 5.0},
    "激进": {"elasticity": 5.0, "MA_weight": 0.8, "alpha":15.0,  "beta":10.0},
}

# 基线支出等级映射（固定为“中（中城）”）
BASE_EXP_MAP = {
    "低（小城）":  50000,
    "中（中城）": 200000,
    "高（大城）":1000000,
}

# ---------- 初始化参数 ----------
def initialize_parameters():
    income_groups = ["低收入", "中等收入", "高收入"]
    regions = ["核心区", "边缘区", "郊区"]
    initial_population = {
        "核心区": {"低收入": 30, "中等收入": 50, "高收入": 20},
        "边缘区": {"低收入": 40, "中等收入": 30, "高收入": 10},
        "郊区":   {"低收入": 50, "中等收入": 20, "高收入": 5},
    }
    HQG = {"核心区": 0.8, "边缘区": 0.6, "郊区": 0.4}
    SGI = {"核心区": 0.85, "边缘区": 0.65, "郊区": 0.35}
    base_PIR = {"低收入": 15, "中等收入": 8, "高收入": 4}
    preferences = {
        "低收入":   {"h": 0.4, "s": 0.4, "p": 0.2},
        "中等收入": {"h": 0.3, "s": 0.5, "p": 0.2},
        "高收入":   {"h": 0.2, "s": 0.5, "p": 0.3},
    }
    return income_groups, regions, initial_population, HQG, SGI, base_PIR, preferences

# ---------- 核心模型函数 ----------
def calculate_matching_utility(HQG_r, SGI_r, PIR_g, pref, MA_weight, group):
    h, s, p = pref["h"], pref["s"], pref["p"]
    gamma = 0.15
    delta = 0.2 if group == "中等收入" else 0.0
    return (
        h * HQG_r +
        s * SGI_r -
        p * PIR_g -
        MA_weight * abs(HQG_r - SGI_r) +
        gamma * HQG_r * SGI_r +
        delta * HQG_r ** 2
    )

def generate_utility_table(groups, regions, HQG, SGI, base_PIR, prefs,
                           MA_weight, pop, theta, beta_sgi):
    total_pop = sum(sum(pop[r].values()) for r in pop) or 1e-6
    rows = []
    for r in regions:
        pop_r = sum(pop[r].values())
        SGI_eff = SGI[r] / (1 + beta_sgi * pop_r**1.5)
        for g in groups:
            share = pop_r / total_pop
            PIR_adj = base_PIR[g] * (1 + theta * share**1.2)
            raw_mu = calculate_matching_utility(
                HQG[r], SGI_eff, PIR_adj, prefs[g], MA_weight, g
            )
            rows.append({"区域": r, "收入组": g, "raw_MU": raw_mu})
    df = pd.DataFrame(rows)
    mn, mx = df["raw_MU"].min(), df["raw_MU"].max()
    df["MU"] = 0.5 if mn == mx else (df["raw_MU"] - mn) / (mx - mn)
    return df

def compute_migration_index(util_df, base_PIR, elasticity):
    dfs = []
    for g in base_PIR:
        df = util_df[util_df["收入组"] == g].copy()
        df["MI"] = (df["MU"] / base_PIR[g] * elasticity).clip(lower=0)
        tot = df["MI"].sum() or 1e-6
        df["MI_Share"] = df["MI"] / tot
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def simulate_population_migration(prev_pop, mi_df, base_PIR, retention_rate):
    groups  = list(base_PIR.keys())
    regions = list(prev_pop.keys())
    new_pop = {r: {g: 0.0 for g in groups} for r in regions}
    for g in groups:
        shares = mi_df[mi_df["收入组"] == g].set_index("区域")["MI_Share"].to_dict()
        for origin in regions:
            origin_pop = prev_pop[origin][g]
            retained   = origin_pop * retention_rate
            movable    = origin_pop * (1 - retention_rate)
            for dest in regions:
                new_pop[dest][g] += (retained if dest == origin else 0) + movable * shares.get(dest, 0)
    for r in regions:
        for g in groups:
            new_pop[r][g] = round(new_pop[r][g], 2)
    return new_pop

def compute_fiscal_expenditure(prev_pop, new_pop, util_df, base_PIR,
                               alpha, beta, base_exp):
    recs = []
    for r in prev_pop:
        for g in base_PIR:
            delta = max(new_pop[r][g] - prev_pop[r][g], 0)
            mu    = util_df.query("区域==@r & 收入组==@g")["MU"].iat[0]
            fiscal = base_exp + alpha * delta + beta * (1 - mu)
            recs.append({
                "区域": r, "收入组": g,
                "新增人口": delta, "MU": mu,
                "财政支出": round(fiscal, 2)
            })
    return pd.DataFrame(recs)

def apply_policy_scenario(HQG, SGI, sc):
    H, S = HQG.copy(), SGI.copy()
    if sc in ["B", "D"]:
        H = {r: min(H[r] + 0.15, 1.0) for r in H}
    if sc in ["C", "D"]:
        S = {r: min(S[r] + 0.20, 1.0) for r in S}
    return H, S

def run_simulation(scenario, periods, MA_w, elasticity,
                   alpha, beta, theta, beta_sgi,
                   retention_rate, base_exp):
    groups, regions, init_pop, HQG0, SGI0, base_PIR, prefs = initialize_parameters()
    pop = copy.deepcopy(init_pop)
    HQG_cur, SGI_cur = HQG0.copy(), SGI0.copy()
    results = []
    for t in range(1, periods + 1):
        HQG_cur, SGI_cur = apply_policy_scenario(HQG_cur, SGI_cur, scenario)
        util_df = generate_utility_table(
            groups, regions, HQG_cur, SGI_cur,
            base_PIR, prefs, MA_w, pop, theta, beta_sgi
        )
        mi_df   = compute_migration_index(util_df, base_PIR, elasticity)
        new_pop = simulate_population_migration(pop, mi_df, base_PIR, retention_rate)
        fiscal  = compute_fiscal_expenditure(
            pop, new_pop, util_df, base_PIR, alpha, beta, base_exp
        )
        results.append({
            "period": t,
            "population": new_pop,
            "utility_df": util_df,
            "fiscal_df": fiscal
        })
        pop = new_pop
    return results

# ---------- 可视化函数 ----------
def create_matching_utility_fig(df):
    apply_font()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=df, x="区域", y="MU", hue="收入组", ax=ax)
    ax.set_ylabel("匹配效用 (归一化)")
    ax.set_title("匹配效用分布")
    ax.set_xlabel("")
    ax.legend(
        title=None,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=3
    )
    plt.tight_layout()
    return fig

def create_population_change_fig(prev_pop, new_pop):
    apply_font()
    regs   = list(prev_pop.keys())
    groups = list(prev_pop[regs[0]].keys())
    x      = np.arange(len(regs))
    w      = 0.25
    fig, ax = plt.subplots(figsize=(6, 4))
    for i, g in enumerate(groups):
        ax.bar(x + i*w,     [prev_pop[r][g] for r in regs], w, label=f"{g}（期初）")
        ax.bar(x + i*w + w, [new_pop[r][g] for r in regs], w, alpha=0.7, label=f"{g}（期末）")
    ax.set_xticks(x + w)
    ax.set_xticklabels(regs)
    ax.set_ylabel("人口（万人）")
    ax.set_title("人口结构变化")
    ax.legend(title="收入组", frameon=False,
              loc="upper center", bbox_to_anchor=(0.5, -0.15),
              ncol=len(groups))
    plt.tight_layout()
    return fig

def create_fiscal_radar_fig(df, region):
    apply_font()
    data_keys = ["财政支出", "新增人口", "MU"]
    display_labels = ["财政支出", "新增人口", "匹配效用"]
    angles = np.linspace(0, 2 * np.pi, len(data_keys), endpoint=False).tolist()
    angles += angles[:1]

    max_vals = {k: df[k].max() for k in data_keys}
    min_vals = {k: df[k].min() for k in data_keys}
    for k in data_keys:
        if max_vals[k] == min_vals[k]:
            max_vals[k] += 1  # 避免除以0

    sub = df[df["区域"] == region]
    raw_vals = {k: sub[k].mean() for k in data_keys}

    norm_vals = [
        ((raw_vals[k] - min_vals[k]) / (max_vals[k] - min_vals[k] + 1e-6)) ** 0.7
        for k in data_keys
    ]
    norm_vals += norm_vals[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.plot(angles, norm_vals, linewidth=2)
    ax.fill(angles, norm_vals, alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(display_labels)
    ax.set_title(f"{region} 财政雷达图", y=1.1)
    ax.set_yticklabels([])
    ax.set_ylim(0, 1)
    plt.tight_layout()
    return fig

# ---------- 主程序入口 ----------
def main():
    st.title("🏘️ 住房—服务双梯度动态模拟平台")

    with st.sidebar:
        adv_mod = st.checkbox("高级模式：手动调整核心参数", False)

        if adv_mod:
            elasticity = st.slider("迁移弹性 elasticity", 0.1, 10.0, PRESETS["中性"]["elasticity"], 0.1)
            MA_weight = st.slider("惩罚权重 MA_weight", 0.0, 1.0, PRESETS["中性"]["MA_weight"], 0.05)
            alpha = st.slider("新增人口系数 α", 0.0, 20.0, PRESETS["中性"]["alpha"], 1.0)
            beta = st.slider("效用补偿系数 β", 0.0, 20.0, PRESETS["中性"]["beta"], 1.0)
        else:
            settings = PRESETS["中性"]
            elasticity = settings["elasticity"]
            MA_weight = settings["MA_weight"]
            alpha = settings["alpha"]
            beta = settings["beta"]

        theta = st.slider("房价收入比敏感度 θ", 0.0, 2.0, 0.5, 0.1)
        beta_sgi = st.slider("服务承载压力系数 β_sgi", 0.0, 1.0, 0.2, 0.05)
        retention_rate = st.slider("人口留存率 (年)", 0.5, 1.0, 0.9, 0.05)

        base_exp = BASE_EXP_MAP["中（中城）"]

        scenario = st.selectbox(
            "选择模拟情景",
            ["A：基准方案", "B：住房优化", "C：服务优化", "D：双协同优化"]
        )
        periods = st.slider("模拟期数（年）", 1, 20, 15)
        plot_each = st.checkbox("每年绘图", False)
        run_btn = st.button("🚀 开始模拟")

    if not run_btn:
        st.markdown("### 👈 请在左侧设置参数后点击“开始模拟”")
        st.markdown("""
        本模拟器用于探索住房–服务双梯度政策的系统影响。
        ✅ 左侧选择模拟参数与情景  
        ✅ 点击“开始模拟”查看匹配效用、人群迁移与财政支出变化  
        ✅ 可视化结果支持分区域对比，支持多期动态模拟
        """)
    else:
        code = scenario.split("：")[0]
        results = run_simulation(
            code, periods,
            MA_weight, elasticity,
            alpha, beta, theta, beta_sgi,
            retention_rate, base_exp
        )
        to_display = results if plot_each else [results[-1]]

        st.markdown("### 📊 模拟结果")
        tab_list = [f"第 {res['period']} 年" for res in to_display]
        tabs = st.tabs(tab_list)

        for i, res in enumerate(to_display):
            with tabs[i]:
                st.subheader(f"📅 第 {res['period']} 年模拟结果")
                col1, col2 = st.columns(2)
                with col1:
                    st.pyplot(create_matching_utility_fig(res["utility_df"]), use_container_width=True)
                with col2:
                    prev = results[res["period"] - 2]["population"] if res["period"] > 1 else res["population"]
                    st.pyplot(create_population_change_fig(prev, res["population"]), use_container_width=True)

                st.markdown("#### 各区域财政表现")
                r_cols = st.columns(3)
                for j, reg in enumerate(["核心区", "边缘区", "郊区"]):
                    r_cols[j].pyplot(create_fiscal_radar_fig(res["fiscal_df"], reg), use_container_width=True)

if __name__ == "__main__":
    main()
