from manim import *
import numpy as np, random

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_height = 16
config.frame_width = 9
config.frame_rate = 30
config.background_color = "#14151A"

ARM = "Noto Serif Armenian"; ARMS = "Noto Sans Armenian"; GRF = "Noto Serif"
BLUE_C3 = "#58C4DD"; YEL = "#F7D96F"; GRN = "#83C167"; RD = "#FC6255"; TL = "#5CD0B3"; GLD = "#F0AC5F"; GRY = "#6B6E78"
# scene start times (seconds) — same timeline as the Remotion versions, so one voice track fits all
T = dict(hook=0, etym=6.5, contest=13.5, masks=19.0, poet=22.5, temple=28.0, peri=31.5, cath=37.0, today=41.5, arch=47.0, logo=52.5, end=55.5)

def Brace2(m, color=WHITE):
    w = m.width; l = m.get_corner(DL) + DOWN * 0.15; r = m.get_corner(DR) + DOWN * 0.15; c = (l + r) / 2
    p = VMobject(color=color, stroke_width=5)
    p.set_points_smoothly([l, l + DOWN * 0.18 + RIGHT * 0.12, (l + c) / 2 + DOWN * 0.2, c + DOWN * 0.42 + LEFT * 0.02])
    q = VMobject(color=color, stroke_width=5)
    q.set_points_smoothly([r, r + DOWN * 0.18 + LEFT * 0.12, (r + c) / 2 + DOWN * 0.2, c + DOWN * 0.42 + RIGHT * 0.02])
    g = VGroup(p, q); g.tip = c + DOWN * 0.42; return g

def A(t, **kw):
    return Text(t, font=ARM, **kw)

class Lesson(Scene):
    def until(self, t):
        dt = t - self.renderer.time
        if dt > 0.02:
            self.wait(dt)

    def construct(self):
        # ---------- 1. Athens: 17 000 people ----------
        title = A("2500 տարի առաջ", weight=BOLD).scale(0.95).to_edge(UP, buff=1.3)
        sub = A("Աթենք · Դիոնիսոսի թատրոն", color=GRY).scale(0.42).next_to(title, DOWN, buff=0.25)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        dots = VGroup()
        random.seed(3)
        for r in range(18):
            R = 1.0 + r * 0.17
            n = int(np.pi * R / 0.16)
            for i in range(n):
                a = np.pi * (i + 0.5) / n
                d = Dot(point=[-np.cos(a) * R, -0.6 - np.sin(a) * R * 0.55 + 0, 0], radius=0.035, color=YEL if random.random() < 0.03 else BLUE_C3)
                dots.add(d)
        stage = Line(LEFT * 0.9, RIGHT * 0.9, color=GLD, stroke_width=6).move_to([0, -0.45, 0])
        dots.shift(UP * 0.2)
        cv = ValueTracker(0)
        counter = always_redraw(lambda: Text(f"{int(cv.get_value()):,}".replace(",", " "), font=GRF, color=YEL).scale(1.3).move_to([-1.75, 2.6, 0], aligned_edge=LEFT))
        approx = Text("≈", color=YEL, font=GRF).scale(1.1)
        approx.move_to([-2.3, 2.6, 0])
        self.play(Create(stage), FadeIn(approx), FadeIn(counter), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.004), cv.animate.set_value(17000), run_time=3.0)
        legend = VGroup(Dot(radius=0.06, color=BLUE_C3), Text("= 10 հանդիսատես", font=ARMS, color=GRY).scale(0.32)).arrange(RIGHT, buff=0.15).next_to(counter, DOWN, buff=0.35)
        self.play(FadeIn(legend), run_time=0.4)
        self.until(T['etym'] - 0.9)

        # ---------- 2. birth of the word: dots collapse into δρᾶμα ----------
        w1 = Text("δρᾶμα", font=GRF, color=BLUE_C3).scale(1.25).move_to([-1.9, 0.6, 0])
        w2 = Text("ἔργον", font=GRF, color=GRN).scale(1.25).move_to([1.9, 0.6, 0])
        plus = Text("+", font=GRF).scale(1.1).move_to([0, 0.6, 0])
        t2 = A("դրամատուրգիա", weight=BOLD, color=YEL).scale(0.95).to_edge(UP, buff=1.3)
        self.play(ReplacementTransform(dots, w1), FadeOut(VGroup(counter, approx, legend, stage, sub)), FadeTransform(title, t2), run_time=1.2)
        g1 = A("գործողություն", color=GRY).scale(0.4).next_to(w1, DOWN, buff=0.3)
        self.play(FadeIn(g1, shift=UP * 0.2), run_time=0.5)
        self.play(Write(plus), FadeIn(w2, shift=LEFT * 0.4), run_time=0.8)
        g2 = A("աշխատանք", color=GRY).scale(0.4).next_to(w2, DOWN, buff=0.3)
        self.play(FadeIn(g2, shift=UP * 0.2), run_time=0.5)
        self.wait(0.6)
        merged = VGroup(Text("δραμα", font=GRF, color=BLUE_C3), Text("τουργία", font=GRF, color=GRN)).arrange(RIGHT, buff=0.04).scale(1.15).move_to([0, 0.6, 0])
        self.play(TransformMatchingShapes(VGroup(w1, plus, w2), merged), FadeOut(g1), FadeOut(g2), run_time=1.3)
        brace = Brace2(merged, color=YEL)
        dfn = A("գործողությունը կառուցելու արվեստ").scale(0.5).move_to(brace.tip + DOWN * 0.45)
        dfn[13:22].set_color(YEL)
        self.play(Create(brace), Write(dfn), run_time=1.2)
        self.until(T['contest'] - 0.8)

        # ---------- 3. the contest: lifespans on a number line ----------
        t3 = A("Թատրոնը՝ մրցույթ", weight=BOLD).scale(0.85).to_edge(UP, buff=1.3)
        t3s = A("Դիոնիսոսի տոներին", color=GRY).scale(0.42).next_to(t3, DOWN, buff=0.25)
        nl = NumberLine(x_range=[-530, -400, 25], length=7.6, color=GRY, include_numbers=False).move_to([0, -2.6, 0])
        labels = VGroup(*[Text(str(-v), font=GRF, color=GRY).scale(0.32).next_to(nl.n2p(v), DOWN, buff=0.2) for v in range(-525, -399, 25)])
        self.play(FadeTransform(t2, t3), FadeOut(VGroup(brace, dfn)), merged.animate.scale(0.5).to_corner(UR, buff=0.5).set_opacity(0.4), run_time=0.8)
        self.play(FadeIn(t3s), Create(nl), FadeIn(labels, lag_ratio=0.1), run_time=0.8)
        people = [("Էսքիլես", -525, -456, BLUE_C3), ("Սոֆոկլես", -497, -406, GRN), ("Եվրիպիդես", -480, -406, GLD)]
        bars = VGroup()
        for k, (n, a, b, c) in enumerate(people):
            x0, x1 = nl.n2p(a)[0], nl.n2p(b)[0]
            y = 1.3 - k * 1.25
            bar = Rectangle(width=x1 - x0, height=0.62, color=c, fill_opacity=0.25, stroke_width=4).move_to([(x0 + x1) / 2, y, 0])
            lab = A(n, weight=BOLD).scale(0.42).move_to(bar.get_left() + RIGHT * 0.15, aligned_edge=LEFT)
            dash = DashedLine(bar.get_corner(DL), [x0, nl.get_y(), 0], color=c, stroke_width=2)
            bars.add(VGroup(bar, lab, dash))
            self.play(GrowFromEdge(bar, LEFT), FadeIn(lab), Create(dash), run_time=0.6)
        cap = Text("մ.թ.ա. տարիներ", font=ARMS, color=GRY).scale(0.32).next_to(labels, DOWN, buff=0.2)
        self.play(FadeIn(cap), run_time=0.3)
        self.until(T['masks'] - 0.8)

        # ---------- 4. masks: the mouth is a function y = a·x² ----------
        a = ValueTracker(0.9)
        t4 = A("Դերասաններ՝ դիմակներով", weight=BOLD).scale(0.72).to_edge(UP, buff=1.3)
        def face(cx, sign, col):
            outline = Ellipse(width=2.9, height=3.7, color=col, stroke_width=6).move_to([cx, 0.2, 0])
            eyes = VGroup(*[Arc(radius=0.35, start_angle=PI * 0.15, angle=PI * 0.7, color=col, stroke_width=6).move_to([cx + s * 0.6, 0.75, 0]) for s in (-1, 1)])
            mouth = always_redraw(lambda: FunctionGraph(lambda x: sign * a.get_value() * x * x - sign * a.get_value() * 0.36 - 0.65, x_range=[-0.6, 0.6], color=col, stroke_width=7).shift(RIGHT * cx))
            return VGroup(outline, eyes, mouth)
        fL, fR = face(-2.0, 1, YEL), face(2.0, -1, BLUE_C3)
        self.play(ReplacementTransform(bars, VGroup(fL[0], fR[0])), FadeOut(VGroup(nl, labels, cap, t3s)), FadeTransform(t3, t4), run_time=0.9)
        self.play(Create(fL[1]), Create(fR[1]), FadeIn(fL[2]), FadeIn(fR[2]), run_time=0.5)
        eq = always_redraw(lambda: VGroup(Text("y = ", font=GRF), Text(f"{a.get_value():+.1f}", font=GRF, color=YEL if a.get_value() > 0 else BLUE_C3), Text("· x²", font=GRF)).arrange(RIGHT, buff=0.12).scale(0.8).move_to([0, -2.8, 0]))
        self.add(eq)
        self.play(a.animate.set_value(-0.9), run_time=1.0)
        self.play(a.animate.set_value(0.9), run_time=0.6)
        self.until(T['poet'] - 0.7)

        # ---------- 5. Aristotle: a timeline to today ----------
        t5 = A("Արիստոտել", weight=BOLD, color=YEL).scale(1.0).to_edge(UP, buff=1.3)
        t5s = VGroup(A("«Պոետիկա» · ").scale(0.46), Text("ΠΕΡΙ ΠΟΙΗΤΙΚΗΣ", font=GRF, color=GRY).scale(0.4)).arrange(RIGHT, buff=0.1).next_to(t5, DOWN, buff=0.3)
        tl = NumberLine(x_range=[-600, 2100, 500], length=7.8, color=GRY).move_to([0, 0, 0])
        tl_lab = VGroup(*[Text(s, font=GRF, color=GRY).scale(0.3).next_to(tl.n2p(v), DOWN, buff=0.25) for v, s in [(-500, "500 մ.թ.ա."), (0, "0"), (1000, "1000"), (2026, "2026")]])
        self.remove(eq)
        self.play(ReplacementTransform(VGroup(fL, fR), tl), FadeTransform(t4, t5), run_time=0.9)
        self.play(FadeIn(t5s), FadeIn(tl_lab), run_time=0.5)
        dot = Dot(tl.n2p(-335), color=YEL, radius=0.12)
        tag = Text("−335", font=GRF, color=YEL).scale(0.7).next_to(dot, UP, buff=0.6)
        stem = Line(dot.get_center(), tag.get_bottom(), color=YEL)
        self.play(FadeIn(dot, scale=3), Create(stem), Write(tag), run_time=0.8)
        arc = ArcBetweenPoints(tl.n2p(-335) + DOWN * 0.15, tl.n2p(2026) + DOWN * 0.15, angle=PI / 2, color=BLUE_C3)
        note = A("2360 տարի անց՝ դեռ գործում է", color=BLUE_C3).scale(0.42).move_to([0, -2.6, 0])
        self.play(Create(arc), Write(note), run_time=1.3)
        self.until(T['temple'] - 0.7)

        # ---------- 6. beginning · middle · end ----------
        t6 = A("Պատմություն =", weight=BOLD).scale(0.8).to_edge(UP, buff=1.3)
        acts = VGroup(*[Rectangle(width=2.3, height=2.6, color=c, fill_opacity=0.15, stroke_width=5) for c in (BLUE_C3, GRN, RD)]).arrange(RIGHT, buff=0.35).move_to([0, 0.3, 0])
        names = VGroup(*[A(n, weight=BOLD, color=c).scale(0.42).move_to(r) for n, c, r in zip(["սկիզբ", "միջնամաս", "վերջ"], (BLUE_C3, GRN, RD), acts)])
        self.play(ReplacementTransform(VGroup(tl, arc), acts), FadeOut(VGroup(dot, tag, stem, note, tl_lab, t5s)), FadeTransform(t5, t6), run_time=0.9)
        self.play(LaggedStart(*[Write(n) for n in names], lag_ratio=0.3), run_time=0.9)
        br = Brace2(acts, color=YEL); whole = A("ամբողջություն", color=YEL).scale(0.45).move_to(br.tip + DOWN * 0.4)
        self.play(Create(br), FadeIn(whole), run_time=0.6)
        self.until(T['peri'] - 0.7)

        # ---------- 7. peripeteia: the derivative changes sign ----------
        t7 = A("Սյուժեն՝ հոգին է", weight=BOLD).scale(0.85).to_edge(UP, buff=1.3)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=7.4, y_length=5.2, axis_config={"color": GRY, "include_ticks": False}, tips=True).move_to([0, -0.2, 0])
        axl = VGroup(Text("ժամանակ", font=ARMS, color=GRY).scale(0.3).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT), Text("ճակատագիր", font=ARMS, color=GRY).scale(0.3).next_to(ax.y_axis, UP, buff=0.1))
        fortune = lambda t: max(0.03, 0.15 + 0.75 * np.sin(np.pi * min(t, 1) * 0.9) * (t / 0.55 if t < 0.55 else 1) - (max(0.0, t - 0.55) / 0.45) ** 1.6 * 0.7)
        curve = ax.plot(fortune, x_range=[0, 1], color=BLUE_C3, stroke_width=7)
        self.play(ReplacementTransform(VGroup(acts, names, br, whole), ax), FadeTransform(t6, t7), FadeIn(axl), run_time=0.9)
        tt = ValueTracker(0.02)
        self.play(Create(curve), run_time=1.0)
        pt = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), fortune(tt.get_value())), color=YEL, radius=0.1))
        tan = always_redraw(lambda: ax.get_secant_slope_group(tt.get_value(), curve, dx=0.01, secant_line_color=YEL, secant_line_length=3.2).submobjects[-1])
        self.add(pt, tan)
        self.play(tt.animate.set_value(0.95), run_time=2.0, rate_func=linear)
        peri = VGroup(Text("περιπέτεια", font=GRF, color=RD).scale(0.9), A("f′(t) փոխում է նշանը՝ շրջադարձ").scale(0.38)).arrange(DOWN, buff=0.15).move_to([0, -3.6, 0])
        ring = Circle(radius=0.28, color=RD, stroke_width=6).move_to(ax.c2p(0.55, fortune(0.55)))
        self.play(Create(ring), FadeIn(peri, shift=UP * 0.2), run_time=0.6)
        self.until(T['cath'] - 0.7)

        # ---------- 8. catharsis: area under the tension curve ----------
        t8 = VGroup(A("վախ", color=BLUE_C3).scale(0.55), Text("+", font=GRF).scale(0.6), A("կարեկցանք", color=GRN).scale(0.55), Text("→", font=GRF).scale(0.6)).arrange(RIGHT, buff=0.18).to_edge(UP, buff=1.2)
        kat = A("կաթարսիս", weight=BOLD, color=YEL).scale(1.0).next_to(t8, DOWN, buff=0.3)
        tension = lambda t: max(0.03, 0.1 + 0.12 * t + 0.7 * (np.sin(np.pi * min(t, 0.82) / 0.82 / 2) ** 3) - (max(0, t - 0.8) * 3.3))
        tcurve = ax.plot(tension, x_range=[0, 1], color=YEL, stroke_width=7)
        self.remove(pt, tan)
        self.play(ReplacementTransform(curve, tcurve), FadeOut(VGroup(ring, peri)), FadeTransform(t7, t8), run_time=1.0)
        area = ax.get_area(tcurve, x_range=[0, 1], color=YEL, opacity=0.25)
        self.play(FadeIn(area), Write(kat), run_time=1.2)
        kl = VGroup(Text("κάθαρσις", font=GRF).scale(0.55), A("· մաքրում").scale(0.45)).arrange(RIGHT, buff=0.15).move_to([0, -3.6, 0])
        self.play(FadeIn(kl), run_time=0.5)
        self.until(T['today'] - 0.7)

        # ---------- 9. 2500 years later: every story, the same curve ----------
        t9 = A("2500 տարի անց", weight=BOLD, color=YEL).scale(0.95).to_edge(UP, buff=1.3)
        t9s = A("գրեթե ամեն ֆիլմ ու սերիա", color=WHITE).scale(0.46).next_to(t9, DOWN, buff=0.25)
        self.play(FadeOut(VGroup(area, kl, kat)), FadeTransform(t8, t9), tcurve.animate.set_color(WHITE), run_time=0.8)
        self.play(FadeIn(t9s), run_time=0.4)
        random.seed(5)
        many = VGroup(*[ax.plot(lambda t, s=random.uniform(-0.06, 0.06), k=random.uniform(0.85, 1.12): min(1, tension(min(1, max(0, t + s))) * k), x_range=[0, 1], color=random.choice([BLUE_C3, GRN, TL, GLD]), stroke_width=2, stroke_opacity=0.5) for _ in range(36)])
        self.play(LaggedStart(*[Create(m) for m in many], lag_ratio=0.05), run_time=2.4)
        same = A("նույն կորը", color=WHITE).scale(0.5).move_to([0, -3.6, 0])
        self.play(FadeIn(same), run_time=0.4)
        self.until(T['arch'] - 0.7)

        # ---------- 10. columns -> acts ----------
        t10 = A("Սյուները փոխվել են։", weight=BOLD).scale(0.72).to_edge(UP, buff=1.2)
        t10b = A("Կառույցը՝ ոչ։", weight=BOLD, color=YEL).scale(0.9).next_to(t10, DOWN, buff=0.25)
        cols = VGroup()
        for k in range(3):
            shaft = Rectangle(width=1.3, height=4.0, color=WHITE, stroke_width=5).move_to([-2.6 + k * 2.6, -0.6, 0])
            flutes = VGroup(*[Line(shaft.get_top() + DOWN * 0.15 + RIGHT * (-0.4 + j * 0.27), shaft.get_bottom() + UP * 0.15 + RIGHT * (-0.4 + j * 0.27), color=WHITE, stroke_width=2, stroke_opacity=0.6) for j in range(4)])
            cols.add(VGroup(shaft, flutes))
        ped = Polygon([-4.0, 1.7, 0], [0, 3.1, 0], [4.0, 1.7, 0], color=YEL, stroke_width=6)
        base = Line([-4.1, -2.75, 0], [4.1, -2.75, 0], color=WHITE, stroke_width=6)
        dram = Text("ԴՐԱՄԱՏՈՒՐԳԻԱ", font=ARMS, weight=BOLD, color=YEL).scale(0.38).move_to([0, 2.15, 0])
        self.play(ReplacementTransform(VGroup(tcurve, many, ax, axl), cols), FadeOut(VGroup(same, t9s)), FadeTransform(t9, t10), run_time=1.0)
        self.play(Create(ped), Create(base), Write(dram), FadeIn(t10b), run_time=0.9)
        acts2 = VGroup(*[Rectangle(width=1.5, height=4.0, color=c, fill_opacity=0.2, stroke_width=5).move_to(cols[k][0]) for k, c in enumerate((BLUE_C3, GRN, RD))])
        roman = VGroup(*[Text(r, font=GRF, color=c).scale(0.9).move_to(acts2[k]) for k, (r, c) in enumerate(zip(["I", "II", "III"], (BLUE_C3, GRN, RD)))])
        self.play(ReplacementTransform(cols, acts2), FadeIn(roman, scale=0.6), run_time=1.0)
        arch = A("պատմության ճարտարապետությունը").scale(0.42).move_to([0, -3.6, 0])
        self.play(Write(arch), run_time=0.9)
        self.until(T['logo'] - 0.8)

        # ---------- 11. everything folds into the logo ----------
        logo = SVGMobject("logo_rev.svg"); logo.scale_to_fit_width(7.2).move_to([0, 0.6, 0])
        everything = VGroup(acts2, roman, ped, base, dram, t10, t10b, arch, merged)
        self.play(ReplacementTransform(everything, logo), run_time=1.2)
        lab = A("Սցենարի դաս · 01", color=YEL).scale(0.55).next_to(logo, DOWN, buff=0.1)
        self.play(FadeIn(lab, shift=UP * 0.2), run_time=0.5)
        self.until(T['end'])
