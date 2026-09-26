import json
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# 1. 基础周历数据设定
start_date = datetime.date(2026, 8, 3)
week_labels = [
    "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8",
    "H1",
    "W9", "W10", "W11", "W12", "W13",
    "R1", "E1", "E2"
]
headers = ["周次", "周一", "周二", "周三", "周四", "周五", "周六", "周日"]
day_to_idx = {"周一": 0, "周二": 1, "周三": 2, "周四": 3, "周五": 4, "周六": 5, "周日": 6}


# 2. 读取配置文件
def load_assessments(filepath="assessments.txt"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


assessments = load_assessments("assessments.txt")

# 3. 课程专属高对比度色彩映射
unique_courses = list(dict.fromkeys([item["course"] for item in assessments]))
course_palette = ["#2980B9", "#16A085", "#8E44AD", "#D35400", "#C0392B", "#27AE60", "#2C3E50"]
course_color_map = {
    course: course_palette[i % len(course_palette)]
    for i, course in enumerate(unique_courses)
}

for item in assessments:
    item["color"] = course_color_map[item["course"]]


# 4. 周次解析逻辑
def parse_weeks(weeks_str, week_labels):
    active_indices = set()
    segments = [s.strip() for s in weeks_str.replace(";", ",").split(",") if s.strip()]

    for seg in segments:
        if "-" in seg:
            parts = [p.strip() for p in seg.split("-")]
            s_week, e_week = parts[0], parts[1]
            if s_week in week_labels and e_week in week_labels:
                s_idx = week_labels.index(s_week)
                e_idx = week_labels.index(e_week)
                for w_idx in range(s_idx, e_idx + 1):
                    label = week_labels[w_idx]
                    if s_week.startswith("W") and e_week.startswith("W"):
                        if label.startswith("H") or label.startswith("R"):
                            continue
                    active_indices.add(w_idx)
        else:
            if seg in week_labels:
                active_indices.add(week_labels.index(seg))

    return sorted(list(active_indices))


# 5. 事件映射
calendar_events = defaultdict(list)
for item in assessments:
    active_week_indices = parse_weeks(item["weeks"], week_labels)
    day_col = day_to_idx[item['day']]
    for w_idx in active_week_indices:
        calendar_events[(w_idx, day_col)].append(item)

# 6. 中文字体与渲染增强配置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'PingFang SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

num_weeks = len(week_labels)
num_cols = len(headers)

# 7. 创建超高清画布 (dpi=300, 扩大 figsize)
fig, ax = plt.subplots(figsize=(18, 18), dpi=300)

bg_colors = plt.colormaps['tab20'](np.linspace(0, 1, num_weeks))

# 8. 绘制表头
for j, h in enumerate(headers):
    rect = plt.Rectangle((j, num_weeks), 1, 0.7, facecolor='#1A252F', edgecolor='white', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(j + 0.5, num_weeks + 0.35, h, ha='center', va='center', fontsize=13, fontweight='bold', color='white')

# 9. 绘制日历网格
for i in range(num_weeks):
    row_y = num_weeks - 1 - i
    row_color = bg_colors[i]
    week_label = week_labels[i]

    # 周次标记列
    rect_label = plt.Rectangle((0, row_y), 1, 1, facecolor=row_color, edgecolor='white', linewidth=1.5, alpha=0.9)
    ax.add_patch(rect_label)
    ax.text(0.5, row_y + 0.5, week_label, ha='center', va='center', fontsize=12, fontweight='bold', color='black')

    # 每天单元格
    for j in range(7):
        current_date = start_date + datetime.timedelta(days=i * 7 + j)
        date_str = f"{current_date.month}/{current_date.day}"
        cell_x = j + 1

        cell_alpha = 0.12 if week_label == "H1" else 0.25
        rect = plt.Rectangle((cell_x, row_y), 1, 1, facecolor=row_color, edgecolor='white', linewidth=1.5,
                             alpha=cell_alpha)
        ax.add_patch(rect)

        ax.text(cell_x + 0.5, row_y + 0.86, date_str, ha='center', va='center', fontsize=9.5, color='#333333',
                fontweight='bold')

        # 渲染当天发生的考核事项
        day_items = calendar_events.get((i, j), [])
        n_items = len(day_items)

        if n_items > 0:
            avail_h = 0.72
            gap = 0.02
            item_h = (avail_h - (n_items - 1) * gap) / n_items

            for k, item in enumerate(day_items):
                item_y = row_y + 0.04 + (n_items - 1 - k) * (item_h + gap)

                badge = plt.Rectangle(
                    (cell_x + 0.04, item_y), 0.92, item_h,
                    facecolor=item['color'], edgecolor='white', linewidth=1.0, alpha=0.92, zorder=3
                )
                ax.add_patch(badge)

                if n_items == 1:
                    text_str = f"{item['course']}\n{item['type']} ({item['weight']})"
                    font_sz = 8.5
                else:
                    text_str = f"{item['course']} {item['type']}({item['weight']})"
                    font_sz = 7.5

                ax.text(
                    cell_x + 0.5, item_y + item_h / 2, text_str,
                    ha='center', va='center', fontsize=font_sz, fontweight='bold', color='white', zorder=4
                )

# 10. 底部图例与考核清单
legend_y_start = -0.4
# ax.text(0, legend_y_start, "📚 课程色彩图例与考核明细：", fontsize=13, fontweight='bold', color='#1A252F')

# for idx, (course_name, c_color) in enumerate(course_color_map.items()):
#     lx = 3.3 + (idx * 1.9)
#     ax.add_patch(plt.Rectangle((lx, legend_y_start - 0.08), 0.35, 0.16, facecolor=c_color))
#     ax.text(lx + 0.42, legend_y_start, course_name, fontsize=11, fontweight='bold', va='center', color='#222222')

for k, item in enumerate(assessments):
    card_y = legend_y_start - 0.4 - (k * 0.35)
    info_str = (
        f"【{item['course']}】 {item['type']}  |  周次：{item['weeks']} ({item['day']})  "
        f"|  占比：{item['weight']}  |  策略：{item['best_of']}"
    )
    ax.add_patch(plt.Rectangle((0, card_y - 0.09), 0.22, 0.22, facecolor=item['color'], zorder=3))
    ax.text(0.3, card_y, info_str, ha='left', va='center', fontsize=9.5, color='#222222')

ax.set_xlim(0, num_cols)
ax.set_ylim(-0.6 - len(assessments) * 0.35, num_weeks + 0.7)
ax.axis('off')

plt.title("2026 S2 学期日历 (300 DPI 超高清版本)", fontsize=18, fontweight='bold', pad=20)
plt.tight_layout()

# 11. 导出高分辨率图片文件
output_filename = "2026_S2_Academic_Calendar_HD.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"✅ 高清图片已成功保存至：{output_filename}")

plt.show()