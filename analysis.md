你的数据其实比一般 CHI paper 丰富不少。除了验证 hypothesis，还可以做很多 **sanity check / manipulation check / exploratory analysis**。我会按我觉得最后写 paper 最有价值的顺序列一下。你的 study 是 2×3 within-subject design，DV 包括 acceptance、agency、identification、authorship 等。 

---

# **1. Main Effects（最核心）**

每个 DV 都跑


against


例如

```
Acceptance
        ^
        |
Repeat  Enhance  Opposite
```

---

# **最简短结论**

主结果很清楚：**content effect 最强**，而 **voice 和 interaction 基本不显著**。Acceptance 和 SoPA 都呈现 **Repeat 最高、Opposite 最低**；SoNA 则相反，**Opposite 最高**。另外，**trial effect、voice order effect 基本没有明显趋势**，说明主要差异更像是由内容类型驱动，而不是被试逐步适应或顺序造成的。

这就是论文主结果。

---

# **2. Manipulation Check（非常推荐）**

例如

### **Did participant notice?**

```
Notice difference
```

是否

- Repeat < Enhance
- Opposite 最大

如果没有 notice，  
说明 manipulation 很 subtle。

也可以继续分析

```
Notice
↓

Acceptance
Agency
```

看看 notice 是否导致 agency 降低。

---

# **3. Individual Participant Effects**

这个其实很重要。

例如画 spaghetti plot

```
participant

Acceptance
```

看看是不是

```
大多数人一致下降

还是

有人超级喜欢
有人超级讨厌
```

CHI reviewer 很喜欢这种。

可以画

```
each participant

Repeat
Enhance
Opposite
```

---

## **Mixed Model**

加入 participant random effect

```
DV ~
Voice
*
Condition
+
(1|Participant)
```

或者

```
(1+Condition|Participant)
```

看 participant variance。

---

# **4. Participant Traits**

你后测已经很多：

- AI literacy
- Desire of Control
- VR experience
- Age
- Gender

可以做

```
High DoC

↓

Agency
```

例如

```
DV
~
Voice
*
Condition
*
DoC
```

或者 correlation。

例如

```
DoC

↓

Acceptance difference
```

是不是

高 control 的人

更不能接受 AI。

---

# **5. Trial Effect**

12 trial

看看有没有

```
Trial Number

↓

Acceptance
```

是不是

越来越习惯。

例如

```
Trial

1
2
3
...
12
```

---

也可以

```
Block 1

vs

Block 2
```

---

# **6. Voice Order Effect**

因为

Clone first

Robot first

counterbalance

可以 check

```
Order

↓

Acceptance
```

是不是

先体验 clone

后面 robot 更奇怪。

---

# **7. Scenario Effect**

你有很多 moral scenario。

可以看

```
Scenario

↓

Acceptance
```

是不是

某几个题特别极端。

以后 paper 可以写

“No scenario dominated.”

---

# **8. Speaker Gender**

如果

Talker gender

counterbalance

可以 check

```
Male

vs

Female
```

是否 interaction。

---

# **9. Eye Tracking（我觉得很有潜力）**

如果 Quest Pro 全程录 gaze。

可以算：

---

### **(1) Mirror Looking Time**

```
time looking mirror
```

不同条件。

Hypothesis：

```
Clone

>

Robot
```

或者

```
Opposite

>

Repeat
```

因为开始怀疑自己。

---

### **(2) Rabbit Looking Time**

一直盯 rabbit？

---

### **(3) Self vs Other Ratio**

```
Mirror %

Rabbit %

Floor %

Else
```

---

### **(4) Gaze Switch**

一分钟内

```
Mirror

↓

Rabbit

↓

Mirror
```

次数。

可能代表 uncertainty。

---

### **(5) Fixation Duration**

平均 fixation。

---

### **(6) First Gaze**

AI 开始说话以后

第一眼看哪里。

---

### **(7) Head Movement**

虽然不是 eye

也可以

```
Head rotation

Head velocity
```

是不是

Opposite 时

疯狂摇头。

---

# **10. Behaviour Log**

例如

Response length

```
participant

response words
```

是不是

短回答的人

更接受 AI。

---

Latency

有没有影响。

---

# **11. Correlation Between Scales**

非常推荐。

例如

```
Agency

↓

Acceptance
```

```
Identification

↓

Acceptance
```

```
Ownership

↓

Agency
```

最后可以画

```
correlation matrix
```

---

# **12. Cluster Participants（Exploratory）**

例如

根据所有 trial

聚类

得到

```
Trust AI

Cluster

Skeptical

Cluster

Alienated

Cluster
```

这个会很好玩。

---

# **13. Interview（Qualitative）**

这是 paper 第二部分。

可以 thematic analysis：

例如主题：

### **AI as me**

“It still feels like me.”

---

### **Better me**

“It’s what I wanted to say.”

---

### **Separate Agent**

“The AI is speaking.”

---

### **Voice matters**

“The cloned voice was creepy.”

---

### **Opposite Opinion**

“That wasn’t me.”

---

最后可以统计

```
Theme

n participants
```

---

# **14. Quant + Qual Merge（我最推荐）**

例如

低 Acceptance 的 participant

Interview

有没有一直提

```
Alienation
```

高 Acceptance

有没有一直说

```
Better self
```

这是 CHI 很喜欢的 mixed-method。

---

# **15. 还有一些比较容易做的小分析**

- Cronbach’s α / McDonald’s ω（各量表内部一致性）
- 各 DV 的分布（天花板/地板效应）
- 条件间相关（例如 Acceptance 与 “Something I would say” 是否几乎测量同一构念）
- Missing value / Exclusion check
- SSQ pre/post（是否 VR 本身造成明显不适）
- IPQ 与 Agency、Embodiment 的相关
- AI authorship 百分比与各 DV 的相关

---

## **如果我是 reviewer，我最希望看到的分析组合**

**Primary analyses**

1. 2×3 mixed/repeated-measures ANOVA（或 LMM）
2. Manipulation check
3. Individual differences（DoC、AI literacy）
4. Trial / order effect check

**Secondary analyses**  
5. Eye-tracking（mirror、rabbit、gaze switching）  
6. Correlation matrix  
7. Interview thematic analysis  
8. Mixed-method integration（定量 × 定性）

这套分析既覆盖了 hypothesis testing，也充分利用了你收集到的行为、眼动和访谈数据，整体会比较完整。